import os
import sys
import threading
import markdown
import tkinter as tk
from tkinter import filedialog, messagebox
from playwright.sync_api import sync_playwright

def convert_md_to_pdf(md_path, output_pdf=None, status_callback=None):
    if not os.path.exists(md_path):
        if status_callback:
            status_callback(f"오류: 파일을 찾을 수 없습니다 -> {md_path}")
        return

    # 현재 스크립트가 위치한 폴더 (템플릿 및 CSS 로드용)
    basedir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(basedir, "style.css")
    template_path = os.path.join(basedir, "template.html")
    
    if output_pdf is None:
        # 원본 마크다운 파일과 같은 폴더에 pdf라는 확장자로 저장
        output_pdf = os.path.splitext(md_path)[0] + ".pdf"

    if status_callback: status_callback("마크다운 형식 읽는 중...")
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Markdown을 HTML로 변환
    html_content = markdown.markdown(
        md_text,
        extensions=['fenced_code', 'tables', 'sane_lists', 'nl2br', 'mdx_math']
    )

    # 템플릿과 CSS 읽기
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()
    
    # 데이터 주입
    final_html = template.replace("{{css_content}}", css_content)
    final_html = final_html.replace("{{content}}", html_content)
    
    if status_callback: status_callback("PDF로 굽는 중... (화면 렌더링)")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # HTML 삽입
        page.set_content(final_html)
        
        # 웹폰트, KaTeX 수식, PrismJS 코드 하이라이팅이 모두 로드/적용될 때까지 대기
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000) # 혹시 모를 렌더링 지연을 위한 불안정성 대비 1초 대기
        
        page.pdf(
            path=output_pdf,
            format="A4",
            print_background=True,
            margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"}
        )
        browser.close()

    if status_callback: status_callback("✅ 완료! PDF가 생성되었습니다.")
    
    # 윈도우 환경이라면 생성된 PDF를 즉시 열어줍니다.
    if sys.platform == "win32":
        os.startfile(output_pdf)


class PDFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("마크다운 ➔ 예쁜 PDF 변환기")
        self.root.geometry("450x300")
        
        self.selected_file = None
        
        # UI 구성
        self.instruction_label = tk.Label(root, text="마크다운(.md) 파일을 선택하고 변환 버튼을 누르세요.", pady=20, font=("Malgun Gothic", 11))
        self.instruction_label.pack()
        
        self.file_label = tk.Label(root, text="선택된 파일: 없음", fg="#3b82f6", wraplength=400, font=("Malgun Gothic", 9))
        self.file_label.pack(pady=10)
        
        self.select_btn = tk.Button(root, text="파일 찾기", command=self.select_file, font=("Malgun Gothic", 10), width=15)
        self.select_btn.pack(pady=5)
        
        self.convert_btn = tk.Button(root, text="PDF로 변환하고 열기", command=self.start_conversion, font=("Malgun Gothic", 12, "bold"), bg="#3b82f6", fg="black", pady=10, width=25)
        self.convert_btn.pack(pady=15)
        
        self.status_label = tk.Label(root, text="대기 중...", fg="gray")
        self.status_label.pack(side="bottom", pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="마크다운 파일 선택",
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")]
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=f"선택된 파일: {os.path.basename(file_path)}")
            self.status_label.config(text="대기 중...")

    def update_status(self, text):
        self.status_label.config(text=text)
        self.root.update_idletasks()

    def start_conversion(self):
        if not self.selected_file:
            messagebox.showwarning("경고", "먼저 변환할 마크다운 파일을 선택해주세요!")
            return

        # 중복 클릭 방지
        self.convert_btn.config(state="disabled")
        self.select_btn.config(state="disabled")
        
        # GUI 멈춤(렉)을 방지하기 위해 백그라운드 스레드에서 생성 시작
        def run():
            try:
                convert_md_to_pdf(self.selected_file, status_callback=self.update_status)
            except Exception as e:
                self.update_status("오류 발생!")
                messagebox.showerror("변환 오류", f"PDF 변환 중 오류가 발생했습니다.\n\n상세 오류: {e}")
            finally:
                self.convert_btn.config(state="normal")
                self.select_btn.config(state="normal")

        threading.Thread(target=run, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConverterApp(root)
    root.mainloop()
