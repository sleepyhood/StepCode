import sys
import os
import json
import re

md_path = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week04\01_LLM_서식_정리\4차시. 실전 디자인 1 - SNS와 포스터 제작.md"
pdf_txt_path = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week04\pdf_text.txt"
img_dir = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week04\images"

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

with open(pdf_txt_path, 'r', encoding='utf-8', errors='ignore') as f:
    pdf_text = f.read()
pages = pdf_text.split('\x0c')

# Find all placeholders up to 067
ph_matches = list(re.finditer(r'\[이미지 삽입: (IMG_W04_0[0-6][0-9])\]', md_content))
ph_matches = [m for m in ph_matches if int(m.group(1).split('_')[-1]) <= 67]

# Gather images and group by page
from collections import defaultdict
img_dict = defaultdict(list)
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
        match_count = sum(1 for w in words[:20] if len(w) > 1 and w in pages[i])
        if match_count > best_match_count and match_count > 0:
            best_match_count = match_count
            best_i = i
    return best_i

result = {}
current_pdf_page = 0

for m in ph_matches:
    ph_id = m.group(1)
    
    # Extract nearby text for matching
    start_pos = max(0, m.start() - 200)
    end_pos = min(len(md_content), m.end() + 200)
    context_text = md_content[start_pos:end_pos]
    
    # Clean text to find match in PDF
    clean_ctx = re.sub(r'\[.+?\]|#+|\*+|-|`|<.+?>', '', context_text).strip()
    
    current_pdf_page = find_page_for_text(clean_ctx, max(0, current_pdf_page - 1), current_pdf_page + 3)
    phys_page = current_pdf_page + 228

    matched_img = None
    if phys_page in img_dict and img_dict[phys_page]:
        matched_img = img_dict[phys_page].pop(0)
    elif phys_page + 1 in img_dict and img_dict[phys_page + 1]:
        phys_page += 1
        matched_img = img_dict[phys_page].pop(0)
    elif phys_page - 1 in img_dict and img_dict[phys_page - 1]:
        phys_page -= 1
        matched_img = img_dict[phys_page].pop(0)
    
    # Generate alt text
    # Pick a sentence next to placeholder
    next_text = md_content[m.end():m.end()+100]
    first_sentence = re.split(r'[.!?\n]', next_text.strip())[0].strip()
    first_sentence = re.sub(r'[#*-<`>\[\]]', '', first_sentence).strip()
    if not first_sentence:
        prev_text = md_content[m.start()-100:m.start()]
        prev_sentence = re.split(r'[.!?\n]', prev_text.strip())[-1].strip()
        first_sentence = re.sub(r'[#*-<`>\[\]]', '', prev_sentence).strip()
    
    alt_text = first_sentence + ' 예시 이미지' if first_sentence else "예시 이미지"
    
    result[ph_id] = {
        'file_name': matched_img,
        'alt_text': alt_text
    }

with open(r'C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week04\final_match.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Done")
