import os
import re

input_dir = r"c:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\jungol\output"
output_dir = r"c:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\jungol\output\formatted_txt"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

files = ["초등_수업.txt", "중등_수업.txt", "고등_수업.txt", "초등_숙제.txt", "중등_숙제.txt", "고등_숙제.txt"]

def generate_formats(text, filename):
    prefix = ""
    if "초등" in filename: prefix = "초등"
    elif "중등" in filename: prefix = "중등"
    elif "고등" in filename: prefix = "고등"
    
    lines = text.split('\n')
    problems = []
    
    state = "NONE"
    prob_text = []
    exp_text = []
    current_week = f"{prefix} 1주차" # fallback
    
    for line in lines:
        if re.match(r'^\[.*?예상문제\]|\[.*?추가문제\]', line.strip()):
            continue
            
        week_num_match = re.match(r'^(\d+)주차:', line.strip())
        if week_num_match:
            current_week = f"{prefix} {week_num_match.group(1)}주차"
            continue
            
        if re.match(r'^\[문제 \d+ 텍스트\]', line.strip()):
            state = "TEXT"
            prob_text = []
            continue
            
        if re.match(r'^\[문제 \d+ 상세 해설\]', line.strip()):
            state = "EXP"
            exp_text = []
            continue
            
        if line.strip() == "===":
            if prob_text and exp_text:
                problems.append({
                    "week": current_week,
                    "text": "\n".join(prob_text).strip(),
                    "exp": "\n".join(exp_text).strip()
                })
            state = "NONE"
            prob_text = []
            exp_text = []
            continue
            
        if state == "TEXT":
            prob_text.append(line)
        elif state == "EXP":
            exp_text.append(line)
            
    if prob_text and exp_text:
        problems.append({
            "week": current_week,
            "text": "\n".join(prob_text).strip(),
            "exp": "\n".join(exp_text).strip()
        })
        
    student_out = []
    teacher_out = []
    
    for p in problems:
        t_text = p['text']
        t_exp = p['exp']
        
        # Remove top header like "--- 2024 초등 ---"
        t_text = re.sub(r'^---\s*\d+\s*[가-힣]+\s*---\n+', '', t_text).strip()
        
        # Extract number
        num_match = re.match(r'^(\d+)\.\s*', t_text)
        if num_match:
            num = num_match.group(1)
            t_desc = t_text[num_match.end():].strip()
        else:
            num = "?"
            t_desc = t_text
            
        ans_match = re.search(r'\n*정답:\s*(.*)$', t_desc)
        correct_answer = ""
        if ans_match:
            correct_answer = ans_match.group(1).strip()
            t_desc = t_desc[:ans_match.start()].strip()
            
        options_matches = list(re.finditer(r'»○\s*(.*?)(?=\n\s*»○|\Z)', t_desc, re.DOTALL))
        
        if options_matches:
            # Objective
            student_question_part = t_desc[:options_matches[0].start()].strip()
            
            opts_student = []
            opts_teacher = []
            for i, m in enumerate(options_matches):
                opt = m.group(1).strip()
                opt_clean = opt.replace("(정답)", "").strip()
                
                circ = chr(ord('①') + i)
                opts_student.append(f"{circ} {opt_clean}")
                
                if "(정답)" in opt:
                    opts_teacher.append(f"{circ} {opt_clean} (정답)")
                else:
                    opts_teacher.append(f"{circ} {opt_clean}")
                    
            student_opts_str = "\t".join(opts_student)
            teacher_opts_str = "\t".join(opts_teacher)
            
            s_block = (
                "// 객관식\n"
                f"<{p['week']}>\n"
                f"{num}. {student_question_part}\n"
                f"{student_opts_str}"
            )
            
            t_block = (
                "// 객관식\n"
                "// 교사용에는 선택지 뒤에 정답이 표시됌\n"
                f"<{p['week']}>\n"
                f"{num}. {student_question_part}\n"
                f"{teacher_opts_str}\n\n"
                "풀이과정\n"
                f"{t_exp}"
            )
            
        else:
            # Subjective
            s_block = (
                "// 주관식\n"
                f"<{p['week']}>\n"
                f"{num}. {t_desc}"
            )
            
            t_block = (
                "// 주관식\n"
                "// 교사용에는 정답이 표시됌\n"
                f"<{p['week']}>\n"
                f"{num}. {t_desc}\n"
                f"정답: {correct_answer}\n\n"
                "풀이과정\n"
                f"{t_exp}"
            )
            
        student_out.append(s_block)
        teacher_out.append(t_block)
        
    return "\n\n---\n\n".join(student_out), "\n\n---\n\n".join(teacher_out)

for filename in files:
    input_path = os.path.join(input_dir, filename)
    if not os.path.exists(input_path): continue
        
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    student_text, teacher_text = generate_formats(content, filename)
    
    with open(os.path.join(output_dir, filename.replace('.txt', '_학생용_포맷.txt')), 'w', encoding='utf-8') as f:
        f.write(student_text)
        
    with open(os.path.join(output_dir, filename.replace('.txt', '_교사용_포맷.txt')), 'w', encoding='utf-8') as f:
        f.write(teacher_text)
        
print("새로운 txt 포맷 변환 완료!")
