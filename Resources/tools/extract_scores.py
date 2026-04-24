import os
import sys
import json
import time
import requests
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from urllib.parse import quote, urlparse
from datetime import datetime

try:
    from openpyxl import Workbook
    from openpyxl.styles import PatternFill, Font, Alignment
    from openpyxl.formatting.rule import ColorScaleRule
    from openpyxl.utils import get_column_letter
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

class ScoreExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StepCode 성적 추출기 (대학생 공지용)")
        self.root.geometry("800x850")
        
        self.stop_event = threading.Event()
        self.is_running = False
        
        self._build_ui()
        
        if not HAS_OPENPYXL:
            messagebox.showwarning("라이브러리 누락", "openpyxl 라이브러리가 설치되어 있지 않아 엑셀 생성이 불가능할 수 있습니다.\n`pip install openpyxl`을 실행해주세요.")
    
    def _build_ui(self):
        # 1. 서버 및 인증 정보
        auth_frame = tk.LabelFrame(self.root, text="[ 1. 서버 및 계정 정보 ]", padx=10, pady=10)
        auth_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(auth_frame, text="서버 주소:").grid(row=0, column=0, sticky="e")
        self.base_url_var = tk.StringVar(value="http://edu.doingcoding.com")
        tk.Entry(auth_frame, textvariable=self.base_url_var, width=40).grid(row=0, column=1, sticky="w", padx=5)
        
        tk.Label(auth_frame, text="관리자 ID:").grid(row=1, column=0, sticky="e", pady=5)
        self.admin_id_var = tk.StringVar()
        tk.Entry(auth_frame, textvariable=self.admin_id_var, width=20).grid(row=1, column=1, sticky="w", padx=5)
        
        tk.Label(auth_frame, text="관리자 PW:").grid(row=1, column=2, sticky="e", pady=5)
        self.admin_pw_var = tk.StringVar()
        tk.Entry(auth_frame, textvariable=self.admin_pw_var, show="*", width=20).grid(row=1, column=3, sticky="w", padx=5)
        
        # 2. 문제 구간 설정
        prob_frame = tk.LabelFrame(self.root, text="[ 2. 문제 범위 설정 ]", padx=10, pady=10)
        prob_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(prob_frame, text="문제 접두사(Prefix):").grid(row=0, column=0, sticky="e")
        self.prefix_var = tk.StringVar(value="ky_2026_01_26682_")
        tk.Entry(prob_frame, textvariable=self.prefix_var, width=25).grid(row=0, column=1, sticky="w", padx=5)
        
        tk.Label(prob_frame, text="시작 번호:").grid(row=0, column=2, sticky="e")
        self.start_id_var = tk.IntVar(value=1)
        tk.Entry(prob_frame, textvariable=self.start_id_var, width=5).grid(row=0, column=3, sticky="w", padx=5)
        
        tk.Label(prob_frame, text="~ 끝 번호:").grid(row=0, column=4, sticky="e")
        self.end_id_var = tk.IntVar(value=10)
        tk.Entry(prob_frame, textvariable=self.end_id_var, width=5).grid(row=0, column=5, sticky="w", padx=5)
        
        tk.Label(prob_frame, text="자리수(Padding):").grid(row=1, column=0, sticky="e", pady=5)
        self.pad_var = tk.IntVar(value=2)
        tk.Entry(prob_frame, textvariable=self.pad_var, width=5).grid(row=1, column=1, sticky="w", padx=5)
        tk.Label(prob_frame, text="(예: 2로 설정 시 01, 02...)", fg="gray").grid(row=1, column=2, columnspan=2, sticky="w")
        
        # 3. 대상 학생 명단
        student_frame = tk.LabelFrame(self.root, text="[ 3. 대상 학생 명단 (줄바꿈으로 구분) ]", padx=10, pady=10)
        student_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.student_text = scrolledtext.ScrolledText(student_frame, height=8)
        self.student_text.pack(fill="both", expand=True)
        self.student_text.insert(tk.END, "student_01\nstudent_02\nstudent_03") # 기본 더미 데이터
        
        # 4. 저장 및 실행
        exec_frame = tk.LabelFrame(self.root, text="[ 4. 저장 경로 및 실행 ]", padx=10, pady=10)
        exec_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(exec_frame, text="저장 폴더:").grid(row=0, column=0, sticky="e")
        self.save_dir_var = tk.StringVar(value=os.getcwd())
        tk.Entry(exec_frame, textvariable=self.save_dir_var, width=50, state="readonly").grid(row=0, column=1, sticky="w", padx=5)
        tk.Button(exec_frame, text="변경", command=self._select_dir).grid(row=0, column=2)
        
        self.mock_mode_var = tk.BooleanVar(value=True) # 기본값을 True로 설정 (테스트용)
        tk.Checkbutton(exec_frame, text="테스트 모드 (네트워크 접속 안 함)", variable=self.mock_mode_var).grid(row=1, column=1, sticky="w", pady=5)
        
        btn_frame = tk.Frame(exec_frame)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        self.start_btn = tk.Button(btn_frame, text="🚀 추출 시작", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="black", command=self._start_extraction)
        self.start_btn.pack(side="left", padx=10)
        
        self.stop_btn = tk.Button(btn_frame, text="🛑 중단", font=("Helvetica", 12, "bold"), bg="#f44336", fg="black", command=self._stop_extraction, state=tk.DISABLED)
        self.stop_btn.pack(side="left")
        
        # 로그 창
        self.log_area = scrolledtext.ScrolledText(self.root, height=10, state="disabled", bg="#f0f0f0")
        self.log_area.pack(fill="both", expand=True, padx=10, pady=10)
        
    def _select_dir(self):
        d = filedialog.askdirectory(initialdir=self.save_dir_var.get())
        if d:
            self.save_dir_var.set(d)
            
    def log(self, msg):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")
        self.root.update()

    def _start_extraction(self):
        if self.is_running:
            return
            
        students_raw = self.student_text.get("1.0", tk.END).strip()
        if not students_raw:
            messagebox.showwarning("오류", "학생 명단을 입력해주세요.")
            return
            
        self.student_list = [s.strip() for s in students_raw.split("\n") if s.strip()]
        
        self.is_running = True
        self.stop_event.clear()
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.student_text.config(state=tk.DISABLED)
        
        self.log("="*50)
        self.log(f"추출 시작... 총 대상: {len(self.student_list)}명")
        
        threading.Thread(target=self._extraction_task, daemon=True).start()

    def _stop_extraction(self):
        self.stop_event.set()
        self.log("중단 요청됨. 진행 중인 작업을 마무리하는 중...")

    def _extraction_task(self):
        base_url = self.base_url_var.get().strip()
        admin_id = self.admin_id_var.get().strip()
        admin_pw = self.admin_pw_var.get().strip()
        prefix = self.prefix_var.get().strip()
        start_id = self.start_id_var.get()
        end_id = self.end_id_var.get()
        pad = self.pad_var.get()
        is_mock = self.mock_mode_var.get()
        save_dir = self.save_dir_var.get()
        
        # 문제 ID 리스트 생성
        problem_ids = [f"{prefix}{str(i).zfill(pad)}" for i in range(start_id, end_id + 1)]
        self.log(f"대상 문제: {problem_ids[0]} ~ {problem_ids[-1]} ({len(problem_ids)}개)")
        
        session = None
        if not is_mock:
            self.log("서버 로그인 시도 중...")
            session = self._login(base_url, admin_id, admin_pw)
            if not session:
                self.log("❌ 로그인 실패. 중단합니다.")
                self._finish_task()
                return
            self.log("✅ 로그인 성공!")
        else:
            self.log("⚠️ 테스트 모드로 실행 (가짜 데이터 생성)")
            
        all_data = []
        error_students = []
        
        # Checkpoint load
        checkpoint_file = os.path.join(save_dir, "scores_checkpoint.json")
        processed_users = set()
        if os.path.exists(checkpoint_file):
            try:
                with open(checkpoint_file, "r", encoding="utf-8") as f:
                    all_data = json.load(f)
                processed_users = {d["username"] for d in all_data}
                self.log(f"🔄 체크포인트 로드 됨: 이미 완료된 {len(processed_users)}명 건너뜀.")
            except:
                self.log("⚠️ 체크포인트 파일을 읽을 수 없어 새로 시작합니다.")
                
        # Main Loop
        for i, username in enumerate(self.student_list):
            if self.stop_event.is_set():
                break
                
            if username in processed_users:
                continue
                
            self.log(f"조회 중 ({i+1}/{len(self.student_list)}): {username}")
            
            try:
                if is_mock:
                    time.sleep(0.05) # 모의 지연
                    import random
                    student_scores = {"username": username}
                    # 20% 확률로 미제출, 나머지는 무작위 점수
                    for pid in problem_ids:
                        if random.random() > 0.2:
                            student_scores[pid] = random.choice([0, 50, 80, 100, 100, 100])
                    all_data.append(student_scores)
                else:
                    res = session.get(f"{base_url}/api/profile?username={quote(username)}", timeout=10)
                    data = res.json()
                    
                    if data.get("error"):
                        self.log(f"  ! Error: {data['error']}")
                        error_students.append(username)
                    else:
                        problems = data.get("data", {}).get("oi_problems_status", {}).get("problems", {})
                        student_scores = {"username": username}
                        for p_id_string, p_info in problems.items():
                            if p_id_string in problem_ids:
                                student_scores[p_id_string] = p_info.get("score", 0)
                        all_data.append(student_scores)
                    time.sleep(0.15)
                    
            except Exception as e:
                self.log(f"  ! Exception: {e}")
                error_students.append(username)
                
            # Checkpoint save
            if (i + 1) % 50 == 0:
                self._save_checkpoint(checkpoint_file, all_data)
                
        # Final Processing
        self.log("✅ 조회 루프 완료. 엑셀 생성을 준비합니다.")
        self._save_checkpoint(checkpoint_file, all_data) # final
        
        if error_students:
            err_file = os.path.join(save_dir, "error_students.log")
            with open(err_file, "w", encoding="utf-8") as f:
                f.write("\n".join(error_students))
            self.log(f"⚠️ 실패한 학생 {len(error_students)}명은 error_students.log에 저장되었습니다.")
            
        self._generate_excel(all_data, problem_ids, save_dir)
        self._finish_task()
        
    def _login(self, base_url, username, password):
        # 실제 로그인 로직 구현 필요 (CSRF, JSON 등 사이트 구조에 맞게)
        # 이 부분은 legacy API에 맞춘 더미 형태입니다. 실제 환경에서는 수정이 필요합니다.
        session = requests.Session()
        try:
            # 예시 로그인
            res = session.post(f"{base_url}/api/login", json={"username": username, "password": password})
            if res.status_code == 200 and res.json().get("error") is None:
                return session
        except Exception:
            pass
        return None

    def _save_checkpoint(self, path, data):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.log("💾 체크포인트 저장 완료.")
        except Exception as e:
            self.log(f"⚠️ 체크포인트 저장 실패: {e}")

    def _generate_excel(self, data, problem_ids, save_dir):
        if not HAS_OPENPYXL:
            self.log("❌ openpyxl이 없어 엑셀을 생성할 수 없습니다.")
            return
            
        self.log("📊 데이터 집계 및 엑셀 포맷팅 시작...")
        
        # Calculate stats
        for row in data:
            total = 0
            count = 0
            feedback = []
            for pid in problem_ids:
                val = row.get(pid, "미제출")
                if isinstance(val, (int, float)):
                    total += val
                    count += 1
                    if val < 50:
                        feedback.append(f"{pid[-2:]}번 미흡")
                else:
                    feedback.append(f"{pid[-2:]}번 미제출")
                    
            row["Total"] = total
            row["Average"] = total / len(problem_ids) if problem_ids else 0
            row["Feedback"] = ", ".join(feedback) if feedback else "통과"
            
        # Rank sorting
        data.sort(key=lambda x: x["Total"], reverse=True)
        for i, row in enumerate(data):
            row["Rank"] = i + 1
            
        # Generate XLSX
        wb = Workbook()
        ws = wb.active
        ws.title = "Scores"
        
        headers = ["Rank", "username"] + problem_ids + ["Total", "Average", "Feedback"]
        ws.append(headers)
        
        # Style headers
        for col_idx, _ in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center")
            
        # Data & Missing styles
        missing_fill = PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid")
        for row_idx, row_data in enumerate(data, 2):
            for col_idx, header in enumerate(headers, 1):
                val = row_data.get(header, "")
                cell = ws.cell(row=row_idx, column=col_idx, value=val)
                if header in problem_ids and val == "미제출":
                    cell.fill = missing_fill
                    
        # Conditional Formatting (Gradient)
        rule = ColorScaleRule(start_type='num', start_value=0, start_color='FF6347', # Red
                              mid_type='num', mid_value=50, mid_color='FFD700',      # Yellow
                              end_type='num', end_value=100, end_color='90EE90')     # Green
                              
        for col_idx, header in enumerate(headers, 1):
            if header in problem_ids or header in ["Total", "Average"]:
                col_letter = get_column_letter(col_idx)
                ws.conditional_formatting.add(f'{col_letter}2:{col_letter}{len(data)+1}', rule)
                
        output_path = os.path.join(save_dir, "student_scores.xlsx")
        try:
            wb.save(output_path)
            self.log(f"✅ 엑셀 파일 저장 성공: {output_path}")
        except Exception as e:
            self.log(f"❌ 엑셀 저장 에러: {e}")

    def _finish_task(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.student_text.config(state=tk.NORMAL)
        self.log("="*50)
        self.log("작업이 완전히 종료되었습니다.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreExtractorApp(root)
    root.mainloop()
