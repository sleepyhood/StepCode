import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import time
import os
import sys
import queue

# 상위 폴더나 외부 모듈 의존성 등을 위해 경로 추가
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
if MODULE_DIR not in sys.path:
    sys.path.append(MODULE_DIR)

# 기존 선생님이 작성/보유하신 크롤링 모듈 임포트
try:
    from .crawl import scrape_baekjoon, scrape_doingcoding
except ImportError:
    from crawl import scrape_baekjoon, scrape_doingcoding

DOINGCODING_ADMIN_ID_ENV = "DOINGCODING_ADMIN_ID"
DOINGCODING_ADMIN_PASSWORD_ENV = "DOINGCODING_ADMIN_PASSWORD"


def build_output_filepath(save_dir, filename):
    base, ext = os.path.splitext(filename)
    candidate = os.path.join(save_dir, filename)
    suffix = 1
    while os.path.exists(candidate):
        candidate = os.path.join(save_dir, f"{base}_{suffix}{ext}")
        suffix += 1
    return candidate


def resolve_admin_credentials(username, password):
    resolved_username = (username or "").strip() or os.getenv(DOINGCODING_ADMIN_ID_ENV, "").strip()
    resolved_password = (password or "").strip() or os.getenv(DOINGCODING_ADMIN_PASSWORD_ENV, "").strip()
    return resolved_username, resolved_password

