from __future__ import annotations

import argparse
import json
import sys

from content_scaffold_lib import (
    ScaffoldError,
    build_front_matter,
    collect_existing_ids,
    display_path,
    ensure_id_available,
    load_category_meta,
    next_steps_text,
    normalize_lang,
    parse_positive_int,
    resolve_category_root,
    validate_identifier,
    worksheet_doc_id,
    worksheet_file_stem,
    write_text,
)


VALID_DIFFICULTIES = {"basic", "challenge"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create worksheet, answer, and optional interactive scaffold.")
    parser.add_argument("--category-root", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--worksheet-id", required=True)
    parser.add_argument("--difficulty", required=True)
    parser.add_argument("--round", required=True)
    parser.add_argument("--audience", default="common")
    parser.add_argument("--with-interactive", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def build_worksheet_body(title: str) -> str:
    return (
        "\n"
        f"# {title}\n\n"
        "### Q1.\n\n"
        "문항 내용을 작성하세요.\n"
    )


def build_answer_body(title: str) -> str:
    return (
        f"# {title} 정답\n\n"
        "## Q1.\n\n"
        "- 정답:\n"
        "- 해설:\n"
    )


def build_interactive_payload(
    *,
    worksheet_id: str,
    title: str,
    category_id: str,
    track: str,
    lang: str,
    difficulty: str,
    round_no: int,
) -> str:
    payload = {
        "meta": {
            "id": worksheet_id,
            "contentType": "interactive",
            "track": track,
            "lang": lang,
            "categoryId": category_id,
            "title": title,
            "round": round_no,
            "difficulty": difficulty,
            "status": "active",
        },
        "id": worksheet_id,
        "title": title,
        "categoryId": category_id,
        "availableLanguages": [lang],
        "problems": [],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    args = parse_args()

    try:
        category_root = resolve_category_root(args.category_root)
        category = load_category_meta(category_root)
        worksheet_id = validate_identifier(args.worksheet_id, "worksheet-id")

        difficulty = args.difficulty.strip().lower()
        if difficulty not in VALID_DIFFICULTIES:
            raise ScaffoldError("difficulty must be one of: basic, challenge")

        round_no = parse_positive_int(args.round, "round")
        audience = args.audience.strip() or "common"
        lang_machine, _ = normalize_lang(str(category["lang"]))
        track = str(category["track"])
        category_id = str(category["id"])

        stem = worksheet_file_stem(difficulty, round_no)
        worksheet_md_id = worksheet_doc_id(category_root, difficulty, round_no)
        worksheets_dir = category_root / "worksheets"
        interactive_dir = category_root / "interactive"
        worksheet_path = worksheets_dir / f"worksheet_{stem}.md"
        answer_path = worksheets_dir / f"answer_{stem}.md"
        interactive_path = interactive_dir / f"interactive_{stem}.json"

        if not args.force:
            if worksheet_path.exists():
                raise ScaffoldError(f"{display_path(worksheet_path)} already exists")
            if answer_path.exists():
                raise ScaffoldError(f"{display_path(answer_path)} already exists")
            if args.with_interactive and interactive_path.exists():
                raise ScaffoldError(f"{display_path(interactive_path)} already exists")

        existing_ids = collect_existing_ids()
        ensure_id_available(worksheet_md_id, existing_ids, "worksheet document id")
        ensure_id_available(worksheet_id, existing_ids, "worksheetId")

        worksheet_front_matter = build_front_matter(
            [
                ("id", worksheet_md_id),
                ("contentType", "worksheet"),
                ("track", track),
                ("lang", lang_machine),
                ("categoryId", category_id),
                ("title", args.title.strip()),
                ("round", round_no),
                ("difficulty", difficulty),
                ("status", "active"),
                ("audience", audience),
                ("printDefault", True),
            ]
        )
        worksheet_text = worksheet_front_matter + build_worksheet_body(args.title.strip())
        answer_text = build_answer_body(args.title.strip())

        write_text(worksheet_path, worksheet_text)
        write_text(answer_path, answer_text)

        created_paths = [worksheet_path, answer_path]

        if args.with_interactive:
            interactive_dir.mkdir(parents=True, exist_ok=True)
            write_text(
                interactive_path,
                build_interactive_payload(
                    worksheet_id=worksheet_id,
                    title=args.title.strip(),
                    category_id=category_id,
                    track=track,
                    lang=lang_machine,
                    difficulty=difficulty,
                    round_no=round_no,
                ),
            )
            created_paths.append(interactive_path)

        print(next_steps_text(created_paths))
        return 0
    except ScaffoldError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
