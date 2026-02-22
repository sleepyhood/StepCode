#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


DEFAULT_TEMPLATE = Path(
    "practice/data/theory/contest/checklists/py_theory_contest_w01_w12_concept_checklist.md"
)
DEFAULT_OUT_DIR = Path("practice/data/theory/contest/checklists/students")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate per-student Python theory contest checklist files."
    )
    parser.add_argument(
        "--names",
        nargs="*",
        default=[],
        help="Student names (space-separated or quoted). Example: --names 홍길동 김철수",
    )
    parser.add_argument(
        "--names-file",
        type=Path,
        help="Path to a text file with one student name per line.",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=DEFAULT_TEMPLATE,
        help=f"Checklist template path (default: {DEFAULT_TEMPLATE})",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUT_DIR})",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned outputs without creating files.",
    )
    return parser.parse_args()


def read_names(cli_names: list[str], names_file: Path | None) -> list[str]:
    names: list[str] = []
    names.extend(n.strip() for n in cli_names if n.strip())

    if names_file:
        if not names_file.exists():
            raise FileNotFoundError(f"names file not found: {names_file}")
        lines = names_file.read_text(encoding="utf-8").splitlines()
        names.extend(line.strip() for line in lines if line.strip())

    # Keep order, remove duplicates.
    unique: list[str] = []
    seen: set[str] = set()
    for name in names:
        if name not in seen:
            seen.add(name)
            unique.append(name)
    return unique


def safe_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)
    cleaned = re.sub(r"\s+", "_", cleaned).strip("._")
    return cleaned or "student"


def fill_student_info(template_text: str, name: str) -> str:
    today = dt.date.today().isoformat()
    text = re.sub(r"^- 이름:\s*$", f"- 이름: {name}", template_text, flags=re.MULTILINE)
    text = re.sub(r"^- 체크일:\s*$", f"- 체크일: {today}", text, flags=re.MULTILINE)
    return text


def main() -> int:
    args = parse_args()
    names = read_names(args.names, args.names_file)

    if not names:
        print("No student names provided. Use --names or --names-file.")
        return 1

    if not args.template.exists():
        print(f"Template not found: {args.template}")
        return 1

    template_text = args.template.read_text(encoding="utf-8")
    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    created = 0
    skipped = 0
    for name in names:
        filename = f"py_theory_contest_checklist_{safe_filename(name)}.md"
        out_path = out_dir / filename

        if out_path.exists() and not args.overwrite:
            print(f"SKIP (exists): {out_path}")
            skipped += 1
            continue

        filled = fill_student_info(template_text, name)
        if args.dry_run:
            print(f"DRY-RUN: would write {out_path}")
        else:
            out_path.write_text(filled, encoding="utf-8")
            print(f"OK: {out_path}")
        created += 1

    print(f"Done. created={created}, skipped={skipped}, total_names={len(names)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
