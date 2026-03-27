# PARA rules

## High-level classification

- `Projects`: active work with an end condition
- `Areas`: long-lived operating assets
- `Resources`: reusable references, guides, templates
- `Archives`: completed, experimental, temporary, or regenerable outputs

## Repository-specific placement

### Prefer `Resources/reference/guides/`

- Long-lived operating guides
- Naming rules
- PARA rules
- Repeat-use setup documentation

### Prefer `Projects/active/`

- Task-specific notes
- Temporary working documents
- Short-lived source artifacts for active efforts

### Prefer `Archives/`

- Experimental scripts
- Backups and migration leftovers
- Re-generated outputs
- Temporary capture bundles and work products no longer on the active path

## Protected runtime paths

Treat these as move-resistant unless the request explicitly requires a restructure:

- `practice/`
- `practice/data/**`
- `practice/assets/**`
- `scripts/`
- `docs/`
- `README.md`

## Decision rule

1. Classify the artifact by purpose
2. Check whether it is operationally referenced by current code or tests
3. Check whether it is runtime-critical
4. Choose the PARA bucket
5. Apply naming rules only after the placement decision is stable

## Boundary-case exception rule

When a folder looks temporary but is still directly referenced by active code or tests inside a protected path:

- prefer "documented exception in place" over immediate relocation
- treat it as runtime-adjacent until that dependency is removed
- only move it to `Archives/` or `Projects/active/` after the dependency is intentionally changed