class CrawlerApp:
    def __init__(self, root):
        self.root = root
        self.ui_queue = queue.Queue()
        self.root.title("StepCode Reference 수집기 (GUI) - 접두어 패치판")
        self.root.geometry("620x550")
        
        # 1. 타겟 도메인 라디오 버튼
        self.domain_var = tk.StringVar(value="baekjoon")
        tk.Label(root, text="[ 타겟 도메인 ]", font=("Helvetica", 10, "bold")).pack(pady=(15, 5))
        frame_radio = tk.Frame(root)
        frame_radio.pack()
        tk.Radiobutton(frame_radio, text="백준 (acmicpc.net)", variable=self.domain_var, value="baekjoon").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(frame_radio, text="자체사이트 (doingcoding)", variable=self.domain_var, value="doingcoding").pack(side=tk.LEFT, padx=10)
        
        self.domain_var.trace('w', self.update_url_template)

        # 2. URL 템플릿 입력 구간
        tk.Label(root, text="[ URL 템플릿 ( '{id}' 위치에 조합된 ID가 삽입됩니다 ) ]", font=("Helvetica", 10, "bold")).pack(pady=(15, 5))
        self.url_template = tk.Entry(root, width=70)
        self.url_template.insert(0, "https://www.acmicpc.net/problem/{id}")
        self.url_template.pack(pady=5)
        
        # 3. ID 범위 및 조합기 (접두어 + 번호 + 접미어)
        tk.Label(root, text="[ 수집할 문제 ID 범위 설정 ]\n(예: Prefix P101v + 시작 01 ~ 종료 10)", font=("Helvetica", 10, "bold")).pack(pady=(15, 10))
        
        frame_input = tk.Frame(root)
        frame_input.pack()
        
        tk.Label(frame_input, text="접두어(Prefix):\n(예: P101v)").pack(side=tk.LEFT)
        self.prefix_id = tk.Entry(frame_input, width=10)
        self.prefix_id.insert(0, "")
        self.prefix_id.pack(side=tk.LEFT, padx=(5, 15))
        
        tk.Label(frame_input, text="시작 번호:\n(예: 01)").pack(side=tk.LEFT)
        self.start_id = tk.Entry(frame_input, width=8)
        self.start_id.insert(0, "1000")
        self.start_id.pack(side=tk.LEFT, padx=(5, 5))
        
        tk.Label(frame_input, text="~ 종료 번호:\n(예: 10)").pack(side=tk.LEFT)
        self.end_id = tk.Entry(frame_input, width=8)
        self.end_id.insert(0, "1005")
        self.end_id.pack(side=tk.LEFT, padx=(5, 15))
        
        tk.Label(frame_input, text="접미어(Suffix):\n(선택)").pack(side=tk.LEFT)
        self.suffix_id = tk.Entry(frame_input, width=8)
        self.suffix_id.insert(0, "")
        self.suffix_id.pack(side=tk.LEFT, padx=5)

        # 4. 옵션 (코드 템플릿 수집 여부)
        self.get_templates_var = tk.BooleanVar(value=False)
        self.check_template = tk.Checkbutton(root, text="코드 템플릿 포함 (수집 속도가 현저히 느려질 수 있습니다)", variable=self.get_templates_var)
        self.check_template.pack(pady=5)

        self.get_testcases_var = tk.BooleanVar(value=False)
        self.check_testcases = tk.Checkbutton(
            root,
            text="채점용 테스트케이스 포함 (doingcoding 관리자 로그인 필요)",
            variable=self.get_testcases_var,
        )
        self.check_testcases.pack(pady=5)

        self.show_browser_var = tk.BooleanVar(value=False)
        self.check_show_browser = tk.Checkbutton(
            root,
            text="doingcoding 진행 화면 표시",
            variable=self.show_browser_var,
        )
        self.check_show_browser.pack(pady=5)

        admin_frame = tk.Frame(root)
        admin_frame.pack(pady=(0, 10))
        tk.Label(admin_frame, text="관리자 ID").pack(side=tk.LEFT)
        self.admin_username = tk.Entry(admin_frame, width=18)
        self.admin_username.pack(side=tk.LEFT, padx=(5, 10))
        tk.Label(admin_frame, text="관리자 PW").pack(side=tk.LEFT)
        self.admin_password = tk.Entry(admin_frame, width=18, show="*")
        self.admin_password.pack(side=tk.LEFT, padx=(5, 0))

        # 4. 저장 폴더 지정
        frame_dir = tk.Frame(root)
        frame_dir.pack(pady=20)
        self.save_dir = tk.StringVar(value=os.getcwd())
        tk.Label(frame_dir, text="저장 폴더:").pack(side=tk.LEFT)
        tk.Entry(frame_dir, textvariable=self.save_dir, width=50, state='readonly').pack(side=tk.LEFT, padx=5)
        tk.Button(frame_dir, text="폴더 변경", command=self.select_dir).pack(side=tk.LEFT)
        
        # 5. 크롤링 시작 버튼
        self.start_btn = tk.Button(root, text="🚀 지정된 ID 범위 크롤링 시작", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="black", command=self.start_crawl)
        self.start_btn.pack(pady=5)

        # 6. 진행 상황 로그 출력 창
        self.log_area = scrolledtext.ScrolledText(root, width=75, height=10, state='disabled', bg="#f0f0f0")
        self.log_area.pack(pady=5)
        self.root.after(100, self.process_ui_queue)

    def update_url_template(self, *args):
        self.url_template.delete(0, tk.END)
        if self.domain_var.get() == "baekjoon":
            self.url_template.insert(0, "https://www.acmicpc.net/problem/{id}")
            self.prefix_id.delete(0, tk.END)
            self.start_id.delete(0, tk.END)
            self.start_id.insert(0, "1000")
            self.end_id.delete(0, tk.END)
            self.end_id.insert(0, "1005")
        else:
            self.url_template.insert(0, "http://edu.doingcoding.com/problem/{id}")
            self.prefix_id.delete(0, tk.END)
            self.prefix_id.insert(0, "P101v")
            self.start_id.delete(0, tk.END)
            self.start_id.insert(0, "0701")
            self.end_id.delete(0, tk.END)
            self.end_id.insert(0, "0710")

    def select_dir(self):
        directory = filedialog.askdirectory(initialdir=self.save_dir.get())
        if directory:
            self.save_dir.set(directory)

    def _append_log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def _set_start_button(self, state, text):
        self.start_btn.config(state=state, text=text)

    def process_ui_queue(self):
        while True:
            try:
                action, payload = self.ui_queue.get_nowait()
            except queue.Empty:
                break

            if action == "log":
                self._append_log(payload)
            elif action == "button":
                state, text = payload
                self._set_start_button(state, text)

        self.root.after(100, self.process_ui_queue)

    def log(self, message):
        self.ui_queue.put(("log", message))

    def start_crawl(self):
        try:
            start_str = self.start_id.get().strip()
            end_str = self.end_id.get().strip()
            prefix = self.prefix_id.get().strip()
            suffix = self.suffix_id.get().strip()
            
            # 자리수 유지 처리 (예: 01, 02 ..)
            pad_length = len(start_str)
            start_val = int(start_str)
            end_val = int(end_str)
            
            if start_val > end_val:
                messagebox.showerror("오류", "시작 번호가 종료 번호보다 큽니다.")
                return
            
            target_ids = []
            for i in range(start_val, end_val + 1):
                # 0701 등 앞에 0이 붙어있어야 할 경우 zfill 로 맞춰줌
                num_str = str(i).zfill(pad_length) if pad_length > 1 and start_str.startswith('0') else str(i)
                full_id = f"{prefix}{num_str}{suffix}"
                target_ids.append(full_id)
                
        except ValueError:
            messagebox.showerror("입력 오류", "시작 번호와 종료 번호는 반드시 숫자로 입력해 주세요.")
            return

        domain = self.domain_var.get()
        template = self.url_template.get().strip()
        save_path = self.save_dir.get()
        get_templates = self.get_templates_var.get()
        get_testcases = self.get_testcases_var.get()
        show_browser = self.show_browser_var.get()
        admin_username, admin_password = resolve_admin_credentials(
            self.admin_username.get(),
            self.admin_password.get(),
        )

        if "{id}" not in template:
            messagebox.showerror("입력 오류", "URL 템플릿 안에 반드시 '{id}' 라는 문자가 포함되어야 합니다.")
            return

        if get_testcases and domain != "doingcoding":
            messagebox.showerror("입력 오류", "채점용 테스트케이스 수집은 doingcoding에서만 사용할 수 있습니다.")
            return

        if get_testcases and (not admin_username or not admin_password):
            messagebox.showerror(
                "입력 오류",
                "채점용 테스트케이스 수집에는 관리자 ID/PW가 필요합니다. 입력란 또는 환경변수를 확인해 주세요.",
            )
            return

        os.makedirs(save_path, exist_ok=True)

        self._set_start_button(tk.DISABLED, "크롤링 진행 중...")
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')
        self._append_log(f"=== 대량 수집 시작 (조합된 ID 총 {len(target_ids)} 개) ===")
        
        thread = threading.Thread(
            target=self.crawl_process,
            args=(
                target_ids,
                domain,
                template,
                save_path,
                get_templates,
                get_testcases,
                admin_username,
                admin_password,
                show_browser,
            ),
        )
        thread.daemon = True
        thread.start()

    def crawl_process(
        self,
        target_ids,
        domain,
        template,
        save_path,
        get_templates,
        get_testcases,
        admin_username,
        admin_password,
        show_browser,
    ):
        success_count = 0
        failures = []
        
        for current_id in target_ids:
            target_url = template.replace("{id}", current_id)
            self.log(f"\n[접속 시도] {target_url}")
            
            md_output = None
            title = ""
            try:
                if domain == "baekjoon":
                    result = scrape_baekjoon(target_url)
                    prefix = "bj"
                else:
                    result = scrape_doingcoding(
                        target_url,
                        get_templates=get_templates,
                        get_testcases=get_testcases,
                        admin_username=admin_username,
                        admin_password=admin_password,
                        testcase_download_dir=save_path,
                        show_browser=show_browser,
                        logger=self.log,
                    )
                    prefix = "dc"
                
                if result == (None, None):
                    self.log(f"  ❌ 크롤링 실패 (요소를 찾을 수 없거나 삭제된 문제입니다)")
                    failures.append(target_url)
                    time.sleep(1)
                    continue
                
                title, md_output = result
                
                if md_output:
                    filename = f"01_{prefix}_{current_id}.md"
                    filepath = build_output_filepath(save_path, filename)
                    with open(filepath, 'w', encoding='utf-8-sig') as f:
                        f.write(md_output)
                    
                    self.log(f"  ✅ [추출 성공] '{title}'")
                    self.log(f"  📂 저장 완료: {os.path.basename(filepath)}")
                    success_count += 1
                
                time.sleep(1.5)
                
            except Exception as e:
                self.log(f"  ❌ 시스템 에러 발생: {e}")
                failures.append(target_url)

        if failures:
            failure_report = os.path.join(save_path, "crawl_failures.txt")
            with open(failure_report, "w", encoding="utf-8-sig") as failure_file:
                failure_file.write("\n".join(failures) + "\n")
            self.log(f"  ⚠ 실패 목록 저장: {os.path.basename(failure_report)}")

        self.log(f"\n=== 전체 수집을 완료했습니다. (최종 성공: {success_count} 건) ===")
        self.ui_queue.put(("button", (tk.NORMAL, "🚀 지정된 ID 범위 크롤링 시작")))

if __name__ == "__main__":
    root = tk.Tk()
    app = CrawlerApp(root)
    root.mainloop()
