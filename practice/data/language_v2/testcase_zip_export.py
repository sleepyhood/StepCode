import re
import zipfile
from pathlib import Path


TESTCASE_SECTION_HEADING = "## 5. 채점용 테스트케이스"
TESTCASE_BLOCK_RE = re.compile(
    r"^###\s*테스트케이스\s*(?P<case_id>\d+)\s*(?P<kind>입력|출력)\s*$"
    r"\n```(?:text)?\n(?P<body>.*?)\n```",
    re.MULTILINE | re.DOTALL,
)
TESTCASE_HEADING_RE = re.compile(
    r"^###\s*테스트케이스\s*(?P<case_id>\d+)\s*(?P<kind>입력|출력)\s*$",
    re.MULTILINE,
)


def _normalize_newlines(text):
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _extract_testcase_section(md_text):
    normalized = _normalize_newlines(md_text)
    heading_index = normalized.find(TESTCASE_SECTION_HEADING)
    if heading_index < 0:
        return ""

    tail = normalized[heading_index:]
    answer_index = tail.find("<!-- ANSWER_START -->")
    if answer_index >= 0:
        tail = tail[:answer_index]
    return tail


def _shorten_line(value, limit=60):
    single_line = " ".join(value.splitlines()).strip()
    if len(single_line) <= limit:
        return single_line
    return single_line[: limit - 3] + "..."


def parse_testcases_from_markdown(md_text):
    section = _extract_testcase_section(md_text)
    if not section:
        return []

    headings = list(TESTCASE_HEADING_RE.finditer(section))
    if not headings:
        return []

    matches = list(TESTCASE_BLOCK_RE.finditer(section))
    if len(matches) != len(headings):
        raise ValueError("테스트케이스 블록 형식이 올바르지 않습니다.")

    case_map = {}
    case_order = []
    for match in matches:
        source_id = match.group("case_id")
        kind = match.group("kind")
        body = _normalize_newlines(match.group("body"))

        if source_id not in case_map:
            case_map[source_id] = {"source_id": source_id, "input_text": None, "output_text": None}
            case_order.append(source_id)

        key = "input_text" if kind == "입력" else "output_text"
        if case_map[source_id][key] is not None:
            raise ValueError(f"테스트케이스 {source_id}의 {kind} 블록이 중복되었습니다.")
        case_map[source_id][key] = body

    cases = []
    for index, source_id in enumerate(case_order, start=1):
        case = case_map[source_id]
        if case["input_text"] is None or case["output_text"] is None:
            raise ValueError(f"테스트케이스 {source_id}의 입력/출력 쌍이 맞지 않습니다.")
        cases.append(
            {
                "id": str(index),
                "source_id": source_id,
                "input_text": case["input_text"],
                "output_text": case["output_text"],
            }
        )
    return cases


def build_testcase_preview(cases, limit=3):
    total = len(cases)
    lines = [f"총 테스트케이스: {total}개"]
    if not cases:
        lines.append("미리볼 테스트케이스가 없습니다.")
        return "\n".join(lines)

    for case in cases[:limit]:
        lines.append(
            f"[{case['id']}] 입력: {_shorten_line(case['input_text']) or '(빈 입력)'}"
        )
        lines.append(
            f"[{case['id']}] 출력: {_shorten_line(case['output_text']) or '(빈 출력)'}"
        )
    if total > limit:
        lines.append(f"... 외 {total - limit}개")
    return "\n".join(lines)


def export_testcases_to_zip(cases, output_dir, zip_name):
    if not cases:
        raise ValueError("저장할 테스트케이스가 없습니다.")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not zip_name:
        raise ValueError("ZIP 파일 이름이 필요합니다.")

    zip_filename = zip_name if zip_name.lower().endswith(".zip") else f"{zip_name}.zip"
    zip_path = output_path / zip_filename

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for index, case in enumerate(cases, start=1):
            archive.writestr(f"{index}.in", _normalize_newlines(case["input_text"]))
            archive.writestr(f"{index}.out", _normalize_newlines(case["output_text"]))

    return str(zip_path)


def build_default_zip_name(markdown_path):
    stem = Path(markdown_path).stem or "testcases"
    return f"{stem}_testcases.zip"
