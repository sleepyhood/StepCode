import os
import json
import re
import shutil

BASE_DIR = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data"
THEORY_DIR = os.path.join(BASE_DIR, "theory", "language")
SETS_DIR = os.path.join(BASE_DIR, "sets", "language")
V2_DIR = os.path.join(BASE_DIR, "language_v2")

def get_mapped_topic(topic, filename):
    # Mapping old names to new standard theory topic names
    if topic == 'if':
        return 'lv06_if'
    if topic == 'array':
        return 'lv10_array'
    if topic == 'array2d':
        return 'lv15_array2d'
    return topic

def extract_metadata_from_filename(filename):
    basename = filename.replace('.json', '')
    pattern = r'^(c|py|java)_(.+?)_([bc]\d+)$'
    match = re.search(pattern, basename)
    if match:
        lang = match.group(1)
        topic_part = match.group(2)
        round_str = match.group(3)
        
        # fix b1 -> b01 to normalize format
        if len(round_str) == 2 and round_str.startswith('b'):
            round_str = f"b0{round_str[1]}"
            
        topic_part = get_mapped_topic(topic_part, basename)
        return lang, topic_part, round_str
    return None, None, None

def create_md_content(data, filename):
    lines = []
    lines.append("---")
    lines.append(f"id: \"{data.get('id', '')}\"")
    lines.append(f"title: \"{data.get('title', '')}\"")
    lines.append(f"categoryId: \"{data.get('categoryId', '')}\"")
    if 'availableLanguages' in data:
        lines.append(f"availableLanguages: {json.dumps(data.get('availableLanguages'))}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {data.get('title', '')}")
    lines.append("")
    
    for idx, prob in enumerate(data.get('problems', [])):
        title = prob.get('title', '문제').replace('\n', ' ')
        lines.append(f"### Q{idx+1}. {title}")
        lines.append("")
        desc = prob.get('description', '')
        if desc:
            lines.append(desc)
            lines.append("")
            
        if prob.get('code'):
            lang_lbl = "c"
            lines.append("```" + lang_lbl)
            lines.append(prob.get('code'))
            lines.append("```")
            lines.append("")
            
        if prob.get('type') == 'mcq' and 'options' in prob:
            for i, opt in enumerate(prob['options']):
                lbl = prob.get('optionLabels', ['A','B','C','D'])[i] if i < len(prob.get('optionLabels', [])) else str(i)
                lines.append(f"- **{lbl}**: {opt.replace(chr(10), ' ')}")
            lines.append("")
            
        lines.append("---")
        lines.append("<!-- ANSWER_START -->")
        lines.append("### [답안 및 해설]")
        if prob.get('type') == 'mcq':
            lines.append(f"- **정답 인덱스:** {prob.get('correctIndex')}")
        elif prob.get('type') == 'short':
            if 'expectedText' in prob:
                lines.append(f"- **정답:** `{prob.get('expectedText')}`")
            if 'expectedGrid' in prob:
                lines.append(f"- **Trace 정답 표:** {json.dumps(prob.get('expectedGrid'), ensure_ascii=False)}")
            if 'expectedAnyOf' in prob:
                lines.append(f"- **복수 정답 허용:** {json.dumps(prob.get('expectedAnyOf'), ensure_ascii=False)}")
        elif prob.get('type') == 'code':
            lines.append(f"- **모범 코드:**\n```c\n{prob.get('expectedCode')}\n```")
        else:
            lines.append("- (추가 해설 없음)")
        lines.append("<!-- ANSWER_END -->")
        lines.append("")
        
    return "\n".join(lines)

def run():
    print("Starting migration...")
    if os.path.exists(V2_DIR):
        shutil.rmtree(V2_DIR)
    os.makedirs(V2_DIR)
    
    # 1. Theories
    if os.path.exists(THEORY_DIR):
        for f in os.listdir(THEORY_DIR):
            if not f.endswith('.md'): continue
            basename = f.replace('.md', '')
            
            is_guide = False
            topic = ""
            if basename.startswith('guide_'):
                is_guide = True
                topic = basename.replace('guide_', '')
            elif basename.startswith('theory_'):
                topic = basename.replace('theory_', '')
            else:
                continue
                
            docs_path = os.path.join(V2_DIR, topic, "_docs")
            os.makedirs(os.path.join(docs_path, "reference"), exist_ok=True)
            
            src_path = os.path.join(THEORY_DIR, f)
            dest_name = "guide.md" if is_guide else "theory.md"
            dst_path = os.path.join(docs_path, dest_name)
            shutil.copy2(src_path, dst_path)
            
    # 2. Sets
    count = 0
    if os.path.exists(SETS_DIR):
        for f in os.listdir(SETS_DIR):
            if not f.endswith('.json'): continue
            lang, topic, round_str = extract_metadata_from_filename(f)
            if not topic:
                print(f"Skipping format mismatch: {f}")
                continue
                
            src_path = os.path.join(SETS_DIR, f)
            with open(src_path, 'r', encoding='utf-8-sig') as file_obj:
                try:
                    data = json.load(file_obj)
                except Exception as e:
                    print(f"Failed to read {f}: {e}")
                    continue
                    
            md_content = create_md_content(data, f)
            dest_dir = os.path.join(V2_DIR, topic, lang)
            os.makedirs(dest_dir, exist_ok=True)
            dst_path = os.path.join(dest_dir, f"{round_str}.md")
            
            with open(dst_path, 'w', encoding='utf-8') as out_f:
                out_f.write(md_content)
            count += 1
            
    print(f"Migration Success! Converted {count} json files.")

if __name__ == "__main__":
    run()
