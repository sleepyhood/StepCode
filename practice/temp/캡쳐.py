import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

import mss
from PIL import Image
import pygetwindow as gw
from pynput import keyboard


class AutoCaptureApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("창 지정 타이머 자동 캡처 도구")
        self.root.geometry("550x450")
        self.root.resizable(False, False)

        self.stop_requested = False
        self.is_running = False
        self.hotkey_listener = None

        self.target_window_var = tk.StringVar()
        self.output_dir_var = tk.StringVar(value=str(Path.cwd() / "output" / "auto_capture"))
        self.file_prefix_var = tk.StringVar(value="capture")
        self.start_index_var = tk.IntVar(value=1)
        self.capture_count_var = tk.IntVar(value=100)
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
        ttk.Button(row1, text="새로고침", command=self._refresh_windows).pack(side="left")

        # 2. 저장 설정
        out_box = ttk.LabelFrame(container, text="2. 저장 설정")
        out_box.pack(fill="x", pady=(0, 10))
        
        self._labeled_entry(out_box, "저장 폴더", self.output_dir_var, browse=self.choose_output_dir)
        self._labeled_entry(out_box, "파일 접두사", self.file_prefix_var)

        # 3. 캡처 옵션
        opt_box = ttk.LabelFrame(container, text="3. 캡처 옵션")
        opt_box.pack(fill="x", pady=(0, 10))
        
        self._labeled_spinbox(opt_box, "시작 번호", self.start_index_var, 1, 999999, 1)
        self._labeled_spinbox(opt_box, "캡처 장수", self.capture_count_var, 1, 999999, 1)
        self._labeled_spinbox(opt_box, "캡처 간격(초)", self.interval_var, 0.1, 3600.0, 0.1)

        # 제어부
        action_row = ttk.Frame(container)
        action_row.pack(fill="x", pady=(10, 5))
        
        ttk.Button(action_row, text="캡처 시작", command=self.start_capture).pack(side="left")
        ttk.Button(action_row, text="중지 요청 (F8)", command=self.request_stop).pack(side="left", padx=10)
        
        ttk.Label(container, textvariable=self.status_var, foreground="#003366", wraplength=500).pack(anchor="w", pady=(10, 0))

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
        self._set_status(f"창 목록 갱신 완료 ({len(valid_titles)}개 감지됨)")

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

        self.is_running = True
        self.stop_requested = False
        
        # GUI 얼어붙음 방지 위해 별도 스레드 시작
        thread = threading.Thread(target=self._capture_worker, args=(target, out_dir), daemon=True)
        thread.start()

    def _capture_worker(self, target_title: str, out_dir: Path):
        try:
            prefix = self.file_prefix_var.get().strip() or "capture"
            start_idx = self.start_index_var.get()
            count = self.capture_count_var.get()
            interval = self.interval_var.get()

            self._set_status("3초 후 캡처를 시작합니다. 대상 창을 최상단으로 꺼내주세요...")
            time.sleep(3)

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
                    self._set_status(f"[{saved_count}/{count}] 저장 완료: {save_path.name}")

                    # 남은 캡처가 있고 중지 요청이 없다면 interval만큼 대기
                    if i < count - 1 and not self.stop_requested:
                        time.sleep(interval)

            if self.stop_requested:
                self._set_status(f"중지됨. 총 {saved_count}장 저장 완료.")
            else:
                self._set_status(f"캡처 완료! 총 {saved_count}장 저장됨.")
                
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
