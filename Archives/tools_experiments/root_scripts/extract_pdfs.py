import os
import PyPDF2

directory = r"c:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\jungol"

with open(r"c:\Users\osw\Desktop\Workspace\#Projects\StepCode\extract_pdfs.txt", "w", encoding="utf-8") as f:
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            f.write(f"--- {file} ---\n")
            try:
                reader = PyPDF2.PdfReader(os.path.join(directory, file))
                text = ""
                for i in range(min(15, len(reader.pages))): # Get more pages to find all 12 questions
                    page = reader.pages[i]
                    text += page.extract_text() + "\n"
                # Remove extra newlines or spaces to make output concise
                text = "\n".join([line for line in text.split("\n") if line.strip()])
                f.write(text[:3000] + "\n\n")
            except Exception as e:
                f.write(f"Error reading {file}: {e}\n\n")
