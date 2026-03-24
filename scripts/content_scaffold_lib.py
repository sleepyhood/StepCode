from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "practice" / "data"
CONTENT_ROOT = DATA_ROOT / "content"
GENERATED_ROOT = DATA_ROOT / "generated"

VALID_TRACKS = {"language", "unity", "canva", "contest"}
VALID_NAME_RE = re.compile(r"^[a-z0-9_]+$")
VALID_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_]*$")
LANG_DISPLAY = {
    "python": "Python",
    "c": "C",
    "java": "Java",
    "csharp": "C#",
    "canva": "Canva",
}


class ScaffoldError(Exception):
    pass


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text_if_absent(path: Path, content: str):
    if path.exists():
        raise ScaffoldError(f"{display_path(path)} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def normalize_lang(lang: str) -> tuple[str, str]:
    machine = lang.strip().lower()
    if machine not in LANG_DISPLAY:
        supported = ", ".join(sorted(LANG_DISPLAY))
        raise ScaffoldError(f"lang must be one of: {supported}")
    return machine, LANG_DISPLAY[machine]


def validate_track(track: str) -> str:
    value = track.strip().lower()
    if value not in VALID_TRACKS:
        allowed = ", ".join(sorted(VALID_TRACKS))
        raise ScaffoldError(f"track must be one of: {allowed}")
    return value


def validate_slug(slug: str) -> str:
    value = slug.strip().lower()
    if not VALID_SLUG_RE.fullmatch(value):
        raise ScaffoldError("slug must match ^[a-z0-9][a-z0-9_]*$")
    return value


def validate_identifier(name: str, label: str) -> str:
    value = name.strip()
    if not VALID_NAME_RE.fullmatch(value):
        raise ScaffoldError(f"{label} must match ^[a-z0-9_]+$")
    return value


def parse_positive_int(raw: str, label: str) -> int:
    try:
        value = int(raw)
    except ValueError as exc:
        raise ScaffoldError(f"{label} must be an integer") from exc
    if value <= 0:
        raise ScaffoldError(f"{label} must be a positive integer")
    return value


def parse_csv_list(raw: str | None) -> list[str]:
    if raw is None:
        return []
    parts = [part.strip() for part in raw.split(",")]
    return [part for part in parts if part]


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
            raise ScaffoldError(f"invalid metadata line at {lineno}: {raw}")
        key, value = raw.split(":", 1)
        out[key.strip()] = parse_scalar(value)
    return out


def load_json_list(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        payload = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise ScaffoldError(f"invalid json in {display_path(path)}: {exc}") from exc
    if not isinstance(payload, list):
        raise ScaffoldError(f"{display_path(path)} must contain a JSON array")
    return [item for item in payload if isinstance(item, dict)]


def iter_content_metadata() -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []

    for meta_path in sorted(CONTENT_ROOT.glob("**/category.meta.yml")):
        meta = parse_simple_yaml(read_text(meta_path))
        content_id = str(meta.get("id") or "").strip()
        if content_id:
            found.append((content_id, display_path(meta_path)))

    for md_path in sorted(CONTENT_ROOT.glob("**/*.md")):
        try:
            text = read_text(md_path)
        except OSError:
            continue
        if not text.startswith("---\n"):
            continue
        parts = text.split("\n---\n", 1)
        if len(parts) != 2:
            continue
        meta = parse_simple_yaml("\n".join(parts[0].splitlines()[1:]))
        content_id = str(meta.get("id") or "").strip()
        if content_id:
            found.append((content_id, display_path(md_path)))

    for json_path in sorted(CONTENT_ROOT.glob("**/*.json")):
        try:
            payload = json.loads(read_text(json_path))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict):
            meta = payload.get("meta")
            if isinstance(meta, dict):
                content_id = str(meta.get("id") or "").strip()
                if content_id:
                    found.append((content_id, display_path(json_path)))

    return found


def collect_existing_ids() -> dict[str, str]:
    found: dict[str, str] = {}

    for content_id, source in iter_content_metadata():
        found.setdefault(content_id, source)

    for item in load_json_list(DATA_ROOT / "categories.json"):
        content_id = str(item.get("id") or "").strip()
        if content_id:
            found.setdefault(content_id, display_path(DATA_ROOT / "categories.json"))

    for item in load_json_list(DATA_ROOT / "sets.index.json"):
        content_id = str(item.get("id") or "").strip()
        if content_id:
            found.setdefault(content_id, display_path(DATA_ROOT / "sets.index.json"))

    for item in load_json_list(DATA_ROOT / "theory.index.json"):
        content_id = str(item.get("conceptId") or "").strip()
        if content_id:
            found.setdefault(content_id, display_path(DATA_ROOT / "theory.index.json"))
        category_id = str(item.get("categoryId") or "").strip()
        if category_id:
            found.setdefault(category_id, display_path(DATA_ROOT / "theory.index.json"))
        recommended = str(item.get("recommendedSetId") or "").strip()
        if recommended:
            found.setdefault(recommended, display_path(DATA_ROOT / "theory.index.json"))

    for json_path in sorted(GENERATED_ROOT.glob("*.json")):
        for item in load_json_list(json_path):
            for key in ("id", "conceptId", "categoryId", "recommendedSetId"):
                value = str(item.get(key) or "").strip()
                if value:
                    found.setdefault(value, display_path(json_path))

    return found


def ensure_id_available(content_id: str, existing_ids: dict[str, str], label: str):
    source = existing_ids.get(content_id)
    if source:
        raise ScaffoldError(f"{label} {content_id} already exists in {source}")


def category_root(track: str, lang: str, slug: str) -> Path:
    return CONTENT_ROOT / track / lang / slug


def resolve_category_root(raw_path: str) -> Path:
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = (ROOT / candidate).resolve()
    return candidate


def load_category_meta(root: Path) -> dict:
    meta_path = root / "category.meta.yml"
    if not meta_path.exists():
        raise ScaffoldError(f"category.meta.yml not found under {display_path(root)}")
    meta = parse_simple_yaml(read_text(meta_path))
    required = ("id", "track", "lang", "name", "order", "status")
    missing = [key for key in required if not str(meta.get(key) or "").strip()]
    if missing:
        joined = ", ".join(missing)
        raise ScaffoldError(f"{display_path(meta_path)} missing required metadata: {joined}")
    return meta


def scalar_to_yaml(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        inner = ", ".join(scalar_to_yaml(item) for item in value)
        return f"[{inner}]"
    text = str(value)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def build_front_matter(meta: list[tuple[str, object]]) -> str:
    lines = ["---"]
    for key, value in meta:
        lines.append(f"{key}: {scalar_to_yaml(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def build_category_meta(
    *,
    category_id: str,
    track: str,
    lang_display: str,
    title: str,
    part_name: str,
    order: int,
    legacy_path: str | None,
) -> str:
    lines = [
        f"id: {category_id}",
        f"track: {track}",
        f"lang: {lang_display}",
        f"name: {title}",
        f"partName: {part_name}",
        f"order: {order}",
        "status: active",
    ]
    if legacy_path:
        lines.append(f"legacySourcePath: {legacy_path}")
    return "\n".join(lines) + "\n"


def ensure_directory_state(path: Path, allow_existing_dir: bool):
    if path.exists() and not path.is_dir():
        raise ScaffoldError(f"{display_path(path)} exists and is not a directory")
    if path.exists() and not allow_existing_dir:
        raise ScaffoldError(f"{display_path(path)} already exists")


def next_steps_text(created_paths: list[Path]) -> str:
    lines = ["Created:"]
    for path in created_paths:
        lines.append(f"- {display_path(path)}")
    lines.extend(
        [
            "",
            "Next:",
            "1. 본문 내용을 작성하세요.",
            "2. python scripts/generate_content_indexes.py 를 실행하세요.",
            "3. index.html 에서 반영 여부를 확인하세요.",
        ]
    )
    return "\n".join(lines)


def worksheet_file_stem(difficulty: str, round_no: int) -> str:
    return f"{difficulty}_r{round_no:02d}"


def worksheet_doc_id(category_root: Path, difficulty: str, round_no: int) -> str:
    slug = category_root.name
    return f"{slug}_{difficulty}_r{round_no:02d}"
