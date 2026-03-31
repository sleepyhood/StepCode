import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import os
import opendataloader_pdf


class OpenDataLoaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF ➔ Markdown/JSON 자동 추출기 (OpenDataLoader)")
        self.root.geometry("600x550")

        self.input_files = []
        self.output_dir = tk.StringVar()

        # --- [1. 입력 파일 설정 영역] ---
        frame_input = tk.LabelFrame(
            root, text="1. 대상 PDF 파일 선택 (일괄 변환 권장)", padx=10, pady=10
        )
        frame_input.pack(fill=tk.X, padx=15, pady=10)

        # 리스트 박스 (선택된 파일 목록 표시)
        self.listbox_files = tk.Listbox(frame_input, height=5, selectmode=tk.EXTENDED)
        self.listbox_files.pack(fill=tk.X, side=tk.TOP, pady=(0, 5))

        # 버튼 그룹
        btn_frame = tk.Frame(frame_input)
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text="+ PDF 파일 추가", command=self.add_files).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(btn_frame, text="+ 폴더 단위 추가", command=self.add_folder).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(btn_frame, text="- 선택 삭제", command=self.remove_selected).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(btn_frame, text="초기화", command=self.clear_files).pack(
            side=tk.RIGHT, padx=2
        )

        # --- [2. 출력 폴더 설정 영역] ---
        frame_output = tk.LabelFrame(root, text="2. 결과물 저장 폴더", padx=10, pady=10)
        frame_output.pack(fill=tk.X, padx=15, pady=5)

        tk.Entry(
            frame_output, textvariable=self.output_dir, state="readonly", width=50
        ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Button(frame_output, text="경로 지정", command=self.select_output_dir).pack(
            side=tk.RIGHT
        )

        # --- [3. 추출 포맷 설정 영역] ---
        frame_format = tk.LabelFrame(root, text="3. 추출 포맷", padx=10, pady=10)
        frame_format.pack(fill=tk.X, padx=15, pady=5)

        self.var_md = tk.BooleanVar(value=True)
        self.var_json = tk.BooleanVar(value=True)
        tk.Checkbutton(frame_format, text="Markdown (.md)", variable=self.var_md).pack(
            side=tk.LEFT, padx=10
        )
        tk.Checkbutton(frame_format, text="JSON (.json)", variable=self.var_json).pack(
            side=tk.LEFT, padx=10
        )

        # --- [4. 실행 및 로그 영역] ---
        self.btn_run = tk.Button(
            root,
            text="일괄 추출 시작 (Batch Convert)",
            command=self.start_conversion,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            pady=10,
        )
        self.btn_run.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(root, text="작업 로그:").pack(anchor=tk.W, padx=15)
        self.log_area = scrolledtext.ScrolledText(
            root, height=8, bg="#f4f4f4", state=tk.DISABLED
        )
        self.log_area.pack(fill=tk.BOTH, padx=15, pady=(0, 15), expand=True)

    # --- [UI 기능 함수] ---
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="PDF 파일 선택", filetypes=[("PDF Files", "*.pdf")]
        )
        for f in files:
            if f not in self.input_files:
                self.input_files.append(f)
                self.listbox_files.insert(tk.END, os.path.basename(f))
        self.log(f"{len(files)}개 파일 추가됨.")

    def add_folder(self):
        folder = filedialog.askdirectory(title="PDF가 있는 폴더 선택")
        if folder:
            count = 0
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(".pdf"):
                        full_path = os.path.join(root, file).replace("\\", "/")
                        if full_path not in self.input_files:
                            self.input_files.append(full_path)
                            self.listbox_files.insert(tk.END, file)
                            count += 1
            self.log(f"폴더에서 {count}개의 PDF 파일을 찾아 추가했습니다.")

    def remove_selected(self):
        selected_indices = self.listbox_files.curselection()
        for i in reversed(selected_indices):  # 뒤에서부터 지워야 인덱스가 꼬이지 않음
            del self.input_files[i]
            self.listbox_files.delete(i)

    def clear_files(self):
        self.input_files.clear()
        self.listbox_files.delete(0, tk.END)
        self.log("파일 목록 초기화 됨.")

    def select_output_dir(self):
        folder = filedialog.askdirectory(title="저장할 폴더 선택")
        if folder:
            self.output_dir.set(folder)
            self.log(f"저장 폴더 설정: {folder}")

    def log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)  # 자동 스크롤
        self.log_area.config(state=tk.DISABLED)

    # --- [변환 실행 로직 (스레드 사용)] ---
    def start_conversion(self):
        if not self.input_files:
            messagebox.showwarning("경고", "변환할 PDF 파일을 추가해 주세요.")
            return
        if not self.output_dir.get():
            messagebox.showwarning("경고", "결과물을 저장할 폴더를 지정해 주세요.")
            return

        formats = []
        if self.var_md.get():
            formats.append("markdown")
        if self.var_json.get():
            formats.append("json")

        if not formats:
            messagebox.showwarning("경고", "최소 1개 이상의 추출 포맷을 선택하세요.")
            return

        format_str = ",".join(formats)

        # UI 비활성화 (중복 실행 방지)
        self.btn_run.config(
            state=tk.DISABLED, text="변환 중... (시간이 걸릴 수 있습니다)"
        )
        self.log("=== 추출 작업 시작 ===")
        self.log(f"총 {len(self.input_files)}개 파일 Batch 처리 중...")

        # 무거운 변환 작업은 별도의 스레드에서 실행하여 UI 멈춤 방지
        threading.Thread(
            target=self.run_conversion_task,
            args=(self.input_files.copy(), self.output_dir.get(), format_str),
            daemon=True,
        ).start()

    def run_conversion_task(self, inputs, out_dir, fmt):
        try:
            # OpenDataLoader API 호출 (Batch로 한 번에 전달)
            opendataloader_pdf.convert(
                input_path=inputs, output_dir=out_dir, format=fmt
            )
            self.root.after(0, self.conversion_success)  # UI 업데이트는 메인 스레드에서
        except Exception as e:
            self.root.after(0, self.conversion_error, str(e))

    def conversion_success(self):
        self.log("✅ 모든 변환 작업이 완료되었습니다!")
        messagebox.showinfo("완료", "PDF 추출이 성공적으로 완료되었습니다.")
        self.btn_run.config(state=tk.NORMAL, text="일괄 추출 시작 (Batch Convert)")

    def conversion_error(self, err_msg):
        self.log(f"❌ 오류 발생: {err_msg}")
        messagebox.showerror("오류", f"변환 중 문제가 발생했습니다.\n{err_msg}")
        self.btn_run.config(state=tk.NORMAL, text="일괄 추출 시작 (Batch Convert)")


if __name__ == "__main__":
    root = tk.Tk()
    app = OpenDataLoaderGUI(root)
    root.mainloop()
