import pypandoc
import os

try:
    pandoc_path = pypandoc.get_pandoc_path()
    os.environ.setdefault("PYPANDOC_PANDOC", pandoc_path)
except OSError:
    pypandoc.download_pandoc()
    pandoc_path = pypandoc.get_pandoc_path()
    os.environ.setdefault("PYPANDOC_PANDOC", pandoc_path)

input_file = r"practice\data\theory\jungol\중등\2026년_1차_중등_수업_교사용_2019-2025.docx"
output_file = "test_pandoc.md"

pypandoc.convert_file(input_file, 'md', outputfile=output_file)
print("Conversion successful.")
