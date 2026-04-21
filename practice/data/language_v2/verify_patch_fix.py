import re
import json

def test_patch_logic(content, badges):
    # Mocking the split logic from patch_file_badges
    fm_match = re.match(r"^(---\n)(.*?)(---\n?)(.*)", content, re.DOTALL)
    if not fm_match:
        return "Fail: FM match"

    pre_delim = fm_match.group(1)
    frontmatter = fm_match.group(2)
    end_delim = fm_match.group(3)
    body = fm_match.group(4)

    badges_str = json.dumps(badges, ensure_ascii=False)
    new_field = f"badges: {badges_str}\n"

    # Current logic (Buggy)
    legacy_frontmatter = frontmatter.rstrip("\n") + "\n" + new_field
    current_output = pre_delim + legacy_frontmatter + end_delim + body

    # Proposed fixed logic
    if re.search(r"^badges:", frontmatter, re.MULTILINE):
        fixed_frontmatter = re.sub(r"^badges:.*$", new_field.rstrip(), frontmatter, flags=re.MULTILINE)
    elif re.search(r"^source_url:", frontmatter, re.MULTILINE):
        # Insert BEFORE source_url
        fixed_frontmatter = re.sub(r"^(source_url:)", new_field + r"\1", frontmatter, flags=re.MULTILINE)
    else:
        fixed_frontmatter = frontmatter.rstrip("\n") + "\n" + new_field
    
    fixed_output = pre_delim + fixed_frontmatter + end_delim + body
    
    return current_output, fixed_output

# Mock legacy content
legacy_md = """---
id: bj_1000
tags: ["math"]
tag_keys: ["math"]
source_url: "https://www.acmicpc.net/problem/1000"
---

# Content
"""

badges = ["스페셜 저지"]
current, fixed = test_patch_logic(legacy_md, badges)

print("=== CURRENT (BEFORE) ===")
print(current)
print("\n=== FIXED (AFTER) ===")
print(fixed)
