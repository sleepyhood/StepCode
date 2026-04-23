import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
import os
import sys
import queue
from datetime import datetime

# 상위 폴더나 외부 모듈 의존성 등을 위해 경로 추가
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
if MODULE_DIR not in sys.path:
    sys.path.append(MODULE_DIR)

# 엔진 모듈 임포트 (가져오기 실패 시 에러 방지)
try:
    import crawler_baekjoon_engine as engine
except ImportError:
    engine = None

class VerifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StepCode BOJ 데이터 검증기 (GUI)")
        self.root.geometry("800x700")
        
        self.ui_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.is_running = False
        
        # 설정 변수
        self.target_dir = tk.StringVar(value=os.path.join(os.getcwd(), "scraped"))
        self.check_online = tk.BooleanVar(value=False)
        self.sample_size = tk.StringVar(value="전체") # 전체 또는 숫자
        
        self._build_ui()
        self.root.after(100, self.process_ui_queue)

    def _build_ui(self):
        # 1. 상단: 폴더 설정
        self.header_frame = tk.LabelFrame(self.root, text="검증 설정", padx=12, pady=12)
        self.header_frame.pack(fill="x", padx=10, pady=10)
        
        dir_row = tk.Frame(self.header_frame)
        dir_row.pack(fill="x")
        tk.Label(dir_row, text="수집 폴더:").pack(side=tk.LEFT)
        tk.Entry(dir_row, textvariable=self.target_dir, width=60, state="readonly").pack(side=tk.LEFT, padx=5)
        tk.Button(dir_row, text="폴더 변경", command=self.select_dir).pack(side=tk.LEFT)
        
        # 옵션 행
        opt_row = tk.Frame(self.header_frame)
        opt_row.pack(fill="x", pady=(10, 0))
        
        tk.Checkbutton(opt_row, text="온라인 대조 검사 (Playwright 사용)", variable=self.check_online, fg="blue").pack(side=tk.LEFT)
        
        tk.Label(opt_row, text="  |  검사 표본 수:").pack(side=tk.LEFT)
        self.combo_sample = ttk.Combobox(opt_row, textvariable=self.sample_size, values=["전체", "10", "50", "100", "500"], width=7)
        self.combo_sample.pack(side=tk.LEFT, padx=5)
        
        # 2. 중앙: 상태 요약 대시보드
        self.dash_frame = tk.Frame(self.root)
        self.dash_frame.pack(fill="x", padx=10)
        
        self.stats = {
            "total": tk.StringVar(value="0"),
            "pass": tk.StringVar(value="0"),
            "fail": tk.StringVar(value="0"),
            "warn": tk.StringVar(value="0")
        }
        
        for i, (label, var) in enumerate([("전체 대상", "total"), ("통과(PASS)", "pass"), ("실패(FAIL)", "fail"), ("주의(WARN)", "warn")]):
            f = tk.Frame(self.dash_frame, relief="groove", bd=2, padx=10, pady=5)
            f.pack(side=tk.LEFT, expand=True, fill="both", padx=2)
            tk.Label(f, text=label, font=("Helvetica", 9)).pack()
            tk.Label(f, textvariable=self.stats[var], font=("Helvetica", 12, "bold"), fg="#333" if i==0 else ("green" if i==1 else "red")).pack()

        # 3. 중앙: 로그 영역
        self.log_area = scrolledtext.ScrolledText(self.root, width=90, height=20, state="disabled", bg="#f8f9fa", font=("Consolas", 9))
        self.log_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 4. 하단: 제어 버튼
        self.footer_frame = tk.Frame(self.root)
        self.footer_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.start_btn = tk.Button(self.footer_frame, text="🔍 검증 시작", bg="#4CAF50", fg="black", font=("Helvetica", 11, "bold"), width=15, command=self.start_verification)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(self.footer_frame, text="🛑 중단", bg="#f44336", fg="black", font=("Helvetica", 11, "bold"), width=15, command=self.stop_verification, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_btn = tk.Button(self.footer_frame, text="📄 실패 리포트 저장", command=self.export_report, state=tk.DISABLED)
        self.export_btn.pack(side=tk.RIGHT, padx=5)

    def log(self, message):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        self.ui_queue.put(f"{timestamp} {message}\n")

    def process_ui_queue(self):
        try:
            while True:
                msg = self.ui_queue.get_nowait()
                self.log_area.config(state="normal")
                self.log_area.insert(tk.END, msg)
                self.log_area.see(tk.END)
                self.log_area.config(state="disabled")
        except queue.Empty:
            pass
        self.root.after(100, self.process_ui_queue)

    def select_dir(self):
        directory = filedialog.askdirectory(initialdir=self.target_dir.get())
        if directory:
            self.target_dir.set(directory)

    def start_verification(self):
        if not engine:
            messagebox.showerror("오류", "crawler_baekjoon_engine.py를 찾을 수 없습니다.")
            return
        
        self.is_running = True
        self.stop_event.clear()
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.export_btn.config(state=tk.DISABLED)
        
        # 통계 초기화
        for var in self.stats.values():
            var.set("0")
            
        self.log("=== 검증 작업을 시작합니다 ===")
        # 검증 루프는 다음 단계에서 구현
        threading.Thread(target=self._run_loop, daemon=True).start()

    def _run_loop(self):
        target_path = self.target_dir.get()
        if not os.path.isdir(target_path):
            self.log(f"❌ 오류: '{target_path}' 폴더가 존재하지 않습니다.")
            self.ui_queue.put(("FINISH",))
            return

        # 1. 파일 목록 확보
        all_files = [f for f in os.listdir(target_path) if f.endswith(".md")]
        total_count = len(all_files)
        
        # 샘플링 처리
        sample_str = self.sample_size.get()
        if sample_str != "전체":
            try:
                limit = int(sample_str)
                import random
                all_files = random.sample(all_files, min(limit, total_count))
                total_count = len(all_files)
            except ValueError:
                pass

        self.ui_queue.put(("UPDATE_STAT", "total", str(total_count)))
        self.log(f"🔍 총 {total_count}개의 파일을 검증합니다...")

        self.failure_list = []
        counts = {"pass": 0, "fail": 0, "warn": 0}

        # 2. 브라우저 세션 (필요 시)
        from playwright.sync_api import sync_playwright
        import random

        with sync_playwright() as p:
            browser_context = None
            if self.check_online.get():
                self.log("🌐 브라우저 엔진 초기화 중...")
                browser_context = p.chromium.launch(headless=True).new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                )

            # 3. 루프 시작
            for i, filename in enumerate(all_files):
                if self.stop_event.is_set():
                    self.log("🛑 사용자에 의해 중단되었습니다.")
                    break
                
                file_path = os.path.join(target_path, filename)
                problem_id = filename.split("_")[-1].replace(".md", "")
                
                # [기본 검사] 오프라인 정적 분석
                res = self._validate_offline(file_path, filename)
                
                # [온라인 대조]
                if self.check_online.get() and res["status"] != "FAIL":
                    res = self._validate_online(problem_id, res, browser_context)

                # 결과 집계
                status = res["status"]
                counts[status.lower()] += 1
                
                # UI 업데이트 (5개마다 또는 마지막)
                if i % 5 == 0 or i == total_count - 1:
                    self.ui_queue.put(("UPDATE_STAT", "pass", str(counts["pass"])))
                    self.ui_queue.put(("UPDATE_STAT", "fail", str(counts["fail"])))
                    self.ui_queue.put(("UPDATE_STAT", "warn", str(counts["warn"])))

                if status != "PASS":
                    self.failure_list.append({
                        "id": problem_id,
                        "file": filename,
                        "status": status,
                        "reason": res["reason"]
                    })
                    self.log(f"[{status}] {filename}: {res['reason']}")

            self.log("=" * 40)
            self.log(f"🏁 검증 작업 완료!")
            self.log(f"   - 전체 대상: {total_count}")
            self.log(f"   - 통과(PASS): {counts['pass']}")
            self.log(f"   - 실패(FAIL): {counts['fail']}")
            self.log(f"   - 주의(WARN): {counts['warn']}")
            self.log("=" * 40)
            
            if counts['fail'] > 0 or counts['warn'] > 0:
                self.log("💡 '실패 리포트 저장' 버튼을 눌러 상세 내역을 확인할 수 있습니다.")
            
            if browser_context:
                browser_context.browser.close()
            self.ui_queue.put(("FINISH",))

    def _validate_offline(self, file_path, filename):
        """파일을 읽지 않고/읽어서 기본적인 구조적 결함을 찾습니다."""
        try:
            # 1. 파일 크기 체크
            fsize = os.path.getsize(file_path)
            if fsize < 100:
                return {"status": "FAIL", "reason": "파일 크기 너무 작음 (데이터 누락 의심)"}

            with open(file_path, "r", encoding="utf-8-sig") as f:
                content = f.read()

            # 2. 404 더미 체크
            if "존재하지 않는 문제" in content or "is_existent: false" in content:
                return {"status": "PASS", "reason": "404 격리 파일"}

            # 3. 필수 섹션 체크 (description은 필수)
            import re
            # ## 문제 설명 또는 ## 문제설명 등
            if not re.search(r"##\s*(문제\s*설명|문제설명|설명)", content):
                return {"status": "FAIL", "reason": "문제 설명(Description) 섹션 누락"}

            # 4. 입력/출력 섹션 체크 (일반적인 문제 기준)
            # 4. 입력/출력 섹션 체크 (일반적인 문제 기준)
            has_input = bool(re.search(r"##\s*입력", content))
            has_output = bool(re.search(r"##\s*출력", content))
            
            if not has_input or not has_output:
                return {"status": "WARN", "reason": "입력 또는 출력 섹션 누락 (특수 문제일 수 있음)", "content": content}

            # 5. 샘플 코드 블록 체크
            if "```" not in content:
                return {"status": "WARN", "reason": "코드 블록(예제)이 전혀 없음", "content": content}

            return {"status": "PASS", "reason": "정상", "content": content}

        except Exception as e:
            return {"status": "FAIL", "reason": f"파일 읽기 오류: {e}", "content": ""}

    def _validate_online(self, problem_id, prev_res, context):
        """실제 웹페이지에 접속하여 섹션 구성 및 예제 개수를 대조합니다."""
        url = f"https://www.acmicpc.net/problem/{problem_id}"
        try:
            page = context.new_page()
            # 타임아웃 설정 및 접속 (commit 단계까지만 대기하여 속도 향상)
            page.goto(url, wait_until="commit", timeout=40000)
            # 수동으로 조금 더 대기 (섹션 렌더링 확인용)
            page.wait_for_timeout(2000)
            
            # 1. 원본 페이지 상태 확인 (404 등)
            if "페이지를 찾을 수 없습니다" in page.title():
                page.close()
                return prev_res # 이미 오프라인에서 404 체크를 했으므로 패스

            # 2. 섹션 개수 대조
            # 원본에서 주요 섹션 추출
            target_sections = {
                "Description": "#problem_description",
                "Input": "#problem_input",
                "Output": "#problem_output",
                "Hint": "#problem_hint"
            }
            
            missing_in_local = []
            local_content = prev_res.get("content", "")
            
            for name, selector in target_sections.items():
                if page.locator(selector).count() > 0:
                    # 원본에는 있는데 로컬 MD에 해당 키워드가 없는지 확인
                    # (간단한 키워드 매칭 방식)
                    keywords = {
                        "Description": ["문제 설명", "문제설명", "설명"],
                        "Input": ["입력"],
                        "Output": ["출력"],
                        "Hint": ["힌트"]
                    }
                    found = False
                    for kw in keywords[name]:
                        if f"## {kw}" in local_content or f"##{kw}" in local_content:
                            found = True
                            break
                    if not found:
                        missing_in_local.append(name)

            # 3. 예제(Sample) 개수 대조
            remote_samples = page.locator("pre.sampledata[id^='sample-input-']").count()
            import re
            local_samples = len(re.findall(r"##\s*예제\s*입력", local_content))
            # 예제 입력 섹션이 명시적이지 않은 경우 코드 블록 개수로 보조 확인
            if local_samples == 0:
                local_samples = local_content.count("```") // 2

            if remote_samples > local_samples:
                page.close()
                return {"status": "FAIL", "reason": f"예제 개수 불일치 (원본: {remote_samples}, 로컬: {local_samples})"}
            
            if missing_in_local:
                page.close()
                return {"status": "FAIL", "reason": f"필수 섹션 누락 탐지: {', '.join(missing_in_local)}"}

            page.close()
            return prev_res

        except Exception as e:
            if 'page' in locals(): page.close()
            return {"status": "WARN", "reason": f"온라인 대조 실패 (네트워크/타임아웃): {e}"}

    def stop_verification(self):
        if self.is_running:
            self.stop_event.set()
            self.log("🛑 중단 요청됨... 현재 작업 중인 파일까지만 진행합니다.")

    def finish_ui(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.export_btn.config(state=tk.NORMAL if hasattr(self, 'failure_list') and self.failure_list else tk.DISABLED)

    def export_report(self):
        if not hasattr(self, 'failure_list') or not self.failure_list:
            messagebox.showinfo("알림", "내보낼 실패 내역이 없습니다.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"boj_verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"=== BOJ 데이터 검증 리포트 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===\n")
                    f.write(f"대상 폴더: {self.target_dir.get()}\n")
                    f.write(f"총 실패/주의 항목: {len(self.failure_list)}개\n")
                    f.write("-" * 50 + "\n\n")
                    for item in self.failure_list:
                        f.write(f"[{item['status']}] {item['id']} ({item['file']})\n")
                        f.write(f"사유: {item['reason']}\n\n")
                messagebox.showinfo("성공", f"리포트가 저장되었습니다:\n{file_path}")
            except Exception as e:
                messagebox.showerror("오류", f"리포트 저장 중 오류가 발생했습니다: {e}")

    def process_ui_queue(self):
        try:
            while True:
                msg = self.ui_queue.get_nowait()
                if msg == ("FINISH",):
                    self.finish_ui()
                    continue
                
                if isinstance(msg, tuple) and msg[0] == "UPDATE_STAT":
                    _, key, val = msg
                    self.stats[key].set(val)
                    continue

                self.log_area.config(state="normal")
                self.log_area.insert(tk.END, msg)
                self.log_area.see(tk.END)
                self.log_area.config(state="disabled")
        except queue.Empty:
            pass
        self.root.after(100, self.process_ui_queue)

if __name__ == "__main__":
    root = tk.Tk()
    app = VerifierApp(root)
    root.mainloop()
