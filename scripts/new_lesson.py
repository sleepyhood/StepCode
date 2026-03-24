from __future__ import annotations

import argparse
import sys
from pathlib import Path

from content_scaffold_lib import (
    ScaffoldError,
    build_front_matter,
    collect_existing_ids,
    display_path,
    ensure_id_available,
    load_category_meta,
    next_steps_text,
    normalize_lang,
    parse_csv_list,
    parse_positive_int,
    resolve_category_root,
    validate_identifier,
    write_text,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new lesson scaffold.")
    parser.add_argument("--category-root", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--lesson-id", required=True)
    parser.add_argument("--tags")
    parser.add_argument("--recommended-set-id")
    parser.add_argument("--prerequisites")
    parser.add_argument("--next-concepts")
    parser.add_argument("--priority", default="2")
    parser.add_argument("--audience", default="common")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def build_lesson_body(title: str) -> str:
    return (
        "\n"
        f"# {title}\n\n"
        "> [!goal]\n"
        "> 오늘의 목표\n"
        "> - 목표 1\n"
        "> - 목표 2\n"
    )


def main() -> int:
    args = parse_args()

    try:
        category_root = resolve_category_root(args.category_root)
        category = load_category_meta(category_root)
        lesson_id = validate_identifier(args.lesson_id, "lesson-id")
        priority = parse_positive_int(args.priority, "priority")
        audience = args.audience.strip() or "common"

        existing_ids = collect_existing_ids()
        ensure_id_available(lesson_id, existing_ids, "lessonId")

        lang_machine, _ = normalize_lang(str(category["lang"]))
        lesson_path = category_root / "lesson" / "lesson.md"

        if lesson_path.exists() and not args.force:
            raise ScaffoldError(f"{display_path(lesson_path)} already exists")

        tags = parse_csv_list(args.tags)
        prerequisites = parse_csv_list(args.prerequisites)
        next_concepts = parse_csv_list(args.next_concepts)
        recommended_set_id = (args.recommended_set_id or "").strip()

        front_matter = build_front_matter(
            [
                ("id", lesson_id),
                ("contentType", "lesson"),
                ("track", str(category["track"])),
                ("lang", lang_machine),
                ("categoryId", str(category["id"])),
                ("title", args.title.strip()),
                ("status", "active"),
                ("order", int(category["order"])),
                ("audience", audience),
                ("tags", tags),
                ("recommendedSetId", recommended_set_id),
                ("relatedSetIds", []),
                ("prerequisites", prerequisites),
                ("nextConcepts", next_concepts),
                ("priority", priority),
            ]
        )
        content = front_matter + build_lesson_body(args.title.strip())
        write_text(lesson_path, content)

        print(next_steps_text([lesson_path]))
        return 0
    except ScaffoldError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
