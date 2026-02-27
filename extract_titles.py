import re

with open(r"c:\Users\osw\Desktop\Workspace\#Projects\StepCode\extract_pdfs.txt", "r", encoding="utf-8") as f:
    with open(r"c:\Users\osw\Desktop\Workspace\#Projects\StepCode\extract_titles_output.txt", "w", encoding="utf-8") as fout:
        for line in f:
            line = line.strip()
            if line.startswith("--- ") and line.endswith(" ---"):
                fout.write(f"\n{line}\n")
                continue
            
            if re.match(r"^\d+\..*?\(?.*점\)?$", line):
                fout.write(f"  {line}\n")
