import sys
import os
import json
import re
from collections import defaultdict

md_path = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week05\02_이미지_추가\5차시. 실전 디자인 2 - 기업형 디자인과 자산 관리.md"
pdf_txt_path = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week05\pdf_text.txt"
img_dir = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week05\images"
out_json = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week05\final_match_complete.json"

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

with open(pdf_txt_path, 'r', encoding='utf-8', errors='ignore') as f:
    pdf_text = f.read()
pages = pdf_text.split('\x0c')

ph_matches = list(re.finditer(r'\[(?:이미지 삽입|이미지 매칭 실패): (IMG_W05_[0-9]{3})\]', md_content))

img_dict = defaultdict(list)
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
        valid_words = [w for w in words[:40] if len(w) > 1]
        match_count = sum(1 for w in valid_words if w in pages[i])
        if match_count > best_match_count and match_count > 0:
            best_match_count = match_count
            best_i = i
    return best_i

current_pdf_page = 0
result = {}

for m in ph_matches:
    ph_id = m.group(1)
    
    start_pos = max(0, m.start() - 300)
    end_pos = min(len(md_content), m.end() + 300)
    context_text = md_content[start_pos:end_pos]
    
    clean_ctx = re.sub(r'\[.+?\]|#+|\*+|-|`|<.+?>', '', context_text).strip()
    current_pdf_page = find_page_for_text(clean_ctx, max(0, current_pdf_page - 1), min(len(pages), current_pdf_page + 4))
    
    phys_page = current_pdf_page + 322

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
    sentences = re.split(r'[.!?\n]', next_text.strip())
    first_sentence = sentences[0].strip()
    first_sentence = re.sub(r'[#*-<`>\[\]]', '', first_sentence).strip()
    
    if not first_sentence:
        prev_text = md_content[m.start()-150:m.start()]
        prev_sentences = re.split(r'[.!?\n]', prev_text.strip())
        prev_sentence = prev_sentences[-1].strip() if len(prev_sentences) > 0 else " "
        first_sentence = re.sub(r'[#*-<`>\[\]]', '', prev_sentence).strip()
    
    alt_text = first_sentence + ' 설명 이미지' if first_sentence else "설명 이미지"
    
    result[ph_id] = {
        'file_name': matched_img,
        'alt_text': alt_text
    }

with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Generated {out_json} successfully with {len(result)} items.")
