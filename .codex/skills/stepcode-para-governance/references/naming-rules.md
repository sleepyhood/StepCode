# Naming rules and exceptions

## Default naming

- Use lowercase snake_case for new files and folders
- Avoid spaces in path names
- Avoid new Korean path names
- Avoid meaningless underscore prefixes

## Exceptions currently tolerated

- Existing runtime-sensitive paths
- Documented legacy exceptions in Canva or language_v2 areas
- `.obsidian` folders
- Temporary or preserved structures that are still under evaluation

## Rename order

1. Safe document and archive paths
2. Temporary work folders
3. Runtime or test-coupled paths last

## Before renaming

- Check whether tests, scripts, or runtime routes depend on the path
- Check the repo naming docs before changing a documented exception
- Record the reason when leaving an exception in place
