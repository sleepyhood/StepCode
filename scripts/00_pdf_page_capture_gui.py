from __future__ import annotations

import random
import threading
import time
from dataclasses import dataclass
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import cv2
import mss
import numpy as np
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


@dataclass
class CaptureJobConfig:
    output_dir: Path
    prefix: str
    start_page: int
    total: int
    start_delay: float
    page_turn_delay: float
    post_key_delay: float
    turn_key: str
    next_click_x_offset: int
    next_click_y_offset: int
    page_turn_delay_extra_min: float
    page_turn_delay_extra_max: float
    post_key_delay_extra_min: float
    post_key_delay_extra_max: float
    next_click_x_jitter: int
    next_click_y_jitter: int


@dataclass
class DetectionDebugInfo:
    bright_candidates: int
    edge_candidates: int
    accepted_candidates: int
    rejection_counts: dict[str, int]
    best_score: float | None = None
    candidate_details: list["CandidateDebugRecord"] | None = None

    def failure_summary(self) -> str:
        if self.accepted_candidates > 0:
            return "후보는 있었지만 최종 선택 단계에서 문제가 발생했습니다."

        if self.bright_candidates == 0 and self.edge_candidates == 0:
            return "페이지처럼 보이는 밝은 영역이나 외곽선을 찾지 못했습니다."

        reasons = []
        labels = {
            "too_small": "후보 영역이 너무 작았습니다",
            "bad_aspect": "페이지 비율과 너무 달랐습니다",
            "bad_area_ratio": "화면 대비 너무 크거나 작았습니다",
        }
        for key in ("too_small", "bad_aspect", "bad_area_ratio"):
            count = self.rejection_counts.get(key, 0)
            if count:
                reasons.append(f"{labels[key]}({count}개)")

        if reasons:
            return "감지 후보가 있었지만 " + ", ".join(reasons) + "."

        return "감지 후보 점수가 충분하지 않았습니다."


@dataclass
class CandidateDebugRecord:
    source: str
    rect: tuple[int, int, int, int]
    accepted: bool
    reason: str
    score: float | None = None

    def sort_key(self) -> tuple[int, float]:
        return (
            0 if self.accepted else 1,
            -(self.score if self.score is not None else 0.0),
        )


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
            self.canvas.coords(
                self.rect_id, self.start_x, self.start_y, event.x, event.y
            )

    def _on_release(self, event):
        left = min(self.start_x, event.x)
        top = min(self.start_y, event.y)
        right = max(self.start_x, event.x)
        bottom = max(self.start_y, event.y)

        if right - left < 50 or bottom - top < 50:
            messagebox.showwarning(
                "영역 선택", "영역이 너무 작습니다. 다시 선택하세요.", parent=self
            )
            return

        self.on_selected(CaptureRegion(left, top, right - left, bottom - top))
        self.destroy()


class RegionConfirmDialog(tk.Toplevel):
    def __init__(
        self,
        master: tk.Tk,
        screenshot: Image.Image,
        detected_region: CaptureRegion,
        on_confirm,
    ):
        super().__init__(master)
        self.on_confirm = on_confirm
        self.detected_region = detected_region
        self.title("자동 감지 결과 확인")
        self.attributes("-topmost", True)
        self.configure(bg="white")

        preview = screenshot.copy()
        draw = np.array(preview)
        x1 = detected_region.left
        y1 = detected_region.top
        x2 = detected_region.left + detected_region.width
        y2 = detected_region.top + detected_region.height
        cv2.rectangle(draw, (x1, y1), (x2, y2), (0, 229, 255), 4)
        cv2.putText(
            draw,
            "Detected region",
            (x1, max(30, y1 - 12)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 229, 255),
            2,
            cv2.LINE_AA,
        )
        preview = Image.fromarray(draw)

        max_width = 1100
        max_height = 760
        scale = min(max_width / preview.width, max_height / preview.height, 1.0)
        shown = preview.resize(
            (int(preview.width * scale), int(preview.height * scale)),
            Image.Resampling.LANCZOS,
        )
        self.preview_photo = tk.PhotoImage(data=self._to_png_bytes_base64(shown))

        ttk.Label(
            self,
            text="자동 감지된 영역입니다. 맞으면 사용, 아니면 수동 선택으로 다시 지정하세요.",
            padding=(12, 12, 12, 8),
        ).pack(anchor="w")
        ttk.Label(self, image=self.preview_photo).pack(padx=12, pady=4)

        button_row = ttk.Frame(self, padding=(12, 8, 12, 12))
        button_row.pack(fill="x")
        ttk.Button(button_row, text="이 영역 사용", command=self._confirm).pack(
            side="left"
        )
        ttk.Button(button_row, text="수동 선택", command=self._fallback_manual).pack(
            side="left", padx=(8, 0)
        )
        ttk.Button(button_row, text="취소", command=self.destroy).pack(side="right")

        self.grab_set()
        self.focus_force()

    def _to_png_bytes_base64(self, image: Image.Image) -> bytes:
        import base64
        import io

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue())

    def _confirm(self):
        self.on_confirm(self.detected_region, manual=False)
        self.destroy()

    def _fallback_manual(self):
        self.on_confirm(None, manual=True)
        self.destroy()


