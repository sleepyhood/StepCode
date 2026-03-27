---
name: stepcode-para-governance
description: Apply StepCode's documented PARA rules when deciding where files, folders, documents, or generated artifacts belong. Use when a request asks where to place a new document, whether something belongs in `Projects`, `Areas`, `Resources`, or `Archives`, whether a path should move under `Resources/reference/guides/`, `Projects/active/`, or `Archives/`, or when checking naming-rule exceptions before reorganizing files.
---

# StepCode PARA Governance

Use this skill to classify and place repository artifacts using the existing PARA rules.

## Quick start

1. Read [para-rules.md](references/para-rules.md) for the repository-specific classification rules.
2. Read [naming-rules.md](references/naming-rules.md) when renaming or judging path exceptions.
3. Classify first, move later.
4. Protect runtime-critical paths over cosmetic cleanup.

## Workflow

1. Determine whether the artifact is:
   - active project work
   - long-lived operating asset
   - reusable reference material
   - archive or temporary output
2. Map it to `Projects`, `Areas`, `Resources`, or `Archives`.
3. Check whether the artifact is directly referenced by current code, tests, or active workflow.
4. Check whether the target path is one of the documented protected runtime paths.
5. Check naming rules and exceptions before recommending a rename or move.

## Guardrails

- Do not move `practice/`, `scripts/`, `docs/`, or other runtime-critical paths without a strong reason and explicit request.
- A valid outcome can be "leave in place and document as an exception" when a temp-looking folder is still directly used by current code or tests.
- Classify by operational dependency first; archive only when the artifact is not required by current workflows.
- Prefer `Resources/reference/guides/` for long-lived operational docs.
- Prefer `Projects/active/<slug>/` for temporary work-in-progress notes and artifacts.
- Prefer `Archives/` for regenerated outputs, backups, and experiments no longer on the active path.
