import json
import re
import os

md_path = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week03\02_이미지_추가\3차시. 디자인 정돈 및 AI 창작 워크플로 체험.md"
mapping_file = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week03\03_mapping.json"

with open(mapping_file, 'r', encoding='utf-8') as f:
    mapping = json.load(f)

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

for k, v in mapping.items():
    if v and v.get('file_name'):
        img_str = f"![{v['alt_text']}](../images/{v['file_name']})"
        md_content = md_content.replace(f"[이미지 삽입: {k}]", img_str)
    else:
        # If no image found for the placeholder
        md_content = md_content.replace(f"[이미지 삽입: {k}]", f"[이미지 매칭 실패: {k}]")

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"Replacement done for {md_path}")
