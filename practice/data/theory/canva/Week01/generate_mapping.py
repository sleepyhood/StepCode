import sys
import os
import json
import re
from collections import defaultdict

md_path = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week01\01_LLM_서식_정리\1차시. 캔바 첫 세팅과 작업 영역 적응.md"
pdf_txt_path = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week01\pdf_text.txt"
img_dir = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week01\images"

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

with open(pdf_txt_path, 'r', encoding='utf-8', errors='ignore') as f:
    pdf_text = f.read()
pages = pdf_text.split('\x0c')

ph_matches = list(re.finditer(r'\[이미지 삽입: (IMG_W01_\d{3})\]', md_content))

img_dict = defaultdict(list)
# Populate dict from images folder
if os.path.exists(img_dir):
    for img in os.listdir(img_dir):
        if img.endswith('.png'):
            m = re.match(r'p(\d+)_(\d+)\.png', img)
            if m:
                img_dict[int(m.group(1))].append(img)
for k in img_dict:
    img_dict[k].sort()

def find_page_for_text(text_snippet, start_page=0, end_page=None):
    if end_page is None:
        end_page = len(pages)
    words = text_snippet.split()
    best_match_count = -1
    best_i = start_page
    for i in range(start_page, end_page):
        # Allow checking words that are 2+ chars
        valid_words = [w for w in words[:40] if len(w) > 1]
        match_count = sum(1 for w in valid_words if w in pages[i])
        if match_count > best_match_count and match_count > 0:
            best_match_count = match_count
            best_i = i
    return best_i

# Index 0 is page 16, so offset is 16
current_pdf_page = 0
result = {}

for m in ph_matches:
    ph_id = m.group(1)
    
    start_pos = max(0, m.start() - 300)
    end_pos = min(len(md_content), m.end() + 300)
    context_text = md_content[start_pos:end_pos]
    
    clean_ctx = re.sub(r'\[.+?\]|#+|\*+|-|`|<.+?>', '', context_text).strip()
    
    # Check current page and next 4 pages
    current_pdf_page = find_page_for_text(clean_ctx, max(0, current_pdf_page - 1), min(len(pages), current_pdf_page + 4))
    phys_page = current_pdf_page + 16

    matched_img = None
    if phys_page in img_dict and img_dict[phys_page]:
        matched_img = img_dict[phys_page].pop(0)
    elif phys_page + 1 in img_dict and img_dict[phys_page + 1]:
        phys_page += 1
        matched_img = img_dict[phys_page].pop(0)
    elif phys_page - 1 in img_dict and img_dict[phys_page - 1]:
        phys_page -= 1
        matched_img = img_dict[phys_page].pop(0)
    elif phys_page + 2 in img_dict and img_dict[phys_page + 2]:
        phys_page += 2
        matched_img = img_dict[phys_page].pop(0)
    
    next_text = md_content[m.end():m.end()+150]
    first_sentence = re.split(r'[.!?\n]', next_text.strip())[0].strip()
    first_sentence = re.sub(r'[#*-<`>\[\]]', '', first_sentence).strip()
    if not first_sentence:
        prev_text = md_content[m.start()-150:m.start()]
        sentences = re.split(r'[.!?\n]', prev_text.strip())
        prev_sentence = sentences[-1].strip() if len(sentences) > 0 else " "
        first_sentence = re.sub(r'[#*-<`>\[\]]', '', prev_sentence).strip()
    
    alt_text = first_sentence + ' 설명 이미지' if first_sentence else "설명 이미지"
    
    result[ph_id] = {
        'file_name': matched_img,
        'alt_text': alt_text
    }

out_file = r'C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week01\final_match_complete.json'
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Mapped", len(result), "images")
