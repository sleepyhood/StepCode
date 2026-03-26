from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "practice" / "data"
CONTENT_ROOT = DATA_ROOT / "content"
GENERATED_ROOT = DATA_ROOT / "generated"


class ValidationError(Exception):
    pass


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_scalar(raw: str):
    value = raw.strip()
    if not value:
        return ""
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part) for part in inner.split(",")]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def parse_simple_yaml(text: str) -> dict:
    out: dict = {}
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in raw:
            raise ValidationError(f"invalid metadata line at {lineno}: {raw}")
        key, value = raw.split(":", 1)
        out[key.strip()] = parse_scalar(value)
    return out


def parse_front_matter(path: Path) -> tuple[dict, str]:
    text = read_text(path)
    if not text.startswith("---\n"):
        raise ValidationError(f"{path}: front matter is required")
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValidationError(f"{path}: closing front matter marker is missing")
    raw_meta = parts[0].splitlines()[1:]
    meta = parse_simple_yaml("\n".join(raw_meta))
    body = parts[1]
    return meta, body


def ensure_required(meta: dict, required: list[str], path: Path):
    missing = [key for key in required if key not in meta or meta[key] in ("", None)]
    if missing:
        raise ValidationError(f"{path}: missing required metadata: {', '.join(missing)}")


def rel_data_path(path: Path) -> str:
    return "./data/" + path.relative_to(DATA_ROOT).as_posix()


def validate_asset_refs(path: Path, body: str):
    refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", body)
    refs += re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", body, flags=re.IGNORECASE)
    for ref in refs:
        target = ref.strip()
        if not target or target.startswith("http://") or target.startswith("https://"):
            continue
        if target.startswith("./data/"):
            actual = DATA_ROOT / target[len("./data/") :]
        else:
            actual = (path.parent / target).resolve()
        if not actual.exists():
            raise ValidationError(f"{path}: asset not found: {target}")


def validate_file_name(path: Path, content_type: str):
    name = path.name
    if content_type == "lesson" and not re.fullmatch(r"lesson(?:_[a-z0-9_]+)?\.md", name):
        raise ValidationError(f"{path}: lesson filename must match lesson*.md")
    if content_type == "worksheet" and not re.fullmatch(r"worksheet_[a-z0-9]+_r\d{2}\.md", name):
        raise ValidationError(f"{path}: worksheet filename must match worksheet_<difficulty>_r<round>.md")
    if content_type == "interactive" and not re.fullmatch(r"interactive_[a-z0-9]+_r\d{2}\.json", name):
        raise ValidationError(f"{path}: interactive filename must match interactive_<difficulty>_r<round>.json")


def parse_interactive(path: Path) -> dict:
    validate_file_name(path, "interactive")
    try:
        payload = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path}: invalid json: {exc}") from exc
    meta = payload.get("meta")
    if not isinstance(meta, dict):
        raise ValidationError(f"{path}: interactive json requires root meta object")
    ensure_required(meta, ["id", "contentType", "track", "categoryId", "title", "status"], path)
    if meta.get("contentType") != "interactive":
        raise ValidationError(f"{path}: contentType must be interactive")
    return meta


def pair_answer_path(worksheet_path: Path) -> Path | None:
    name = worksheet_path.name.replace("worksheet_", "answer_", 1)
    target = worksheet_path.with_name(name)
    return target if target.exists() else None


