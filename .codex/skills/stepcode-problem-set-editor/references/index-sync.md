# Index synchronization

## Core files

- `practice/data/categories.json`
- `practice/data/sets.index.json`
- `practice/data/theory.index.json`
- `practice/data/sets/*.json`
- `practice/data/theory/**/*.md`

## Change mapping

### Add or edit a category

- Update `categories.json`
- Update any set metadata that points at the category

### Add or edit a set

- Update `practice/data/sets/<id>.json`
- Update the corresponding row in `sets.index.json`

### Add a problem to an existing set

- Edit the `problems` array in the set JSON
- Recount and update `numProblems` in `sets.index.json`

### Add or edit theory

- Create or edit the Markdown file
- Add or update the matching row in `theory.index.json`

## Required metadata checks

- `id`
- `categoryId`
- `title`
- `round`
- `difficulty`
- `numProblems`
- `file`
- `conceptId`
- `mdPath`

## Validation

Run after set content edits:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_sets_index.ps1
```
