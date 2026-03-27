---
name: stepcode-content-workflow
description: Create or extend StepCode content using the repo's generator-first workflow. Use when adding a new category, extending an existing category with a new worksheet round, creating a lesson, worksheet, answer sheet, or interactive set under `practice/data/content/**`, or when a request mentions `new_content_category.py`, `new_lesson.py`, `new_worksheet.py`, or `generate_content_indexes.py`. Prefer this skill over direct JSON editing unless the request is explicitly about legacy fallback files.
---

# StepCode Content Workflow

Use the generator-first workflow for new content. Work from repo root.

## Quick start

1. Read [content-creation.md](references/content-creation.md) for the standard sequence.
2. Read [content-ids.md](references/content-ids.md) when naming or wiring IDs.
3. Prefer `practice/data/content/**` as the source of truth.
4. Regenerate indexes after content changes.
5. Treat direct edits to `categories.json`, `sets.index.json`, and `theory.index.json` as fallback only.

## Workflow

1. Confirm whether the request is:
   - a brand-new category flow, or
   - an existing category extension with a new worksheet round.
2. If extending an existing category, inspect the current worksheet filenames and round pattern before generating the next round.
3. If the task needs a globally unique worksheet or interactive id, inspect existing set and generated ids before choosing it.
4. Run the generators in the needed order:
   - new category flow: `new_content_category.py` -> `new_lesson.py` -> `new_worksheet.py`
   - existing category extension: `new_worksheet.py`
5. Replace scaffold placeholder content with at least minimally usable worksheet and answer content.
6. Run `scripts/generate_content_indexes.py`.
7. Verify the result in generated metadata first, then in local app pages if needed.

## Guardrails

- Keep new content in the generator-backed structure unless the request explicitly targets legacy JSON.
- Keep IDs aligned across category meta, lesson front matter, worksheet ids, worksheet document ids, and interactive ids.
- Inspect both local round naming and global id occupancy before choosing a new worksheet or interactive id.
- Check generated scaffold ids against the existing category convention before accepting them as final.
- Do not skip index regeneration after source changes.
- Treat scaffold placeholders as incomplete; fill the generated files with minimally usable content before considering the task done.
- If the user asks for both content creation and legacy JSON edits, generate the source structure first and explain any fallback edits separately.
