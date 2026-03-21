# 0) 준비하기

1. 파이썬과 pygame 설치

```bash
pip install pygame
```

2. 작업 폴더를 만들고 `main.py` 파일을 생성해요. 이후 코드는 `main.py`에 붙여넣고 실행(▶)합니다.

---

# 4.1 스네이크 게임 규칙

* 뱀은 격자(Grid) 위를 이동합니다. (한 번에 한 칸)
* 방향키(↑↓←→)로 진행 방향을 바꿀 수 있지만 **즉시 반대로**(예: 왼쪽→오른쪽) 꺾을 수는 없게 합니다.
* 빨간 먹이를 먹으면 뱀의 길이가 1칸 늘고, 점수가 올라갑니다.
* 벽 또는 자기 몸과 **충돌**하면 게임 오버.
* (옵션) 벽을 통과해서 반대편으로 나오는 **래핑(wrap-around)** 모드.
* (옵션) 점수가 오를수록 게임이 조금씩 빨라지도록.

✔ 체크포인트: 규칙을 구체적으로 정리했나요? ‘벽에 부딪히면 끝 vs 반대편으로 나오기’ 같은 룰을 실습 중에 토글할 예정입니다.

---

# 4.2 스네이크 게임 만들기

아래는 **격자 단위**로 움직이는 전형적인 스네이크 구현입니다. 단계별로 코드를 추가해 보세요.

## 4.2.1 패키지 import

```python
import pygame
import random
from collections import deque
```

## 4.2.2 게임 화면 구성

* 격자 크기와 화면 크기를 먼저 정합니다.
* 시계를 만들어 FPS를 제한합니다.

```python
# --- 초기 설정 ---
pygame.init()

CELL = 20          # 격자 한 칸(px)
GRID_W, GRID_H = 32, 24  # 격자 수(가로 x 세로)
WIDTH, HEIGHT = GRID_W * CELL, GRID_H * CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
FPS = 12  # 시작 속도(프레임)
```

✔ 체크포인트: 까만 창이 켜지고 닫히면 OK.

## 4.2.3 방향 개념 이해

* 방향은 (dx, dy) **벡터**로 표현합니다.
* 너무 빠른 방향 전환(정반대) 방지를 위해, 현재 진행 방향의 **역방향 입력은 무시**합니다.

```python
# --- 방향 상수 ---
UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)

opposite = {UP:DOWN, DOWN:UP, LEFT:RIGHT, RIGHT:LEFT}
```

## 4.2.4 색상 정의

```python
# --- 색상 ---
BG    = (18, 18, 18)
GRID  = (32, 32, 32)
SNAKE = (0, 200, 120)
HEAD  = (0, 230, 150)
FOOD  = (220, 70, 70)
WHITE = (240, 240, 240)
```

## 4.2.5 뱀 객체 정의

* 몸통은 큐/데크로 관리하면 **앞에 머리를 추가, 뒤를 제거**하기 편합니다.
* `grow` 플래그가 True일 때는 꼬리를 제거하지 않아 길이가 늘어납니다.

```python
class Snake:
    def __init__(self, x, y):
        self.body = deque([(x, y), (x-1, y), (x-2, y)])  # 머리, 몸, 꼬리
        self.dir = RIGHT
        self.grow = False

    @property
    def head(self):
        return self.body[0]

    def set_dir(self, new_dir):
        # 정반대 입력 무시
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
```

## 4.2.6 먹이 객체 정의

* 먹이는 뱀 몸통과 **겹치지 않게** 스폰합니다.

```python
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
```

## 4.2.7 게임 객체 정의

* **벽 충돌 vs 래핑**: 토글 가능하도록 옵션으로 둡니다.
* 점수, 최고점(세션 기준), 속도 증가 등을 관리합니다.

```python
class Game:
    def __init__(self, wrap=False):
        self.wrap = wrap
        self.reset()
        self.best = 0
        self.font = pygame.font.SysFont("malgungothic", 24)  # 한글 OK(윈도우)

    def reset(self):
        cx, cy = GRID_W//2, GRID_H//2
        self.snake = Snake(cx, cy)
        self.food = Food()
        self.food.respawn(set(self.snake.body))
        self.score = 0
        self.speed = FPS  # 시작 속도
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.snake.move()
        hx, hy = self.snake.head

        # 벽 처리
        if self.wrap:
            hx %= GRID_W
            hy %= GRID_H
            # 머리 좌표를 래핑 적용하여 갱신
            self.snake.body[0] = (hx, hy)
        else:
            if not (0 <= hx < GRID_W and 0 <= hy < GRID_H):
                self.alive = False
                return

        # 자기 몸 충돌
        if self.snake.hits_self():
            self.alive = False
            return

        # 먹이 체크
        if self.snake.head == self.food.pos:
            self.snake.grow = True
            self.score += 1
            if self.score % 5 == 0:  # 5점마다 속도 증가(최대 30)
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
```

## 4.2.8 메인 함수 정의

