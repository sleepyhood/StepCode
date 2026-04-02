from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "practice" / "data"
LABELS = [
    "난이도",
    "형식",
    "출제 의도",
    "문제",
    "정답",
    "해설",
    "부분 정답 기준",
    "실제 실행 확인 결과",
    "검수 체크",
]
LEVEL_MAP = {
    "하": "basic",
    "중": "intermediate",
    "중상": "intermediate",
    "상": "advanced",
}
TYPE_MAP = {
    "코드 입력형": "code",
    "빈칸형": "short",
    "복수정답 객관식형": "mcq_multi",
}
COPYABLE_START_RE = re.compile(
    r"^\s*#\s*COPYABLE_START:\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(asset|helper|logic)\s*$"
)
COPYABLE_END_RE = re.compile(r"^\s*#\s*COPYABLE_END:\s*(.+?)\s*$")


class ReviewParseError(Exception):
    pass


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_markdown_blocks(text: str, pattern: re.Pattern[str]) -> list[tuple[re.Match[str], str]]:
    matches = list(pattern.finditer(text))
    blocks: list[tuple[re.Match[str], str]] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        blocks.append((match, text[start:end].strip()))
    return blocks


def split_labeled_fields(text: str) -> dict[str, str]:
    lines = text.splitlines()
    fields: dict[str, list[str]] = {}
    current: str | None = None
    in_code = False

    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            if current:
                fields.setdefault(current, []).append(line)
            continue

        if not in_code and stripped.endswith(":"):
            label = stripped[:-1].strip()
            if label in LABELS:
                current = label
                fields.setdefault(current, [])
                continue

        if current:
            fields.setdefault(current, []).append(line)

    return {key: "\n".join(value).strip() for key, value in fields.items()}


def extract_code_fences(text: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"```(?:[^\n]*)\n(.*?)```", text, flags=re.S)]


def extract_copyable_blocks(code: str) -> tuple[str, list[dict]]:
    if not code:
        return code, []

    # COPYABLE_START/END는 문제 검수 markdown 안에서
    # 학생에게 부분 복사를 허용할 자산/helper 블록을 표시하는 마커다.
    # 전체 section.code에서는 마커 줄을 제거하고, snippet만 별도 추출한다.
    lines = code.splitlines()
    clean_lines: list[str] = []
    blocks: list[dict] = []
    active: dict | None = None
    active_lines: list[str] = []

    for line in lines:
        start_match = COPYABLE_START_RE.match(line)
        if start_match:
            active = {
                "id": start_match.group(1).strip(),
                "title": start_match.group(2).strip(),
                "role": start_match.group(3).strip(),
                "copyPolicy": "allowed",
            }
            active_lines = []
            continue

        end_match = COPYABLE_END_RE.match(line)
        if end_match and active:
            end_id = end_match.group(1).strip()
            if end_id == active["id"]:
                active["code"] = "\n".join(active_lines).strip()
                if active["code"]:
                    blocks.append(active)
                active = None
                active_lines = []
                continue

        clean_lines.append(line)
        if active is not None:
            active_lines.append(line)

    clean_code = "\n".join(clean_lines).strip()
    return clean_code, blocks


def remove_code_fences(text: str) -> str:
    return re.sub(r"```(?:[^\n]*)\n.*?```", "", text, flags=re.S)


def extract_bullets(text: str) -> list[str]:
    bullets: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
    return bullets


def clean_text_block(text: str) -> str:
    raw = remove_code_fences(text)
    lines = []
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        if stripped.startswith("- ") and re.match(r"^-[ ]+[ㄱ-ㅎA-Z]\.", stripped):
            continue
        lines.append(stripped)
    return "\n".join(lines).strip()


def first_sentence(text: str) -> str:
    compact = " ".join(line.strip() for line in text.splitlines() if line.strip())
    if not compact:
        return "문항"
    compact = compact.replace("`", "")
    if len(compact) <= 28:
        return compact
    return compact[:28].rstrip() + "..."


