# Problem schema checklist

## Common fields

- `id`
- `type`
- `level`
- `title`
- `description`
- `code`

## MCQ

- `options`
- `optionLabels`
- `correctIndex`

## Short answer

- `expectedText` or `expectedAnyOf`

## Code answer

- `expectedCode`
- optional `hint`

## Theory linkage checklist

- `conceptId` is stable and unique
- `categoryId` points to an existing category
- `title` matches the displayed concept name
- `mdPath` points to an existing Markdown file

## Editing rules

- Do not invent new schema fields for a single set
- Keep problem ids unique within the set
- Keep the set `id` identical to the row in `sets.index.json`
- Use existing difficulty values unless the repo rules are intentionally changed
