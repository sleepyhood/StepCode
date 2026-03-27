# ID and path rules

## Category-level IDs

- `category.meta.yml` uses the category id
- Example: `py_for`

## Lesson-level IDs

- `lesson/lesson.md` front matter uses the concept id
- Example: `py_lv07_for`

## Worksheet document IDs

- `worksheet_*.md` front matter `id` should follow the existing category convention
- Example: `py_lv07_for_basic_r02`

## Worksheet and interactive IDs

- `interactive_*.json` root id and `meta.id` use the worksheet or set id
- Example: `py_lv07_for_b01`

## File naming expectations

- Keep file and folder names in lowercase snake_case unless an explicit documented exception applies
- Keep generator roots aligned with the category slug

## Practical naming pattern

- Category id: short and stable, tied to the learning category
- Lesson id: language + topic level
- Worksheet id: lesson/topic + difficulty + round

## Common failure modes

- Reusing a legacy set id that already exists in `practice/data/sets.index.json`
- Choosing a worksheet id from local round naming alone without checking global occupancy
- Accepting a generated worksheet document id without comparing it to the existing category pattern
- Forgetting to keep lesson prerequisites and next concepts aligned
- Generating content under the wrong category root
- Editing generated output instead of the source files

## Practical note from field test

- Existing worksheet file rounds and globally unique worksheet ids are not always the same namespace.
- When extending an existing category, inspect both:
  - local worksheet file stems such as `worksheet_basic_r01.md`
  - global ids already present in `sets.index.json` or generated indexes
