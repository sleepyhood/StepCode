import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from playwright.sync_api import sync_playwright
import threading
import time
import os
import sys
import queue
import random

# 상위 폴더나 외부 모듈 의존성 등을 위해 경로 추가
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
if MODULE_DIR not in sys.path:
    sys.path.append(MODULE_DIR)

# 기존 선생님이 작성/보유하신 크롤링 모듈 임포트
try:
    from .crawl import (
        close_doingcoding_admin_session,
        open_doingcoding_admin_session,
        scrape_baekjoon,
        scrape_doingcoding,
        upload_doingcoding_testcases_with_session,
    )
    from .testcase_zip_export import (
        build_default_zip_name,
        build_testcase_preview,
        export_testcases_to_zip,
        parse_testcases_from_markdown,
    )
except ImportError:
    from crawl import (
        close_doingcoding_admin_session,
        open_doingcoding_admin_session,
        scrape_baekjoon,
        scrape_doingcoding,
        upload_doingcoding_testcases_with_session,
    )
    from testcase_zip_export import (
        build_default_zip_name,
        build_testcase_preview,
        export_testcases_to_zip,
        parse_testcases_from_markdown,
    )

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
    resolved_username = (username or "").strip() or os.getenv(
        DOINGCODING_ADMIN_ID_ENV, ""
    ).strip()
    resolved_password = (password or "").strip() or os.getenv(
        DOINGCODING_ADMIN_PASSWORD_ENV, ""
    ).strip()
    return resolved_username, resolved_password


