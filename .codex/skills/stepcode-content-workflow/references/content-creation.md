# Content creation workflow

## Use this flow for

- New category scaffolding
- New lesson scaffolding
- New worksheet and answer scaffolding
- New interactive set scaffolding
- Existing category extension with a new worksheet round
- Content changes that should flow through generated indexes

## Standard order

### Brand-new category flow

1. Create category scaffold with `scripts/new_content_category.py`
2. Create lesson scaffold with `scripts/new_lesson.py`
3. Create worksheet scaffold with `scripts/new_worksheet.py`
4. Fill in source content under `practice/data/content/**`
5. Regenerate indexes with `scripts/generate_content_indexes.py`
6. Verify generated metadata and local app behavior

### Existing category extension flow

1. Inspect current worksheet filenames under the category root
2. Choose the next worksheet round and a globally unique worksheet id
3. Create the worksheet scaffold with `scripts/new_worksheet.py`
4. Replace placeholder worksheet and answer content
5. Regenerate indexes with `scripts/generate_content_indexes.py`
6. Verify generated metadata and local app behavior

## Default command set

```powershell
python scripts/new_content_category.py `
  --track language `
  --lang python `
  --slug lv07_for `
  --category-id py_for `
  --title "Python - Lv7 반복1(for)" `
  --part-name "반복1(for)" `
  --order 207 `
  --with-interactive

python scripts/new_lesson.py `
  --category-root "practice/data/content/language/python/lv07_for" `
  --title "Python Lv7 for문" `
  --lesson-id py_lv07_for `
  --tags "for,loop,range" `
  --recommended-set-id py_lv07_for_b01 `
  --prerequisites py_lv06_if `
  --next-concepts py_lv08_while `
  --priority 3

python scripts/new_worksheet.py `
  --category-root "practice/data/content/language/python/lv07_for" `
  --title "Python for문 기초 1회차" `
  --worksheet-id py_lv07_for_b01 `
  --difficulty basic `
  --round 1 `
  --with-interactive

python scripts/generate_content_indexes.py
```

## Source of truth

- Prefer `practice/data/content/**`
- Treat `practice/data/generated/*.json` as generated output
- Treat direct edits to `categories.json`, `sets.index.json`, and `theory.index.json` as fallback only

## Final checks

- Category is visible in indexes
- Lesson and worksheet ids are linked correctly
- Generated files reflect the new source content
- New worksheet rounds appear in `practice/data/generated/worksheet.index.json`
- Local app pages can discover the new content
