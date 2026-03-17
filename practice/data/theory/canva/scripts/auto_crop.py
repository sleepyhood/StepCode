import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import numpy as np
import re


class ImageCropperBatchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Image Batch Cropper")
        self.root.geometry("400x400")  # UI 추가로 인해 창 높이를 조금 더 키웠습니다.

        self.file_paths = []
        self.output_dir = ""

        # --- [UI 요소 설정] ---
        # 1. 파일 선택 영역
        self.lbl_info = tk.Label(
            root,
            text="스캔된 이미지 파일들을 선택하세요.\n(드래그 또는 Ctrl/Shift로 다중 선택)",
            pady=10,
        )
        self.lbl_info.pack()

        self.btn_select = tk.Button(
            root, text="이미지 파일(들) 선택", command=self.select_files
        )
        self.btn_select.pack(pady=5)

        # 2. 저장 폴더 선택 영역
        self.lbl_out_dir = tk.Label(
            root, text="결과물이 저장될 단일 폴더를 선택하세요.", pady=10
        )
        self.lbl_out_dir.pack()

        self.btn_select_dir = tk.Button(
            root, text="저장 폴더 선택", command=self.select_output_dir
        )
        self.btn_select_dir.pack(pady=5)

        # 3. 페이지 번호 보정값 설정 영역 (새로 추가된 부분)
        frame_offset = tk.Frame(root)
        frame_offset.pack(pady=10)

        self.lbl_offset = tk.Label(
            frame_offset, text="페이지 번호 차이 (파일명 숫자 - 실제 페이지 번호):"
        )
        self.lbl_offset.pack(side=tk.LEFT, padx=5)

        # 기본값을 -2로 설정. Spinbox를 사용해 위아래 화살표로 쉽게 조절 가능합니다.
        self.page_offset_var = tk.IntVar(value=-2)
        self.spin_offset = tk.Spinbox(
            frame_offset, from_=-50, to=50, textvariable=self.page_offset_var, width=5
        )
        self.spin_offset.pack(side=tk.LEFT)

        # 4. 진행 상황 표시 및 실행 버튼
        self.lbl_status = tk.Label(root, text="대기 중...", fg="blue", pady=10)
        self.lbl_status.pack()

        self.btn_process = tk.Button(
            root,
            text="일괄 자동 크롭 실행",
            command=self.process_images,
            state=tk.DISABLED,
        )
        self.btn_process.pack(pady=10)

    # --- [기능 구현] ---
    def select_files(self):
        self.file_paths = filedialog.askopenfilenames(
            title="이미지 여러 장 선택",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")],
        )
        if self.file_paths:
            self.file_paths = sorted(self.file_paths)
            self.lbl_info.config(text=f"선택됨: 총 {len(self.file_paths)}장의 파일")
            self.check_ready()

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="저장할 단일 폴더 선택")
        if self.output_dir:
            self.lbl_out_dir.config(text=f"저장 위치:\n{self.output_dir}")
            self.check_ready()

    def check_ready(self):
        if self.file_paths and self.output_dir:
            self.btn_process.config(state=tk.NORMAL)
        else:
            self.btn_process.config(state=tk.DISABLED)

    def extract_page_number(self, filename):
        match = re.search(r"(\d+)(?=\.\w+$)", filename)
        if match:
            return match.group(1)
        else:
            return os.path.splitext(filename)[0]

    def process_images(self):
        if not self.file_paths or not self.output_dir:
            return

        self.btn_process.config(state=tk.DISABLED)
        total_files = len(self.file_paths)
        total_crops = 0

        # 사용자가 입력한 보정값을 가져옵니다.
        try:
            offset_value = self.page_offset_var.get()
        except tk.TclError:
            offset_value = 0  # 잘못된 값이 입력되면 0으로 간주

        try:
            for idx, file_path in enumerate(self.file_paths):
                self.lbl_status.config(
                    text=f"처리 중: {idx + 1} / {total_files} 장 진행 중..."
                )
                self.root.update()

                filename = os.path.basename(file_path)
                page_num_str = self.extract_page_number(filename)

                # --- [수정된 부분: 페이지 번호 보정 로직] ---
                if page_num_str.isdigit():
                    actual_page = int(page_num_str) - offset_value
                    if actual_page > 0:
                        # 정상적인 페이지 번호 (예: 059)
                        page_num = f"{actual_page:03d}"
                    else:
                        # 0이나 음수가 될 경우 (목차, 앞표지 등) 원본 번호를 유지하며 '앞부분' 표시
                        page_num = f"앞부분_{int(page_num_str):03d}"
                else:
                    page_num = page_num_str
                # ---------------------------------------------

                img_array = np.fromfile(file_path, np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                if img is None:
                    continue

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
                contours, _ = cv2.findContours(
                    thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )

                min_area = 5000
                valid_rects = []

                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if area > min_area:
                        x, y, w, h = cv2.boundingRect(cnt)

                        # --- [새로 추가할 필터링 로직: 가로세로 비율 검사] ---
                        # 0으로 나누는 오류를 방지하기 위해 max(w, 1), max(h, 1)을 사용합니다.
                        aspect_ratio_h = h / max(
                            w, 1
                        )  # 세로가 가로에 비해 얼마나 긴가?
                        aspect_ratio_w = w / max(
                            h, 1
                        )  # 가로가 세로에 비해 얼마나 긴가?

                        # 가로나 세로 중 한쪽이 다른 쪽보다 5배 이상 길면(즉, 얇은 선이면) 무시하고 넘어갑니다.
                        limit_ratio = 6.0
                        if aspect_ratio_h > limit_ratio or aspect_ratio_w > limit_ratio:
                            continue  # 저장하지 않고 다음 윤곽선으로 넘어감
                        # -----------------------------------------------------

                        valid_rects.append((x, y, w, h))

                valid_rects.sort(key=lambda rect: (rect[1] // 50, rect[0]))

                for crop_idx, (x, y, w, h) in enumerate(valid_rects):
                    pad = 5
                    y1, y2 = max(0, y - pad), min(img.shape[0], y + h + pad)
                    x1, x2 = max(0, x - pad), min(img.shape[1], x + w + pad)

                    cropped = img[y1:y2, x1:x2]

                    save_name = f"p{page_num}_{crop_idx + 1:02d}.png"
                    save_path = os.path.join(self.output_dir, save_name)

                    is_success, im_buf_arr = cv2.imencode(".png", cropped)
                    if is_success:
                        im_buf_arr.tofile(save_path)
                        total_crops += 1

            self.lbl_status.config(text="모든 작업이 완료되었습니다!")
            messagebox.showinfo(
                "일괄 처리 완료",
                f"총 {total_files}장의 원본을 분석하여\n{total_crops}개의 이미지를 추출했습니다!\n\n저장 위치: {self.output_dir}",
            )

        except Exception as e:
            messagebox.showerror("오류", f"작업 중 문제가 발생했습니다:\n{str(e)}")
            self.lbl_status.config(text="오류 발생으로 중단됨")
        finally:
            self.btn_process.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropperBatchGUI(root)
    root.mainloop()
