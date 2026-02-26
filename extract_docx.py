import zipfile
import xml.etree.ElementTree as ET
import sys
import os

def read_docx(file_path):
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    text_content = []
    
    with zipfile.ZipFile(file_path) as docx:
        tree = ET.fromstring(docx.read('word/document.xml'))
        for paragraph in tree.findall('.//w:p', ns):
            para_text = []
            for run in paragraph.findall('.//w:r', ns):
                for t in run.findall('.//w:t', ns):
                    if t.text:
                        para_text.append(t.text)
            if para_text:
                text_content.append(''.join(para_text))
            else:
                text_content.append('')
                
    return '\n'.join(text_content)

base_dir = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\jungol\중등"
out_path = os.path.join(r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode", "extracted_all_docx.txt")

docx_files = [
    "[수업] 2025년 2차_중등_교사용_2019-2022_최종.docx",
    "[수업] 2025년 3차_중등_교사용_2019-2022.docx",
    "[수업] 2025년 4차_중등_교사용_2019-2022.docx",
    "[수업] 2025년 5차_중등_교사용_2019-2022.docx"
]

with open(out_path, "w", encoding="utf-8") as f:
    for filename in docx_files:
        file_path = os.path.join(base_dir, filename)
        try:
            extracted = read_docx(file_path)
            f.write(f"\n=======================================================\n")
            f.write(f"=== {filename} ===\n")
            f.write(f"=======================================================\n\n")
            f.write(extracted)
            f.write("\n")
            print(f"Extraction successful: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
print(f"All done! Output saved to: {out_path}")