def to_media_path(source_path: Path, rel_media_path: str) -> str:
    rel = rel_media_path.strip()
    if rel.startswith("./"):
        rel = rel[2:]
    actual = source_path.parent / rel
    rel_from_content = actual.relative_to(DATA_ROOT / "content").as_posix()
    return f"../content/{rel_from_content}"


def media_type_from_path(path: str) -> str:
    return "gif" if path.lower().endswith(".gif") else "image"


def parse_option_lines(text: str) -> list[str]:
    options: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        match = re.match(r"^-[ ]+[ㄱ-ㅎA-Z]\.[ ]+(.*)$", stripped)
        if match:
            options.append(match.group(1).strip())
    return options


def parse_correct_indexes(answer_text: str, options: list[str]) -> list[int]:
    answer_line = next((item for item in extract_bullets(answer_text) if item), "")
    if not answer_line:
        raise ReviewParseError("복수정답 객관식형 정답을 찾을 수 없습니다.")

    labels = [part.strip() for part in re.split(r"[,\s]+", answer_line.replace("`", "")) if part.strip()]
    symbol_map = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ"]
    indexes: list[int] = []
    for label in labels:
        if label in symbol_map:
            indexes.append(symbol_map.index(label))
            continue
        if label in ["A", "B", "C", "D", "E", "F"]:
            indexes.append(ord(label) - ord("A"))
            continue
    indexes = [idx for idx in indexes if idx < len(options)]
    if not indexes:
        raise ReviewParseError("복수정답 객관식형 correctIndexes 파싱에 실패했습니다.")
    return indexes


def build_teacher_explain_md(text: str) -> str:
    bullets = extract_bullets(text)
    if bullets:
        return "\n".join(f"- {item}" for item in bullets)
    cleaned = clean_text_block(text)
    if not cleaned:
        return ""
    return "\n".join(f"- {line}" for line in cleaned.splitlines() if line.strip())


def parse_short_answer(answer_text: str, question_text: str) -> dict:
    bullets = extract_bullets(answer_text)
    code_blocks = extract_code_fences(question_text)
    if len(bullets) > 1 and code_blocks:
        return {
            "answerUi": {
                "kind": "grid",
                "rows": [str(i) for i in range(1, len(bullets) + 1)],
                "columns": ["정답"],
                "narrowAnswerColumn": True,
                "rowSep": "\n",
                "colSep": " ",
            },
            "expectedGrid": [[item] for item in bullets],
        }
    if bullets:
        return {"expectedText": bullets[0].replace("`", "")}
    code_answers = extract_code_fences(answer_text)
    if code_answers:
        return {"expectedText": code_answers[0]}
    cleaned = clean_text_block(answer_text)
    if not cleaned:
        raise ReviewParseError("빈칸형 정답 파싱에 실패했습니다.")
    return {"expectedText": cleaned}


def parse_child(section_no: int, heading_no: str, body: str) -> dict:
    fields = split_labeled_fields(body)
    raw_type = extract_bullets(fields.get("형식", ""))[0]
    raw_level = extract_bullets(fields.get("난이도", ""))[0]
    qtype = TYPE_MAP[raw_type]
    level = LEVEL_MAP.get(raw_level, "intermediate")
    question_text = fields.get("문제", "")
    answer_text = fields.get("정답", "")
    description = clean_text_block(question_text)
    code_blocks = extract_code_fences(question_text)

    child = {
        "id": f"p{section_no}_{heading_no.split('.')[-1]}",
        "type": qtype,
        "level": level,
        "title": f"{heading_no} {first_sentence(description)}",
        "description": description,
        "teacherExplainMd": build_teacher_explain_md(fields.get("해설", "")),
    }

    if code_blocks:
        child["code"] = code_blocks[0]

    if qtype == "code":
        code_answers = extract_code_fences(answer_text)
        if code_answers:
            child["expectedCode"] = code_answers[0]
        else:
            child["expectedCode"] = extract_bullets(answer_text)[0].replace("`", "")
    elif qtype == "short":
        child.update(parse_short_answer(answer_text, question_text))
    elif qtype == "mcq_multi":
        options = parse_option_lines(question_text)
        correct_indexes = parse_correct_indexes(answer_text, options)
        child["options"] = options
        child["optionLabels"] = [chr(ord("A") + i) for i in range(len(options))]
        child["correctIndexes"] = correct_indexes
        child["minSelections"] = len(correct_indexes)
        child["maxSelections"] = len(correct_indexes)

    return child


