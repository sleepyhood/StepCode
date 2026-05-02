import re

file_path = 'c:/Users/osw/Desktop/Workspace/Projects/StepCode/Resources/tools/crawler_doingcoding_engine.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

funcs_to_remove = [
    'get_solvedac_level_and_tags',
    'scrape_baekjoon',
    'scrape_baekjoon_light',
    'get_solvedac_tier_name',
    'patch_file_badges',
    'analyze_badge_status',
    'has_special_badge'
]

new_lines = []
skip = False

for line in lines:
    # Check if a new top-level function definition starts
    match = re.match(r'^def ([a-zA-Z0-9_]+)\(', line)
    if match:
        func_name = match.group(1)
        if func_name in funcs_to_remove:
            skip = True
        else:
            skip = False

    # Check if we are exiting a function block (a line with no indentation that is not empty/comment)
    # Wait, top-level comments or decorators might break this.
    # Decorators start with @. Comments start with #.
    if skip and line.strip() and not line.startswith(' ') and not line.startswith('def ') and not line.startswith('@') and not line.startswith('#'):
        # We exited the skipped block
        # Actually, let's keep it simple: wait for the next `def ` or end of file.
        pass
        
    # Better logic:
    # If skip is true, and we see `def ` which is NOT in funcs_to_remove, we stop skipping.
    if skip and match and match.group(1) not in funcs_to_remove:
        skip = False

    if not skip:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

