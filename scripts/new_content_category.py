from __future__ import annotations

import argparse
import sys
from pathlib import Path

from content_scaffold_lib import (
    ScaffoldError,
    build_category_meta,
    category_root,
    collect_existing_ids,
    ensure_directory_state,
    ensure_id_available,
    next_steps_text,
    normalize_lang,
    parse_positive_int,
    validate_identifier,
    validate_slug,
    validate_track,
    write_text_if_absent,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new content category scaffold.")
    parser.add_argument("--track", required=True)
    parser.add_argument("--lang", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--category-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--part-name", required=True)
    parser.add_argument("--order", required=True)
    parser.add_argument("--with-interactive", action="store_true")
    parser.add_argument("--legacy-path")
    parser.add_argument("--allow-existing-dir", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        track = validate_track(args.track)
        lang_machine, lang_display = normalize_lang(args.lang)
        slug = validate_slug(args.slug)
        category_id = validate_identifier(args.category_id, "category-id")
        order = parse_positive_int(args.order, "order")

        root = category_root(track, lang_machine, slug)
        ensure_directory_state(root, args.allow_existing_dir)

        existing_ids = collect_existing_ids()
        ensure_id_available(category_id, existing_ids, "categoryId")

        meta_path = root / "category.meta.yml"
        lesson_dir = root / "lesson"
        worksheets_dir = root / "worksheets"
        interactive_dir = root / "interactive"

        if args.allow_existing_dir and meta_path.exists():
            raise ScaffoldError(f"{meta_path.as_posix()} already exists")

        root.mkdir(parents=True, exist_ok=True)
        lesson_dir.mkdir(exist_ok=True)
        worksheets_dir.mkdir(exist_ok=True)

        created_paths: list[Path] = []

        if args.with_interactive:
            interactive_dir.mkdir(exist_ok=True)

        meta_text = build_category_meta(
            category_id=category_id,
            track=track,
            lang_display=lang_display,
            title=args.title.strip(),
            part_name=args.part_name.strip(),
            order=order,
            legacy_path=(args.legacy_path or "").strip() or None,
        )
        write_text_if_absent(meta_path, meta_text)
        created_paths.append(meta_path)
        created_paths.append(lesson_dir)
        created_paths.append(worksheets_dir)
        if args.with_interactive:
            created_paths.append(interactive_dir)

        print(next_steps_text(created_paths))
        return 0
    except ScaffoldError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
