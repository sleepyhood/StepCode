import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import re


class MarkdownAssemblerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("마크다운 이미지 최종 조립기 (Assembler)")
        self.root.geometry("500x400")

        self.md_path = ""
        self.json_path = ""
        self.output_folder = ""

        # --- [UI 설정] ---
        tk.Label(
            root,
            text="마크다운 이미지 자동 조립 도구",
            font=("Arial", 14, "bold"),
            pady=15,
        ).pack()

        # 1. 마크다운 파일 선택 (01_LLM_서식_정리 폴더 내 파일)
        frame_md = tk.Frame(root)
        frame_md.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(frame_md, text="대상 마크다운:").pack(side=tk.LEFT)
        self.lbl_md = tk.Label(
            frame_md, text="파일을 선택하세요...", fg="gray", width=30, anchor="e"
        )
        self.lbl_md.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_md, text="찾기", command=self.select_md).pack(side=tk.RIGHT)

        # 2. JSON 매핑 파일 선택 (images 폴더 내 03_mapping.json)
        frame_json = tk.Frame(root)
        frame_json.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(frame_json, text="매핑 JSON:").pack(side=tk.LEFT)
        self.lbl_json = tk.Label(
            frame_json, text="파일을 선택하세요...", fg="gray", width=30, anchor="e"
        )
        self.lbl_json.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_json, text="찾기", command=self.select_json).pack(side=tk.RIGHT)

        # 3. 저장될 폴더 선택 (02_이미지_추가 폴더)
        frame_out = tk.Frame(root)
        frame_out.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(frame_out, text="저장 폴더:").pack(side=tk.LEFT)
        self.lbl_out = tk.Label(
            frame_out, text="폴더를 선택하세요...", fg="gray", width=30, anchor="e"
        )
        self.lbl_out.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_out, text="찾기", command=self.select_output).pack(
            side=tk.RIGHT
        )

        # 4. 실행 버튼
        self.btn_run = tk.Button(
            root,
            text="이미지 결합 및 저장 시작",
            command=self.run_assembly,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            pady=10,
            state=tk.DISABLED,
        )
        self.btn_run.pack(pady=30)

        self.lbl_status = tk.Label(root, text="준비됨", fg="blue")
        self.lbl_status.pack()

    # --- [파일 선택 기능] ---
    def select_md(self):
        self.md_path = filedialog.askopenfilename(
            title="마크다운 파일 선택", filetypes=[("Markdown Files", "*.md")]
        )
        if self.md_path:
            self.lbl_md.config(text=os.path.basename(self.md_path), fg="black")
            self.check_ready()

    def select_json(self):
        self.json_path = filedialog.askopenfilename(
            title="JSON 매핑 파일 선택", filetypes=[("JSON Files", "*.json")]
        )
        if self.json_path:
            self.lbl_json.config(text=os.path.basename(self.json_path), fg="black")
            self.check_ready()

    def select_output(self):
        self.output_folder = filedialog.askdirectory(title="결과물 저장 폴더 선택")
        if self.output_folder:
            self.lbl_out.config(text=os.path.basename(self.output_folder), fg="black")
            self.check_ready()

    def check_ready(self):
        if self.md_path and self.json_path and self.output_folder:
            self.btn_run.config(state=tk.NORMAL)

    # --- [핵심 조립 로직] ---
    def run_assembly(self):
        try:
            # 1. JSON 데이터 로드
            with open(self.json_path, "r", encoding="utf-8") as f:
                mapping_data = json.load(f)

            # 2. 마크다운 파일 읽기
            with open(self.md_path, "r", encoding="utf-8") as f:
                md_content = f.read()

            # 3. 정규표현식으로 이미지 태그 치환
            # 패턴: [이미지 삽입: ID_XXXX]
            def replace_image(match):
                img_id = match.group(1).strip()
                if img_id in mapping_data:
                    info = mapping_data[img_id]
                    file_name = info.get("file_name", "")
                    alt_text = info.get("alt_text", "이미지 설명")
                    # 이미지 경로 설정 (선생님의 구조에 맞게 images/ 경로 추가)
                    return f"![{alt_text}](../images/{file_name})"
                else:
                    # 매핑 데이터가 없는 경우 원본 유지 또는 경고 표시
                    return match.group(0)

            # [이미지 삽입: ] 내부의 ID를 캡처하는 정규식
            final_content = re.sub(
                r"\[이미지 삽입:\s*([^\]]+)\]", replace_image, md_content
            )

            # 4. 파일 저장
            save_name = os.path.basename(self.md_path)
            save_path = os.path.join(self.output_folder, save_name)

            with open(save_path, "w", encoding="utf-8") as f:
                f.write(final_content)

            messagebox.showinfo(
                "성공", f"최종 마크다운이 생성되었습니다!\n경로: {save_path}"
            )
            self.lbl_status.config(text="작업 완료!", fg="green")

        except Exception as e:
            messagebox.showerror("오류", f"작업 중 문제가 발생했습니다:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MarkdownAssemblerGUI(root)
    root.mainloop()
