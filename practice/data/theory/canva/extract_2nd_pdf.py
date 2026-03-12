import sys
import os

try:
    import fitz
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF"])
    import fitz

pdf_path = r"c:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\2차시. 디자인 기초 다지기 - 텍스트와 요소.pdf"
output_md_path = r"c:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\00_텍스트추출(단순 원본)_2차시. 디자인 기초 다지기 - 텍스트와 요소.md"

print(f"Processing PDF: {pdf_path}")
doc = fitz.open(pdf_path)
md_content = "# 2차시. 디자인 기초 다지기 - 텍스트와 요소\n\n"

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text("text")
    
    md_content += f"\n\n<!-- Page {page_num + 1} -->\n\n"
    if text.strip():
        md_content += text + "\n"
    
    image_list = page.get_images(full=True)
    if image_list:
        md_content += "\n"
        for _ in range(len(image_list)):
            md_content += "[이미지 삽입]\n"

with open(output_md_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

doc.close()
print(f"Extraction successful! Saved to: {output_md_path}")
