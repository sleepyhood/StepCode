import tkinter as tk
from tkinter import scrolledtext, messagebox
import re


class MarkdownIDAssignerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("마크다운 이미지 ID 자동 부여기")
        self.root.geometry("800x600")

        # --- [1. 상단 설정 영역] ---
        frame_settings = tk.Frame(root, pady=10)
        frame_settings.pack(fill=tk.X, padx=10)

        # 찾을 문자열
        tk.Label(frame_settings, text="찾을 문자열:").pack(side=tk.LEFT)
        self.target_var = tk.StringVar(value="[이미지 삽입]")
        tk.Entry(frame_settings, textvariable=self.target_var, width=15).pack(
            side=tk.LEFT, padx=5
        )

        # ID 접두사
        tk.Label(frame_settings, text="ID 접두사:").pack(side=tk.LEFT, padx=(15, 0))
        self.prefix_var = tk.StringVar(value="IMG_")
        tk.Entry(frame_settings, textvariable=self.prefix_var, width=10).pack(
            side=tk.LEFT, padx=5
        )

        # 숫자 자릿수 (예: 2로 설정하면 01, 02 / 3으로 설정하면 001, 002)
        tk.Label(frame_settings, text="숫자 자릿수:").pack(side=tk.LEFT, padx=(15, 0))
        self.padding_var = tk.IntVar(value=2)
        tk.Spinbox(
            frame_settings, from_=1, to=5, textvariable=self.padding_var, width=5
        ).pack(side=tk.LEFT, padx=5)

        # 실행 버튼
        self.btn_process = tk.Button(
            frame_settings,
            text="ID 자동 부여 실행",
            command=self.process_text,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
        )
        self.btn_process.pack(side=tk.RIGHT, padx=10)

        # --- [2. 중간 텍스트 입출력 영역] ---
        frame_text = tk.Frame(root)
        frame_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 왼쪽: 원본 입력창
        frame_input = tk.Frame(frame_text)
        frame_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        tk.Label(frame_input, text="원본 마크다운 입력").pack(anchor=tk.W)
        self.txt_input = scrolledtext.ScrolledText(frame_input, wrap=tk.WORD)
        self.txt_input.pack(fill=tk.BOTH, expand=True)

        # 오른쪽: 결과 출력창 (회색 배경으로 구분)
        frame_output = tk.Frame(frame_text)
        frame_output.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        tk.Label(frame_output, text="변환된 마크다운 결과").pack(anchor=tk.W)
        self.txt_output = scrolledtext.ScrolledText(
            frame_output, wrap=tk.WORD, bg="#f4f4f4"
        )
        self.txt_output.pack(fill=tk.BOTH, expand=True)

        # --- [3. 하단 상태 표시 영역] ---
        self.lbl_status = tk.Label(
            root,
            text="대기 중... 마크다운 텍스트를 붙여넣고 실행 버튼을 눌러주세요.",
            fg="blue",
            pady=10,
        )
        self.lbl_status.pack()

    # --- [기능 구현] ---
    def process_text(self):
        input_text = self.txt_input.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("경고", "마크다운 텍스트를 입력해 주세요.")
            return

        target_str = self.target_var.get()
        prefix = self.prefix_var.get()

        try:
            padding = self.padding_var.get()
        except tk.TclError:
            padding = 2  # 잘못된 값이 들어가면 기본값 2로 설정

        if not target_str:
            messagebox.showwarning("경고", "찾을 문자열을 지정해 주세요.")
            return

        # 정규표현식 패턴 생성 (특수문자 안전하게 이스케이프 처리)
        pattern = re.compile(re.escape(target_str))

        counter = [1]
        generated_ids = []

        def replace_func(match):
            # 사용자가 설정한 접두사와 자릿수로 ID 생성 (예: IMG_01)
            current_id = f"{prefix}{counter[0]:0{padding}d}"
            generated_ids.append(current_id)
            counter[0] += 1

            # [이미지 삽입] 처럼 대괄호로 끝나는 문자열이라면 깔끔하게 합쳐줍니다.
            # 결과: [이미지 삽입: IMG_01]
            if target_str.endswith("]"):
                return target_str[:-1] + f": {current_id}]"
            else:
                return f"{target_str} ({current_id})"

        # 텍스트 일괄 치환
        output_text = pattern.sub(replace_func, input_text)

        # 오른쪽 창에 결과 출력
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, output_text)

        # 상태 업데이트
        count = len(generated_ids)
        self.lbl_status.config(
            text=f"✅ 작업 완료: 총 {count}개의 ID({prefix}{1:0{padding}d} ~ {prefix}{count:0{padding}d})가 부여되었습니다."
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = MarkdownIDAssignerGUI(root)
    root.mainloop()