def parse_section(source_path: Path, number: int, title: str, body: str) -> dict:
    child_pattern = re.compile(r"^###\s+(\d+\.\d+)\s*$", re.M)
    child_blocks = split_markdown_blocks(body, child_pattern)
    intro_end = child_blocks[0][0].start() if child_blocks else len(body)
    intro = body[:intro_end].strip()

    description_match = re.search(r"코드 설명:\s*(.*?)(?:\n제시 코드:|\n참고 이미지:|\Z)", intro, flags=re.S)
    description = clean_text_block(description_match.group(1) if description_match else "")

    code_blocks = extract_code_fences(intro)
    images = []
    for match in re.finditer(r"!\[(.*?)\]\((.*?)\)", intro):
        caption = match.group(1).strip() or "참고 이미지"
        raw_path = match.group(2).strip()
        media_path = to_media_path(source_path, raw_path)
        images.append(
            {
                "type": media_type_from_path(media_path),
                "path": media_path,
                "caption": caption,
            }
        )

    section = {
        "id": f"s{number}",
        "title": title.strip(),
        "description": description,
        "children": [parse_child(number, match.group(1), child_body) for match, child_body in child_blocks],
    }
    if code_blocks:
        cleaned_code, copyable_blocks = extract_copyable_blocks(code_blocks[0])
        section["code"] = cleaned_code
        # pygame review 기반 section 제시 코드는 학생 화면에서 기본 잠금한다.
        # host UI만 전체 복사 예외를 갖고, 학생용 부분 복사는 codeBlocks로 분리한다.
        section["codePolicy"] = "teacher_only"
        if copyable_blocks:
            section["codeBlocks"] = copyable_blocks
    if images:
        section["media"] = images
    return section


def parse_review_markdown(source_path: Path, set_id: str, title: str, category_id: str) -> dict:
    text = read_text(source_path).replace("\r\n", "\n")
    section_pattern = re.compile(r"^##\s+(\d+)번\.\s+(.*?)\s*$", re.M)
    section_blocks = split_markdown_blocks(text, section_pattern)
    if not section_blocks:
        raise ReviewParseError("대문항(## n번.)을 찾을 수 없습니다.")

    sections = [
        parse_section(source_path, int(match.group(1)), f"{match.group(1)}번 {match.group(2)}", body)
        for match, body in section_blocks
    ]

    concepts = []
    for idx, section in enumerate(sections, start=1):
        concept_id = f"sec_{idx}"
        section["conceptRef"] = concept_id
        concepts.append(
            {
                "id": concept_id,
                "title": section["title"],
                "summary": section["description"],
                "relatedProblems": [child["id"] for child in section["children"]],
            }
        )

    return {
        "id": set_id,
        "title": title,
        "categoryId": category_id,
        "availableLanguages": ["python"],
        "defaultDisplayGroup": "by_section",
        "displayGroups": [
            {
                "id": "by_section",
                "label": "대문항별",
                "note": f"{len(sections)}개 대문항 묶음으로 학습",
                "renderMode": "section",
                "filter": {},
            }
        ],
        "concepts": concepts,
        "sections": sections,
    }


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pygame 검수 markdown을 sections형 세트 JSON으로 변환합니다.")
    parser.add_argument("--source", required=True, help="검수 markdown 경로")
    parser.add_argument("--output", required=True, help="생성할 세트 JSON 경로")
    parser.add_argument("--set-id", required=True, help="생성할 세트 ID")
    parser.add_argument("--title", required=True, help="생성할 세트 제목")
    parser.add_argument("--category-id", required=True, help="생성할 카테고리 ID")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    source_path = Path(args.source).resolve()
    output_path = Path(args.output).resolve()
    payload = parse_review_markdown(source_path, args.set_id, args.title, args.category_id)
    write_json(output_path, payload)
    print(f"OK: generated {output_path}")


if __name__ == "__main__":
    main()
