from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from content_scaffold_lib import (
    DATA_ROOT,
    build_category_meta,
    build_front_matter,
    parse_simple_yaml,
    read_text,
    write_text,
)


LEGACY_ROOT = DATA_ROOT / "language_v2"
TARGET_ROOT = DATA_ROOT / "content" / "language" / "python"

PYTHON_LEVELS = [
    "lv01_print",
    "lv02_var",
    "lv03_input",
    "lv04_operator",
    "lv05_cast",
    "lv06_if",
    "lv07_for",
    "lv08_while",
    "lv09_nfor",
    "lv10_array",
    "lv15_array2d",
]

ANSWER_BLOCK_RE = re.compile(
    r"(?ms)^### (?P<heading>Q\d+\.[^\n]+)\n(?P<section>.*?)<!-- ANSWER_START -->\n(?P<answer>.*?)<!-- ANSWER_END -->"
)
ANSWER_ONLY_RE = re.compile(r"\n?<!-- ANSWER_START -->.*?<!-- ANSWER_END -->\n?", re.S)


@dataclass
class LegacyTheory:
    concept_id: str
    title: str
    category_id: str
    recommended_set_id: str
    related_set_ids: list[str]
    prerequisites: list[str]
    next_concepts: list[str]
    priority: int


@dataclass
class LegacyCategory:
    category_id: str
    name: str
    order: int


@dataclass
class LegacyWorksheet:
    source_path: Path
    worksheet_id: str
    title: str
    difficulty: str
    round_no: int