class MonitorSelectDialog(tk.Toplevel):
    def __init__(self, master: tk.Tk, monitor_previews: list[tuple[dict, Image.Image]]):
        super().__init__(master)
        self.title("자동 감지할 화면 선택")
        self.attributes("-topmost", True)
        self.configure(bg="white")
        self.selected_monitor: dict | None = None
        self.preview_photos: list[tk.PhotoImage] = []

        ttk.Label(
            self,
            text="자동 감지를 실행할 화면을 스크린샷으로 확인한 뒤 선택하세요.",
            padding=(12, 12, 12, 8),
        ).pack(anchor="w")

        container = ttk.Frame(self, padding=(12, 0, 12, 12))
        container.pack(fill="both", expand=True)

        for index, (monitor, screenshot) in enumerate(monitor_previews, start=1):
            card = ttk.LabelFrame(
                container,
                text=(
                    f"{index}. left={monitor['left']}, top={monitor['top']}, "
                    f"width={monitor['width']}, height={monitor['height']}"
                ),
                padding=8,
            )
            card.pack(fill="x", pady=(0, 10))

            preview = screenshot.copy()
            max_width = 460
            max_height = 260
            scale = min(max_width / preview.width, max_height / preview.height, 1.0)
            shown = preview.resize(
                (
                    max(1, int(preview.width * scale)),
                    max(1, int(preview.height * scale)),
                ),
                Image.Resampling.LANCZOS,
            )
            photo = tk.PhotoImage(data=self._to_png_bytes_base64(shown))
            self.preview_photos.append(photo)

            ttk.Label(card, image=photo).pack(anchor="w")
            ttk.Button(
                card,
                text="이 화면 선택",
                command=lambda selected=monitor: self._select(selected),
            ).pack(anchor="e", pady=(8, 0))

        ttk.Button(self, text="취소", command=self.destroy).pack(
            anchor="e", padx=12, pady=(0, 12)
        )

        self.grab_set()
        self.focus_force()

    def _to_png_bytes_base64(self, image: Image.Image) -> bytes:
        import base64
        import io

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue())

    def _select(self, monitor: dict):
        self.selected_monitor = monitor
        self.destroy()


class PdfCaptureApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PDF 페이지 캡쳐 도구")
        self.root.geometry("700x980")
        self.root.minsize(620, 720)
        self.root.resizable(True, True)

        self.capture_region: CaptureRegion | None = None
        self.stop_requested = False
        self.is_running = False
        self.hotkey_listener: keyboard.Listener | None = None
        self.scroll_canvas: tk.Canvas | None = None
        self.scrollable_frame: ttk.Frame | None = None
        self._scroll_window_id: int | None = None

        self.output_dir_var = tk.StringVar(
            value=str(Path.cwd() / "output" / "pdf_capture")
        )
        self.file_prefix_var = tk.StringVar(value="page")
        self.start_page_var = tk.IntVar(value=1)
        self.capture_count_var = tk.IntVar(value=10)
        self.start_delay_var = tk.DoubleVar(value=3.0)
        self.page_turn_delay_var = tk.DoubleVar(value=1.2)
        self.post_key_delay_var = tk.DoubleVar(value=1.0)
        self.turn_key_var = tk.StringVar(value="next_button_click")
        self.next_click_x_offset_var = tk.IntVar(value=26)
        self.next_click_y_offset_var = tk.IntVar(value=0)
        self.page_turn_delay_extra_min_var = tk.DoubleVar(value=0.0)
        self.page_turn_delay_extra_max_var = tk.DoubleVar(value=0.0)
        self.post_key_delay_extra_min_var = tk.DoubleVar(value=0.0)
        self.post_key_delay_extra_max_var = tk.DoubleVar(value=0.0)
        self.next_click_x_jitter_var = tk.IntVar(value=0)
        self.next_click_y_jitter_var = tk.IntVar(value=0)
        self.click_to_focus_var = tk.BooleanVar(value=True)
        self.refine_manual_selection_var = tk.BooleanVar(value=True)
        self.trim_edges_var = tk.BooleanVar(value=False)
        self.trim_top_bottom_var = tk.BooleanVar(value=False)
        self.bg_threshold_var = tk.IntVar(value=18)
        self.edge_margin_var = tk.IntVar(value=4)
        self.status_var = tk.StringVar(value="영역을 선택한 뒤 캡쳐를 시작하세요.")
        self.region_var = tk.StringVar(value="미선택")

        self._build_ui()
        self._start_hotkey_listener()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        outer = ttk.Frame(self.root)
        outer.pack(fill="both", expand=True)

        self.scroll_canvas = tk.Canvas(
            outer,
            highlightthickness=0,
            borderwidth=0,
        )
        scrollbar = ttk.Scrollbar(
            outer,
            orient="vertical",
            command=self.scroll_canvas.yview,
        )
        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        container = ttk.Frame(self.scroll_canvas, padding=16)
        self.scrollable_frame = container
        self._scroll_window_id = self.scroll_canvas.create_window(
            (0, 0),
            window=container,
            anchor="nw",
        )

        container.bind("<Configure>", self._on_scrollable_frame_configure)
        self.scroll_canvas.bind("<Configure>", self._on_canvas_configure)
        self.scroll_canvas.bind_all("<MouseWheel>", self._on_mousewheel, add="+")

        ttk.Label(
            container, text="웹 PDF 페이지 캡쳐", font=("Malgun Gothic", 16, "bold")
        ).pack(anchor="w")
        ttk.Label(
            container,
            text="PDF가 열린 브라우저를 띄운 상태에서 페이지 영역만 지정하면 됩니다.",
            foreground="#555555",
        ).pack(anchor="w", pady=(2, 14))

        region_box = ttk.LabelFrame(container, text="1. 캡쳐 영역")
        region_box.pack(fill="x", pady=(0, 10))
        button_row = ttk.Frame(region_box)
        button_row.pack(anchor="w", padx=12, pady=(10, 6))
        ttk.Button(button_row, text="자동 감지", command=self.auto_detect_region).pack(
            side="left"
        )
        ttk.Button(button_row, text="수동 선택", command=self.select_region).pack(
            side="left", padx=(8, 0)
        )
        ttk.Label(region_box, textvariable=self.region_var).pack(
            anchor="w", padx=12, pady=(0, 10)
        )

        output_box = ttk.LabelFrame(container, text="2. 저장 설정")
        output_box.pack(fill="x", pady=(0, 10))
        self._labeled_entry(
            output_box, "저장 폴더", self.output_dir_var, browse=self.choose_output_dir
        )
        self._labeled_entry(output_box, "파일 접두사", self.file_prefix_var)

        required_box = ttk.LabelFrame(container, text="3. 필수 옵션")
        required_box.pack(fill="x", pady=(0, 10))
        ttk.Label(
            required_box,
            text="기본 캡쳐에 필요한 설정입니다.",
            foreground="#555555",
        ).pack(anchor="w", padx=12, pady=(8, 2))
        self._labeled_spinbox(
            required_box, "시작 페이지 번호", self.start_page_var, 1, 999999, 1
        )
        self._labeled_spinbox(
            required_box, "캡쳐 장수", self.capture_count_var, 1, 999999, 1
        )
        self._labeled_spinbox(
            required_box, "시작 전 대기(초)", self.start_delay_var, 0, 30, 0.5
        )
        self._labeled_spinbox(
            required_box,
            "페이지 넘김 전 대기(초)",
            self.page_turn_delay_var,
            0,
            10,
            0.1,
        )
        self._labeled_spinbox(
            required_box, "우측키 후 대기(초)", self.post_key_delay_var, 0, 10, 0.1
        )
        self._labeled_combobox(
            required_box,
            "페이지 넘김 키",
            self.turn_key_var,
            ("next_button_click", "right", "pagedown", "space"),
        )
        self._labeled_spinbox(
            required_box,
            "다음 버튼 X 오프셋",
            self.next_click_x_offset_var,
            -200,
            300,
            1,
        )
        self._labeled_spinbox(
            required_box,
            "다음 버튼 Y 오프셋",
            self.next_click_y_offset_var,
            -300,
            300,
            1,
        )

        optional_box = ttk.LabelFrame(container, text="4. 선택 옵션")
        optional_box.pack(fill="x", pady=(0, 10))
        ttk.Label(
            optional_box,
            text="정확도나 안정성을 더 높이고 싶을 때만 조정하세요.",
            foreground="#555555",
        ).pack(anchor="w", padx=12, pady=(8, 2))
        ttk.Checkbutton(
            optional_box,
            text="수동 선택 후 내부에서 자동 보정",
            variable=self.refine_manual_selection_var,
        ).pack(anchor="w", padx=12, pady=(10, 4))
        ttk.Checkbutton(
            optional_box,
            text="캡쳐 전 브라우저 영역 클릭해서 포커스 확보",
            variable=self.click_to_focus_var,
        ).pack(anchor="w", padx=12, pady=4)
        self._labeled_spinbox(
            optional_box,
            "넘김 전 추가 최소(초)",
            self.page_turn_delay_extra_min_var,
            0,
            3,
            0.05,
        )
        self._labeled_spinbox(
            optional_box,
            "넘김 전 추가 최대(초)",
            self.page_turn_delay_extra_max_var,
            0,
            3,
            0.05,
        )
        self._labeled_spinbox(
            optional_box,
            "넘김 후 추가 최소(초)",
            self.post_key_delay_extra_min_var,
            0,
            3,
            0.05,
        )
        self._labeled_spinbox(
            optional_box,
            "넘김 후 추가 최대(초)",
            self.post_key_delay_extra_max_var,
            0,
            3,
            0.05,
        )
        self._labeled_spinbox(
            optional_box, "클릭 X 지터(px)", self.next_click_x_jitter_var, 0, 50, 1
        )
        self._labeled_spinbox(
            optional_box, "클릭 Y 지터(px)", self.next_click_y_jitter_var, 0, 50, 1
        )
        ttk.Separator(optional_box, orient="horizontal").pack(fill="x", padx=12, pady=8)
        ttk.Checkbutton(
            optional_box,
            text="가장자리 배경색 기준 자동 트리밍",
            variable=self.trim_edges_var,
        ).pack(anchor="w", padx=12, pady=4)
        ttk.Checkbutton(
            optional_box,
            text="상하 여백도 같이 트리밍",
            variable=self.trim_top_bottom_var,
        ).pack(anchor="w", padx=12, pady=4)
        self._labeled_spinbox(
            optional_box, "배경 허용 오차", self.bg_threshold_var, 1, 80, 1
        )
        self._labeled_spinbox(
            optional_box, "안전 여백(px)", self.edge_margin_var, 0, 30, 1
        )

        action_row = ttk.Frame(container)
        action_row.pack(fill="x", pady=(6, 8))
        ttk.Button(action_row, text="테스트 캡쳐 1장", command=self.capture_test).pack(
            side="left"
        )
        ttk.Button(action_row, text="캡쳐 시작", command=self.start_capture).pack(
            side="left", padx=8
        )
        ttk.Button(action_row, text="중지 요청", command=self.request_stop).pack(
            side="left"
        )

        ttk.Label(
            container, text="중지는 F8 키로도 가능합니다.", foreground="#555555"
        ).pack(anchor="w")
        ttk.Label(
            container,
            textvariable=self.status_var,
            wraplength=520,
            foreground="#003366",
        ).pack(anchor="w", pady=(8, 0))

    def _on_scrollable_frame_configure(self, _event):
        if self.scroll_canvas is None:
            return
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        if self.scroll_canvas is None or self._scroll_window_id is None:
            return
        self.scroll_canvas.itemconfigure(self._scroll_window_id, width=event.width)

    def _on_mousewheel(self, event):
        if self.scroll_canvas is None:
            return
        if not self.root.winfo_exists():
            return
        delta = int(-event.delta / 120) if event.delta else 0
        if delta:
            self.scroll_canvas.yview_scroll(delta, "units")

    def _labeled_entry(self, parent, label: str, variable: tk.StringVar, browse=None):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=12, pady=6)
        ttk.Label(frame, text=label, width=14).pack(side="left")
        ttk.Entry(frame, textvariable=variable).pack(side="left", fill="x", expand=True)
        if browse:
            ttk.Button(frame, text="찾기", command=browse).pack(
                side="left", padx=(6, 0)
            )

    def _labeled_spinbox(
        self, parent, label: str, variable, minimum, maximum, increment
    ):
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

    def _labeled_combobox(
        self, parent, label: str, variable: tk.StringVar, values: tuple[str, ...]
    ):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=12, pady=4)
        ttk.Label(frame, text=label, width=18).pack(side="left")
        combo = ttk.Combobox(
            frame, textvariable=variable, values=values, state="readonly", width=12
        )
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
        selected = filedialog.askdirectory(
            initialdir=self.output_dir_var.get() or str(Path.cwd())
        )
        if selected:
            self.output_dir_var.set(selected)

    def select_region(self):
        self.root.withdraw()

        def handle_region(region: CaptureRegion):
            self.root.deiconify()
            self.root.lift()
            self.root.update()

            if self.refine_manual_selection_var.get():
                self._refine_selected_region(region)
                return

            self._apply_capture_region(
                region, prefix=None, status_message="캡쳐 영역이 설정되었습니다."
            )

        selector = RegionSelector(self.root, handle_region)

        def restore_on_close():
            self.root.deiconify()
            self.root.lift()

        selector.bind("<Destroy>", lambda _event: restore_on_close())

    def auto_detect_region(self):
        try:
            self._set_status(
                "대상 화면을 선택한 뒤 PDF 페이지 영역을 자동 감지합니다..."
            )
            monitor = self._choose_monitor()
            if not monitor:
                self._set_status("자동 감지가 취소되었습니다.")
                return

            self.root.withdraw()
            self.root.update()
            time.sleep(0.2)

            screenshot = self._grab_monitor_image(monitor)
            detected, debug_info = self._detect_pdf_region_with_debug(screenshot)
            if not detected:
                debug_path = self._save_detection_debug_image(
                    screenshot,
                    debug_info,
                    prefix="auto_detect_failure",
                )
                raise RuntimeError(
                    "자동 감지에 실패했습니다.\n"
                    f"- 원인: {debug_info.failure_summary()}\n"
                    f"- 밝은 영역 후보: {debug_info.bright_candidates}개\n"
                    f"- 외곽선 후보: {debug_info.edge_candidates}개\n"
                    f"- 디버그 이미지: {debug_path}\n"
                    "- 수동 선택 또는 수동 선택 후 자동 보정을 사용하세요."
                )

            def handle_confirm(region: CaptureRegion | None, manual: bool):
                if manual:
                    self.select_region()
                    return
                assert region is not None
                self.capture_region = CaptureRegion(
                    left=monitor["left"] + region.left,
                    top=monitor["top"] + region.top,
                    width=region.width,
                    height=region.height,
                )
                self.region_var.set(
                    "auto: "
                    f"left={self.capture_region.left}, top={self.capture_region.top}, "
                    f"width={self.capture_region.width}, height={self.capture_region.height}"
                )
                self._set_status(
                    "자동 감지 영역을 설정했습니다. 테스트 캡쳐로 먼저 확인하세요."
                )

            self.root.after(
                0,
                lambda: RegionConfirmDialog(
                    self.root, screenshot, detected, handle_confirm
                ),
            )
        except Exception as exc:
            messagebox.showerror("자동 감지 실패", str(exc))
            self._set_status(f"자동 감지 실패: {exc}")
        finally:
            self.root.deiconify()
            self.root.lift()

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
            messagebox.showwarning(
                "시작 페이지", "시작 페이지 번호는 1 이상이어야 합니다."
            )
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
            messagebox.showinfo(
                "테스트 캡쳐", f"테스트 이미지를 저장했습니다.\n{test_path}"
            )
        except Exception as exc:
            messagebox.showerror("테스트 실패", str(exc))

    def start_capture(self):
        if self.is_running:
            messagebox.showinfo("캡쳐 중", "이미 캡쳐가 진행 중입니다.")
            return
        if not self._validate():
            return

        config = CaptureJobConfig(
            output_dir=Path(self.output_dir_var.get()).expanduser(),
            prefix=self.file_prefix_var.get().strip() or "page",
            start_page=int(self.start_page_var.get()),
            total=int(self.capture_count_var.get()),
            start_delay=float(self.start_delay_var.get()),
            page_turn_delay=float(self.page_turn_delay_var.get()),
            post_key_delay=float(self.post_key_delay_var.get()),
            turn_key=self.turn_key_var.get().strip() or "right",
            next_click_x_offset=int(self.next_click_x_offset_var.get()),
            next_click_y_offset=int(self.next_click_y_offset_var.get()),
            page_turn_delay_extra_min=max(
                0.0, float(self.page_turn_delay_extra_min_var.get())
            ),
            page_turn_delay_extra_max=max(
                0.0, float(self.page_turn_delay_extra_max_var.get())
            ),
            post_key_delay_extra_min=max(
                0.0, float(self.post_key_delay_extra_min_var.get())
            ),
            post_key_delay_extra_max=max(
                0.0, float(self.post_key_delay_extra_max_var.get())
            ),
            next_click_x_jitter=max(0, int(self.next_click_x_jitter_var.get())),
            next_click_y_jitter=max(0, int(self.next_click_y_jitter_var.get())),
        )

        self.stop_requested = False
        self.is_running = True
        self.root.iconify()
        thread = threading.Thread(
            target=self._capture_worker, args=(config,), daemon=True
        )
        thread.start()

    def _capture_worker(self, config: CaptureJobConfig):
        try:
            saved_count = 0

            self._set_status(
                f"{config.start_delay:.1f}초 후 캡쳐를 시작합니다. 브라우저 PDF 화면이 맨 앞으로 오도록 준비하세요."
            )
            time.sleep(max(0.0, config.start_delay))

            for index in range(config.total):
                if self.stop_requested:
                    break

                page_no = config.start_page + index
                self._set_status(f"{page_no}페이지 캡쳐 중...")
                image = self._grab_region()
                save_path = config.output_dir / f"{config.prefix}_{page_no:04d}.png"
                image.save(save_path)
                saved_count += 1

                if index == config.total - 1 or self.stop_requested:
                    continue

                self._set_status(
                    f"{page_no}페이지 저장 완료. 다음 페이지로 넘기는 중..."
                )
                time.sleep(
                    self._apply_delay_range(
                        config.page_turn_delay,
                        config.page_turn_delay_extra_min,
                        config.page_turn_delay_extra_max,
                    )
                )
                self._send_page_turn_action(config)
                time.sleep(
                    self._apply_delay_range(
                        config.post_key_delay,
                        config.post_key_delay_extra_min,
                        config.post_key_delay_extra_max,
                    )
                )

            if self.stop_requested:
                self._set_status(
                    f"중지 요청으로 캡쳐를 종료했습니다. 저장 장수: {saved_count}"
                )
            else:
                self._set_status(
                    f"캡쳐 완료. {saved_count}장을 저장했습니다: {config.output_dir}"
                )
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

    def _send_page_turn_action(self, config: CaptureJobConfig):
        if config.turn_key == "next_button_click":
            self._click_next_button(
                x_offset=config.next_click_x_offset,
                y_offset=config.next_click_y_offset,
                x_jitter=config.next_click_x_jitter,
                y_jitter=config.next_click_y_jitter,
            )
            return

        self._focus_pdf_viewer()
        time.sleep(0.1)
        pyautogui.press(config.turn_key)

    def _click_next_button(
        self, x_offset: int, y_offset: int, x_jitter: int = 0, y_jitter: int = 0
    ):
        if not self.capture_region:
            return
        jitter_x = random.randint(-x_jitter, x_jitter) if x_jitter > 0 else 0
        jitter_y = random.randint(-y_jitter, y_jitter) if y_jitter > 0 else 0
        x = self.capture_region.left + self.capture_region.width + x_offset + jitter_x
        y = (
            self.capture_region.top
            + self.capture_region.height // 2
            + y_offset
            + jitter_y
        )
        pyautogui.click(x, y)

    def _apply_delay_range(
        self, base_delay: float, extra_min: float, extra_max: float
    ) -> float:
        base = max(0.0, base_delay)
        low = max(0.0, extra_min)
        high = max(low, extra_max)
        return base + random.uniform(low, high)

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

    def _choose_monitor(self) -> dict | None:
        with mss.mss() as sct:
            monitors = [dict(monitor) for monitor in sct.monitors[1:]]

        if not monitors:
            return None
        if len(monitors) == 1:
            return monitors[0]

        monitor_previews = [
            (monitor, self._grab_monitor_image(monitor)) for monitor in monitors
        ]
        dialog = MonitorSelectDialog(self.root, monitor_previews)
        self.root.wait_window(dialog)
        return dialog.selected_monitor

    def _grab_monitor_image(self, monitor: dict) -> Image.Image:
        with mss.mss() as sct:
            shot = sct.grab(monitor)
        image = Image.frombytes("RGB", shot.size, shot.rgb)
        return image

    def _grab_image_from_region(self, region: CaptureRegion) -> Image.Image:
        with mss.mss() as sct:
            shot = sct.grab(region.as_mss())
        return Image.frombytes("RGB", shot.size, shot.rgb)

    def _detect_pdf_region(self, image: Image.Image) -> CaptureRegion | None:
        region, _debug_info = self._detect_pdf_region_with_debug(image)
        return region

    def _detect_pdf_region_with_debug(
        self, image: Image.Image
    ) -> tuple[CaptureRegion | None, DetectionDebugInfo]:
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        screen_h, screen_w = gray.shape
        bright_candidates = self._find_bright_page_candidates(gray)
        edge_candidates = self._find_edge_based_candidates(gray)
        inner_candidates = self._find_inner_page_candidates(
            gray, bright_candidates, screen_w, screen_h
        )
        candidates: list[tuple[int, int, int, int, float]] = []
        candidate_details: list[CandidateDebugRecord] = []
        rejection_counts = {
            "too_small": 0,
            "bad_aspect": 0,
            "bad_area_ratio": 0,
        }

        for candidate in bright_candidates:
            score, reason = self._score_pdf_candidate(
                candidate,
                screen_w,
                screen_h,
                prefer_bright=True,
                rejection_counts=rejection_counts,
            )
            if score > 0:
                candidates.append((*candidate, score))
                candidate_details.append(
                    CandidateDebugRecord(
                        source="bright",
                        rect=candidate,
                        accepted=True,
                        reason=reason,
                        score=score,
                    )
                )
            else:
                candidate_details.append(
                    CandidateDebugRecord(
                        source="bright",
                        rect=candidate,
                        accepted=False,
                        reason=reason,
                        score=None,
                    )
                )

        for candidate in edge_candidates:
            score, reason = self._score_pdf_candidate(
                candidate,
                screen_w,
                screen_h,
                prefer_bright=False,
                rejection_counts=rejection_counts,
            )
            if score > 0:
                candidates.append((*candidate, score))
                candidate_details.append(
                    CandidateDebugRecord(
                        source="edge",
                        rect=candidate,
                        accepted=True,
                        reason=reason,
                        score=score,
                    )
                )
            else:
                candidate_details.append(
                    CandidateDebugRecord(
                        source="edge",
                        rect=candidate,
                        accepted=False,
                        reason=reason,
                        score=None,
                    )
                )

        for candidate in inner_candidates:
            score, reason = self._score_pdf_candidate(
                candidate,
                screen_w,
                screen_h,
                prefer_bright=True,
                rejection_counts=rejection_counts,
            )
            if score > 0:
                candidates.append((*candidate, score))
                candidate_details.append(
                    CandidateDebugRecord(
                        source="inner",
                        rect=candidate,
                        accepted=True,
                        reason=reason,
                        score=score,
                    )
                )
            else:
                candidate_details.append(
                    CandidateDebugRecord(
                        source="inner",
                        rect=candidate,
                        accepted=False,
                        reason=reason,
                        score=None,
                    )
                )

        if not candidates:
            return None, DetectionDebugInfo(
                bright_candidates=len(bright_candidates),
                edge_candidates=len(edge_candidates) + len(inner_candidates),
                accepted_candidates=0,
                rejection_counts=rejection_counts,
                best_score=None,
                candidate_details=candidate_details,
            )

        x, y, w, h, _score = max(candidates, key=lambda item: item[4])
        best_rect = (x, y, w, h)

        x, y, w, h = best_rect
        padding = 6
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(screen_w - x, w + padding * 2)
        h = min(screen_h - y, h + padding * 2)

        return CaptureRegion(left=x, top=y, width=w, height=h), DetectionDebugInfo(
            bright_candidates=len(bright_candidates),
            edge_candidates=len(edge_candidates) + len(inner_candidates),
            accepted_candidates=len(candidates),
            rejection_counts=rejection_counts,
            best_score=_score,
            candidate_details=candidate_details,
        )

    def _refine_selected_region(self, region: CaptureRegion):
        try:
            self._set_status(
                "선택 영역 내부에서 PDF 페이지 경계를 자동 보정하는 중입니다..."
            )
            time.sleep(0.15)
            screenshot = self._grab_image_from_region(region)
            detected, debug_info = self._detect_pdf_region_with_debug(screenshot)
            if not detected:
                debug_path = self._save_detection_debug_image(
                    screenshot,
                    debug_info,
                    prefix="manual_refine_failure",
                )
                self._apply_capture_region(
                    region,
                    prefix=None,
                    status_message=(
                        "자동 보정에 실패하여 수동 선택 영역을 그대로 사용합니다. "
                        f"원인: {debug_info.failure_summary()}"
                    ),
                )
                self.root.after(
                    0,
                    lambda: messagebox.showwarning(
                        "자동 보정 실패",
                        "수동 선택 영역 내부에서 페이지를 다시 찾지 못했습니다.\n"
                        f"- 원인: {debug_info.failure_summary()}\n"
                        f"- 밝은 영역 후보: {debug_info.bright_candidates}개\n"
                        f"- 외곽선 후보: {debug_info.edge_candidates}개\n"
                        f"- 디버그 이미지: {debug_path}\n"
                        "- 방금 선택한 수동 영역을 그대로 사용합니다.",
                    ),
                )
                return

            refined_region = CaptureRegion(
                left=region.left + detected.left,
                top=region.top + detected.top,
                width=detected.width,
                height=detected.height,
            )

            def handle_confirm(_selected: CaptureRegion | None, manual: bool):
                if manual:
                    self._apply_capture_region(
                        region,
                        prefix=None,
                        status_message="수동 선택 영역을 사용합니다.",
                    )
                    return
                self._apply_capture_region(
                    refined_region,
                    prefix="refined",
                    status_message="수동 선택 영역 내부에서 자동 보정한 결과를 적용했습니다.",
                )

            self.root.after(
                0,
                lambda: RegionConfirmDialog(
                    self.root, screenshot, detected, handle_confirm
                ),
            )
        except Exception as exc:
            self._apply_capture_region(
                region,
                prefix=None,
                status_message=f"자동 보정 중 오류가 발생해 수동 선택 영역을 사용합니다: {exc}",
            )

    def _apply_capture_region(
        self, region: CaptureRegion, prefix: str | None, status_message: str
    ):
        self.capture_region = region
        label_prefix = f"{prefix}: " if prefix else ""
        self.region_var.set(
            f"{label_prefix}left={region.left}, top={region.top}, width={region.width}, height={region.height}"
        )
        self._set_status(status_message)

    def _save_detection_debug_image(
        self,
        screenshot: Image.Image,
        debug_info: DetectionDebugInfo,
        prefix: str,
    ) -> Path:
        debug_dir = Path(self.output_dir_var.get()).expanduser() / "_debug"
        debug_dir.mkdir(parents=True, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        debug_path = debug_dir / f"{prefix}_{timestamp}.png"

        canvas = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        accepted_color = (0, 220, 120)
        rejected_bright_color = (0, 180, 255)
        rejected_edge_color = (0, 90, 255)
        ranked_candidates = sorted(
            debug_info.candidate_details or [],
            key=lambda item: item.sort_key(),
        )

        for index, candidate in enumerate(ranked_candidates[:12], start=1):
            x, y, w, h = candidate.rect
            if candidate.accepted:
                color = accepted_color
                label = f"{index}. {candidate.source} ok {candidate.score:.2f}"
                thickness = 3
            else:
                color = (
                    rejected_bright_color
                    if candidate.source == "bright"
                    else rejected_edge_color
                )
                label = f"{index}. {candidate.source} {candidate.reason}"
                thickness = 2

            cv2.rectangle(canvas, (x, y), (x + w, y + h), color, thickness)
            cv2.putText(
                canvas,
                label,
                (x, max(18, y - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.48,
                color,
                1,
                cv2.LINE_AA,
            )

        summary_lines = [
            f"bright={debug_info.bright_candidates}, edge={debug_info.edge_candidates}, accepted={debug_info.accepted_candidates}",
            f"summary: {debug_info.failure_summary()}",
        ]
        y_cursor = 24
        for line in summary_lines:
            cv2.putText(
                canvas,
                line,
                (16, y_cursor),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                3,
                cv2.LINE_AA,
            )
            cv2.putText(
                canvas,
                line,
                (16, y_cursor),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (24, 24, 24),
                1,
                cv2.LINE_AA,
            )
            y_cursor += 26

        Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)).save(debug_path)
        return debug_path

    def _find_bright_page_candidates(
        self, gray: np.ndarray
    ) -> list[tuple[int, int, int, int]]:
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        masks = [
            cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)[1]
            for threshold in (200, 215, 230, 240)
        ]
        kernel = np.ones((5, 5), np.uint8)
        candidates: list[tuple[int, int, int, int]] = []
        seen: set[tuple[int, int, int, int]] = set()

        for mask in masks:
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            for contour in contours:
                area = cv2.contourArea(contour)
                if area <= 0:
                    continue

                x, y, w, h = cv2.boundingRect(contour)
                rect_area = w * h
                if rect_area <= 0:
                    continue

                fill_ratio = area / rect_area
                if fill_ratio < 0.65:
                    continue

                candidate = (x, y, w, h)
                if candidate not in seen:
                    seen.add(candidate)
                    candidates.append(candidate)

        return candidates

    def _find_edge_based_candidates(
        self, gray: np.ndarray
    ) -> list[tuple[int, int, int, int]]:
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 40, 120)
        edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
        edges = cv2.erode(edges, np.ones((3, 3), np.uint8), iterations=1)

        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        candidates: list[tuple[int, int, int, int]] = []
        seen: set[tuple[int, int, int, int]] = set()

        for contour in contours:
            area = cv2.contourArea(contour)
            if area <= 0:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            rect_area = w * h
            if rect_area <= 0:
                continue

            fill_ratio = area / rect_area
            if fill_ratio < 0.12:
                continue

            candidate = (x, y, w, h)
            if candidate not in seen:
                seen.add(candidate)
                candidates.append(candidate)

        return candidates

    def _find_inner_page_candidates(
        self,
        gray: np.ndarray,
        bright_candidates: list[tuple[int, int, int, int]],
        screen_w: int,
        screen_h: int,
    ) -> list[tuple[int, int, int, int]]:
        candidates: list[tuple[int, int, int, int]] = []
        seen: set[tuple[int, int, int, int]] = set()

        for x, y, w, h in bright_candidates:
            area_ratio = (w * h) / max(screen_w * screen_h, 1)
            if area_ratio < 0.82:
                continue
            if w < screen_w * 0.9 and h < screen_h * 0.9:
                continue

            inset_x = max(16, int(w * 0.06))
            inset_y = max(16, int(h * 0.03))
            left = x + inset_x
            top = y + inset_y
            right = x + w - inset_x
            bottom = y + h - inset_y
            if right - left < screen_w * 0.15 or bottom - top < screen_h * 0.2:
                continue

            roi = gray[top:bottom, left:right]
            if roi.size == 0:
                continue

            estimated = self._estimate_inner_content_rect(roi)
            if estimated is not None:
                inner_x, inner_y, inner_w, inner_h = estimated
                mapped = (left + inner_x, top + inner_y, inner_w, inner_h)
                if mapped not in seen:
                    seen.add(mapped)
                    candidates.append(mapped)

            roi_candidates = self._find_bright_page_candidates(roi)
            roi_candidates.extend(self._find_edge_based_candidates(roi))

            for inner_x, inner_y, inner_w, inner_h in roi_candidates:
                mapped = (left + inner_x, top + inner_y, inner_w, inner_h)
                if mapped not in seen:
                    seen.add(mapped)
                    candidates.append(mapped)

        return candidates

    def _estimate_inner_content_rect(
        self, gray: np.ndarray
    ) -> tuple[int, int, int, int] | None:
        height, width = gray.shape
        if width < 50 or height < 50:
            return None

        sample_w = max(2, min(12, width // 20))
        sample_h = max(2, min(12, height // 20))
        bg_samples = np.concatenate(
            [
                gray[:, :sample_w].reshape(-1),
                gray[:, width - sample_w :].reshape(-1),
                gray[:sample_h, :].reshape(-1),
                gray[height - sample_h :, :].reshape(-1),
            ]
        )
        bg_value = float(np.median(bg_samples))
        diff = np.abs(gray.astype(np.float32) - bg_value)

        col_strength = diff.mean(axis=0)
        row_strength = diff.mean(axis=1)
        col_threshold = max(6.0, float(np.percentile(col_strength, 70)) * 0.55)
        row_threshold = max(6.0, float(np.percentile(row_strength, 70)) * 0.55)

        left = 0
        while left < width - 1 and col_strength[left] < col_threshold:
            left += 1

        right = width - 1
        while right > 0 and col_strength[right] < col_threshold:
            right -= 1

        top = 0
        while top < height - 1 and row_strength[top] < row_threshold:
            top += 1

        bottom = height - 1
        while bottom > 0 and row_strength[bottom] < row_threshold:
            bottom -= 1

        if right - left < width * 0.12 or bottom - top < height * 0.2:
            return None

        return (left, top, right - left + 1, bottom - top + 1)

    def _score_pdf_candidate(
        self,
        rect: tuple[int, int, int, int],
        screen_w: int,
        screen_h: int,
        prefer_bright: bool,
        rejection_counts: dict[str, int] | None = None,
    ) -> tuple[float, str]:
        x, y, w, h = rect
        if w < screen_w * 0.12 or h < screen_h * 0.18:
            if rejection_counts is not None:
                rejection_counts["too_small"] += 1
            return -1.0, "too_small"

        aspect = w / max(h, 1)
        if not 0.45 <= aspect <= 1.15:
            if rejection_counts is not None:
                rejection_counts["bad_aspect"] += 1
            return -1.0, "bad_aspect"

        rect_area = w * h
        area_ratio = rect_area / max(screen_w * screen_h, 1)
        if area_ratio < 0.04 or area_ratio > 0.92:
            if rejection_counts is not None:
                rejection_counts["bad_area_ratio"] += 1
            return -1.0, "bad_area_ratio"

        screen_center_x = screen_w / 2
        screen_center_y = screen_h / 2
        center_x = x + w / 2
        center_y = y + h / 2
        center_distance = (
            abs(center_x - screen_center_x) / screen_w
            + abs(center_y - screen_center_y) / screen_h
        )
        center_score = max(0.0, 1.0 - center_distance)

        target_aspects = (0.707, 0.773, 0.82)
        aspect_error = min(abs(aspect - target) for target in target_aspects)
        aspect_score = max(0.0, 1.0 - aspect_error / 0.45)

        height_score = min(1.0, h / max(screen_h * 0.55, 1))
        width_score = min(1.0, w / max(screen_w * 0.55, 1))
        size_score = min(1.0, area_ratio / 0.25)
        bright_bonus = 0.08 if prefer_bright else 0.0

        return (
            size_score * 0.34
            + center_score * 0.24
            + aspect_score * 0.22
            + height_score * 0.12
            + width_score * 0.08
            + bright_bonus
        ), "accepted"

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
            return tuple(
                sum(channel[i] for channel in points) // count for i in range(3)
            )

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
