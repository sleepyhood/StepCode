import json
import re
from pathlib import Path


ROOT = Path("practice/data/sets")
SKIP_PREFIXES = ("stepcode_log_",)


RE_LOOP = re.compile(r"\bfor\b|\bwhile\b", re.IGNORECASE)
RE_TRACE_HINT = re.compile(r"trace|추적|실행|흐름", re.IGNORECASE)
RE_REVERSE_HINT = re.compile(
    r"(출력).*(입력|초기값|초깃값|조건)|"
    r"(입력|초기값|초깃값).*(출력)|"
    r"(몇\s*회|몇\s*번|몇\s*차|횟수).*(if|조건|참|거짓)|"
    r"(분기|조건).*횟수|"
    r"(중간|직후|반복)\s*상태",
    re.IGNORECASE,
)


def iter_sets(root: Path):
    for path in sorted(root.glob("*.json")):
        if path.name.startswith(SKIP_PREFIXES):
            continue
        yield path


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"__error__": str(e), "__path__": str(path)}


def is_grid_problem(p: dict) -> bool:
    ui = p.get("answerUi") or {}
    return ui.get("kind") == "grid"


def problem_text(p: dict) -> str:
    return " ".join(
        str(p.get(k, "") or "")
        for k in ("title", "description", "code")
    )


def check_set(data: dict, path: Path):
    if "__error__" in data:
        return [f"[ERROR] {path.name}: {data['__error__']}"]

    problems = data.get("problems") or []
    total = len(problems)
    mcq = [p for p in problems if p.get("type") == "mcq"]
    mcq_count = len(mcq)

    warnings = []

    # MCQ 비중 경고 (기본 25% 또는 2개 초과)
    if total > 0:
        max_mcq = max(2, int(total * 0.25))
        if mcq_count > max_mcq:
            warnings.append(
                f"MCQ 비중 높음: {mcq_count}/{total} (권장 <= {max_mcq})"
            )

    # 반복문/추적형은 grid 권장
    loop_short_no_grid = []
    for p in problems:
        if p.get("type") != "short":
            continue
        text = problem_text(p)
        if RE_LOOP.search(text) or RE_TRACE_HINT.search(text):
            if not is_grid_problem(p):
                loop_short_no_grid.append(p.get("id", "?"))
    if loop_short_no_grid:
        warnings.append(
            "반복/추적형 short에서 grid 미사용: " + ", ".join(loop_short_no_grid)
        )

    # 역추적형 포함 여부
    has_reverse = False
    for p in problems:
        text = problem_text(p)
        if RE_REVERSE_HINT.search(text):
            has_reverse = True
            break
    if not has_reverse:
        warnings.append("역추적형 문제 없음(출력→입력/중간상태/분기 추론)")

    if warnings:
        return [f"{path.name}: " + " | ".join(warnings)]
    return []


def main():
    if not ROOT.exists():
        print(f"[ERROR] not found: {ROOT}")
        return

    findings = []
    for path in iter_sets(ROOT):
        data = load_json(path)
        findings.extend(check_set(data, path))

    if not findings:
        print("OK: no warnings")
        return

    print("Warnings:")
    for line in findings:
        print("-", line)


if __name__ == "__main__":
    main()
