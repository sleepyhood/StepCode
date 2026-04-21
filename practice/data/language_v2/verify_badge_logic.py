import re
import json

def analyze_badge_status(content):
    fm_match = re.match(r"^(---\n)(.*?)(---\n?)", content, re.DOTALL)
    if not fm_match: return "ERROR", None
    fm = fm_match.group(2)
    
    badge_match = re.search(r"^badges:\s*(.*)$", fm, re.MULTILINE)
    if not badge_match:
        return "MISSING", None
        
    try:
        badges = json.loads(badge_match.group(1))
    except:
        badges = []
        
    source_url_match = re.search(r"^source_url:", fm, re.MULTILINE)
    if source_url_match:
        # Check if badges is immediately followed by source_url
        if re.search(r"^badges:.*\nsource_url:", fm, re.MULTILINE):
            return "CORRECT", badges
        else:
            return "WRONG_POSITION", badges
    return "CORRECT", badges

def patch_file_badges_improved(content, badges):
    fm_match = re.match(r"^(---\n)(.*?)(---\n?)(.*)", content, re.DOTALL)
    if not fm_match: return None
    
    pre = fm_match.group(1)
    fm = fm_match.group(2)
    end = fm_match.group(3)
    body = fm_match.group(4)
    
    new_field = f"badges: {json.dumps(badges, ensure_ascii=False)}\n"
    
    # 1. Remove existing badges line if it exists
    fm = re.sub(r"^badges:.*$\n?", "", fm, flags=re.MULTILINE)
    
    # 2. Insert in correct position
    if re.search(r"^source_url:", fm, re.MULTILINE):
        fm = re.sub(r"^(source_url:)", new_field + r"\1", fm, flags=re.MULTILINE)
    else:
        fm = fm.rstrip("\n") + "\n" + new_field
        
    return pre + fm + end + body

# Test Cases
casess = [
    ("Missing badges", """---
id: 1000
source_url: "url"
---
body"""),
    ("Correct badges", """---
id: 1000
badges: ["A"]
source_url: "url"
---
body"""),
    ("Wrong position", """---
id: 1000
source_url: "url"
badges: ["A"]
---
body"""),
    ("Wrong position 2 (badges at top)", """---
badges: ["A"]
id: 1000
source_url: "url"
---
body""")
]

for name, content in casess:
    status, val = analyze_badge_status(content)
    print(f"CASE: {name} -> Status: {status}, Val: {val}")
    if status != "CORRECT":
        patched = patch_file_badges_improved(content, val or ["NEW"])
        print("Patched Result:")
        print(patched)
        print("-" * 20)
