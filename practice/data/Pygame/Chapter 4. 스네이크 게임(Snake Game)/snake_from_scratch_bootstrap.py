# Snake Game (pygame) - 거의 100% 직접 구현용 부트스트랩
# 수업/과제용: 윈도우 생성과 루프 뼈대만 제공하고, 대부분을 학생이 작성합니다.

import pygame
import random
from collections import deque

pygame.init()

# --- 상수/설정 (학생이 조정 가능) ---
CELL = 20
GRID_W, GRID_H = 32, 24
WIDTH, HEIGHT = GRID_W * CELL, GRID_H * CELL
FPS = 12

# 색상 예시(필요하면 수정/추가)
BG    = (18, 18, 18)
GRID  = (32, 32, 32)
SNAKE = (0, 200, 120)
HEAD  = (0, 230, 150)
FOOD  = (220, 70, 70)
WHITE = (240, 240, 240)

# --- 방향 벡터/유틸 ---
UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)
opposite = {UP:DOWN, DOWN:UP, LEFT:RIGHT, RIGHT:LEFT}

# --- TODO: Snake 클래스 구현 ---
# - 속성: body(deque), dir, grow
# - 메서드: head@property, set_dir(역방향 무시), move(), hits_self(), draw()
class Snake:
    def __init__(self, x, y):
        raise NotImplementedError("Snake.__init__ 구현")

    @property
    def head(self):
        raise NotImplementedError("Snake.head 구현")

    def set_dir(self, new_dir):
        raise NotImplementedError("Snake.set_dir 구현")

    def move(self):
        raise NotImplementedError("Snake.move 구현")

    def hits_self(self):
        raise NotImplementedError("Snake.hits_self 구현")

    def draw(self, surf):
        raise NotImplementedError("Snake.draw 구현")

# --- TODO: Food 클래스 구현 ---
# - 속성: pos
# - 메서드: respawn(occupied와 겹치지 않게), draw()
class Food:
    def __init__(self):
        raise NotImplementedError("Food.__init__ 구현")

    def respawn(self, occupied:set):
        raise NotImplementedError("Food.respawn 구현")

    def draw(self, surf):
        raise NotImplementedError("Food.draw 구현")

# --- TODO: Game 클래스 구현 ---
# - 속성: wrap, show_grid, paused, snake, food, score, speed, alive, best, font
# - 메서드: reset(), _speed_schedule(), update(), handle_input(), draw_grid(), draw_hud(), draw()
class Game:
    def __init__(self, wrap=False):
        raise NotImplementedError("Game.__init__ 구현")

    def reset(self):
        raise NotImplementedError("Game.reset 구현")

    def _speed_schedule(self):
        raise NotImplementedError("Game._speed_schedule 구현")

    def update(self):
        raise NotImplementedError("Game.update 구현")

    def handle_input(self, event):
        raise NotImplementedError("Game.handle_input 구현")

    def draw_grid(self, surf):
        raise NotImplementedError("Game.draw_grid 구현")

    def draw_hud(self, surf):
        raise NotImplementedError("Game.draw_hud 구현")

    def draw(self, surf):
        raise NotImplementedError("Game.draw 구현")

# --- TODO: main 루프 구현 ---
def main():
    # 윈도우/시계/표시 설정
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game - From Scratch")
    clock = pygame.time.Clock()

    # 게임 상태 생성
    raise NotImplementedError("main: Game 생성 및 루프 구현")

if __name__ == "__main__":
    main()
