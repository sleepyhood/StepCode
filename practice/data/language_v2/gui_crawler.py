import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import time
import os
import sys

# 상위 폴더나 외부 모듈 의존성 등을 위해 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__name__)))

# 기존 선생님이 작성/보유하신 크롤링 모듈 임포트
from crawl import scrape_baekjoon, scrape_doingcoding

class CrawlerApp:
    def __init__(self, root):
        self.root = root
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

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        self.root.update_idletasks()

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

        if "{id}" not in template:
            messagebox.showerror("입력 오류", "URL 템플릿 안에 반드시 '{id}' 라는 문자가 포함되어야 합니다.")
            return

        self.start_btn.config(state=tk.DISABLED, text="크롤링 진행 중...")
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')
        self.log(f"=== 대량 수집 시작 (조합된 ID 총 {len(target_ids)} 개) ===")
        
        thread = threading.Thread(target=self.crawl_process, args=(target_ids, domain, template, save_path))
        thread.daemon = True
        thread.start()

    def crawl_process(self, target_ids, domain, template, save_path):
        success_count = 0
        
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
                    result = scrape_doingcoding(target_url)
                    prefix = "dc"
                
                if result == (None, None):
                    self.log(f"  ❌ 크롤링 실패 (요소를 찾을 수 없거나 삭제된 문제입니다)")
                    time.sleep(1)
                    continue
                
                title, md_output = result
                
                if md_output:
                    filename = f"01_{prefix}_{current_id}.md"
                    filepath = os.path.join(save_path, filename)
                    with open(filepath, 'w', encoding='utf-8-sig') as f:
                        f.write(md_output)
                    
                    self.log(f"  ✅ [추출 성공] '{title}'")
                    self.log(f"  📂 저장 완료: {filename}")
                    success_count += 1
                
                time.sleep(1.5)
                
            except Exception as e:
                self.log(f"  ❌ 시스템 에러 발생: {e}")

        self.log(f"\n=== 전체 수집을 완료했습니다. (최종 성공: {success_count} 건) ===")
        self.start_btn.config(state=tk.NORMAL, text="🚀 지정된 ID 범위 크롤링 시작")

if __name__ == "__main__":
    root = tk.Tk()
    app = CrawlerApp(root)
    root.mainloop()