def scan_category(category_root: Path) -> tuple[dict, list[dict], list[dict], list[dict]]:
    meta_path = category_root / "category.meta.yml"
    category = parse_simple_yaml(read_text(meta_path))
    ensure_required(category, ["id", "track", "lang", "name", "order", "status"], meta_path)

    lessons: list[dict] = []
    worksheets: list[dict] = []
    interactive: list[dict] = []

    lesson_dir = category_root / "lesson"
    worksheets_dir = category_root / "worksheets"
    interactive_dir = category_root / "interactive"

    if lesson_dir.exists():
        for path in sorted(lesson_dir.glob("*.md")):
            validate_file_name(path, "lesson")
            meta, body = parse_front_matter(path)
            ensure_required(meta, ["id", "contentType", "track", "categoryId", "title", "status"], path)
            if meta.get("contentType") != "lesson":
                raise ValidationError(f"{path}: contentType must be lesson")
            if meta.get("categoryId") != category["id"]:
                raise ValidationError(f"{path}: categoryId does not match category.meta.yml")
            validate_asset_refs(path, body)
            lessons.append(
                {
                    "conceptId": meta["id"],
                    "title": meta["title"],
                    "categoryId": meta["categoryId"],
                    "lang": str(meta.get("lang") or category.get("lang") or "").lower(),
                    "track": meta.get("track", category["track"]),
                    "mdPath": rel_data_path(path),
                    "recommendedSetId": meta.get("recommendedSetId", ""),
                    "relatedSetIds": meta.get("relatedSetIds", []),
                    "prerequisites": meta.get("prerequisites", []),
                    "nextConcepts": meta.get("nextConcepts", []),
                    "priority": meta.get("priority", 2),
                    "sourcePath": rel_data_path(path),
                }
            )

    if worksheets_dir.exists():
        for path in sorted(worksheets_dir.glob("worksheet_*.md")):
            validate_file_name(path, "worksheet")
            meta, body = parse_front_matter(path)
            ensure_required(meta, ["id", "contentType", "track", "categoryId", "title", "status"], path)
            if meta.get("contentType") != "worksheet":
                raise ValidationError(f"{path}: contentType must be worksheet")
            if meta.get("categoryId") != category["id"]:
                raise ValidationError(f"{path}: categoryId does not match category.meta.yml")
            validate_asset_refs(path, body)
            answer_path = pair_answer_path(path)
            worksheets.append(
                {
                    "id": meta["id"],
                    "title": meta["title"],
                    "categoryId": meta["categoryId"],
                    "track": meta.get("track", category["track"]),
                    "lang": str(meta.get("lang") or category.get("lang") or "").lower(),
                    "difficulty": meta.get("difficulty", ""),
                    "round": meta.get("round", 0),
                    "status": meta.get("status", "active"),
                    "audience": meta.get("audience", "common"),
                    "printDefault": meta.get("printDefault", True),
                    "mdPath": rel_data_path(path),
                    "answerMdPath": rel_data_path(answer_path) if answer_path else "",
                    "sourcePath": rel_data_path(path),
                }
            )

    if interactive_dir.exists():
        for path in sorted(interactive_dir.glob("interactive_*.json")):
            meta = parse_interactive(path)
            if meta.get("categoryId") != category["id"]:
                raise ValidationError(f"{path}: categoryId does not match category.meta.yml")
            interactive.append(
                {
                    "id": meta["id"],
                    "categoryId": meta["categoryId"],
                    "title": meta["title"],
                    "round": meta.get("round", 0),
                    "difficulty": meta.get("difficulty", ""),
                    "lang": str(meta.get("lang") or category.get("lang") or "").lower(),
                    "track": meta.get("track", category["track"]),
                    "status": meta.get("status", "active"),
                    "file": path.name,
                    "dataPath": meta.get("dataPath", rel_data_path(path)),
                    "sourcePath": rel_data_path(path),
                }
            )

    category_entry = {
        "id": category["id"],
        "name": category["name"],
        "lang": category["lang"],
        "track": category["track"],
        "order": category["order"],
        "partName": category.get("partName", ""),
        "status": category["status"],
        "contentRootPath": rel_data_path(category_root),
    }
    return category_entry, lessons, worksheets, interactive


def ensure_unique(items: list[dict], key: str, label: str):
    seen: dict[str, str] = {}
    for item in items:
        item_key = str(item.get(key) or "")
        if not item_key:
            raise ValidationError(f"{label}: missing {key}")
        if item_key in seen:
            raise ValidationError(f"{label}: duplicate {key}: {item_key}")
        seen[item_key] = item_key


def main():
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    categories: list[dict] = []
    theories: list[dict] = []
    worksheets: list[dict] = []
    interactive: list[dict] = []

    if CONTENT_ROOT.exists():
        for meta_path in sorted(CONTENT_ROOT.glob("**/category.meta.yml")):
            category_root = meta_path.parent
            category_entry, lesson_rows, worksheet_rows, interactive_rows = scan_category(category_root)
            categories.append(category_entry)
            theories.extend(lesson_rows)
            worksheets.extend(worksheet_rows)
            interactive.extend(interactive_rows)

    ensure_unique(categories, "id", "categories")
    ensure_unique(theories, "conceptId", "theory.index")
    ensure_unique(worksheets, "id", "worksheet.index")
    ensure_unique(interactive, "id", "interactive.index")

    (GENERATED_ROOT / "categories.json").write_text(
        json.dumps(sorted(categories, key=lambda x: int(x.get("order", 0))), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (GENERATED_ROOT / "theory.index.json").write_text(
        json.dumps(theories, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (GENERATED_ROOT / "worksheet.index.json").write_text(
        json.dumps(worksheets, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (GENERATED_ROOT / "interactive.index.json").write_text(
        json.dumps(interactive, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("OK: generated content indexes")
    print(f"categories={len(categories)} theory={len(theories)} worksheets={len(worksheets)} interactive={len(interactive)}")


if __name__ == "__main__":
    main()
