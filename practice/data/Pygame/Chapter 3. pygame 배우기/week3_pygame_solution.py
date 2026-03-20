# Week 3 - pygame 기본기 (From Scratch 과제) 풀이
# TODO에 대응하는 완성 해답입니다.

import pygame
import random
from dataclasses import dataclass
import math

# ------------------------------ 상수 ------------------------------
WIDTH, HEIGHT = 800, 600      # TODO 1
FPS_START = 60
PLAYER_SIZE = 28
PLAYER_SPEED = 220            # px/s (기본값)
TARGET_RADIUS = 12
SPEED_STEP_SCORE = 5          # TODO 10
FONT_NAME = "malgungothic"
BG = (18, 18, 18)
FG = (230, 230, 230)
GRID = (40, 40, 40)
PLAYER_COLOR = (0, 200, 120)
TARGET_COLOR = (220, 70, 70)

def clamp(value, low, high):
    return max(low, min(value, high))

@dataclass
class Player:
    x: float
    y: float
    w: int = PLAYER_SIZE
    h: int = PLAYER_SIZE
    vx: float = 0.0
    vy: float = 0.0

    # TODO 6: 입력/속도/위치/경계
    def update(self, dt, keys, speed):
        # 방향 결정: 화살표 또는 WASD
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN]  or keys[pygame.K_s]) - (keys[pygame.K_UP]   or keys[pygame.K_w])
        # 대각선 이동 보정
        mag = math.hypot(dx, dy)
        if mag > 0:
            dx /= mag
            dy /= mag
        self.vx = dx * speed
        self.vy = dy * speed

        self.x += self.vx * dt
        self.y += self.vy * dt

        # 경계 클램프
        self.x = clamp(self.x, 0, WIDTH - self.w)
        self.y = clamp(self.y, 0, HEIGHT - self.h)

    # TODO 4: 그리기
    def draw(self, surf):
        pygame.draw.rect(surf, PLAYER_COLOR, (int(self.x), int(self.y), self.w, self.h), border_radius=6)

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

@dataclass
class Target:
    x: float
    y: float
    r: int = TARGET_RADIUS

    # TODO 8: 원 그리기
    def draw(self, surf):
        pygame.draw.circle(surf, TARGET_COLOR, (int(self.x), int(self.y)), self.r)

    @property
    def pos(self):
        return (int(self.x), int(self.y))

class Game:
    def __init__(self):
        # TODO 2: 초기화/화면/시계/폰트/상태
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Week 3 Collect Game - Solution")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(FONT_NAME, 24)

        self.reset()

    def reset(self):
        self.player = Player(WIDTH//2 - PLAYER_SIZE//2, HEIGHT//2 - PLAYER_SIZE//2)
        self.score = 0
        self.best = 0
        self.player_speed = PLAYER_SPEED
        self.target = None
        self.running = True
        self.show_grid = True
        self.pick_sound = None  # (옵션) mixer를 사용할 수 있음
        self.spawn_target()

    # TODO 3: 메인 루프
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS_START) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_g:
                        self.show_grid = not self.show_grid

            self.handle_input(dt)
            self.check_collision()
            self.draw()

        pygame.quit()

    # TODO 5: 입력 처리
    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys, self.player_speed)

    # TODO 7: 타겟 스폰
    def spawn_target(self):
        r = TARGET_RADIUS
        x = random.randint(r, WIDTH - r)
        y = random.randint(r, HEIGHT - r)
        self.target = Target(x, y, r)

    # 충돌 보조: 원-사각형 충돌(정확)
    def circle_rect_collide(self, circle_pos, r, rect: pygame.Rect):
        cx, cy = circle_pos
        # 사각형에 대한 최근접점
        nearest_x = clamp(cx, rect.left, rect.right)
        nearest_y = clamp(cy, rect.top, rect.bottom)
        dx = cx - nearest_x
        dy = cy - nearest_y
        return (dx*dx + dy*dy) <= (r*r)

    # TODO 9: 충돌판정
    def check_collision(self):
        if self.target and self.circle_rect_collide(self.target.pos, self.target.r, self.player.rect):
            self.on_score()

    # TODO 10: 점수/난이도
    def on_score(self):
        self.score += 1
        self.best = max(self.best, self.score)
        # 속도 상승: 5점마다 +10% (상한선 2.0배)
        if self.score % SPEED_STEP_SCORE == 0:
            self.player_speed = min(self.player_speed * 1.1, PLAYER_SPEED * 2.0)
        # (옵션) 타겟 반지름을 점차 줄여 난이도 상승
        new_r = max(6, int(self.target.r * 0.98))
        self.target = None
        self.target = Target(0, 0, new_r)
        self.spawn_target()
        # (옵션) 사운드
        if self.pick_sound:
            self.pick_sound.play()

    def draw_grid(self):
        if not self.show_grid:
            return
        for x in range(0, WIDTH, 20):
            pygame.draw.line(self.screen, GRID, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 20):
            pygame.draw.line(self.screen, GRID, (0, y), (WIDTH, y))

    # TODO 4/8: 렌더
    def draw(self):
        self.screen.fill(BG)
        self.draw_grid()
        if self.target:
            self.target.draw(self.screen)
        self.player.draw(self.screen)

        # HUD
        hud = f"점수: {self.score}   최고: {self.best}   속도: {int(self.player_speed)}   [←↑→↓/WASD 이동, R 재시작, G 그리드]"
        self.screen.blit(self.font.render(hud, True, FG), (10, 8))

        pygame.display.flip()

if __name__ == "__main__":
    Game().run()
