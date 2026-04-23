import os
import re
import urllib.parse
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
from datetime import datetime

class ImageSanitizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Baekjoon Image Sanitizer - StepCode")
        self.root.geometry("800x600")

        # Variables
        self.target_path = tk.StringVar(value=os.path.join(os.getcwd(), "practice", "data", "content", "programming", "baekjoon", "scraped"))
        if not os.path.exists(self.target_path.get()):
            self.target_path.set(os.getcwd())

        self._build_ui()

    def _build_ui(self):
        # Header
        header_frame = tk.Frame(self.root, pady=10)
        header_frame.pack(fill="x", padx=20)
        tk.Label(header_frame, text="백준 이미지 파일명 정규화 도구", font=("Malgun Gothic", 16, "bold")).pack(side="left")

        # Path Selection
        path_frame = tk.LabelFrame(self.root, text="작업 대상 설정", padx=10, pady=10)
        path_frame.pack(fill="x", padx=20, pady=10)

        tk.Entry(path_frame, textvariable=self.target_path, width=70).pack(side="left", padx=(0, 10))
        tk.Button(path_frame, text="폴더 선택", command=self._select_folder).pack(side="left")
        tk.Button(path_frame, text="파일 선택", command=self._select_file).pack(side="left", padx=5)

        # Control Buttons
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack(fill="x", padx=20)

        self.start_btn = tk.Button(btn_frame, text="작업 시작", command=self._start_task, bg="#4CAF50", fg="white", font=("bold"), padx=20)
        self.start_btn.pack(side="left")

        self.test_btn = tk.Button(btn_frame, text="로직 자체 검증 실행", command=self._run_self_test, bg="#2196F3", fg="white", padx=10)
        self.test_btn.pack(side="right")

        # Progress
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", padx=20, pady=5)

        # Log Area
        self.log_area = scrolledtext.ScrolledText(self.root, height=20, font=("Consolas", 9))
        self.log_area.pack(fill="both", expand=True, padx=20, pady=10)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_area.see(tk.END)

    def _select_folder(self):
        folder = filedialog.askdirectory(initialdir=self.target_path.get())
        if folder:
            self.target_path.set(folder)

    def _select_file(self):
        file = filedialog.askopenfilename(initialdir=self.target_path.get(), filetypes=[("Markdown files", "*.md")])
        if file:
            self.target_path.set(file)

    def _run_self_test(self):
        self.log("--- 로직 자체 검증 시작 ---")
        test_cases = [
            ("10219_%EA%B4%B4%EA%B8%B0.png", "10219_괴기.png"),
            ("1074_Screen%20Shot%202020.png", "1074_Screen_Shot_2020.png"),
            ("simple_image.png", "simple_image.png"),
            ("Korean 한글.png", "Korean_한글.png")
        ]
        
        success_count = 0
        for raw, expected in test_cases:
            result = self.sanitize_filename(raw)
            if result == expected:
                self.log(f"✅ PASS: {raw} -> {result}")
                success_count += 1
            else:
                self.log(f"❌ FAIL: {raw} (Got: {result}, Expected: {expected})")
        
        self.log(f"--- 검증 완료 ({success_count}/{len(test_cases)}) ---")
        if success_count == len(test_cases):
            messagebox.showinfo("검증 완료", "모든 로직 검증을 통과했습니다.")

    def sanitize_filename(self, filename):
        # 1. URL 디코딩
        decoded = urllib.parse.unquote(filename)
        # 2. 공백을 언더바로 치환
        cleaned = decoded.replace(' ', '_')
        # 3. 연속된 언더바 제거 (옵션)
        cleaned = re.sub(r'_+', '_', cleaned)
        return cleaned

    def _start_task(self):
        path = self.target_path.get()
        if not os.path.exists(path):
            messagebox.showerror("오류", "유효하지 않은 경로입니다.")
            return

        self.start_btn.config(state=tk.DISABLED)
        threading.Thread(target=self._run_engine, args=(path,), daemon=True).start()

    def _run_engine(self, path):
        try:
            if os.path.isfile(path):
                self._process_single_md(path)
            else:
                self._process_folder(path)
            
            self.log("🏁 모든 작업이 완료되었습니다.")
            messagebox.showinfo("완료", "이미지 정규화 작업이 완료되었습니다.")
        except Exception as e:
            self.log(f"🛑 치명적 에러 발생: {e}")
            messagebox.showerror("에러", str(e))
        finally:
            self.start_btn.config(state=tk.NORMAL)
            self.progress_var.set(0)

    def _process_folder(self, folder_path):
        md_files = [f for f in os.listdir(folder_path) if f.endswith(".md")]
        total = len(md_files)
        self.log(f"📂 폴더 탐색 시작: {folder_path} (총 {total}개 파일)")
        
        for i, filename in enumerate(md_files):
            md_path = os.path.join(folder_path, filename)
            self._process_single_md(md_path, verbose=False)
            self.progress_var.set(((i + 1) / total) * 100)
            self.root.update_idletasks()

    def _process_single_md(self, md_path, verbose=True):
        md_dir = os.path.dirname(md_path)
        img_dir = os.path.join(md_dir, "images")
        
        if not os.path.exists(md_path):
            return

        with open(md_path, "r", encoding="utf-8-sig") as f:
            content = f.read()

        # Regex for ![] (./images/...)
        # Matches: ![](./images/filename.ext)
        pattern = r'(!\[.*?\]\(\.\/images\/)(.*?)(\))'
        matches = re.findall(pattern, content)
        
        if not matches:
            if verbose: self.log(f"⏩ {os.path.basename(md_path)}: 이미지 링크 없음")
            return

        modified = False
        new_content = content
        
        # 파일 내에서 중복 매칭 제거를 위해 set 사용
        unique_matches = set(matches)
        
        processed_images_in_this_file = 0

        for prefix, raw_filename, suffix in unique_matches:
            # 정규화된 이름 생성
            clean_name = self.sanitize_filename(raw_filename)
            
            # 변경이 필요한 경우만 진행
            if raw_filename != clean_name:
                # 1. 실제 파일 이름 변경
                old_img_path = os.path.join(img_dir, raw_filename)
                new_img_path = os.path.join(img_dir, clean_name)
                
                if os.path.exists(old_img_path):
                    try:
                        # 만약 대상 이름이 이미 존재하면? (내용이 같으면 그냥 삭제, 다르면 덮어쓰기 등 선택 필요)
                        if os.path.exists(new_img_path) and old_img_path != new_img_path:
                            self.log(f"⚠️ 충돌: {clean_name} 가 이미 존재함. 기존 파일 유지.")
                            # 이미 존재하므로 이름 변경은 안 하지만, MD 링크는 업데이트 해야 함 (동일 파일 참조로 간주)
                        else:
                            os.rename(old_img_path, new_img_path)
                            self.log(f"✅ 파일명 변경: {raw_filename} -> {clean_name}")
                    except Exception as e:
                        self.log(f"❌ 파일 변경 실패 ({raw_filename}): {e}")
                
                # 2. 마크다운 내용 업데이트 (모든 동일한 링크 교체)
                old_link = f"{prefix}{raw_filename}{suffix}"
                new_link = f"{prefix}{clean_name}{suffix}"
                new_content = new_content.replace(old_link, new_link)
                modified = True
                processed_images_in_this_file += 1

        if modified:
            with open(md_path, "w", encoding="utf-8-sig") as f:
                f.write(new_content)
            self.log(f"📝 {os.path.basename(md_path)}: 링크 업데이트 완료 ({processed_images_in_this_file}개 이미지)")
        else:
            if verbose: self.log(f"⏩ {os.path.basename(md_path)}: 변경 사항 없음")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSanitizerGUI(root)
    root.mainloop()
