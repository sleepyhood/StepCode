import sys
import os

try:
    import fitz
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF"])
    import fitz

pdf_path = r"c:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\1차시. 캔바 첫 세팅과 작업 영역 적응.pdf"
output_md_path = r"c:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\1차시. 캔바 첫 세팅과 작업 영역 적응.md"

print(f"Processing PDF: {pdf_path}")
doc = fitz.open(pdf_path)
md_content = "# 1차시. 캔바 첫 세팅과 작업 영역 적응\n\n"

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
