---
name: stepcode-problem-set-editor
description: Edit StepCode legacy or operating content indexes with consistency checks. Use when adding or modifying `practice/data/sets/*.json`, `practice/data/categories.json`, `practice/data/sets.index.json`, or `practice/data/theory.index.json`, including requests to add a set, add a problem, add a category, connect a theory document, or reconcile `numProblems`, `file`, `categoryId`, or `mdPath`.
---

# StepCode Problem Set Editor

Use this skill for legacy JSON edits and index synchronization. Work from repo root.

## Quick start

1. Read [index-sync.md](references/index-sync.md) for the affected files and sync order.
2. Read [problem-schema.md](references/problem-schema.md) when editing problem objects or theory links.
3. Make the minimum set of coordinated edits across the related JSON files.
4. Run `scripts/check_sets_index.ps1` after changing set contents or `numProblems`.

## Workflow

1. Identify which artifact changed:
   - category
   - set metadata
   - set problem list
   - theory document linkage
2. Update every coupled file in the same pass.
3. Recount problems when the set body changes.
4. Edit metadata by matching the target `id` block, not by blind value replacement.
5. Verify ids, file names, category wiring, and theory paths before finishing.

## Guardrails

- Keep `id`, `categoryId`, `file`, and `numProblems` consistent between the set body and index metadata.
- When fixing repeated `numProblems` mismatches, patch the specific entry block identified by `id` or `file`; do not do sequential global replacements of the same number.
- When adding theory, treat the Markdown file and `theory.index.json` entry as one unit.
- Use the README fallback rules and schema instead of inventing new fields.
- If the request is actually a generator-backed content task, hand off to `stepcode-content-workflow` instead of forcing legacy JSON edits.
