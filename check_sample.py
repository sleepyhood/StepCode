import os
from docx import Document

def analyze_sample(file_path):
    try:
        doc = Document(file_path)
        with open("sample_output.txt", "w", encoding="utf-8") as f:
            for i, para in enumerate(doc.paragraphs):
                text = para.text.strip()
                if text:
                    f.write(f"P{i}: {text}\n")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    analyze_sample(r"practice\data\theory\jungol\문제 샘플.docx")
