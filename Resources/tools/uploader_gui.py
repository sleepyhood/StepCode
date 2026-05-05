import tkinter as tk
from tkinter import ttk,  filedialog, messagebox, scrolledtext
import threading
import os
import sys
from uploader_engine import run_uploader, perform_login

# 상위 경로를 sys.path에 추가 (필요시)
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
if MODULE_DIR not in sys.path:
    sys.path.append(MODULE_DIR)

try:
    from uploader_engine import run_uploader
except ImportError:
    pass

class UploaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("온라인 저지 자동 업로더 (Smart Uploader)")
        self.root.geometry("700x600")
        
        self.state_path = "state.json"
        
        # 탭 컨트롤러 생성
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 탭 1 (로그인), 탭 2 (업로드) 프레임 생성
        self.tab_login = ttk.Frame(self.notebook)
        self.tab_upload = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_login, text="🔑 1단계: 관리자 로그인")
        
        # 업로드 탭은 초기에 비활성화 (disabled) 상태로 추가
        self.notebook.add(self.tab_upload, text="🚀 2단계: 문제 업로드", state="disabled")
        
        self._build_login_tab()
        self._build_upload_tab()
        self._build_log_area() # 로그창은 탭 아래에 공통으로 노출
        
        # 이미 이전에 로그인한 세션 파일이 있다면 바로 탭 2 활성화
        if os.path.exists(self.state_path):
            self.notebook.tab(self.tab_upload, state="normal")
            self._log("💡 저장된 로그인 세션이 감지되었습니다. 2단계로 바로 넘어갈 수 있습니다.")

    def _build_login_tab(self):
        self.admin_id_var = tk.StringVar()
        self.admin_pwd_var = tk.StringVar()
        
        frame = tk.LabelFrame(self.tab_login, text="[ 관리자 계정 정보 ]", padx=20, pady=20)
        frame.pack(fill="x", padx=20, pady=20)
        
        tk.Label(frame, text="아이디:").grid(row=0, column=0, pady=5, sticky="e")
        tk.Entry(frame, textvariable=self.admin_id_var, width=30).grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="비밀번호:").grid(row=1, column=0, pady=5, sticky="e")
        tk.Entry(frame, textvariable=self.admin_pwd_var, width=30, show="*").grid(row=1, column=1, pady=5, padx=10)
        
        self.login_btn = tk.Button(frame, text="로그인 및 세션 저장", bg="#2196F3", fg="white", 
                                   font=("Helvetica", 10, "bold"), command=self._start_login)
        self.login_btn.grid(row=2, column=1, pady=15, sticky="w")

    def _build_upload_tab(self):
        self.target_url_var = tk.StringVar(value="http://edu.doingcoding.com/admin/problem/create")
        self.md_path_var = tk.StringVar()
        self.zip_path_var = tk.StringVar()
        
        # URL 영역
        url_frame = tk.LabelFrame(self.tab_upload, text="[ 대상 URL ]", padx=10, pady=10)
        url_frame.pack(fill="x", padx=10, pady=5)
        tk.Entry(url_frame, textvariable=self.target_url_var, width=80).pack(fill="x")
        
        # 파일 영역
        file_frame = tk.LabelFrame(self.tab_upload, text="[ 데이터 선택 ]", padx=10, pady=10)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        md_sub = tk.Frame(file_frame)
        md_sub.pack(fill="x", pady=2)
        tk.Label(md_sub, text="MD 파일:", width=10).pack(side="left")
        tk.Entry(md_sub, textvariable=self.md_path_var, state="readonly", width=55).pack(side="left", padx=5)
        tk.Button(md_sub, text="찾기", command=self._select_md).pack(side="left")
        
        zip_sub = tk.Frame(file_frame)
        zip_sub.pack(fill="x", pady=2)
        tk.Label(zip_sub, text="ZIP 파일:", width=10).pack(side="left")
        tk.Entry(zip_sub, textvariable=self.zip_path_var, state="readonly", width=55).pack(side="left", padx=5)
        tk.Button(zip_sub, text="찾기", command=self._select_zip).pack(side="left")
        
        tk.Button(file_frame, text="MD 경로로 ZIP 자동 추론 (02_workspace -> 04_testcases)", 
                  command=self._auto_infer_zip).pack(pady=5, anchor="w")
                  
        self.start_btn = tk.Button(self.tab_upload, text="🚀 문제 주입 실행", bg="#4CAF50", fg="white", 
                                   font=("Helvetica", 12, "bold"), command=self._start_upload)
        self.start_btn.pack(pady=10)

    def _build_log_area(self):
        log_frame = tk.LabelFrame(self.root, text="작업 로그", padx=10, pady=5)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_area = scrolledtext.ScrolledText(log_frame, width=80, height=10, state="disabled", bg="#2b2b2b", fg="#ffffff")
        self.log_area.pack(fill="both", expand=True)

    def _log(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")

    def _select_md(self):
        path = filedialog.askopenfilename(filetypes=[("Markdown", "*.md")])
        if path:
            self.md_path_var.set(path)
            
    def _select_zip(self):
        path = filedialog.askopenfilename(filetypes=[("ZIP Archive", "*.zip")])
        if path:
            self.zip_path_var.set(path)
            
    def _auto_infer_zip(self):
        md = self.md_path_var.get()
        if not md: return
        # 02_workspace를 04_testcases로 바꾸고 .md를 .zip으로
        inferred = md.replace("02_workspace", "04_testcases").replace(".md", ".zip")
        self.zip_path_var.set(inferred)
        self._log(f"ZIP 경로 자동 추론 완료: {inferred}")

    def _start_login(self):
            admin_id = self.admin_id_var.get().strip()
            admin_pwd = self.admin_pwd_var.get().strip()
            if not admin_id or not admin_pwd:
                messagebox.showerror("에러", "아이디와 비밀번호를 입력하세요.")
                return
                
            self.login_btn.config(state="disabled", text="로그인 중...")
            self._log("="*50)
            
            def task():
                success = perform_login(admin_id, admin_pwd, self.state_path, self._log)
                if success:
                    # 로그인 성공 시: 업로드 탭 잠금 해제 및 이동
                    self.notebook.tab(self.tab_upload, state="normal")
                    self.notebook.select(self.tab_upload)
                self.login_btn.config(state="normal", text="로그인 및 세션 저장")
                
            threading.Thread(target=task, daemon=True).start()

    def _start_upload(self):
        url = self.target_url_var.get().strip()
        md = self.md_path_var.get().strip()
        zip_path = self.zip_path_var.get().strip()
        
        if not md:
            messagebox.showerror("에러", "MD 파일을 선택하세요.")
            return
            
        self.start_btn.config(state="disabled", text="실행 중...")
        self._log("="*50)
        
        def task():
            try:
                # 이제 admin_id, pw 대신 state_path를 넘깁니다.
                run_uploader(url, md, zip_path, self.state_path, log_callback=self._log)
            except Exception as e:
                self._log(f"[치명적 오류] {e}")
            finally:
                self.start_btn.config(state="normal", text="🚀 문제 주입 실행")
                
        threading.Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = UploaderGUI(root)
    root.mainloop()