def load_json(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalize_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in ("", None, {}):
        return []
    return [str(value)]


def load_legacy_lookup():
    categories = {}
    for row in load_json(DATA_ROOT / "categories.json"):
        if row.get("track") == "language" and row.get("lang") == "Python":
            categories[str(row["id"])] = LegacyCategory(
                category_id=str(row["id"]),
                name=str(row["name"]),
                order=int(row["order"]),
            )

    theory = {}
    for row in load_json(DATA_ROOT / "theory.index.json"):
        if row.get("lang") == "python" and row.get("categoryId") in categories:
            theory[str(row["categoryId"])] = LegacyTheory(
                concept_id=str(row["conceptId"]),
                title=str(row["title"]),
                category_id=str(row["categoryId"]),
                recommended_set_id=str(row.get("recommendedSetId") or ""),
                related_set_ids=normalize_list(row.get("relatedSetIds")),
                prerequisites=normalize_list(row.get("prerequisites")),
                next_concepts=normalize_list(row.get("nextConcepts")),
                priority=int(row.get("priority") or 2),
            )

    sets_lookup = {}
    for row in load_json(DATA_ROOT / "sets.index.json"):
        if str(row.get("categoryId") or "").startswith("py_"):
            sets_lookup[str(row["id"])] = row

    return categories, theory, sets_lookup


def split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("front matter is required")
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValueError("closing front matter marker is missing")
    raw_meta = parts[0].splitlines()[1:]
    meta = parse_simple_yaml("\n".join(raw_meta))
    return meta, parts[1].lstrip("\n")


def derive_part_name(category_name: str) -> str:
    if " - " in category_name:
        return category_name.split(" - ", 1)[1].strip()
    return category_name


def load_legacy_worksheets(level_root: Path, sets_lookup: dict[str, dict]) -> list[LegacyWorksheet]:
    worksheets: list[LegacyWorksheet] = []
    for source_path in sorted((level_root / "py").glob("*.md")):
        meta, _ = split_front_matter(read_text(source_path))
        worksheet_id = str(meta["id"])
        set_meta = sets_lookup.get(worksheet_id)
        difficulty = str(set_meta["difficulty"]) if set_meta else ("challenge" if source_path.stem.startswith("c") else "basic")
        round_no = int(set_meta["round"]) if set_meta else int(source_path.stem[1:])
        worksheets.append(
            LegacyWorksheet(
                source_path=source_path,
                worksheet_id=worksheet_id,
                title=str(meta["title"]),
                difficulty=difficulty,
                round_no=round_no,
            )
        )
    return worksheets


def build_lesson_text(category: LegacyCategory, theory: LegacyTheory, theory_body: str) -> str:
    front_matter = build_front_matter(
        [
            ("id", theory.concept_id),
            ("contentType", "lesson"),
            ("track", "language"),
            ("lang", "python"),
            ("categoryId", category.category_id),
            ("title", theory.title),
            ("status", "active"),
            ("order", category.order),
            ("audience", "common"),
            ("recommendedSetId", theory.recommended_set_id),
            ("relatedSetIds", theory.related_set_ids),
            ("prerequisites", theory.prerequisites),
            ("nextConcepts", theory.next_concepts),
            ("priority", theory.priority),
        ]
    )
    return front_matter + theory_body.rstrip() + "\n"


def build_worksheet_text(category_id: str, title: str, worksheet_doc_id: str, difficulty: str, round_no: int, body: str) -> str:
    front_matter = build_front_matter(
        [
            ("id", worksheet_doc_id),
            ("contentType", "worksheet"),
            ("track", "language"),
            ("lang", "python"),
            ("categoryId", category_id),
            ("title", title),
            ("round", round_no),
            ("difficulty", difficulty),
            ("status", "active"),
            ("audience", "common"),
            ("printDefault", True),
        ]
    )
    return front_matter + body.rstrip() + "\n"


def build_answer_text(title: str, worksheet_body: str) -> str:
    parts = [f"# {title} 정답"]
    for match in ANSWER_BLOCK_RE.finditer(worksheet_body):
        heading = match.group("heading").strip()
        answer = match.group("answer").strip()
        parts.append(f"## {heading}")
        parts.append(answer)
    if len(parts) == 1:
        parts.append("## 정답")
        parts.append("- 정답/해설을 수동으로 확인하세요.")
    return "\n\n".join(parts).rstrip() + "\n"


def strip_answer_blocks(worksheet_body: str) -> str:
    stripped = ANSWER_ONLY_RE.sub("\n", worksheet_body)
    stripped = re.sub(r"\n{3,}", "\n\n", stripped)
    return stripped.strip() + "\n"


def worksheet_doc_id_for(slug: str, difficulty: str, round_no: int) -> str:
    return f"py_{slug}_{difficulty}_r{round_no:02d}"


def worksheet_file_stem(difficulty: str, round_no: int) -> str:
    return f"{difficulty}_r{round_no:02d}"


def build_interactive_seed(category_id: str, worksheet_id: str, title: str, difficulty: str, round_no: int) -> str:
    payload = {
        "meta": {
            "id": worksheet_id,
            "contentType": "interactive",
            "track": "language",
            "lang": "python",
            "categoryId": category_id,
            "title": title,
            "round": round_no,
            "difficulty": difficulty,
            "status": "active",
        },
        "id": worksheet_id,
        "title": title,
        "categoryId": category_id,
        "availableLanguages": ["python"],
        "problems": [],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def migrate_level(level_name: str, legacy_categories: dict[str, LegacyCategory], legacy_theory: dict[str, LegacyTheory], sets_lookup: dict[str, dict]) -> dict:
    level_root = LEGACY_ROOT / level_name
    theory_path = level_root / "_docs" / "theory.md"
    worksheets = load_legacy_worksheets(level_root, sets_lookup)
    if not worksheets:
        raise ValueError(f"no python worksheets found under {level_root}")

    first_meta, _ = split_front_matter(read_text(worksheets[0].source_path))
    category_id = str(first_meta["categoryId"])
    category = legacy_categories[category_id]
    theory = legacy_theory[category_id]
    target_root = TARGET_ROOT / level_name

    created = {"category": False, "lesson": False, "worksheets": 0, "interactive": 0, "skipped": 0}

    if not target_root.exists():
        write_text(
            target_root / "category.meta.yml",
            build_category_meta(
                category_id=category.category_id,
                track="language",
                lang_display="Python",
                title=category.name,
                part_name=derive_part_name(category.name),
                order=category.order,
                legacy_path=level_root.as_posix(),
            ),
        )
        created["category"] = True

    lesson_path = target_root / "lesson" / "lesson.md"
    if not lesson_path.exists():
        write_text(lesson_path, build_lesson_text(category, theory, read_text(theory_path)))
        created["lesson"] = True

    for legacy_ws in worksheets:
        stem = worksheet_file_stem(legacy_ws.difficulty, legacy_ws.round_no)
        worksheet_path = target_root / "worksheets" / f"worksheet_{stem}.md"
        answer_path = target_root / "worksheets" / f"answer_{stem}.md"
        interactive_path = target_root / "interactive" / f"interactive_{stem}.json"
        if worksheet_path.exists() and answer_path.exists() and interactive_path.exists():
            created["skipped"] += 1
            continue

        _, worksheet_body_raw = split_front_matter(read_text(legacy_ws.source_path))
        worksheet_body = strip_answer_blocks(worksheet_body_raw)
        answer_body = build_answer_text(legacy_ws.title, worksheet_body_raw)
        worksheet_doc_id = worksheet_doc_id_for(level_name, legacy_ws.difficulty, legacy_ws.round_no)

        if not worksheet_path.exists():
            write_text(
                worksheet_path,
                build_worksheet_text(
                    category_id=category_id,
                    title=legacy_ws.title,
                    worksheet_doc_id=worksheet_doc_id,
                    difficulty=legacy_ws.difficulty,
                    round_no=legacy_ws.round_no,
                    body=worksheet_body,
                ),
            )
            created["worksheets"] += 1

        if not answer_path.exists():
            write_text(answer_path, answer_body)

        if not interactive_path.exists():
            write_text(
                interactive_path,
                build_interactive_seed(
                    category_id=category_id,
                    worksheet_id=legacy_ws.worksheet_id,
                    title=legacy_ws.title,
                    difficulty=legacy_ws.difficulty,
                    round_no=legacy_ws.round_no,
                ),
            )
            created["interactive"] += 1

    return created


def main() -> int:
    legacy_categories, legacy_theory, sets_lookup = load_legacy_lookup()
    summary = {}
    for level_name in PYTHON_LEVELS:
        summary[level_name] = migrate_level(level_name, legacy_categories, legacy_theory, sets_lookup)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
