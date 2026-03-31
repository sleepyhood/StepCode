import tkinter as tk
from tkinter import messagebox
import random
import time
import os
import math

# =========================
# 설정
# =========================
PREVIEW_MS = 2500      # 시작 시 전체 공개 시간(밀리초)
MISMATCH_MS = 700      # 틀렸을 때 다시 뒤집기까지 대기(밀리초)

CARD_BACK_BG = "#3A3A3A"

# ✅ 실행 파일(.py) 위치 기준 assets 폴더
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")


class MemoryGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("기억력 게임 (tkinter)")
        self.resizable(False, False)

        self.header = tk.Frame(self, padx=12, pady=10)
        self.header.pack(fill="x")

        self.info_var = tk.StringVar(value="준비 중…")
        self.info_label = tk.Label(self.header, textvariable=self.info_var, font=("Arial", 12))
        self.info_label.pack(side="left")

        self.restart_btn = tk.Button(self.header, text="새 게임", command=self.new_game)
        self.restart_btn.pack(side="right")

        self.board = tk.Frame(self, padx=12, pady=12)
        self.board.pack()

        # 게임 상태
        self.buttons = []
        self.cards = []              # 각 카드의 "이미지 키"
        self.matched = set()         # 맞춘 인덱스
        self.revealed = []           # 현재 뒤집어 공개된 카드 인덱스 (최대 2개)
        self.locked = False          # 비교 중 입력 잠금
        self.previewing = True       # 시작 프리뷰 중인지

        # 보드 크기(자동)
        self.rows = 0
        self.cols = 0
        self.pair_count = 0          # assets 폴더 PNG 개수(=쌍 개수)
        self.total_tiles = 0         # 타일 총 개수 = pair_count*2

        # 통계/타이머
        self.moves = 0
        self.start_time = None
        self.timer_job = None

        # 이미지 캐시(참조 유지 필수)
        self.face_images = {}        # key -> PhotoImage
        self.back_image = None       # 뒷면(고정 크기) 이미지
        self.card_w = 96
        self.card_h = 96

        self.new_game()

    def make_back_image(self, w, h, color_hex):
        img = tk.PhotoImage(width=w, height=h)
        img.put(color_hex, to=(0, 0, w, h))
        return img

    def load_all_images(self):
        if not os.path.isdir(ASSET_DIR):
            messagebox.showerror("이미지 폴더 없음", f"'{ASSET_DIR}' 폴더를 만들고 PNG를 넣어주세요.")
            return None

        files = []
        for name in os.listdir(ASSET_DIR):
            if name.lower().endswith(".png"):
                files.append(os.path.join(ASSET_DIR, name))

        if len(files) == 0:
            messagebox.showerror("이미지 없음", f"'{ASSET_DIR}' 폴더에 PNG가 없습니다.")
            return None

        random.shuffle(files)

        self.face_images.clear()

        # 전부 로드
        for i, path in enumerate(files):
            key = f"img{i}"
            try:
                self.face_images[key] = tk.PhotoImage(file=path)
            except Exception:
                messagebox.showerror("이미지 로드 실패", f"PNG를 읽을 수 없습니다:\n{path}")
                return None

        # 카드 크기 고정(첫 이미지 크기 기준)
        first_key = next(iter(self.face_images))
        fw = self.face_images[first_key].width()
        fh = self.face_images[first_key].height()

        # 크기 불일치 검사(프리뷰 때 창/버튼 크기 변동 방지)
        for _, img in self.face_images.items():
            if img.width() != fw or img.height() != fh:
                messagebox.showerror(
                    "이미지 크기 불일치",
                    "assets 폴더의 PNG 크기가 서로 다릅니다.\n"
                    "모든 이미지를 같은 크기(예: 96x96)로 맞춰주세요."
                )
                return None

        self.card_w = fw
        self.card_h = fh
        self.back_image = self.make_back_image(self.card_w, self.card_h, CARD_BACK_BG)

        return list(self.face_images.keys())

    def compute_grid_closest_square(self, total_tiles):
        """
        total_tiles(=2*pair_count)를 정확히 채우면서
        rows*cols == total_tiles 이고 |rows-cols|가 최소가 되도록 선택.
        (즉, 정사각형에 최대한 가깝게. 불가하면 자연스럽게 직사각형)
        """
        if total_tiles <= 0:
            return 0, 0

        r = int(math.isqrt(total_tiles))
        while r > 0:
            if total_tiles % r == 0:
                rows = r
                cols = total_tiles // r
                return rows, cols
            r -= 1

        # 이론상 여기까지 올 일 없음(1은 항상 약수)
        return 1, total_tiles

    def new_game(self):
        # 타이머 정리
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None

        self.moves = 0
        self.start_time = None

        # 보드 초기화
        for w in self.board.winfo_children():
            w.destroy()

        self.buttons.clear()
        self.cards.clear()
        self.matched.clear()
        self.revealed.clear()
        self.locked = False
        self.previewing = True

        # assets 폴더의 PNG 전부 로드 -> 개수로 보드 자동 결정
        keys = self.load_all_images()
        if keys is None:
            return

        self.pair_count = len(keys)
        self.total_tiles = self.pair_count * 2

        # ✅ 정사각형에 최대한 가깝게 rows/cols 결정(총 타일 수는 정확히 유지)
        self.rows, self.cols = self.compute_grid_closest_square(self.total_tiles)

        # 덱 만들기: 각 이미지는 2장씩(짝)
        deck = keys * 2
        random.shuffle(deck)
        self.cards = deck

        # 버튼 생성(시작부터 back_image로 크기 고정 -> 시작 시 창 커짐 방지)
        for idx in range(self.total_tiles):
            r = idx // self.cols
            c = idx % self.cols
            btn = tk.Button(
                self.board,
                image=self.back_image,
                relief="raised",
                bd=2,
                command=lambda i=idx: self.on_click(i),
                bg=CARD_BACK_BG,
                activebackground=CARD_BACK_BG
            )
            btn.grid(row=r, column=c, padx=6, pady=6)
            self.buttons.append(btn)

        # 시작 프리뷰: 전부 보여주고 뒤집기
        self.info_var.set("카드를 외우세요!")
        self.show_all_faces()
        self.after(PREVIEW_MS, self.end_preview)

    def end_preview(self):
        self.hide_all_unmatched()
        self.previewing = False
        self.moves = 0
        self.start_time = time.time()
        self.update_info()
        self.schedule_timer()

    def schedule_timer(self):
        self.update_info()
        self.timer_job = self.after(250, self.schedule_timer)

    def elapsed_sec(self):
        if self.start_time is None:
            return 0
        return int(time.time() - self.start_time)

    def update_info(self):
        matched_pairs = len(self.matched) // 2
        total_pairs = self.pair_count
        t = self.elapsed_sec()
        self.info_var.set(f"이동: {self.moves} | 시간: {t}s | 진행: {matched_pairs}/{total_pairs}")

    def show_face(self, idx):
        key = self.cards[idx]
        img = self.face_images[key]
        btn = self.buttons[idx]
        btn.configure(
            image=img,
            relief="sunken",
            state="normal"
        )

    def show_back(self, idx):
        btn = self.buttons[idx]
        btn.configure(
            image=self.back_image,
            relief="raised",
            state="normal",
            bg=CARD_BACK_BG,
            activebackground=CARD_BACK_BG
        )

    def show_all_faces(self):
        for i in range(len(self.cards)):
            self.show_face(i)

    def hide_all_unmatched(self):
        for i in range(len(self.cards)):
            if i not in self.matched:
                self.show_back(i)

    def mark_matched(self, idx):
        btn = self.buttons[idx]
        btn.configure(
            relief="sunken",
            state="disabled"
        )

    def on_click(self, idx):
        if self.previewing or self.locked:
            return
        if idx in self.matched:
            return
        if idx in self.revealed:
            return

        # 카드 공개
        self.show_face(idx)
        self.revealed.append(idx)

        # 첫 장이면 대기
        if len(self.revealed) == 1:
            return

        # 두 장이면 비교
        self.moves += 1
        self.update_info()

        a, b = self.revealed
        if self.cards[a] == self.cards[b]:
            # 매치 성공
            self.matched.add(a)
            self.matched.add(b)
            self.revealed.clear()
            self.mark_matched(a)
            self.mark_matched(b)

            if len(self.matched) == len(self.cards):
                self.finish_game()
        else:
            # 매치 실패 -> 잠깐 보여주고 다시 뒤집기
            self.locked = True
            self.after(MISMATCH_MS, self.flip_back_mismatch)

    def flip_back_mismatch(self):
        for idx in self.revealed:
            if idx not in self.matched:
                self.show_back(idx)
        self.revealed.clear()
        self.locked = False

    def finish_game(self):
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None

        t = self.elapsed_sec()
        msg = f"클리어!\n이동 횟수: {self.moves}\n걸린 시간: {t}초\n\n다시 할까요?"
        if messagebox.askyesno("완료", msg):
            self.new_game()


if __name__ == "__main__":
    MemoryGame().mainloop()
