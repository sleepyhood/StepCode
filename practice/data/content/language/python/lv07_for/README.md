# lv07_for Review Workflow

`lv07_for` set data is managed with review markdown as the primary source.

## Source of truth

- Review markdown: `problem_review/problem_review_*.md`
- Generated set JSON: `practice/data/sets/language/py_lv07_for_*.json`

Do not edit set JSON first. Edit review markdown first, then regenerate.

## Target review files

- `problem_review/problem_review_basic_r01.md`
- `problem_review/problem_review_basic_r02.md`
- `problem_review/problem_review_basic_r03.md`
- `problem_review/problem_review_basic_r04.md`
- `problem_review/problem_review_challenge_r02.md`

## Regeneration commands

```powershell
python scripts/generate_language_set_from_review.py `
  --source practice/data/content/language/python/lv07_for/problem_review/problem_review_basic_r01.md `
  --output practice/data/sets/language/py_lv07_for_b01.json `
  --set-id py_lv07_for_b01 `
  --title "Python for문 기초 1회차" `
  --category-id py_for `
  --round 1 `
  --difficulty basic
```

Repeat with:

- `problem_review_basic_r02.md` -> `py_lv07_for_b02.json`
- `problem_review_basic_r03.md` -> `py_lv07_for_b03.json`
- `problem_review_basic_r04.md` -> `py_lv07_for_b04.json`
- `problem_review_challenge_r02.md` -> `py_lv07_for_c01.json` (`round 2`, `difficulty challenge`)

Then regenerate indexes:

```powershell
python scripts/generate_content_indexes.py
```
