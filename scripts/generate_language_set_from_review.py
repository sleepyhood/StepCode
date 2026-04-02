from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


META_RE = re.compile(r"^([a-z_]+):\s*(.*)$")
PROBLEM_HEADER_RE = re.compile(r"^##\s+Problem\s+\d+\s*$", re.M)


class ReviewParseError(Exception):
    pass


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ReviewParseError("front matter is required")
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ReviewParseError("front matter closing marker is missing")
    meta_block = parts[0].splitlines()[1:]
    meta: dict[str, str] = {}
    for line in meta_block:
        stripped = line.strip()
        if not stripped:
            continue
        m = META_RE.match(stripped)
        if not m:
            raise ReviewParseError(f"invalid front matter line: {line}")
        key = m.group(1)
        value = m.group(2).strip().strip('"')
        meta[key] = value
    return meta, parts[1].lstrip("\n")


def split_problem_blocks(body: str) -> list[str]:
    matches = list(PROBLEM_HEADER_RE.finditer(body))
    if not matches:
        raise ReviewParseError("no problem blocks found")
    blocks: list[str] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        blocks.append(body[start:end].strip())
    return blocks


def extract_section(block: str, name: str) -> str:
    marker = f"### {name}"
    i = block.find(marker)
    if i < 0:
        return ""
    rest = block[i + len(marker) :].lstrip("\n")
    markers = [rest.find("\n### prompt"), rest.find("\n### starter"), rest.find("\n### choices"), rest.find("\n### answer")]
    markers = [x for x in markers if x >= 0]
    end = min(markers) if markers else len(rest)
    return rest[:end].strip()


def parse_scalar_field(block: str, key: str, required: bool = True) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:\s*(.+)$", re.M)
    m = pattern.search(block)
    if not m:
        if required:
            raise ReviewParseError(f"missing field: {key}")
        return ""
    return m.group(1).strip().strip('"')


def parse_code_fence(text: str, language: str) -> str:
    pattern = re.compile(rf"```{re.escape(language)}\n(.*?)```", re.S)
    m = pattern.search(text)
    if not m:
        return ""
    return m.group(1).rstrip("\n")


def parse_json_fence(text: str) -> dict:
    m = re.search(r"```json\n(.*?)```", text, re.S)
    if not m:
        raise ReviewParseError("answer json block is missing")
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError as exc:
        raise ReviewParseError(f"invalid answer json: {exc}") from exc
    if not isinstance(data, dict):
        raise ReviewParseError("answer json must be an object")
    return data


def parse_choices(text: str) -> list[str]:
    out: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            choice = stripped[2:].strip()
            if choice.lower() in {"(none)", "none", "-"}:
                continue
            out.append(choice)
    return out


def parse_problem(block: str) -> dict:
    problem = {
        "id": parse_scalar_field(block, "id"),
        "type": parse_scalar_field(block, "type"),
        "level": parse_scalar_field(block, "level"),
        "title": parse_scalar_field(block, "title"),
        "description": extract_section(block, "prompt"),
    }

    starter = parse_code_fence(extract_section(block, "starter"), "python")
    if starter:
        problem["code"] = starter

    choices = parse_choices(extract_section(block, "choices"))
    if choices:
        problem["choices"] = choices

    answer_obj = parse_json_fence(extract_section(block, "answer"))
    for key in (
        "answerUi",
        "expectedGrid",
        "expectedText",
        "expectedCode",
        "ioExample",
        "correctIndexes",
        "optionLabels",
        "minSelections",
        "maxSelections",
    ):
        if key in answer_obj:
            problem[key] = answer_obj[key]
    return problem


def parse_review_markdown(path: Path, cli_args: argparse.Namespace) -> dict:
    raw = read_text(path).replace("\r\n", "\n")
    meta, body = parse_front_matter(raw)
    required = ["set_id", "category_id", "title", "round", "difficulty", "lang"]
    missing = [key for key in required if key not in meta or not meta[key]]
    if missing:
        raise ReviewParseError(f"missing front matter keys: {', '.join(missing)}")

    if cli_args.set_id and cli_args.set_id != meta["set_id"]:
        raise ReviewParseError(f"set-id mismatch: cli={cli_args.set_id}, md={meta['set_id']}")
    if cli_args.category_id and cli_args.category_id != meta["category_id"]:
        raise ReviewParseError(f"category-id mismatch: cli={cli_args.category_id}, md={meta['category_id']}")
    if cli_args.title and cli_args.title != meta["title"]:
        raise ReviewParseError(f"title mismatch: cli={cli_args.title}, md={meta['title']}")
    if cli_args.round and int(cli_args.round) != int(meta["round"]):
        raise ReviewParseError(f"round mismatch: cli={cli_args.round}, md={meta['round']}")
    if cli_args.difficulty and cli_args.difficulty != meta["difficulty"]:
        raise ReviewParseError(f"difficulty mismatch: cli={cli_args.difficulty}, md={meta['difficulty']}")

    problems = [parse_problem(block) for block in split_problem_blocks(body)]
    payload = {
        "id": meta["set_id"],
        "title": meta["title"],
        "categoryId": meta["category_id"],
        "availableLanguages": [meta["lang"]],
        "problems": problems,
    }
    return payload


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="language 검수 markdown을 set json으로 변환합니다.")
    parser.add_argument("--source", required=True, help="검수 markdown 경로")
    parser.add_argument("--output", required=True, help="생성할 set json 경로")
    parser.add_argument("--set-id", help="set id 강제 검증")
    parser.add_argument("--title", help="title 강제 검증")
    parser.add_argument("--category-id", help="category id 강제 검증")
    parser.add_argument("--round", help="round 강제 검증")
    parser.add_argument("--difficulty", help="difficulty 강제 검증")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    source = Path(args.source).resolve()
    output = Path(args.output).resolve()
    payload = parse_review_markdown(source, args)
    write_json(output, payload)
    print(f"OK: generated {output}")


if __name__ == "__main__":
    main()
