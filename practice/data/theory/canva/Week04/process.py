import re
import os
import json

md_path = r"C:\\Users\\osw\\Desktop\\Workspace\\#Projects\\StepCode\\practice\\data\\theory\\canva\\Week04\\01_LLM_서식_정리\\4차시. 실전 디자인 1 - SNS와 포스터 제작.md"
pdf_txt_path = "pdf_text.txt"
img_dir = r"C:\\Users\\osw\\Desktop\\Workspace\\#Projects\\StepCode\\practice\\data\\theory\\canva\\Week04\\images"

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

with open(pdf_txt_path, 'r', encoding='utf-8', errors='ignore') as f:
    pdf_text = f.read()
pages = pdf_text.split('\x0c')

# Build a simple index for pages: PDF page index -> physical page number
# We know PDF page 0 has 228.
page_map = {}
for i, page in enumerate(pages):
    match = re.search(r'(\d+)\s*$', page.strip())
    if match:
        page_map[i] = match.group(1)
    else:
        # Fallback to offset: since index 0 is 228, index i is 228 + i
        page_map[i] = str(228 + i)

# Now go through placeholders.
# Placeholders are like [이미지 삽입: IMG_W04_001]
ph_matches = list(re.finditer(r'\[이미지 삽입: (IMG_W04_\d+)\]', md_content))

# Collect available images
images = os.listdir(img_dir)
from collections import defaultdict
img_dict = defaultdict(list)
for img in images:
    if img.endswith('.png'):
        m = re.match(r'p(\d+)_(\d+)\.png', img)
        if m:
            img_dict[m.group(1)].append(img)
for k in img_dict:
    img_dict[k].sort()

# Also try to match context
result = {}
last_page_idx = 0

for m in ph_matches:
    ph_id = m.group(1)
    # The context is the text surrounding it
    start_ctx = max(0, m.start() - 200)
    end_ctx = min(len(md_content), m.end() + 200)
    ctx = md_content[start_ctx:end_ctx]

    # Find context in PDF
    # let's just use some keywords after the placeholder
    next_text = md_content[m.end():m.end()+150]
    next_text = re.sub(r'\[.+?\]|#+|\*+|-|`', '', next_text).strip()
    next_words = next_text.split()[:5]
    
    found_page = None
    if len(next_words) > 0:
        search_str = " ".join(next_words).replace('\n', ' ')
        for i in range(last_page_idx, len(pages)):
            if all(word in pages[i] for word in next_words if len(word) > 1):
                found_page = i
                break
    
    if found_page is not None:
        last_page_idx = found_page
        phys_page = page_map[found_page]
    else:
        phys_page = page_map[last_page_idx]

    # Pick an image from the physical page
    matched_img = None
    if img_dict[phys_page]:
        matched_img = img_dict[phys_page].pop(0)

    result[ph_id] = {
        "file_name": matched_img,
        "guessed_page": phys_page,
        "context": next_text[:50]
    }

print(json.dumps(result, ensure_ascii=False, indent=2))
