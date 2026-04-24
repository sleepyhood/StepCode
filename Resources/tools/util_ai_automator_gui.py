import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import glob
import subprocess
import threading
import queue
import time
import shlex # 추가

# draw.io 데스크톱 앱 경로 (필수)
DRAWIO_EXE_PATH = r"C:\Program Files\draw.io\draw.io.exe"

class DrawioAutomatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Draw.io AI 통합 오토메이터 - 최종 완성본")
        self.root.geometry("680x620")
        self.root.resizable(False, False)
        
        self.log_queue = queue.Queue()
        self.create_widgets()
        self.root.after(100, self.process_log_queue)

    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=20, pady=15)
        main_frame.pack(fill="both", expand=True)

        # 1. 배경 이미지 선택
        tk.Label(main_frame, text="1. 배경 이미지 (설명 대상):", font=("", 10, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.bg_img_entry = ttk.Entry(main_frame, width=55)
        self.bg_img_entry.grid(row=0, column=1, padx=10, pady=(0, 5))
        ttk.Button(main_frame, text="찾아보기...", command=self.select_bg_image).grid(row=0, column=2, pady=(0, 5))

        # 2. 저장 폴더 선택 (기본값: 바탕화면)
        tk.Label(main_frame, text="2. 결과 저장 폴더:", font=("", 10, "bold")).grid(row=1, column=0, sticky="w", pady=(0, 15))
        self.save_dir_entry = ttk.Entry(main_frame, width=55)
        self.save_dir_entry.insert(0, os.path.expanduser("~/Desktop"))
        self.save_dir_entry.grid(row=1, column=1, padx=10, pady=(0, 15))
        ttk.Button(main_frame, text="폴더 선택...", command=self.select_save_dir).grid(row=1, column=2, pady=(0, 15))

        # 3. 프롬프트 입력창
        tk.Label(main_frame, text="3. 추가할 다이어그램 설명 (AI에게 전달):", font=("", 10, "bold")).grid(row=2, column=0, columnspan=3, sticky="w", pady=(0, 5))
        self.prompt_text = tk.Text(main_frame, height=6, width=82, wrap="word", font=("", 10))
        self.prompt_text.grid(row=3, column=0, columnspan=3, pady=(0, 15))
        self.prompt_text.insert("1.0", "중앙에 '메인 프로세스'라는 사각형을 그리고, 좌우에 보조 설명을 추가해줘.")

        # 4. 실행 버튼
        self.run_btn = tk.Button(main_frame, text="🚀 AI 다이어그램 생성 및 PNG 자동 변환", 
                                 command=self.start_automation_thread, 
                                 bg="#007BFF", fg="white", font=("", 12, "bold"), height=2, cursor="hand2")
        self.run_btn.grid(row=4, column=0, columnspan=3, sticky="we", pady=(0, 15))

        # 5. 실시간 로그 창
        tk.Label(main_frame, text="실행 로그 (AI 응답 및 프로세스):", font=("", 9)).grid(row=5, column=0, sticky="w", pady=(0, 2))
        self.log_text = tk.Text(main_frame, height=12, width=82, state="disabled", bg="#1e1e1e", fg="#00ff00", font=("Consolas", 9))
        self.log_text.grid(row=6, column=0, columnspan=3)

    def select_bg_image(self):
            file_path = filedialog.askopenfilename(title="배경 이미지 선택", filetypes=[("Images", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*")])
            if file_path:
                # 1. 배경 이미지 입력창 업데이트
                self.bg_img_entry.delete(0, tk.END)
                self.bg_img_entry.insert(0, file_path)
                
                # 2. [추가된 기능] 이미지의 폴더 경로를 추출하여 저장 폴더로 자동 설정
                dir_path = os.path.dirname(file_path)
                self.save_dir_entry.delete(0, tk.END)
                self.save_dir_entry.insert(0, dir_path)
                
                # 3. 로그 창에 안내 메시지 띄우기 (선택 사항)
                self.log(f"💡 편의기능: 결과 저장 폴더가 배경 이미지와 같은 위치로 자동 설정되었습니다.")

    def select_save_dir(self):
        dir_path = filedialog.askdirectory(title="저장할 폴더 선택")
        if dir_path:
            self.save_dir_entry.delete(0, tk.END)
            self.save_dir_entry.insert(0, dir_path)

    def log(self, message):
        self.log_queue.put(message)

    def process_log_queue(self):
        while not self.log_queue.empty():
            message = self.log_queue.get()
            self.log_text.config(state="normal")
            self.log_text.insert(tk.END, f"> {message}\n")
            self.log_text.see(tk.END)
            self.log_text.config(state="disabled")
        self.root.after(100, self.process_log_queue)

    def start_automation_thread(self):
        bg_img = self.bg_img_entry.get().strip()
        save_dir = self.save_dir_entry.get().strip()
        user_prompt = self.prompt_text.get("1.0", tk.END).strip()

        if not user_prompt or not save_dir:
            messagebox.showwarning("경고", "프롬프트와 저장 폴더를 모두 지정해주세요.")
            return

        if not os.path.isdir(save_dir):
            messagebox.showerror("오류", "유효하지 않은 저장 폴더 경로입니다.")
            return

        self.run_btn.config(state=tk.DISABLED, text="처리 중... (AI 작성 대기)", bg="#cccccc")
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END) # 실행 시 로그 초기화
        self.log_text.config(state="disabled")
        
        threading.Thread(target=self.run_orchestration, args=(bg_img, save_dir, user_prompt), daemon=True).start()
    
    def run_orchestration(self, bg_img, save_dir, user_prompt):
        try:
            self.log("[STEP 1] AI 다이어그램 설계 시작")
            
            # 1. 프로세스 시작 시간 기록 (이 시간 이후에 생성된 파일만 유효)
            start_time = time.time()
            
            internal_instruction = (
                f"[시스템 중요 지시사항]\n"
                f"1. 당신은 'drawio' MCP 도구에 연결되어 있습니다. 웹 검색이나 디렉토리 탐색을 하지 마십시오.\n"
                f"2. 즉시 drawio 도구를 실행하여 다이어그램을 생성하십시오.\n"
                f"3. 배경 이미지 경로: '{bg_img}'\n"
                f"4. 저장 위치: '{save_dir}'\n\n"
            )
            final_command_prompt = f"{internal_instruction}사용자 요청 사항: {user_prompt}"
            
            # 2. 명령어 이스케이프 처리 (쌍따옴표 충돌 방지)
            safe_prompt = shlex.quote(final_command_prompt)
            # 윈도우에서 npm으로 설치한 gemini는 gemini.cmd로 실행해야 안전합니다.
            cmd_args = ["gemini.cmd", final_command_prompt] 

            # shell=False로 보안 및 파싱 에러 방지 (윈도우 .cmd 실행 위해 shell=True 유지시에는 텍스트 결합 주의)
            process = subprocess.Popen(
                cmd_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8', # cp949보다는 범용적인 utf-8 권장 (Gemini CLI 출력에 따라 조정)
                errors='replace',
                bufsize=1,
                shell=True # Windows 환경에서 글로벌 npm 명령어(.cmd) 실행 시 필요할 수 있음
            )            
            
            for line in iter(process.stdout.readline, ''):
                if line:
                    self.log(line.strip())
            
            process.stdout.close()
            return_code = process.wait()

            if return_code != 0:
                self.log(f"❌ gemini-cli 실행 중 오류 발생 (코드: {return_code})")
                return

            self.log("✅ AI 설계 완료. (gemini-cli 종료)")
            
            # ---------------------------------------------------------
            # 3단계: 파일 감지 및 PNG 다이렉트 변환
            # ---------------------------------------------------------
            
            search_pattern = os.path.join(save_dir, "*.drawio")
            drawio_files = glob.glob(search_pattern)
            
            # 3. 시간 기반 필터링: 스크립트 실행 이후에 수정/생성된 파일만 추출
            new_files = [f for f in drawio_files if os.path.getmtime(f) > start_time]
            
            if not new_files:
                self.log("❌ 해당 폴더에서 방금 생성된 .drawio 파일을 찾을 수 없습니다. (AI가 파일을 만들지 않음)")
                return
                
            latest_drawio = max(new_files, key=os.path.getmtime)
            file_name = os.path.basename(latest_drawio)
            self.log(f"🔎 최신 다이어그램 감지됨: {file_name}")

    # def run_orchestration(self, bg_img, save_dir, user_prompt):
    #     try:
    #         # ---------------------------------------------------------
    #         # 2단계: AI에게 명령 하달 (gemini-cli 호출)
    #         # ---------------------------------------------------------

    #         self.log("=======================================")
    #         self.log("[STEP 1] AI 다이어그램 설계 시작")
    #         self.log("=======================================")
            
    #         # [수정 1] AI가 헛짓거리(검색, 탐색)를 하지 않도록 "강력한 통제 지시어" 부여
    #         # 저장할 경로도 프롬프트에 직접 명시합니다.
    #         internal_instruction = (
    #             f"[시스템 중요 지시사항]\n"
    #             f"1. 당신은 이미 'drawio' MCP 도구에 연결되어 있습니다. 도구를 찾기 위해 웹 검색(google_web_search)이나 "
    #             f"디렉토리 탐색을 절대 하지 마십시오.\n"
    #             f"2. 즉시 drawio 도구를 실행하여 다이어그램을 생성하십시오.\n"
    #             f"3. 반드시 다음 배경 이미지를 캔버스 맨 뒤에 깔아야 합니다. (배경 경로: '{bg_img}')\n"
    #             f"4. 결과물은 반드시 다음 폴더 안에 저장하십시오. (저장 폴더: '{save_dir}')\n\n"
    #         )
            
    #         final_command_prompt = f"{internal_instruction}사용자 요청 사항: {user_prompt}"
            
    #         cmd_str = f'gemini "{final_command_prompt}"'
            
    #         # [수정 2] cwd=save_dir 삭제 (gemini-cli가 전역 설정(.gemini)을 읽을 수 있도록 샌드박스 해제)
    #         process = subprocess.Popen(
    #             cmd_str,
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.STDOUT,
    #             text=True,
    #             encoding='cp949',
    #             errors='replace',
    #             bufsize=1,
    #             shell=True
    #             # cwd=save_dir 제거됨!
    #         )            
    #         for line in iter(process.stdout.readline, ''):
    #             if line:
    #                 self.log(line.strip())
            
    #         process.stdout.close()
    #         return_code = process.wait()

    #         if return_code != 0:
    #             self.log(f"❌ gemini-cli 실행 중 오류 발생 (코드: {return_code})")
    #             return

    #         self.log("✅ AI 설계 완료. (gemini-cli 종료)")
            
    #         # ---------------------------------------------------------
    #         # 3단계: 파일 감지 및 PNG 다이렉트 변환
    #         # ---------------------------------------------------------
    #         self.log("\n=======================================")
    #         self.log("[STEP 2] PNG 고화질 렌더링 시작")
    #         self.log("=======================================")
            
    #         # 지정된 폴더에서 .drawio 파일들을 모두 찾아 수정 시간 기준으로 정렬
    #         search_pattern = os.path.join(save_dir, "*.drawio")
    #         drawio_files = glob.glob(search_pattern)
            
    #         if not drawio_files:
    #             self.log("❌ 해당 폴더에서 생성된 .drawio 파일을 찾을 수 없습니다.")
    #             return
                
    #         # 가장 최근에 만들어진 파일(방금 AI가 만든 파일) 선택
    #         latest_drawio = max(drawio_files, key=os.path.getmtime)
    #         file_name = os.path.basename(latest_drawio)
    #         self.log(f"🔎 최신 다이어그램 감지됨: {file_name}")

            if not os.path.exists(DRAWIO_EXE_PATH):
                self.log(f"❌ draw.io 엔진을 찾을 수 없습니다. 경로를 확인하세요: {DRAWIO_EXE_PATH}")
                return

            png_path = latest_drawio.rsplit('.', 1)[0] + ".png"
            self.log("🎨 draw.io 공식 엔진으로 배경 포함 투명 렌더링을 진행합니다...")

            cmd = [
                DRAWIO_EXE_PATH,
                "-x",                # Export 모드
                "-f", "png",         # 포맷 지정
                "--transparent",     # 투명 배경 유지 (배경 이미지 제외한 캔버스 여백)
                "-o", png_path,      # 출력 경로
                latest_drawio        # 입력 파일
            ]

            # 윈도우 환경 검은색 터미널 창 숨김 처리
            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            
            subprocess.run(cmd, check=True, creationflags=creation_flags)
            
            self.log(f"🎉 [최종 완료] PNG 변환 성공! -> {os.path.basename(png_path)}")
            
            # 변환이 끝난 폴더 팝업 띄우기
            os.startfile(save_dir)

        except Exception as e:
            self.log(f"⚠ 시스템 오류: {str(e)}")
        
        finally:
            # GUI 스레드에서 안전하게 버튼 상태 복구
            self.root.after(0, lambda: self.run_btn.config(state=tk.NORMAL, text="🚀 AI 다이어그램 생성 및 PNG 자동 변환", bg="#007BFF"))

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawioAutomatorApp(root)
    root.mainloop()