* `R`로 재시작, `M`으로 모드(벽/래핑) 전환, `ESC`로 종료.

```python
def main():
    game = Game(wrap=False)
    running = True
    tick_acc = 0

    while running:
        # --- 입력 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    game.reset()
                elif event.key == pygame.K_m:
                    # 모드 전환(벽 <-> 래핑)
                    game.wrap = not game.wrap
                    game.reset()
                else:
                    game.handle_input(event)

        # --- 업데이트(속도에 맞춰 이동) ---
        clock.tick(60)  # 최대 60 FPS로 그리기
        tick_acc += game.speed / 60  # speed가 클수록 자주 이동
        while tick_acc >= 1:
            game.update()
            tick_acc -= 1

        # --- 그리기 ---
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
```

✔ 체크포인트: 뱀이 먹이를 먹으면 길이가 늘고 점수가 오릅니다. 자기 몸/벽에 부딪히면 게임 오버가 뜨고 `R`로 다시 시작됩니다. `M`으로 래핑 모드가 잘 전환되면 성공!

---

# 4.3 스네이크 게임 실행

```bash
python main.py
```

* 방향키로 조작하세요. `R`: 다시 시작, `M`: 모드 전환(벽↔래핑), `ESC`: 종료.

---

# 4.4 스네이크 게임 실행 파일 만들기

> **PyInstaller**로 단일 실행 파일을 만들어 배포할 수 있습니다.

### Windows

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

* `dist/main.exe` 생성. 아이콘을 넣고 싶다면 `--icon=icon.ico` 옵션을 추가하세요.

### macOS (Intel/Apple Silicon)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

* 최초 실행 시 "확인되지 않은 개발자" 경고가 뜰 수 있어요. 우클릭→열기(또는 시스템 설정→보안 및 개인 정보 보호에서 허용).
* 아이콘: `--icon=icon.icns`.

### 팁

* 리소스(이미지/사운드)가 있다면 **상대 경로** 처리 필요. 이번 예제는 리소스를 쓰지 않아 간단합니다.
* 바이러스 오탐 방지를 위해 배포 전 **압축(zip)** 으로 묶어 전달하는 것을 권장.

---

# 4.5 다양한 스네이크 게임 (확장 과제)

아래 과제를 하나씩 적용해 보세요. (교사용 풀이 힌트는 수업 후 공유)

## A. 난이도/속도 조절

* 점수 3/6/9… 마다 `speed += 1`
* **실습(빈칸)**: 최고 속도를 45로 올리되, 20점 이후에는 2점마다 1씩만 증가하도록 바꿔 보세요.

## B. 장애물(Obstacle)

* 무작위 위치에 벽 블록을 몇 개 생성하고, 뱀이 부딪히면 게임 오버.
* **실습)** `Game.reset()`에서 `self.obstacles = {(x,y), ...}` 생성 후, `draw()`와 충돌 체크에 반영.

## C. 포탈(Portal)

* 서로 연결된 두 타일을 만들어 들어가면 반대 포탈에서 나옴.
* **실습)** `self.portals = {(x1,y1):(x2,y2), (x2,y2):(x1,y1)}` 딕셔너리를 두고, 이동 후 머리가 포탈에 있으면 좌표를 치환.

## D. 독/버프 아이템

* **독(보라색)**: 먹으면 점수 -1, 몸이 1칸 줄어듦.
* **버프(노란색)**: 5초간 래핑 강제 ON 또는 속도 1.5배.
* 아이템은 일정 시간 후 사라지게(`spawn_time` 비교) 만들어 보세요.

## E. 페널티/보너스 규칙

* 10초 동안 먹이를 못 먹으면 자동 실패.
* 직선으로만 N칸 이상 달리면 보너스 +1.

## F. UI/연출

* 일시정지(`P`) 구현: `paused` 상태에서 업데이트 정지.
* 머리/몸 색상 그라데이션, 먹을 때 **점수 팝업 텍스트**.
* 그리드 끄기/켜기(`G`) 토글.

---

# 부록) 디버깅 팁

* **좌표 보정**: "왜 벽에 박지?" → `print(self.snake.head)`로 이동 좌표를 살펴보고, 격자 범위 검사/래핑 로직을 확인하세요.
* **속도/루프**: `tick_acc` 산술이 이상하면 한 번에 두 칸 움직이는 느낌이 날 수 있어요. `while tick_acc >= 1:` 루프가 너무 많이 돌지 않는지 체크.
* **입력 큐**: 빠르게 반대 키를 눌러도 역방향이 무시되는지 테스트.

---

# (참고) 최종 코드 한 번에 보기

> 위에서 단계별로 만들었지만, 아래는 하나로 합친 동작 예시입니다. 그대로 붙여넣어 실행해도 됩니다.

```python
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
```

✔ 체크포인트: 최종 코드가 잘 실행되면, 이제 확장 과제를 통해 "자신만의 스네이크"로 발전시켜 보세요!
