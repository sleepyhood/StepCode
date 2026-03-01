import pypandoc
import os

try:
    pandoc_path = pypandoc.get_pandoc_path()
    os.environ.setdefault("PYPANDOC_PANDOC", pandoc_path)
except OSError:
    pass

input_file = r"practice\data\theory\jungol\중등\2026년_1차_중등_수업_학생용_2019-2025.docx"
output_file = "test_pandoc_student.md"

pypandoc.convert_file(input_file, 'md', outputfile=output_file)
print("Conversion successful.")
