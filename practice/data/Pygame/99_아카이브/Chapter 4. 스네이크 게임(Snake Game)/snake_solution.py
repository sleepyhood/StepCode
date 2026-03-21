import pygame
import random
from collections import deque

# --- 기본 설정 ---
pygame.init()
CELL = 20
GRID_W, GRID_H = 32, 24
WIDTH, HEIGHT = GRID_W * CELL, GRID_H * CELL
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
FPS = 12

# --- 방향 및 색상 ---
UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)
opposite = {UP:DOWN, DOWN:UP, LEFT:RIGHT, RIGHT:LEFT}

BG    = (18, 18, 18)
GRID  = (32, 32, 32)
SNAKE = (0, 200, 120)
HEAD  = (0, 230, 150)
FOOD  = (220, 70, 70)
WHITE = (240, 240, 240)

class Snake:
    def __init__(self, x, y):
        self.body = deque([(x, y), (x-1, y), (x-2, y)])
        self.dir = RIGHT
        self.grow = False

    @property
    def head(self):
        return self.body[0]

    def set_dir(self, new_dir):
        if opposite.get(self.dir) == new_dir:
            return
        self.dir = new_dir

    def move(self):
        hx, hy = self.head
        dx, dy = self.dir
        new_head = (hx + dx, hy + dy)
        self.body.appendleft(new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def hits_self(self):
        return self.head in list(self.body)[1:]

    def draw(self, surf):
        for i, (x, y) in enumerate(self.body):
            color = HEAD if i == 0 else SNAKE
            pygame.draw.rect(surf, color, (x*CELL, y*CELL, CELL-1, CELL-1), border_radius=4)

class Food:
    def __init__(self):
        self.pos = (0, 0)
        self.respawn(set())

    def respawn(self, occupied: set):
        while True:
            x = random.randrange(GRID_W)
            y = random.randrange(GRID_H)
            if (x, y) not in occupied:
                self.pos = (x, y)
                break

    def draw(self, surf):
        x, y = self.pos
        pygame.draw.rect(surf, FOOD, (x*CELL, y*CELL, CELL-1, CELL-1), border_radius=6)

class Game:
    def __init__(self, wrap=False):
        self.wrap = wrap
        self.reset()
        self.best = 0
        self.font = pygame.font.SysFont("malgungothic", 24)

    def reset(self):
        cx, cy = GRID_W//2, GRID_H//2
        self.snake = Snake(cx, cy)
        self.food = Food()
        self.food.respawn(set(self.snake.body))
        self.score = 0
        self.speed = FPS
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.snake.move()
        hx, hy = self.snake.head

        if self.wrap:
            hx %= GRID_W
            hy %= GRID_H
            self.snake.body[0] = (hx, hy)
        else:
            if not (0 <= hx < GRID_W and 0 <= hy < GRID_H):
                self.alive = False
                return

        if self.snake.hits_self():
            self.alive = False
            return

        if self.snake.head == self.food.pos:
            self.snake.grow = True
            self.score += 1
            if self.score % 5 == 0:
                self.speed = min(self.speed + 1, 30)
            self.food.respawn(set(self.snake.body))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.set_dir(UP)
            elif event.key == pygame.K_DOWN:
                self.snake.set_dir(DOWN)
            elif event.key == pygame.K_LEFT:
                self.snake.set_dir(LEFT)
            elif event.key == pygame.K_RIGHT:
                self.snake.set_dir(RIGHT)

    def draw_grid(self, surf):
        for x in range(GRID_W):
            pygame.draw.line(surf, GRID, (x*CELL, 0), (x*CELL, HEIGHT))
        for y in range(GRID_H):
            pygame.draw.line(surf, GRID, (0, y*CELL), (WIDTH, y*CELL))

    def draw_hud(self, surf):
        self.best = max(self.best, self.score)
        msg = f"점수: {self.score}   최고: {self.best}   모드: {'래핑' if self.wrap else '벽충돌'}"
        surf.blit(self.font.render(msg, True, WHITE), (10, 8))
        if not self.alive:
            center = WIDTH//2 - 140, HEIGHT//2 - 20
            surf.blit(self.font.render("게임 오버! R:다시 시작, M:모드 전환", True, WHITE), center)

    def draw(self, surf):
        surf.fill(BG)
        self.draw_grid(surf)
        self.food.draw(surf)
        self.snake.draw(surf)
        self.draw_hud(surf)

def main():
    game = Game(wrap=False)
    running = True
    tick_acc = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    game.reset()
                elif event.key == pygame.K_m:
                    game.wrap = not game.wrap
                    game.reset()
                else:
                    game.handle_input(event)

        clock.tick(60)
        tick_acc += game.speed / 60
        while tick_acc >= 1:
            game.update()
            tick_acc -= 1

        game.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
