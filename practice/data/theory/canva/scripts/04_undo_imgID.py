import tkinter as tk
from tkinter import scrolledtext, messagebox
import re

class MarkdownImageResetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("마크다운 이미지 일괄 초기화 도구 (Reset to ID)")
        self.root.geometry("850x600")

        # --- [상단 설정 및 컨트롤 영역] ---
        frame_top = tk.Frame(root, pady=10)
        frame_top.pack(fill=tk.X, padx=10)

        # ID 접두사 설정
        tk.Label(frame_top, text="새로운 ID 접두사:").pack(side=tk.LEFT)
        self.prefix_var = tk.StringVar(value="IMG_W00_")
        tk.Entry(frame_top, textvariable=self.prefix_var, width=10).pack(side=tk.LEFT, padx=5)

        # 자릿수 설정
        tk.Label(frame_top, text="숫자 자릿수:").pack(side=tk.LEFT, padx=(15, 0))
        self.padding_var = tk.IntVar(value=3)
        tk.Spinbox(frame_top, from_=1, to=5, textvariable=self.padding_var, width=5).pack(side=tk.LEFT, padx=5)

        # 결과 복사 버튼 (편의성)
        self.btn_copy = tk.Button(
            frame_top, text="결과 복사하기", command=self.copy_to_clipboard,
            bg="#FF9800", fg="white", font=("Arial", 10, "bold")
        )
        self.btn_copy.pack(side=tk.RIGHT, padx=5)

        # 변환 실행 버튼
        self.btn_convert = tk.Button(
            frame_top, text="[이미지 삽입] 태그로 일괄 초기화", command=self.reset_images,
            bg="#4CAF50", fg="white", font=("Arial", 10, "bold")
        )
        self.btn_convert.pack(side=tk.RIGHT, padx=10)

        # --- [중간 텍스트 입출력 영역] ---
        frame_text = tk.Frame(root)
        frame_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 왼쪽: 원본 입력창 (기존 MD 텍스트)
        frame_input = tk.Frame(frame_text)
        frame_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        tk.Label(frame_input, text="원본 마크다운 입력 (기존 ![설명](경로) 포함)").pack(anchor=tk.W)
        self.txt_input = scrolledtext.ScrolledText(frame_input, wrap=tk.WORD)
        self.txt_input.pack(fill=tk.BOTH, expand=True)

        # 오른쪽: 결과 출력창 (초기화된 텍스트)
        frame_output = tk.Frame(frame_text)
        frame_output.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        tk.Label(frame_output, text="초기화된 결과 (복사 가능)").pack(anchor=tk.W)
        self.txt_output = scrolledtext.ScrolledText(frame_output, wrap=tk.WORD, bg="#f9f9f9")
        self.txt_output.pack(fill=tk.BOTH, expand=True)

        # --- [하단 상태 표시줄] ---
        self.lbl_status = tk.Label(root, text="대기 중... 기존 이미지가 포함된 마크다운을 붙여넣으세요.", fg="blue", pady=5)
        self.lbl_status.pack()

    # --- [핵심 변환 로직] ---
    def reset_images(self):
        input_text = self.txt_input.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("경고", "마크다운 텍스트를 입력해 주세요.")
            return

        prefix = self.prefix_var.get()
        try:
            padding = self.padding_var.get()
        except tk.TclError:
            padding = 2

        # 정규표현식: ![대체텍스트](이미지경로) 형태를 모두 찾음
        # 설명: !\[ (대괄호 시작) ... \] (대괄호 끝) \( (소괄호 시작) ... \) (소괄호 끝)
        img_pattern = re.compile(r'!\[.*?\]\(.*?\)')

        counter = [1]
        replaced_count = [0]

        def replace_func(match):
            # 새로운 ID 생성
            new_id = f"{prefix}{counter[0]:0{padding}d}"
            counter[0] += 1
            replaced_count[0] += 1
            
            # 초기화된 태그 반환
            return f"[이미지 삽입: {new_id}]"

        # 일괄 치환 실행
        output_text = img_pattern.sub(replace_func, input_text)

        # 결과 출력
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, output_text)

        # 상태 업데이트
        count = replaced_count[0]
        if count > 0:
            self.lbl_status.config(text=f"✅ 작업 완료: 총 {count}개의 이미지 링크가 초기화되었습니다.", fg="green")
        else:
            self.lbl_status.config(text="⚠️ 알림: 변환할 이미지 태그( ![...](...) )를 찾지 못했습니다.", fg="orange")

    # --- [클립보드 복사 로직] ---
    def copy_to_clipboard(self):
        output_text = self.txt_output.get("1.0", tk.END).strip()
        if output_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(output_text)
            self.root.update() # 클립보드에 확실히 남도록 업데이트
            messagebox.showinfo("복사 완료", "초기화된 마크다운 텍스트가 클립보드에 복사되었습니다.\n원하는 곳에 붙여넣기(Ctrl+V) 하세요.")
        else:
            messagebox.showwarning("경고", "복사할 결과물이 없습니다.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkdownImageResetGUI(root)
    root.mainloop()