import base64
import re
import os

md_path = r"c:\Users\DCT2\Desktop\DCT2_공유폴더\StepCode\practice\data\content\programming\doingcoding\STRLv01_Stack1\02_workspace\STRLv01005_1148.md"
img_dir = r"c:\Users\DCT2\Desktop\DCT2_공유폴더\StepCode\practice\data\content\programming\doingcoding\STRLv01_Stack1\02_workspace\images"
svg_path = os.path.join(img_dir, "STRLv01005.svg")

with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

# base64 패턴 찾기
pattern = r"data:image/svg\+xml;base64,([A-Za-z0-9+/=\s\r\n]+)"
match = re.search(pattern, content)

if match:
    base64_data = match.group(1).replace("\r", "").replace("\n", "").replace(" ", "")
    svg_data = base64.b64decode(base64_data).decode("utf-8")
    
    # 이미지 디렉토리 생성
    os.makedirs(img_dir, exist_ok=True)
    
    # SVG 파일 저장
    with open(svg_path, "w", encoding="utf-8") as f_svg:
        f_svg.write(svg_data)
    print(f"SVG saved to {svg_path}")
    
    # Markdown 파일 치환 (base64 부분을 상대 경로로 변경)
    new_content = re.sub(pattern, "./images/STRLv01005.svg", content)
    
    # 변경된 markdown 파일 저장
    with open(md_path, "w", encoding="utf-8") as f_md:
        f_md.write(new_content)
    print("Markdown file updated.")
else:
    print("Base64 pattern not found.")
