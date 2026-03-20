from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import mss
import pyautogui
from PIL import Image, ImageOps
from pynput import keyboard


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05


@dataclass
class CaptureRegion:
    left: int
    top: int
    width: int
    height: int

    @property
    def center(self) -> tuple[int, int]:
        return (self.left + self.width // 2, self.top + self.height // 2)

    def as_mss(self) -> dict[str, int]:
        return {
            "left": self.left,
            "top": self.top,
            "width": self.width,
            "height": self.height,
        }


class RegionSelector(tk.Toplevel):
    def __init__(self, master: tk.Tk, on_selected):
        super().__init__(master)
        self.on_selected = on_selected
        self.start_x = 0
        self.start_y = 0
        self.rect_id = None

        self.attributes("-fullscreen", True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.25)
        self.configure(bg="black")
        self.title("캡쳐 영역 선택")

        self.canvas = tk.Canvas(self, cursor="cross", bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.hint = self.canvas.create_text(
            24,
            24,
            anchor="nw",
            fill="white",
            font=("Malgun Gothic", 18, "bold"),
            text="PDF 페이지 영역만 드래그하세요. ESC: 취소",
        )

        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Escape>", lambda _event: self.destroy())
        self.focus_force()

    def _on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="#00e5ff",
            width=3,
        )

    def _on_drag(self, event):
        if self.rect_id:
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def _on_release(self, event):
        left = min(self.start_x, event.x)
        top = min(self.start_y, event.y)
        right = max(self.start_x, event.x)
        bottom = max(self.start_y, event.y)

        if right - left < 50 or bottom - top < 50:
            messagebox.showwarning("영역 선택", "영역이 너무 작습니다. 다시 선택하세요.", parent=self)
            return

        self.on_selected(CaptureRegion(left, top, right - left, bottom - top))
        self.destroy()


class PdfCaptureApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PDF 페이지 캡쳐 도구")
        self.root.geometry("650x1300")
        self.root.resizable(False, False)

        self.capture_region: CaptureRegion | None = None
        self.stop_requested = False
        self.is_running = False
        self.hotkey_listener: keyboard.Listener | None = None

        self.output_dir_var = tk.StringVar(value=str(Path.cwd() / "output" / "pdf_capture"))
        self.file_prefix_var = tk.StringVar(value="page")
        self.start_page_var = tk.IntVar(value=1)
        self.capture_count_var = tk.IntVar(value=10)
        self.start_delay_var = tk.DoubleVar(value=3.0)
        self.page_turn_delay_var = tk.DoubleVar(value=1.2)
        self.post_key_delay_var = tk.DoubleVar(value=1.0)
        self.turn_key_var = tk.StringVar(value="right")
        self.click_to_focus_var = tk.BooleanVar(value=True)
        self.trim_edges_var = tk.BooleanVar(value=True)
        self.trim_top_bottom_var = tk.BooleanVar(value=False)
        self.bg_threshold_var = tk.IntVar(value=18)
        self.edge_margin_var = tk.IntVar(value=4)
        self.status_var = tk.StringVar(value="영역을 선택한 뒤 캡쳐를 시작하세요.")
        self.region_var = tk.StringVar(value="미선택")

        self._build_ui()
        self._start_hotkey_listener()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="웹 PDF 페이지 캡쳐", font=("Malgun Gothic", 16, "bold")).pack(anchor="w")
        ttk.Label(
            container,
            text="PDF가 열린 브라우저를 띄운 상태에서 페이지 영역만 지정하면 됩니다.",
            foreground="#555555",
        ).pack(anchor="w", pady=(2, 14))

        region_box = ttk.LabelFrame(container, text="1. 캡쳐 영역")
        region_box.pack(fill="x", pady=(0, 10))
        ttk.Button(region_box, text="영역 선택", command=self.select_region).pack(anchor="w", padx=12, pady=(10, 6))
        ttk.Label(region_box, textvariable=self.region_var).pack(anchor="w", padx=12, pady=(0, 10))

        output_box = ttk.LabelFrame(container, text="2. 저장 설정")
        output_box.pack(fill="x", pady=(0, 10))
        self._labeled_entry(output_box, "저장 폴더", self.output_dir_var, browse=self.choose_output_dir)
        self._labeled_entry(output_box, "파일 접두사", self.file_prefix_var)

        options_box = ttk.LabelFrame(container, text="3. 캡쳐 옵션")
        options_box.pack(fill="x", pady=(0, 10))
        self._labeled_spinbox(options_box, "시작 페이지 번호", self.start_page_var, 1, 999999, 1)
        self._labeled_spinbox(options_box, "캡쳐 장수", self.capture_count_var, 1, 999999, 1)
        self._labeled_spinbox(options_box, "시작 전 대기(초)", self.start_delay_var, 0, 30, 0.5)
        self._labeled_spinbox(options_box, "페이지 넘김 전 대기(초)", self.page_turn_delay_var, 0, 10, 0.1)
        self._labeled_spinbox(options_box, "우측키 후 대기(초)", self.post_key_delay_var, 0, 10, 0.1)
        self._labeled_combobox(
            options_box,
            "페이지 넘김 키",
            self.turn_key_var,
            ("right", "pagedown", "space"),
        )

        trim_box = ttk.LabelFrame(container, text="4. 여백 보정")
        trim_box.pack(fill="x", pady=(0, 10))
        ttk.Checkbutton(trim_box, text="가장자리 배경색 기준 자동 트리밍", variable=self.trim_edges_var).pack(
            anchor="w", padx=12, pady=(10, 4)
        )
        ttk.Checkbutton(trim_box, text="상하 여백도 같이 트리밍", variable=self.trim_top_bottom_var).pack(
            anchor="w", padx=12, pady=4
        )
        ttk.Checkbutton(trim_box, text="캡쳐 전 브라우저 영역 클릭해서 포커스 확보", variable=self.click_to_focus_var).pack(
            anchor="w", padx=12, pady=4
        )
        self._labeled_spinbox(trim_box, "배경 허용 오차", self.bg_threshold_var, 1, 80, 1)
        self._labeled_spinbox(trim_box, "안전 여백(px)", self.edge_margin_var, 0, 30, 1)

        action_row = ttk.Frame(container)
        action_row.pack(fill="x", pady=(6, 8))
        ttk.Button(action_row, text="테스트 캡쳐 1장", command=self.capture_test).pack(side="left")
        ttk.Button(action_row, text="캡쳐 시작", command=self.start_capture).pack(side="left", padx=8)
        ttk.Button(action_row, text="중지 요청", command=self.request_stop).pack(side="left")

        ttk.Label(container, text="중지는 F8 키로도 가능합니다.", foreground="#555555").pack(anchor="w")
        ttk.Label(container, textvariable=self.status_var, wraplength=520, foreground="#003366").pack(
            anchor="w", pady=(8, 0)
        )

    def _labeled_entry(self, parent, label: str, variable: tk.StringVar, browse=None):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=12, pady=6)
        ttk.Label(frame, text=label, width=14).pack(side="left")
        ttk.Entry(frame, textvariable=variable).pack(side="left", fill="x", expand=True)
        if browse:
            ttk.Button(frame, text="찾기", command=browse).pack(side="left", padx=(6, 0))

    def _labeled_spinbox(self, parent, label: str, variable, minimum, maximum, increment):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=12, pady=4)
        ttk.Label(frame, text=label, width=18).pack(side="left")
        ttk.Spinbox(
            frame,
            textvariable=variable,
            from_=minimum,
            to=maximum,
            increment=increment,
            width=10,
        ).pack(side="left")

    def _labeled_combobox(self, parent, label: str, variable: tk.StringVar, values: tuple[str, ...]):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=12, pady=4)
        ttk.Label(frame, text=label, width=18).pack(side="left")
        combo = ttk.Combobox(frame, textvariable=variable, values=values, state="readonly", width=12)
        combo.pack(side="left")

    def _start_hotkey_listener(self):
        def on_press(key):
            if key == keyboard.Key.f8:
                self.request_stop(from_hotkey=True)

        self.hotkey_listener = keyboard.Listener(on_press=on_press)
        self.hotkey_listener.daemon = True
        self.hotkey_listener.start()

    def _set_status(self, message: str):
        self.root.after(0, lambda: self.status_var.set(message))

    def _on_close(self):
        if self.is_running:
            if not messagebox.askyesno("종료", "캡쳐 중입니다. 종료하시겠습니까?"):
                return
            self.stop_requested = True
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        self.root.destroy()

    def choose_output_dir(self):
        selected = filedialog.askdirectory(initialdir=self.output_dir_var.get() or str(Path.cwd()))
        if selected:
            self.output_dir_var.set(selected)

    def select_region(self):
        self.root.withdraw()

        def handle_region(region: CaptureRegion):
            self.capture_region = region
            self.region_var.set(
                f"left={region.left}, top={region.top}, width={region.width}, height={region.height}"
            )
            self._set_status("캡쳐 영역이 설정되었습니다.")
            self.root.deiconify()
            self.root.lift()

        selector = RegionSelector(self.root, handle_region)

        def restore_on_close():
            self.root.deiconify()
            self.root.lift()

        selector.bind("<Destroy>", lambda _event: restore_on_close())

    def request_stop(self, from_hotkey: bool = False):
        self.stop_requested = True
        if from_hotkey:
            self._set_status("F8 중지 요청이 들어왔습니다. 현재 작업 후 멈춥니다.")
        else:
            self._set_status("중지 요청이 들어왔습니다. 현재 작업 후 멈춥니다.")

    def _validate(self) -> bool:
        if not self.capture_region:
            messagebox.showwarning("캡쳐 영역", "먼저 캡쳐 영역을 선택하세요.")
            return False
        if self.capture_count_var.get() <= 0:
            messagebox.showwarning("캡쳐 장수", "캡쳐 장수는 1 이상이어야 합니다.")
            return False
        if self.start_page_var.get() <= 0:
            messagebox.showwarning("시작 페이지", "시작 페이지 번호는 1 이상이어야 합니다.")
            return False
        output_dir = Path(self.output_dir_var.get()).expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)
        return True

    def capture_test(self):
        if not self._validate():
            return
        try:
            image = self._grab_region()
            output_dir = Path(self.output_dir_var.get()).expanduser()
            test_path = output_dir / f"{self.file_prefix_var.get()}_test.png"
            image.save(test_path)
            self._set_status(f"테스트 캡쳐 저장 완료: {test_path}")
            messagebox.showinfo("테스트 캡쳐", f"테스트 이미지를 저장했습니다.\n{test_path}")
        except Exception as exc:
            messagebox.showerror("테스트 실패", str(exc))

    def start_capture(self):
        if self.is_running:
            messagebox.showinfo("캡쳐 중", "이미 캡쳐가 진행 중입니다.")
            return
        if not self._validate():
            return

        self.stop_requested = False
        self.is_running = True
        self.root.iconify()
        thread = threading.Thread(target=self._capture_worker, daemon=True)
        thread.start()

    def _capture_worker(self):
        try:
            output_dir = Path(self.output_dir_var.get()).expanduser()
            prefix = self.file_prefix_var.get().strip() or "page"
            start_page = self.start_page_var.get()
            total = self.capture_count_var.get()
            start_delay = float(self.start_delay_var.get())
            page_turn_delay = float(self.page_turn_delay_var.get())
            post_key_delay = float(self.post_key_delay_var.get())
            turn_key = self.turn_key_var.get().strip() or "right"
            saved_count = 0

            self._set_status(
                f"{start_delay:.1f}초 후 캡쳐를 시작합니다. 브라우저 PDF 화면이 맨 앞으로 오도록 준비하세요."
            )
            time.sleep(max(0.0, start_delay))

            for index in range(total):
                if self.stop_requested:
                    break

                page_no = start_page + index
                self._set_status(f"{page_no}페이지 캡쳐 중...")
                image = self._grab_region()
                save_path = output_dir / f"{prefix}_{page_no:04d}.png"
                image.save(save_path)
                saved_count += 1

                if index == total - 1 or self.stop_requested:
                    continue

                time.sleep(max(0.0, page_turn_delay))
                self._send_page_turn_key(turn_key)
                time.sleep(max(0.0, post_key_delay))

            if self.stop_requested:
                self._set_status(f"중지 요청으로 캡쳐를 종료했습니다. 저장 장수: {saved_count}")
            else:
                self._set_status(f"캡쳐 완료. {saved_count}장을 저장했습니다: {output_dir}")
        except Exception as exc:
            self._set_status(f"오류 발생: {exc}")
            self.root.after(0, lambda: messagebox.showerror("캡쳐 오류", str(exc)))
        finally:
            self.is_running = False
            self.stop_requested = False
            self.root.after(0, self._restore_window)

    def _focus_pdf_viewer(self):
        if self.click_to_focus_var.get() and self.capture_region:
            x, y = self.capture_region.center
            pyautogui.click(x, y)

    def _send_page_turn_key(self, key_name: str):
        self._focus_pdf_viewer()
        time.sleep(0.1)
        pyautogui.press(key_name)

    def _restore_window(self):
        self.root.deiconify()
        self.root.lift()

    def _grab_region(self) -> Image.Image:
        if not self.capture_region:
            raise RuntimeError("캡쳐 영역이 설정되지 않았습니다.")

        self._focus_pdf_viewer()
        with mss.mss() as sct:
            shot = sct.grab(self.capture_region.as_mss())
        image = Image.frombytes("RGB", shot.size, shot.rgb)

        if self.trim_edges_var.get():
            image = self._trim_background_edges(
                image,
                threshold=int(self.bg_threshold_var.get()),
                trim_vertical=bool(self.trim_top_bottom_var.get()),
                safety_margin=int(self.edge_margin_var.get()),
            )

        return image

    def _trim_background_edges(
        self,
        image: Image.Image,
        threshold: int,
        trim_vertical: bool,
        safety_margin: int,
    ) -> Image.Image:
        rgb = image.convert("RGB")
        width, height = rgb.size
        pixels = rgb.load()

        def avg_color(points):
            count = max(1, len(points))
            return tuple(sum(channel[i] for channel in points) // count for i in range(3))

        left_sample = [pixels[min(2, width - 1), y] for y in range(height)]
        right_sample = [pixels[max(0, width - 3), y] for y in range(height)]
        top_sample = [pixels[x, min(2, height - 1)] for x in range(width)]
        bottom_sample = [pixels[x, max(0, height - 3)] for x in range(width)]

        left_bg = avg_color(left_sample)
        right_bg = avg_color(right_sample)
        top_bg = avg_color(top_sample)
        bottom_bg = avg_color(bottom_sample)

        def color_distance(c1, c2):
            return sum(abs(a - b) for a, b in zip(c1, c2)) // 3

        def column_is_background(x: int, bg_color) -> bool:
            matches = 0
            for y in range(height):
                if color_distance(pixels[x, y], bg_color) <= threshold:
                    matches += 1
            return matches / height >= 0.97

        def row_is_background(y: int, bg_color) -> bool:
            matches = 0
            for x in range(width):
                if color_distance(pixels[x, y], bg_color) <= threshold:
                    matches += 1
            return matches / width >= 0.97

        left = 0
        while left < width - 1 and column_is_background(left, left_bg):
            left += 1

        right = width - 1
        while right > 0 and column_is_background(right, right_bg):
            right -= 1

        top = 0
        bottom = height - 1
        if trim_vertical:
            while top < height - 1 and row_is_background(top, top_bg):
                top += 1
            while bottom > 0 and row_is_background(bottom, bottom_bg):
                bottom -= 1

        left = max(0, left - safety_margin)
        right = min(width - 1, right + safety_margin)
        top = max(0, top - safety_margin)
        bottom = min(height - 1, bottom + safety_margin)

        if left >= right or top >= bottom:
            return image

        cropped = rgb.crop((left, top, right + 1, bottom + 1))

        # Keep final image orientation and mode predictable for PNG output.
        return ImageOps.exif_transpose(cropped)


def main():
    root = tk.Tk()
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")
    app = PdfCaptureApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
