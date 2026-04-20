import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import re
from datetime import datetime

class MetadataPatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StepCode MD Metadata Patcher (v1.0)")
        self.root.geometry("700x550")
        
        self.total_count = 0
        self.success_count = 0
        self.skip_count = 0
        self.error_count = 0

        self._build_ui()

    def _build_ui(self):
        # 상단 타이틀
        header = tk.Frame(self.root, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="마크다운 메타데이터 패치 도구", font=("Helvetica", 14, "bold")).pack()
        tk.Label(header, text="is_scraped: true 항목 아래에 is_existent: true를 삽입합니다.", fg="gray").pack()

        # 버튼 영역
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack(fill="x", padx=20)

        self.btn_file = tk.Button(btn_frame, text="📄 단일 파일 선택", command=self.select_file, width=25, height=2, bg="#e3f2fd")
        self.btn_file.pack(side=tk.LEFT, padx=10, expand=True)

        self.btn_dir = tk.Button(btn_frame, text="📂 폴더 일괄 처리", command=self.select_dir, width=25, height=2, bg="#fff3e0")
        self.btn_dir.pack(side=tk.LEFT, padx=10, expand=True)

        # 로그 영역
        log_label_frame = tk.LabelFrame(self.root, text="작업 로그", padx=10, pady=10)
        log_label_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.log_area = scrolledtext.ScrolledText(log_label_frame, height=15, state="disabled", bg="#f5f5f5")
        self.log_area.pack(fill="both", expand=True)

        # 하단 요약 바
        self.status_var = tk.StringVar(value="준비됨")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, padx=10)
        self.status_bar.pack(side=tk.BOTTOM, fill="x")

    def log(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])
        if file_path:
            self.reset_stats()
            self.process_file(file_path)
            self.update_status("단일 파일 작업 완료")

    def select_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.reset_stats()
            md_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.lower().endswith(".md")]
            
            if not md_files:
                messagebox.showinfo("알림", "선택한 폴더에 마크다운 파일이 없습니다.")
                return

            self.log(f"🚀 폴더 인계 시작: {len(md_files)}개의 파일을 찾았습니다.")
            for f in md_files:
                self.process_file(f)
            
            self.log(f"✅ 일괄 작업 종료 (성공: {self.success_count}, 건너뜀: {self.skip_count}, 에러: {self.error_count})")
            self.update_status("폴더 일괄 작업 완료")
            messagebox.showinfo("완료", f"작업이 완료되었습니다.\n성공: {self.success_count}\n건너뜀: {self.skip_count}\n에러: {self.error_count}")

    def reset_stats(self):
        self.success_count = 0
        self.skip_count = 0
        self.error_count = 0
        self.log_area.config(state="normal")
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state="disabled")

    def update_status(self, text):
        self.status_var.set(f"{text} | 성공: {self.success_count} / 건너뜀: {self.skip_count} / 에러: {self.error_count}")

    def process_file(self, file_path):
        filename = os.path.basename(file_path)
        try:
            # 보수적으로 utf-8-sig (BOM 대응) 사용
            with open(file_path, "r", encoding="utf-8-sig") as f:
                content = f.read()

            # 1. is_scraped: true 존재 여부 확인
            scraped_match = re.search(r"^is_scraped:\s*true\s*$", content, re.MULTILINE)
            
            if not scraped_match:
                # 사용자가 직접 파일을 보게끔 유도
                self.log(f"⚠️ {filename}: 'is_scraped: true' 필드가 없습니다. 수동 확인이 필요합니다.")
                res = messagebox.askyesno("필드 누락 확인", f"[{filename}]\n'is_scraped: true' 필드를 찾을 수 없습니다.\n직접 파일을 확인하시겠습니까?")
                if res:
                    os.startfile(file_path) # 윈도우에서 파일 열기
                self.error_count += 1
                return

            # 2. 이미 is_existent: true가 있는지 확인
            if re.search(r"^is_existent:\s*true\s*$", content, re.MULTILINE):
                self.log(f"⏩ {filename}: 이미 필드가 존재하여 건너뜁니다.")
                self.skip_count += 1
                return

            # 3. 삽입 (is_scraped: true 바로 아래에 추가)
            start, end = scraped_match.span()
            new_content = content[:end] + "\nis_existent: true" + content[end:]
            
            with open(file_path, "w", encoding="utf-8-sig") as f:
                f.write(new_content)
            
            self.log(f"✨ {filename}: 패치 완료 (is_existent: true 추가됨)")
            self.success_count += 1

        except Exception as e:
            self.log(f"❌ {filename}: 에러 발생 - {e}")
            self.error_count += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = MetadataPatcherApp(root)
    root.mainloop()
