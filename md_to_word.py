import tkinter as tk
from tkinter import messagebox
import pypandoc
import os
import platform
import tempfile


# --- 이 부분을 추가하세요! ---
try:
    pypandoc.get_pandoc_version()
except OSError:
    print("Pandoc 엔진을 다운로드 중입니다. 잠시만 기다려주세요...")
    pypandoc.download_pandoc()
# -----------------------------

def convert_to_word():
    # 1. 텍스트 박스에서 마크다운 텍스트 가져오기
    md_text = text_area.get("1.0", tk.END).strip()
    
    if not md_text:
        messagebox.showwarning("경고", "변환할 마크다운 텍스트를 입력해주세요.")
        return
    
    try:
        # 2. 시스템의 임시 폴더에 docx 파일 저장 경로 설정
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, "converted_markdown.docx")
        
        # 3. pypandoc을 사용해 마크다운을 docx로 변환
        pypandoc.convert_text(md_text, 'docx', format='md', outputfile=output_path)
        
        # 4. 변환된 워드 파일 자동으로 열기
        if platform.system() == 'Darwin':       # macOS
            os.system(f'open "{output_path}"')
        elif platform.system() == 'Windows':    # Windows
            os.startfile(output_path)
        else:                                   # Linux
            os.system(f'xdg-open "{output_path}"')
            
    except Exception as e:
        messagebox.showerror("변환 오류", f"오류가 발생했습니다. Pandoc이 설치되어 있는지 확인하세요.\n\n상세 오류: {e}")

# --- GUI 구성 ---
root = tk.Tk()
root.title("Markdown to Word 변환기")
root.geometry("600x500")

# 안내 레이블
instruction_label = tk.Label(root, text="마크다운 텍스트를 아래에 붙여넣고 변환 버튼을 누르세요.\n(수식은 $$ ... $$ 또는 $ ... $ 형태를 지원합니다)", pady=10)
instruction_label.pack()

# 텍스트 입력 창
text_area = tk.Text(root, wrap=tk.WORD, width=70, height=20, font=("Consolas", 11))
text_area.pack(padx=20, pady=5)

# 변환 버튼
convert_btn = tk.Button(root, text="Word로 변환 후 열기", command=convert_to_word, font=("Arial", 12, "bold"), bg="#4CAF50", fg="black", pady=10)
convert_btn.pack(pady=15)

# 창 실행
root.mainloop()