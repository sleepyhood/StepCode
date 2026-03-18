import json
import re

with open(r'C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week01\final_match_complete.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for k, v in data.items():
    alt = v['alt_text']
    # If the alt text contains "이미지 삽입", clean it
    if "이미지 삽입" in alt:
        new_alt = re.sub(r'이미지 삽입.*?(설명 이미지)', r'\1', alt).strip()
        if new_alt == "설명 이미지" or new_alt == "":
            new_alt = f"{k} 관련 내용 설명 이미지"
        data[k]['alt_text'] = new_alt
        
with open(r'C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week01\final_match_complete.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(json.dumps(data, ensure_ascii=False, indent=2))