class CrawlerApp:
    def __init__(self, root):
        self.root = root
        self.ui_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.worker_thread = None
        self.is_crawling = False
        self.loaded_testcases = []
        self.selected_testcase_markdown = ""
        self.selected_upload_zip_path = ""
        self.last_md_dir = os.getcwd()
        self.last_zip_dir = os.getcwd()
        self.last_directory_dir = os.getcwd()
        self.root.title("StepCode Reference 수집기 (GUI) - 접두어 패치판")
        self.root.geometry("860x760")

        self.domain_var = tk.StringVar(value="baekjoon")
        self.get_templates_var = tk.BooleanVar(value=False)
        self.get_testcases_var = tk.BooleanVar(value=False)
        self.show_browser_var = tk.BooleanVar(value=False)
        self.save_dir = tk.StringVar(value=os.getcwd())
        self.testcase_md_path = tk.StringVar(value="")
        self.testcase_zip_dir = tk.StringVar(value=os.getcwd())
        self.testcase_zip_name = tk.StringVar(value="")
        self.upload_problem_id = tk.StringVar(value="")
        self.upload_zip_path = tk.StringVar(value="")
        self.upload_problem_id.trace("w", self._on_upload_fields_changed)
        self.upload_zip_path.trace("w", self._on_upload_fields_changed)

        self.shared_settings_frame = tk.LabelFrame(root, text="공통 설정", padx=12, pady=12)
        self.shared_settings_frame.pack(fill="x", padx=10, pady=(10, 6))

        self._build_shared_settings()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.crawl_tab = tk.Frame(self.notebook, padx=12, pady=12)
        self.testcase_zip_tab = tk.Frame(self.notebook, padx=12, pady=12)
        self.testcase_upload_tab = tk.Frame(self.notebook, padx=12, pady=12)

        self.notebook.add(self.crawl_tab, text="크롤링")
        self.notebook.add(self.testcase_zip_tab, text="테스트케이스 ZIP 생성")
        self.notebook.add(self.testcase_upload_tab, text="테스트케이스 업로드")

        self._build_crawl_tab()
        self._build_testcase_zip_tab()
        self._build_upload_tab()
        self._set_doingcoding_option_visibility()
        self.root.after(100, self.process_ui_queue)

    def _build_shared_settings(self):
        tk.Label(
            self.shared_settings_frame,
            text="[ 타겟 도메인 ]",
            font=("Helvetica", 10, "bold"),
        ).pack(pady=(0, 5))
        self.frame_radio = tk.Frame(self.shared_settings_frame)
        self.frame_radio.pack()
        tk.Radiobutton(
            self.frame_radio,
            text="백준 (acmicpc.net)",
            variable=self.domain_var,
            value="baekjoon",
        ).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(
            self.frame_radio,
            text="자체사이트 (doingcoding)",
            variable=self.domain_var,
            value="doingcoding",
        ).pack(side=tk.LEFT, padx=10)
        self.domain_var.trace("w", self.update_url_template)

        tk.Label(
            self.shared_settings_frame,
            text="[ URL 템플릿 ( '{id}' 위치에 조합된 ID가 삽입됩니다 ) ]",
            font=("Helvetica", 10, "bold"),
        ).pack(pady=(12, 5))
        self.url_template = tk.Entry(self.shared_settings_frame, width=80)
        self.url_template.insert(0, "https://www.acmicpc.net/problem/{id}")
        self.url_template.pack(fill="x", padx=10)

        self.doingcoding_options_frame = tk.Frame(self.shared_settings_frame)
        self.check_template = tk.Checkbutton(
            self.doingcoding_options_frame,
            text="코드 템플릿 포함 (수집 속도가 현저히 느려질 수 있습니다)",
            variable=self.get_templates_var,
        )
        self.check_template.pack(pady=4)

        self.check_testcases = tk.Checkbutton(
            self.doingcoding_options_frame,
            text="채점용 테스트케이스 포함 (doingcoding 관리자 로그인 필요)",
            variable=self.get_testcases_var,
        )
        self.check_testcases.pack(pady=4)

        self.check_show_browser = tk.Checkbutton(
            self.doingcoding_options_frame,
            text="doingcoding 진행 화면 표시",
            variable=self.show_browser_var,
        )
        self.check_show_browser.pack(pady=4)

        self.admin_frame = tk.Frame(self.doingcoding_options_frame)
        self.admin_frame.pack(pady=(4, 0))
        tk.Label(self.admin_frame, text="관리자 ID").pack(side=tk.LEFT)
        self.admin_username = tk.Entry(self.admin_frame, width=18)
        self.admin_username.pack(side=tk.LEFT, padx=(5, 10))
        tk.Label(self.admin_frame, text="관리자 PW").pack(side=tk.LEFT)
        self.admin_password = tk.Entry(self.admin_frame, width=18, show="*")
        self.admin_password.pack(side=tk.LEFT, padx=(5, 0))

    def _build_crawl_tab(self):
        tk.Label(
            self.crawl_tab,
            text="[ 수집할 문제 ID 범위 설정 ]\n(예: Prefix P101v + 시작 01 ~ 종료 10)",
            font=("Helvetica", 10, "bold"),
        ).pack(pady=(0, 10))

        self.frame_input = tk.Frame(self.crawl_tab)
        self.frame_input.pack()

        tk.Label(self.frame_input, text="접두어(Prefix):\n(예: P101v)").pack(side=tk.LEFT)
        self.prefix_id = tk.Entry(self.frame_input, width=10)
        self.prefix_id.insert(0, "")
        self.prefix_id.pack(side=tk.LEFT, padx=(5, 15))

        tk.Label(self.frame_input, text="시작 번호:\n(예: 01)").pack(side=tk.LEFT)
        self.start_id = tk.Entry(self.frame_input, width=8)
        self.start_id.insert(0, "1000")
        self.start_id.pack(side=tk.LEFT, padx=(5, 5))

        tk.Label(self.frame_input, text="~ 종료 번호:\n(예: 10)").pack(side=tk.LEFT)
        self.end_id = tk.Entry(self.frame_input, width=8)
        self.end_id.insert(0, "1005")
        self.end_id.pack(side=tk.LEFT, padx=(5, 15))

        tk.Label(self.frame_input, text="접미어(Suffix):\n(선택)").pack(side=tk.LEFT)
        self.suffix_id = tk.Entry(self.frame_input, width=8)
        self.suffix_id.insert(0, "")
        self.suffix_id.pack(side=tk.LEFT, padx=5)

        self.frame_dir = tk.Frame(self.crawl_tab)
        self.frame_dir.pack(fill="x", pady=20)
        tk.Label(self.frame_dir, text="저장 폴더:").pack(side=tk.LEFT)
        tk.Entry(
            self.frame_dir, textvariable=self.save_dir, width=55, state="readonly"
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_dir, text="폴더 변경", command=self.select_dir).pack(
            side=tk.LEFT
        )

        self.button_frame = tk.Frame(self.crawl_tab)
        self.button_frame.pack(pady=5)
        self.start_btn = tk.Button(
            self.button_frame,
            text="🚀 지정된 ID 범위 크롤링 시작",
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="black",
            command=self.start_crawl,
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 8))
        self.stop_btn = tk.Button(
            self.button_frame,
            text="🛑 크롤링 중단",
            font=("Helvetica", 12, "bold"),
            bg="#f44336",
            fg="black",
            command=self.stop_crawl,
            state=tk.DISABLED,
        )
        self.stop_btn.pack(side=tk.LEFT)

        self.log_area = scrolledtext.ScrolledText(
            self.crawl_tab, width=90, height=18, state="disabled", bg="#f0f0f0"
        )
        self.log_area.pack(fill="both", expand=True, pady=(12, 0))

    def _build_testcase_zip_tab(self):
        self.testcase_zip_frame = tk.LabelFrame(
            self.testcase_zip_tab,
            text="테스트케이스 ZIP 생성",
            padx=10,
            pady=10,
        )
        self.testcase_zip_frame.pack(fill="both", expand=True)

        testcase_md_frame = tk.Frame(self.testcase_zip_frame)
        testcase_md_frame.pack(fill="x", pady=(0, 6))
        tk.Label(testcase_md_frame, text="마크다운 파일:").pack(side=tk.LEFT)
        tk.Entry(
            testcase_md_frame,
            textvariable=self.testcase_md_path,
            width=62,
            state="readonly",
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            testcase_md_frame,
            text="파일 선택",
            command=self.select_testcase_markdown,
        ).pack(side=tk.LEFT)

        testcase_dir_frame = tk.Frame(self.testcase_zip_frame)
        testcase_dir_frame.pack(fill="x", pady=(0, 6))
        tk.Label(testcase_dir_frame, text="저장 폴더:").pack(side=tk.LEFT)
        tk.Entry(
            testcase_dir_frame,
            textvariable=self.testcase_zip_dir,
            width=62,
            state="readonly",
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            testcase_dir_frame,
            text="폴더 선택",
            command=self.select_testcase_zip_dir,
        ).pack(side=tk.LEFT)

        testcase_zip_name_frame = tk.Frame(self.testcase_zip_frame)
        testcase_zip_name_frame.pack(fill="x", pady=(0, 6))
        tk.Label(testcase_zip_name_frame, text="출력 ZIP 이름:").pack(side=tk.LEFT)
        tk.Entry(
            testcase_zip_name_frame,
            textvariable=self.testcase_zip_name,
            width=30,
        ).pack(side=tk.LEFT, padx=5)

        self.testcase_count_label = tk.Label(
            self.testcase_zip_frame, text="총 테스트케이스: 0개"
        )
        self.testcase_count_label.pack(anchor="w", pady=(0, 4))

        testcase_action_frame = tk.Frame(self.testcase_zip_frame)
        testcase_action_frame.pack(fill="x", pady=(0, 6))

        self.export_testcase_zip_btn = tk.Button(
            testcase_action_frame,
            text="ZIP 생성",
            command=self.export_testcase_zip,
            state=tk.DISABLED,
        )
        self.export_testcase_zip_btn.pack(side=tk.RIGHT)

        preview_frame = tk.Frame(self.testcase_zip_frame)
        preview_frame.pack(fill="both", expand=True)

        self.testcase_preview_area = scrolledtext.ScrolledText(
            preview_frame,
            width=90,
            height=16,
            state="disabled",
            bg="#f7f7f7",
        )
        self.testcase_preview_area.pack(fill="both", expand=True)

    def _build_upload_tab(self):
        self.testcase_upload_frame = tk.LabelFrame(
            self.testcase_upload_tab,
            text="테스트케이스 업로드",
            padx=10,
            pady=10,
        )
        self.testcase_upload_frame.pack(fill="both", expand=True)

        upload_problem_frame = tk.Frame(self.testcase_upload_frame)
        upload_problem_frame.pack(fill="x", pady=(0, 6))
        tk.Label(upload_problem_frame, text="문제 ID:").pack(side=tk.LEFT)
        tk.Entry(
            upload_problem_frame,
            textvariable=self.upload_problem_id,
            width=20,
        ).pack(side=tk.LEFT, padx=5)

        upload_zip_frame = tk.Frame(self.testcase_upload_frame)
        upload_zip_frame.pack(fill="x", pady=(0, 6))
        tk.Label(upload_zip_frame, text="ZIP 파일:").pack(side=tk.LEFT)
        tk.Entry(
            upload_zip_frame,
            textvariable=self.upload_zip_path,
            width=62,
            state="readonly",
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            upload_zip_frame,
            text="ZIP 선택",
            command=self.select_upload_zip_file,
        ).pack(side=tk.LEFT)

        self.upload_summary_label = tk.Label(
            self.testcase_upload_frame,
            text="문제 ID와 ZIP 파일을 선택해 주세요.",
            anchor="w",
            justify=tk.LEFT,
        )
        self.upload_summary_label.pack(anchor="w", pady=(0, 6))

        self.upload_testcase_btn = tk.Button(
            self.testcase_upload_frame,
            text="업로드 실행",
            command=self.upload_testcase_zip,
            state=tk.DISABLED,
        )
        self.upload_testcase_btn.pack(anchor="e")

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
        self._set_doingcoding_option_visibility()

    def _set_doingcoding_option_visibility(self):
        if self.domain_var.get() == "doingcoding":
            self.doingcoding_options_frame.pack(fill="x", pady=(12, 0))
            return

        self.doingcoding_options_frame.pack_forget()
        self.get_templates_var.set(False)
        self.get_testcases_var.set(False)
        self.show_browser_var.set(False)

    def select_dir(self):
        initialdir = self._resolve_initial_dir(
            "directory", current_path=self.save_dir.get()
        )
        directory = filedialog.askdirectory(initialdir=initialdir)
        if directory:
            self._remember_selected_path("directory", directory)
            self.save_dir.set(directory)

    def _resolve_initial_dir(self, kind, current_path=""):
        last_dir_map = {
            "md": getattr(self, "last_md_dir", ""),
            "zip": getattr(self, "last_zip_dir", ""),
            "directory": getattr(self, "last_directory_dir", ""),
        }
        candidate = last_dir_map.get(kind, "") or ""
        if candidate and os.path.isdir(candidate):
            return candidate

        current_path = (current_path or "").strip()
        if current_path:
            if os.path.isdir(current_path):
                return current_path
            parent_dir = os.path.dirname(current_path)
            if parent_dir and os.path.isdir(parent_dir):
                return parent_dir

        fallback = os.getcwd()
        return fallback if os.path.isdir(fallback) else "."

    def _remember_selected_path(self, kind, selected_path):
        if not selected_path:
            return

        directory = selected_path
        if kind in {"md", "zip"}:
            directory = os.path.dirname(selected_path)

        if not directory or not os.path.isdir(directory):
            return

        if kind == "md":
            self.last_md_dir = directory
        elif kind == "zip":
            self.last_zip_dir = directory
        elif kind == "directory":
            self.last_directory_dir = directory

    def _set_testcase_preview(self, preview_text):
        self.testcase_preview_area.config(state="normal")
        self.testcase_preview_area.delete(1.0, tk.END)
        self.testcase_preview_area.insert(tk.END, preview_text)
        self.testcase_preview_area.config(state="disabled")

    def _set_testcase_export_enabled(self, enabled):
        self.export_testcase_zip_btn.config(
            state=tk.NORMAL if enabled else tk.DISABLED
        )

    def _set_testcase_count(self, count):
        self.testcase_count_label.config(text=f"총 테스트케이스: {count}개")

    def _on_upload_fields_changed(self, *args):
        self._refresh_upload_summary()

    def _refresh_upload_summary(self):
        problem_id = self.upload_problem_id.get().strip()
        zip_path = self.upload_zip_path.get().strip()
        if problem_id and zip_path:
            summary = f"업로드 대상 문제: {problem_id}\n선택한 ZIP: {zip_path}"
        elif problem_id:
            summary = f"업로드 대상 문제: {problem_id}\n선택한 ZIP: 없음"
        elif zip_path:
            summary = f"업로드 대상 문제: 없음\n선택한 ZIP: {zip_path}"
        else:
            summary = "문제 ID와 ZIP 파일을 선택해 주세요."
        self.upload_summary_label.config(text=summary)
        self.upload_testcase_btn.config(
            state=tk.NORMAL if problem_id and zip_path else tk.DISABLED
        )

    def load_testcase_markdown(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8-sig") as source_file:
                md_text = source_file.read()
            cases = parse_testcases_from_markdown(md_text)
        except Exception as exc:
            self.loaded_testcases = []
            self.selected_testcase_markdown = filepath
            self._set_testcase_count(0)
            self._set_testcase_preview(f"불러오기 실패: {exc}")
            self._set_testcase_export_enabled(False)
            return False

        self.loaded_testcases = cases
        self.selected_testcase_markdown = filepath
        self._set_testcase_count(len(cases))
        self._set_testcase_preview(build_testcase_preview(cases, limit=3))
        self._set_testcase_export_enabled(bool(cases))

        self.testcase_zip_name.set(build_default_zip_name(filepath))
        return True

    def select_testcase_markdown(self):
        filepath = filedialog.askopenfilename(
            initialdir=self._resolve_initial_dir(
                "md", current_path=self.testcase_md_path.get()
            ),
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
        )
        if not filepath:
            return

        self._remember_selected_path("md", filepath)
        self.testcase_md_path.set(filepath)
        if not self.load_testcase_markdown(filepath):
            messagebox.showerror(
                "불러오기 실패",
                self.testcase_preview_area.get(1.0, tk.END).strip(),
            )

    def select_testcase_zip_dir(self):
        initialdir = self._resolve_initial_dir(
            "directory", current_path=self.testcase_zip_dir.get()
        )
        directory = filedialog.askdirectory(initialdir=initialdir)
        if directory:
            self._remember_selected_path("directory", directory)
            self.testcase_zip_dir.set(directory)

    def select_upload_zip_file(self):
        filepath = filedialog.askopenfilename(
            initialdir=self._resolve_initial_dir(
                "zip", current_path=self.upload_zip_path.get()
            ),
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")],
        )
        if not filepath:
            return

        self._remember_selected_path("zip", filepath)
        self.selected_upload_zip_path = filepath
        self.upload_zip_path.set(filepath)
        self._refresh_upload_summary()

    def upload_testcase_zip(self):
        problem_id = self.upload_problem_id.get().strip()
        zip_path = self.upload_zip_path.get().strip()
        admin_username, admin_password = resolve_admin_credentials(
            self.admin_username.get(),
            self.admin_password.get(),
        )

        if not problem_id:
            messagebox.showerror("업로드 오류", "업로드할 문제 ID를 입력해 주세요.")
            return
        if not zip_path:
            messagebox.showerror("업로드 오류", "업로드할 ZIP 파일을 선택해 주세요.")
            return
        if not os.path.isfile(zip_path):
            messagebox.showerror(
                "업로드 오류",
                f"업로드할 ZIP 파일을 찾지 못했습니다.\n{zip_path}",
            )
            return
        if not zip_path.lower().endswith(".zip"):
            messagebox.showerror("업로드 오류", "ZIP 파일만 업로드할 수 있습니다.")
            return
        if not admin_username or not admin_password:
            messagebox.showerror(
                "업로드 오류",
                "관리자 ID/PW를 입력하거나 환경변수를 설정해 주세요.",
            )
            return

        show_browser = self.show_browser_var.get()
        self._append_log(f"[테스트케이스 업로드] 준비: {problem_id}")

        shared_playwright = None
        shared_browser = None
        admin_session = None
        try:
            shared_playwright = sync_playwright().start()
            shared_browser = shared_playwright.chromium.launch(headless=not show_browser)
            admin_session = open_doingcoding_admin_session(
                shared_browser,
                admin_username,
                admin_password,
                logger=self.log,
            )
            result = upload_doingcoding_testcases_with_session(
                admin_session,
                problem_id,
                zip_path,
                logger=self.log,
            )
        except Exception as exc:
            self._append_log(f"[테스트케이스 업로드] 실패: {exc}")
            messagebox.showerror("업로드 실패", str(exc))
            return
        finally:
            close_doingcoding_admin_session(admin_session)
            if shared_browser is not None:
                shared_browser.close()
            if shared_playwright is not None:
                shared_playwright.stop()

        self._append_log(
            f"[테스트케이스 업로드] 완료: {result['problem_id']} <- {os.path.basename(result['zip_path'])}"
        )
        messagebox.showinfo(
            "업로드 완료",
            f"문제 {result['problem_id']}에 테스트케이스 ZIP을 업로드했습니다.",
        )

    def export_testcase_zip(self):
        if not self.loaded_testcases:
            messagebox.showerror(
                "추출 오류",
                "먼저 테스트케이스가 포함된 마크다운 파일을 불러와 주세요.",
            )
            return

        output_dir = self.testcase_zip_dir.get().strip() or os.getcwd()
        zip_name = self.testcase_zip_name.get().strip()
        if not zip_name and self.selected_testcase_markdown:
            zip_name = build_default_zip_name(self.selected_testcase_markdown)
            self.testcase_zip_name.set(zip_name)

        try:
            target_path = build_output_filepath(
                output_dir,
                zip_name if zip_name.lower().endswith(".zip") else f"{zip_name}.zip",
            )
            zip_path = export_testcases_to_zip(
                self.loaded_testcases,
                output_dir,
                os.path.basename(target_path),
            )
        except Exception as exc:
            messagebox.showerror("ZIP 생성 실패", str(exc))
            return

        self._append_log(f"[테스트케이스 ZIP] 저장 완료: {os.path.basename(zip_path)}")
        messagebox.showinfo(
            "ZIP 생성 완료",
            f"테스트케이스 ZIP을 저장했습니다.\n{zip_path}",
        )

    def _append_log(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")

    def _set_start_button(self, state, text):
        self.start_btn.config(state=state, text=text)

    def _set_stop_button(self, state, text="🛑 크롤링 중단"):
        self.stop_btn.config(state=state, text=text)

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
            elif action == "stop_button":
                state, text = payload
                self._set_stop_button(state, text)
            elif action == "crawl_state":
                self.is_crawling = payload

        self.root.after(100, self.process_ui_queue)

    def log(self, message):
        self.ui_queue.put(("log", message))

    def start_crawl(self):
        if self.is_crawling:
            self._append_log("이미 크롤링이 진행 중입니다.")
            return

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
                num_str = (
                    str(i).zfill(pad_length)
                    if pad_length > 1 and start_str.startswith("0")
                    else str(i)
                )
                full_id = f"{prefix}{num_str}{suffix}"
                target_ids.append(full_id)

        except ValueError:
            messagebox.showerror(
                "입력 오류", "시작 번호와 종료 번호는 반드시 숫자로 입력해 주세요."
            )
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
            messagebox.showerror(
                "입력 오류",
                "URL 템플릿 안에 반드시 '{id}' 라는 문자가 포함되어야 합니다.",
            )
            return

        if get_testcases and domain != "doingcoding":
            messagebox.showerror(
                "입력 오류",
                "채점용 테스트케이스 수집은 doingcoding에서만 사용할 수 있습니다.",
            )
            return

        if get_testcases and (not admin_username or not admin_password):
            messagebox.showerror(
                "입력 오류",
                "채점용 테스트케이스 수집에는 관리자 ID/PW가 필요합니다. 입력란 또는 환경변수를 확인해 주세요.",
            )
            return

        os.makedirs(save_path, exist_ok=True)

        self.stop_event.clear()
        self.is_crawling = True
        self._set_start_button(tk.DISABLED, "크롤링 진행 중...")
        self._set_stop_button(tk.NORMAL)
        self.log_area.config(state="normal")
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state="disabled")
        self._append_log(f"=== 대량 수집 시작 (조합된 ID 총 {len(target_ids)} 개) ===")

        self.worker_thread = threading.Thread(
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
        self.worker_thread.daemon = True
        self.worker_thread.start()

    def stop_crawl(self):
        if not self.is_crawling:
            return
        if self.stop_event.is_set():
            self._append_log("중단 요청이 이미 전달되었습니다. 현재 작업 정리 후 종료합니다.")
            return

        self.stop_event.set()
        self._set_stop_button(tk.DISABLED, "중단 요청됨...")
        self._append_log(
            "중단 요청을 보냈습니다. 현재 처리 중인 항목을 마치거나 가능한 지점에서 종료합니다."
        )

    def _sleep_with_stop(self, seconds, interval=0.1):
        deadline = time.time() + seconds
        while time.time() < deadline:
            if self.stop_event.is_set():
                return False
            time.sleep(min(interval, max(0, deadline - time.time())))
        return True

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
        if not hasattr(self, "stop_event") or self.stop_event is None:
            self.stop_event = threading.Event()

        success_count = 0
        failures = []
        shared_playwright = None
        shared_browser = None
        admin_session = None
        stopped = False

        shared_playwright = sync_playwright().start()
        shared_browser = shared_playwright.chromium.launch(headless=not show_browser)

        if domain == "doingcoding" and get_testcases:
            admin_session = open_doingcoding_admin_session(
                shared_browser,
                admin_username,
                admin_password,
                logger=self.log,
            )

        try:
            for current_id in target_ids:
                if self.stop_event.is_set():
                    stopped = True
                    self.log("\n[중단] 사용자 요청으로 크롤링을 중단합니다.")
                    break

                target_url = template.replace("{id}", current_id)
                self.log(f"\n[접속 시도] {target_url}")

                md_output = None
                title = ""
                try:
                    if domain == "baekjoon":
                        # save_path 인자를 넘겨주어 이미지 저장 경로를 지정합니다.
                        result = scrape_baekjoon(target_url, save_dir=save_path, browser=shared_browser)
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
                            browser=shared_browser,
                            admin_session=admin_session,
                        )
                        prefix = "dc"

                    if result == (None, None):
                        self.log(
                            f"  ❌ 크롤링 실패 (요소를 찾을 수 없거나 삭제된 문제입니다)"
                        )
                        failures.append(target_url)
                        if not self._sleep_with_stop(1):
                            stopped = True
                            self.log("[중단] 실패 처리 대기 중 중단 요청을 확인했습니다.")
                            break
                        continue

                    title, md_output = result

                    if self.stop_event.is_set():
                        stopped = True
                        self.log("[중단] 현재 항목 저장 전에 중단 요청을 확인했습니다.")
                        break

                    if md_output:
                        filename = f"{prefix}_{current_id}.md"
                        filepath = build_output_filepath(save_path, filename)
                        with open(filepath, "w", encoding="utf-8-sig") as f:
                            f.write(md_output)

                        self.log(f"  ✅ [추출 성공] '{title}'")
                        self.log(f"  📂 저장 완료: {os.path.basename(filepath)}")
                        success_count += 1
                    
                    sleep_time = random.uniform(1.5, 3.5)
                    self.log(f"  ⏳ 봇 탐지 우회를 위해 {sleep_time:.2f}초 대기합니다...")

                    if not self._sleep_with_stop(sleep_time):
                        stopped = True
                        self.log("[중단] 다음 항목 진행 전 중단 요청을 확인했습니다.")
                        break

                except Exception as e:
                    self.log(f"  ❌ 시스템 에러 발생: {e}")
                    failures.append(target_url)
        finally:
            close_doingcoding_admin_session(admin_session)
            if shared_browser is not None:
                shared_browser.close()
            if shared_playwright is not None:
                shared_playwright.stop()

        if failures:
            failure_report = os.path.join(save_path, "crawl_failures.txt")
            with open(failure_report, "a", encoding="utf-8-sig") as failure_file:
                failure_file.write("\n".join(failures) + "\n")
            self.log(f"  ⚠ 실패 목록 저장: {os.path.basename(failure_report)}")

        if stopped:
            self.log(f"\n=== 크롤링이 중단되었습니다. (저장 완료: {success_count}건) ===")
        else:
            self.log(f"\n=== 전체 수집을 완료했습니다. (최종 성공: {success_count} 건) ===")
        self.worker_thread = None
        self.stop_event.clear()
        self.ui_queue.put(("crawl_state", False))
        self.ui_queue.put(("button", (tk.NORMAL, "🚀 지정된 ID 범위 크롤링 시작")))
        self.ui_queue.put(("stop_button", (tk.DISABLED, "🛑 크롤링 중단")))


if __name__ == "__main__":
    root = tk.Tk()
    app = CrawlerApp(root)
    root.mainloop()
