import os
import re
import sys
import shutil

def organize_images(md_file_path, week_num):
    # 폴더 구조 세팅
    base_dir = os.path.dirname(os.path.abspath(md_file_path))
    target_img_dir = os.path.join(base_dir, "images", f"week{week_num:02d}")
    os.makedirs(target_img_dir, exist_ok=True)
    
    # 마크다운 내용 읽기
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 마크다운 이미지 링크 찾기 정규식: ![alt_text](image_path)
    pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    matches = pattern.findall(content)
    
    replacements = []
    
    for alt_text, img_path in matches:
        # 이미 week 규칙에 맞게 정리된 경로나 외부 링크는 건너뜀
        processed_path_marker = f"images/week{week_num:02d}"
        if img_path.startswith("http") or processed_path_marker in img_path.replace("\\", "/"):
            continue
            
        full_img_path = os.path.join(base_dir, img_path)
        
        # 실제 파일이 존재하는 경우만 매핑 처리
        if os.path.exists(full_img_path):
            print(f"\n['{img_path}' 발견!]")
            # 이미지 뷰어로 띄우기 (작업자가 보고 이름을 정할 수 있도록)
            try:
                os.startfile(full_img_path)
            except Exception:
                pass # 시작 불가능해도 무시
                
            new_name = input("이 이미지에 부여할 이름을 입력하세요 (예: p017_01 / 스킵하려면 바로 엔터): ").strip()
            
            if new_name:
                # 확장자 유지
                ext = os.path.splitext(img_path)[1]
                if not ext:
                    ext = ".png" # 기본값
                    
                if not (new_name.endswith('.png') or new_name.endswith('.jpg') or new_name.endswith('.svg')):
                    new_name += ext
                
                new_img_rel_path = f"images/week{week_num:02d}/{new_name}"
                new_img_full_path = os.path.join(base_dir, new_img_rel_path)
                
                # 파일 이동 (혹시 이미 타겟 위치에 파일이 있다면 덮어쓰기)
                if os.path.exists(new_img_full_path):
                    os.remove(new_img_full_path)
                shutil.move(full_img_path, new_img_full_path)
                print(f" -> 성공: {new_img_rel_path} 위치로 정리 완료")
                
                # 마크다운 교환 목록 기록
                old_md_str = f"![{alt_text}]({img_path})"
                new_md_str = f"![{alt_text if alt_text else '설명'}]({new_img_rel_path})"
                replacements.append((old_md_str, new_md_str))
                
    # 마크다운에 수정사항 반영
    if replacements:
        for old_str, new_str in replacements:
            content = content.replace(old_str, new_str)
            
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n=> 총 {len(replacements)}개의 이미지가 성공적으로 분류되고, 마크다운 링크가 수정되었습니다!")
    else:
        print("\n=> 현재 새로 정리할 이미지가 없습니다.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법이 잘못되었습니다.")
        print("예시: python organize_pasted_images.py \"01_1차검수(LLM 서식 정리)_1차시. md\" 1")
    else:
        md_file = sys.argv[1]
        try:
            week = int(sys.argv[2])
            organize_images(md_file, week)
        except ValueError:
            print("주차(week)는 숫자로 입력해주세요.")
