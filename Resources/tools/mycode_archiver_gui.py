import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import os
import time
from playwright.sync_api import sync_playwright

def normalize_cookies(raw_cookies):
    valid_keys = {'name', 'value', 'url', 'domain', 'path', 'expires', 'httpOnly', 'secure', 'sameSite'}
    normalized = []
    for c in raw_cookies:
        nc = {}
        for k, v in c.items():
            if k == 'expirationDate':
                nc['expires'] = float(v)
            elif k in valid_keys:
                nc[k] = v
        if 'sameSite' in nc:
            if nc['sameSite'] == 'no_restriction':
                nc['sameSite'] = 'None'
            elif nc['sameSite'] not in ['Strict', 'Lax', 'None']:
                del nc['sameSite']
        normalized.append(nc)
    return normalized

from mycode_archiver_engine import get_best_solutions, extract_code_and_language, merge_code_to_md, copy_md_and_resources

class MyCodeArchiverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("백준 내 코드 아카이버 (My Code Archiver)")
        self.root.geometry("700x550")
        
        self.auth_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auth.json")
        self.manual_cookies_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manual_cookies.json")
        self.user_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_data")
        self.headless_var = tk.BooleanVar(value=True) # 기본값: 창 숨김(True)
        self.browser_context = None
        self.playwright_instance = None
        
        self._build_ui()
        
    def _build_ui(self):
        # 1. 설정 영역
        settings_frame = tk.LabelFrame(self.root, text="설정", padx=10, pady=10)
        settings_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(settings_frame, text="백준 ID:").grid(row=0, column=0, sticky="w", pady=5)
        self.user_id_var = tk.StringVar()
        tk.Entry(settings_frame, textvariable=self.user_id_var, width=20).grid(row=0, column=1, sticky="w", pady=5)

        # Headless 옵션 체크박스 추가
        tk.Checkbutton(settings_frame, text="브라우저 숨기기 (Headless)", variable=self.headless_var).grid(row=0, column=2, sticky="w", padx=10)
        
        tk.Label(settings_frame, text="원본 마크다운 폴더:").grid(row=1, column=0, sticky="w", pady=5)
        self.src_md_dir_var = tk.StringVar(value=os.getcwd())
        tk.Entry(settings_frame, textvariable=self.src_md_dir_var, width=50, state="readonly").grid(row=1, column=1, sticky="w", pady=5)
        tk.Button(settings_frame, text="폴더 선택", command=self.select_src_md_dir).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(settings_frame, text="저장(Output) 폴더:").grid(row=2, column=0, sticky="w", pady=5)
        self.dest_md_dir_var = tk.StringVar()
        tk.Entry(settings_frame, textvariable=self.dest_md_dir_var, width=50, state="readonly").grid(row=2, column=1, sticky="w", pady=5)
        tk.Button(settings_frame, text="폴더 선택", command=self.select_dest_md_dir).grid(row=2, column=2, padx=5, pady=5)
        
        # 2. 액션 버튼
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        self.btn_login = tk.Button(btn_frame, text="[1. 로그인 세션 만들기]", bg="#ffeb3b", command=self.start_login_session)
        self.btn_login.pack(side="left", padx=5)
        
        self.btn_login_done = tk.Button(btn_frame, text="[로그인 완료 (세션 저장)]", bg="#8bc34a", command=self.finish_login_session, state="disabled")
        self.btn_login_done.pack(side="left", padx=5)
        
        self.btn_manual_cookie = tk.Button(btn_frame, text="[1-2. 수동 쿠키 JSON 등록]", bg="#ff9800", command=self.load_manual_cookies)
        self.btn_manual_cookie.pack(side="left", padx=5)
        
        self.btn_start = tk.Button(btn_frame, text="[2. 코드 수집 및 병합 시작]", bg="#2196f3", fg="white", command=self.start_archiving)
        self.btn_start.pack(side="right", padx=5)
        
        # 3. 진행 상태
        self.progress_var = tk.StringVar(value="대기 중...")
        tk.Label(self.root, textvariable=self.progress_var, font=("Helvetica", 10, "bold")).pack(anchor="w", padx=10, pady=5)
        
        # 4. 로그
        self.log_area = scrolledtext.ScrolledText(self.root, width=80, height=18, state="disabled", bg="#f0f0f0")
        self.log_area.pack(fill="both", expand=True, padx=10, pady=10)
        
    def select_src_md_dir(self):
        dir_path = filedialog.askdirectory(initialdir=self.src_md_dir_var.get())
        if dir_path:
            self.src_md_dir_var.set(dir_path)

    def select_dest_md_dir(self):
        dir_path = filedialog.askdirectory(initialdir=self.dest_md_dir_var.get())
        if dir_path:
            self.dest_md_dir_var.set(dir_path)
            
    def load_manual_cookies(self):
        file_path = filedialog.askopenfilename(title="쿠키 JSON 파일 선택", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                import json
                with open(file_path, "r", encoding="utf-8") as f:
                    cookies = json.load(f)
                with open(self.manual_cookies_path, "w", encoding="utf-8") as f:
                    json.dump(cookies, f)
                self.log(f"✅ 수동 쿠키 JSON이 등록되었습니다. 이제 코드 수집을 시작할 수 있습니다.")
                # 마커 파일 생성 (start_archiving 검사용)
                with open(self.auth_json_path, "w") as f:
                    f.write('{"manual_login": true}')
                messagebox.showinfo("성공", "수동 쿠키가 성공적으로 등록되었습니다.")
            except Exception as e:
                self.log(f"⚠️ 쿠키 파일 로드 실패: {e}")
                messagebox.showerror("오류", f"쿠키 JSON 파일을 읽는 데 실패했습니다.\n{e}")
            
    def log(self, msg):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")
        
    def start_login_session(self):
        self.btn_login.config(state="disabled")
        self.btn_login_done.config(state="normal")
        self.log("로그인 브라우저를 시작합니다...")
        
        def run_browser():
            try:
                self.playwright_instance = sync_playwright().start()
                self.browser_context = self.playwright_instance.chromium.launch_persistent_context(
                    user_data_dir=self.user_data_dir,
                    headless=False,
                    channel="msedge",
                    args=["--disable-blink-features=AutomationControlled"]
                )
                page = self.browser_context.pages[0] if self.browser_context.pages else self.browser_context.new_page()
                page.goto("https://www.acmicpc.net/login", wait_until="domcontentloaded", timeout=60000)
                self.log("💡 브라우저에서 로그인을 완료한 후 GUI의 [로그인 완료 (세션 저장)] 버튼을 눌러주세요.")
            except Exception as e:
                self.log(f"⚠️ 브라우저 실행 실패: {e}")
                self.btn_login.config(state="normal")
                self.btn_login_done.config(state="disabled")
            
        threading.Thread(target=run_browser, daemon=True).start()
        
    def finish_login_session(self):
        if self.browser_context:
            try:
                # Persistent context automatically saves state
                with open(self.auth_json_path, "w") as f:
                    f.write('{"login_done": true}')
                self.log(f"✅ 세션이 저장되었습니다.")
            except Exception as e:
                self.log(f"⚠️ 세션 저장 실패: {e}")
            finally:
                try:
                    self.browser_context.close()
                    self.playwright_instance.stop()
                except:
                    pass
                self.browser_context = None
                self.playwright_instance = None
            
        self.btn_login_done.config(state="disabled")
        self.btn_login.config(state="normal")
        messagebox.showinfo("성공", "로그인 세션이 저장되었습니다.\n이제 코드 수집을 시작할 수 있습니다.")
        
    def start_archiving(self):
        user_id = self.user_id_var.get().strip()
        src_md_dir = self.src_md_dir_var.get()
        dest_md_dir = self.dest_md_dir_var.get()
        
        if not user_id:
            messagebox.showwarning("경고", "백준 ID를 입력해주세요.")
            return
            
        if not src_md_dir or not dest_md_dir:
            messagebox.showwarning("경고", "원본 폴더와 저장 폴더를 모두 지정해주세요.")
            return

        if not os.path.exists(self.auth_json_path):
            messagebox.showwarning("경고", "로그인 세션 파일(auth.json)이 없습니다.\n[1. 로그인 세션 만들기]를 먼저 진행해주세요.")
            return
            
        self.btn_start.config(state="disabled")
        self.log("=====================================")
        self.log("🚀 코드 수집을 시작합니다...")
        
        threading.Thread(target=self._archiving_task, args=(user_id, src_md_dir, dest_md_dir), daemon=True).start()
        
    def _archiving_task(self, user_id, src_md_dir, dest_md_dir):
        try:
            with sync_playwright() as p:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=self.user_data_dir,
                    headless=self.headless_var.get(), # 체크박스 값 적용
                    channel="msedge",
                    args=["--disable-blink-features=AutomationControlled"]
                )
                
                if os.path.exists(self.manual_cookies_path):
                    try:
                        import json
                        with open(self.manual_cookies_path, "r", encoding="utf-8") as f:
                            raw_cookies = json.load(f)
                        context.add_cookies(normalize_cookies(raw_cookies))
                        self.log("💡 수동 쿠키를 컨텍스트에 성공적으로 주입했습니다.")
                    except Exception as e:
                        self.log(f"⚠️ 수동 쿠키 주입 실패: {e}")
                
                self.progress_var.set("Step 1: 정답 목록 스캔 중...")
                best_solutions = get_best_solutions(context, user_id, logger=self.log)
                
                if not best_solutions:
                    self.log("⚠️ 수집할 정답 코드가 없거나, 백준 ID가 올바르지 않습니다.")
                    self.progress_var.set("대기 중...")
                    return
                
                total = len(best_solutions)
                self.log(f"💡 총 {total}개의 최적 정답 코드를 찾았습니다.")
                
                skipped_problems = []
                success_count = 0
                
                for idx, (pid, info) in enumerate(best_solutions.items(), 1):
                    self.progress_var.set(f"Step 2: 코드 수집 및 병합 중... [{idx}/{total}] (문제: {pid})")
                    sid = info["sid"]
                    
                    # 1. 대상 마크다운 파일 확인
                    md_filename = f"bj_{pid}.md"
                    src_md_filepath = os.path.join(src_md_dir, md_filename)
                    dest_md_filepath = os.path.join(dest_md_dir, md_filename)
                    
                    if not os.path.exists(src_md_filepath):
                        self.log(f"⏩ 원본 마크다운 파일 없음: {md_filename} (스킵)")
                        skipped_problems.append(f"{pid} (md_not_found)")
                        continue
                        
                    # 2. 코드 추출
                    code, lang_name = extract_code_and_language(context, pid, sid, logger=self.log)
                    
                    if not code:
                        self.log(f"⚠️ 소스 코드 추출 실패: 문제 {pid} (제출번호 {sid})")
                        skipped_problems.append(f"{pid} (code_extract_failed)")
                        continue
                        
                    # 3. 파일 복사 및 병합
                    copy_res = copy_md_and_resources(src_md_filepath, dest_md_filepath, logger=self.log)
                    if copy_res:
                        success = merge_code_to_md(dest_md_filepath, code, lang_name, result_text=info["text"], logger=self.log)
                        if success:
                            self.log(f"✅ [복사 및 병합 완료] 문제 {pid} ({lang_name})")
                            success_count += 1
                        else:
                            self.log(f"⚠️ [병합 실패] 문제 {pid}")
                            skipped_problems.append(f"{pid} (merge_failed)")
                    else:
                        self.log(f"⚠️ [복사 실패] 문제 {pid}")
                        skipped_problems.append(f"{pid} (copy_failed)")
                        
                    # 과도한 트래픽을 방지하기 위한 짧은 대기 (1초)
                    time.sleep(1)
                        
                self.log("=====================================")
                self.log(f"🎉 모든 작업 완료! (성공: {success_count}/{total})")
                
                # skipped problems 기록
                if skipped_problems:
                    skip_file = os.path.join(dest_md_dir, "skipped_problems.txt")
                    with open(skip_file, "w", encoding="utf-8") as f:
                        f.write("\n".join(skipped_problems))
                    self.log(f"💡 건너뛴 문제 목록이 저장되었습니다: {skip_file}")
                    
                self.progress_var.set("작업 완료")
        except Exception as e:
            self.log(f"❌ 작업 중 오류 발생: {e}")
            self.progress_var.set("오류 발생")
        finally:
            self.btn_start.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = MyCodeArchiverGUI(root)
    root.mainloop()
