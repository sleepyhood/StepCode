import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import ctypes
from datetime import datetime

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

import mss
from PIL import Image, ImageTk
import pygetwindow as gw
from pynput import keyboard


class AutoCaptureApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("창 지정 타이머 자동 캡처 도구")
        
        # GUI 스타일 및 폰트 설정
        self.style = ttk.Style()
        self.style.configure(".", font=("Malgun Gothic", 10))
        self.style.configure("TLabelframe.Label", font=("Malgun Gothic", 11, "bold"))

        self.root.geometry("600x1200")
        self.root.resizable(False, False)

        self.stop_requested = False
        self.is_running = False
        self.hotkey_listener = None
        self.preview_photo = None  # ImageTk 참조 유지용

        self.target_window_var = tk.StringVar()
        self.output_dir_var = tk.StringVar(value=str(Path.cwd() / "output" / "auto_capture"))
        self.file_prefix_var = tk.StringVar(value="capture")
        self.start_index_var = tk.IntVar(value=1)
        self.auto_continue_var = tk.BooleanVar(value=False)
        self.capture_count_var = tk.IntVar(value=100)
        self.unlimited_var = tk.BooleanVar(value=False)
        self.interval_var = tk.DoubleVar(value=0.5)
        self.status_var = tk.StringVar(value="창을 선택하고 캡처를 시작하세요.")

        self._build_ui()
        self._refresh_windows()
        self._start_hotkey_listener()
        
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill="both", expand=True)

        # 1. 대상 창 선택
        win_box = ttk.LabelFrame(container, text="1. 대상 창 선택")
        win_box.pack(fill="x", pady=(0, 10))
        
        row1 = ttk.Frame(win_box)
        row1.pack(fill="x", padx=12, pady=10)
        self.combo_windows = ttk.Combobox(row1, textvariable=self.target_window_var, state="readonly", width=40)
        self.combo_windows.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.combo_windows.bind("<<ComboboxSelected>>", lambda _e: self._update_preview())
        ttk.Button(row1, text="새로고침", command=self._refresh_windows).pack(side="left")

        # 미리보기 영역
        self.preview_label = ttk.Label(win_box, text="창을 선택하면 미리보기가 표시됩니다.",
                                       anchor="center", relief="sunken")
        self.preview_label.pack(padx=12, pady=(0, 10), fill="x")

        # 2. 저장 설정
        out_box = ttk.LabelFrame(container, text="2. 저장 설정")
        out_box.pack(fill="x", pady=(0, 10))
        
        self._labeled_entry(out_box, "저장 폴더", self.output_dir_var, browse=self.choose_output_dir)
        self._labeled_entry(out_box, "파일 접두사", self.file_prefix_var)

        # 3. 캡처 옵션
        opt_box = ttk.LabelFrame(container, text="3. 캡처 옵션")
        opt_box.pack(fill="x", pady=(0, 10))
        
        # 시작 번호 + 이어가기 체크박스 + 찾기 버튼
        start_row = ttk.Frame(opt_box)
        start_row.pack(fill="x", padx=12, pady=5)
        ttk.Label(start_row, text="시작 번호", width=14).pack(side="left")
        ttk.Spinbox(start_row, textvariable=self.start_index_var, from_=1, to=999999, increment=1, width=10).pack(side="left")
        ttk.Checkbutton(start_row, text="마지막 번호부터 이어가기", variable=self.auto_continue_var).pack(side="left", padx=10)
        ttk.Button(start_row, text="찾기", command=self._update_start_index_from_folder, width=5).pack(side="left")
        
        # 캡처 장수 + 제한없음
        count_row = ttk.Frame(opt_box)
        count_row.pack(fill="x", padx=12, pady=5)
        ttk.Label(count_row, text="캡처 장수", width=14).pack(side="left")
        self.spin_count = ttk.Spinbox(count_row, textvariable=self.capture_count_var, from_=1, to=999999, increment=1, width=10)
        self.spin_count.pack(side="left")
        ttk.Checkbutton(count_row, text="제한없음", variable=self.unlimited_var, command=self._toggle_unlimited).pack(side="left", padx=10)
        
        self._labeled_spinbox(opt_box, "캡처 간격(초)", self.interval_var, 0.1, 3600.0, 0.1)

        # 제어부
        action_row = ttk.Frame(container)
        action_row.pack(fill="x", pady=(10, 5))
        
        ttk.Button(action_row, text="캡처 시작", command=self.start_capture).pack(side="left")
        ttk.Button(action_row, text="중지 요청 (F8)", command=self.request_stop).pack(side="left", padx=10)
        
        ttk.Label(container, textvariable=self.status_var, foreground="#003366", wraplength=550).pack(anchor="w", pady=(10, 0))

        # 4. 실행 로그
        log_box = ttk.LabelFrame(container, text="4. 실행 로그")
        log_box.pack(fill="both", expand=True, pady=(10, 0))
        
        self.log_text = tk.Text(log_box, height=12, font=("Consolas", 9), state="disabled", bg="#f8f9fa")
        self.log_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        log_scroll = ttk.Scrollbar(log_box, command=self.log_text.yview)
        log_scroll.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=log_scroll.set)

    def _labeled_entry(self, parent, label: str, variable: tk.StringVar, browse=None):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=12, pady=5)
        ttk.Label(frame, text=label, width=12).pack(side="left")
        ttk.Entry(frame, textvariable=variable).pack(side="left", fill="x", expand=True)
        if browse:
            ttk.Button(frame, text="찾기", command=browse).pack(side="left", padx=(5, 0))

    def _labeled_spinbox(self, parent, label: str, variable, minimum, maximum, increment):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=12, pady=5)
        ttk.Label(frame, text=label, width=14).pack(side="left")
        ttk.Spinbox(frame, textvariable=variable, from_=minimum, to=maximum, increment=increment, width=10).pack(side="left")

    def _refresh_windows(self):
        titles = gw.getAllTitles()
        # 빈 제목 필터링
        valid_titles = [t for t in titles if t.strip()]
        valid_titles.sort()
        self.combo_windows["values"] = valid_titles
        if valid_titles:
            self.combo_windows.current(0)
            self._update_preview()
        else:
            self._clear_preview()
        self._set_status(f"창 목록 갱신 완료 ({len(valid_titles)}개 감지됨)")

    def _clear_preview(self):
        """미리보기 영역을 초기 상태로 되돌린다."""
        self.preview_photo = None
        self.preview_label.configure(image="", text="창을 선택하면 미리보기가 표시됩니다.")

    def _update_preview(self):
        """현재 선택된 창의 썸네일을 캡처하여 미리보기에 표시한다."""
        target_title = self.target_window_var.get()
        if not target_title:
            self._clear_preview()
            return

        try:
            windows = gw.getWindowsWithTitle(target_title)
            if not windows:
                self.preview_label.configure(image="", text="창을 찾을 수 없습니다.")
                self.preview_photo = None
                return

            win = windows[0]

            # 최소화 상태이면 미리보기 불가
            if getattr(win, 'isMinimized', False):
                self.preview_label.configure(image="", text="최소화된 창은 미리보기할 수 없습니다.")
                self.preview_photo = None
                return

            if win.width <= 0 or win.height <= 0:
                self.preview_label.configure(image="", text="창 크기가 유효하지 않습니다.")
                self.preview_photo = None
                return

            rect = {
                "left": win.left,
                "top": win.top,
                "width": win.width,
                "height": win.height,
            }

            with mss.mss() as sct:
                shot = sct.grab(rect)
                img = Image.frombytes("RGB", shot.size, shot.rgb)

            # 미리보기 최대 크기에 맞춰 축소
            max_w, max_h = 500, 200
            scale = min(max_w / img.width, max_h / img.height, 1.0)
            thumb = img.resize(
                (max(1, int(img.width * scale)), max(1, int(img.height * scale))),
                Image.Resampling.LANCZOS,
            )

            self.preview_photo = ImageTk.PhotoImage(thumb)
            self.preview_label.configure(
                image=self.preview_photo,
                text="",
            )
        except Exception as exc:
            self.preview_label.configure(image="", text=f"미리보기 실패: {exc}")
            self.preview_photo = None

    def _toggle_unlimited(self):
        """제한없음 체크 시 장수 입력칸 비활성화"""
        if self.unlimited_var.get():
            self.spin_count.configure(state="disabled")
        else:
            self.spin_count.configure(state="normal")

    def _find_next_index(self) -> int:
        """저장 폴더 내의 파일들을 확인하여 다음 번호를 결정한다."""
        out_dir = Path(self.output_dir_var.get()).expanduser()
        if not out_dir.exists():
            return 1

        prefix = self.file_prefix_var.get().strip() or "capture"
        pattern = f"{prefix}_*.png"
        
        max_idx = 0
        found = False
        for p in out_dir.glob(pattern):
            try:
                name = p.stem
                if name.startswith(prefix + "_"):
                    idx_str = name[len(prefix)+1:]
                    if idx_str.isdigit():
                        idx = int(idx_str)
                        if idx > max_idx:
                            max_idx = idx
                            found = True
            except (ValueError, IndexError):
                continue
        
        return max_idx + 1 if found else 1

    def _update_start_index_from_folder(self, silent=False):
        """저장 폴더를 스캔하여 시작 번호를 업데이트한다."""
        next_idx = self._find_next_index()
        self.start_index_var.set(next_idx)
        if not silent:
            self._add_log(f"저장 폴더 스캔 완료: 다음 번호를 {next_idx}로 설정했습니다.")


    def _add_log(self, message: str):
        """로그창에 시간과 함께 메시지 기록"""
        now = datetime.now().strftime("[%H:%M:%S]")
        full_msg = f"{now} {message}\n"
        
        def append():
            self.log_text.configure(state="normal")
            self.log_text.insert("end", full_msg)
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
            
        self.root.after(0, append)

    def choose_output_dir(self):
        selected = filedialog.askdirectory(initialdir=self.output_dir_var.get() or str(Path.cwd()))
        if selected:
            self.output_dir_var.set(selected)

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
            if not messagebox.askyesno("종료", "캡처 중입니다. 강제 종료하시겠습니까?"):
                return
            self.stop_requested = True
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        self.root.destroy()

    def request_stop(self, from_hotkey: bool = False):
        self.stop_requested = True
        msg = "F8 중지 요청이 들어왔습니다." if from_hotkey else "중지 요청이 들어왔습니다."
        self._set_status(msg + " 이번 캡처 후 종료됩니다.")

    def start_capture(self):
        if self.is_running:
            return
        
        target = self.target_window_var.get()
        if not target:
            messagebox.showwarning("오류", "캡처할 창을 선택하세요.")
            return

        out_dir = Path(self.output_dir_var.get()).expanduser()
        out_dir.mkdir(parents=True, exist_ok=True)

        # 이어가기 옵션이 켜져있으면 시작 전 번호 업데이트
        if self.auto_continue_var.get():
            self._update_start_index_from_folder(silent=True)

        self.is_running = True
        self.stop_requested = False
        
        # GUI 얼어붙음 방지 위해 별도 스레드 시작
        thread = threading.Thread(target=self._capture_worker, args=(target, out_dir), daemon=True)
        thread.start()

    def _capture_worker(self, target_title: str, out_dir: Path):
        try:
            prefix = self.file_prefix_var.get().strip() or "capture"
            start_idx = self.start_index_var.get()
            is_unlimited = self.unlimited_var.get()
            count = 999999999 if is_unlimited else self.capture_count_var.get()
            interval = self.interval_var.get()

            self._set_status("3초 후 캡처를 시작합니다. 대상 창을 최상단으로 꺼내주세요...")
            self._add_log(f"캡처 작업 준비... (대상: {target_title})")
            time.sleep(3)
            self._add_log("캡처 시작!")

            saved_count = 0
            with mss.mss() as sct:
                for i in range(count):
                    if self.stop_requested:
                        break

                    windows = gw.getWindowsWithTitle(target_title)
                    if not windows:
                        raise RuntimeError(f"'{target_title}' 창을 찾을 수 없습니다. (창이 닫혔거나 제목이 변경됨)")
                    
                    win = windows[0]
                    # 최소화 상태면 복구 (일부 환경에서만 동작)
                    if getattr(win, 'isMinimized', False):
                        win.restore()
                    
                    # 화면 밖이거나 음수 좌표 처리 방지 (듀얼모니터 고려 left/top은 음수일수있으나 width/height는 커야함)
                    if win.width <= 0 or win.height <= 0:
                        raise ValueError("창 크기가 유효하지 않습니다(최소화 상태일 수 있음).")
                        
                    # mss용 rect 구성
                    rect = {
                        "left": win.left,
                        "top": win.top,
                        "width": win.width,
                        "height": win.height
                    }
                    
                    # 캡처 및 이미지 객체 변환
                    shot = sct.grab(rect)
                    img = Image.frombytes("RGB", shot.size, shot.rgb)
                    
                    # 파일 저장
                    file_no = start_idx + i
                    save_path = out_dir / f"{prefix}_{file_no:04d}.png"
                    img.save(save_path)
                    
                    saved_count += 1
                    status_text = f"[{saved_count}/무제한] 저장 완료: {save_path.name}" if is_unlimited else f"[{saved_count}/{count}] 저장 완료: {save_path.name}"
                    self._set_status(status_text)
                    self._add_log(f"#{saved_count} 저장 완료: {save_path.name}")

                    # 남은 캡처가 있고 중지 요청이 없다면 interval만큼 대기
                    if i < count - 1 and not self.stop_requested:
                        time.sleep(interval)

            if self.stop_requested:
                self._set_status(f"중지됨. 총 {saved_count}장 저장 완료.")
                self._add_log(f"작업이 사용자에 의해 중지되었습니다. (총 {saved_count}장)")
            else:
                self._set_status(f"캡처 완료! 총 {saved_count}장 저장됨.")
                self._add_log(f"모든 캡처 작업이 완료되었습니다. (총 {saved_count}장)")
                
        except Exception as e:
            self._set_status(f"오류 발생: {e}")
            # 에러 발생 시 UI 스레드에서 메세지 박스를 띄우도록 함
            self.root.after(0, lambda err=str(e): messagebox.showerror("오류", f"캡처 중 오류가 발생했습니다:\n{err}"))
        finally:
            self.is_running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoCaptureApp(root)
    root.mainloop()
