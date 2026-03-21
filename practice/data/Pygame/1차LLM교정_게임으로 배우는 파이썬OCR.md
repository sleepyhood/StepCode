# 게임으로 배우는 파이썬: Pygame 입문 교재

이 문서는 OCR로 추출된 원문을 바탕으로, 바로 실습할 수 있도록 Pygame 학습 내용을 교정하고 재구성한 자료입니다.  
설명은 `초기화 -> 화면 설정 -> 메인 루프 -> 이벤트 처리 -> 업데이트 -> 그리기` 흐름에 맞춰 정리했습니다.

## Pygame 준비하기

Pygame은 파이썬으로 2D 게임을 만들 때 많이 사용하는 라이브러리입니다. 화면을 만들고, 키보드와 마우스 입력을 받고, 도형과 이미지를 그리는 기능을 제공합니다.

설치가 아직 되어 있지 않다면 다음 명령으로 설치해 보세요.

```bash
pip install pygame
```

설치가 끝났다면 파이썬에서 아래 코드가 오류 없이 실행되는지 확인합니다.

```python
import pygame
print(pygame.ver)
```

## Pygame 프로그램의 기본 구조

Pygame 프로그램은 대부분 다음 순서로 작성합니다.

1. `pygame.init()`으로 라이브러리를 초기화합니다.
2. `pygame.display.set_mode()`로 화면을 만듭니다.
3. `while True:` 또는 실행 플래그를 사용해 메인 루프를 만듭니다.
4. `pygame.event.get()`으로 이벤트를 처리합니다.
5. 게임 상태를 업데이트합니다.
6. 화면을 지우고, 다시 그리고, `pygame.display.update()` 또는 `pygame.display.flip()`으로 반영합니다.

이 반복 구조를 `이벤트 루프(Event Loop)` 또는 `메인 루프(Main Loop)`라고 합니다.

---

## 1. 가장 단순한 Pygame 창 만들기

먼저 빈 창 하나를 띄워 보겠습니다.

```python
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
surface = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Just Window")


def main():
    while True:
        surface.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main()
```

### 핵심 설명

1. `pygame.init()`은 Pygame의 여러 기능을 사용할 준비를 합니다.
2. `pygame.display.set_mode((400, 300))`은 가로 400, 세로 300 크기의 창을 만듭니다.
3. `surface.fill((255, 255, 255))`은 화면 전체를 흰색으로 칠합니다.
4. `pygame.event.get()`은 이벤트 큐에 들어온 이벤트를 하나씩 꺼냅니다.
5. `QUIT` 이벤트가 발생하면 창 닫기 버튼을 누른 것이므로 프로그램을 종료합니다.
6. `pygame.display.update()`를 호출해야 화면에 그린 내용이 실제 창에 반영됩니다.

---

## 2. 이벤트 루프(Event Loop) 이해하기

창이 열려 있는 동안에는 마우스 이동, 마우스 클릭, 키 입력, 창 닫기 같은 사건이 계속 발생합니다. 이런 사건을 `이벤트(Event)`라고 합니다.

Pygame은 이 이벤트들을 내부의 이벤트 큐에 저장합니다. 프로그램은 메인 루프 안에서 이벤트를 하나씩 꺼내 처리합니다.

기본 골격은 항상 비슷합니다.

```python
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 업데이트

    # 그리기
    pygame.display.update()
```

게임을 만들 때는 이 구조를 확실히 익혀 두는 것이 중요합니다.

---

## 3. 프레임 레이트와 타이머

메인 루프를 아무 제어 없이 돌리면 CPU를 과도하게 사용하게 됩니다. 그래서 보통 `Clock` 객체를 사용해 프레임 레이트를 제한합니다.

```python
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
surface = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()


def main():
    sysfont = pygame.font.SysFont(None, 36)
    counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        counter += 1

        surface.fill((0, 0, 0))
        count_image = sysfont.render(f"count is {counter}", True, (225, 225, 225))
        surface.blit(count_image, (50, 50))

        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main()
```

### 핵심 설명

1. `pygame.time.Clock()`으로 시계 객체를 만듭니다.
2. `clock.tick(10)`은 초당 10프레임 정도로 루프가 돌도록 속도를 조절합니다.
3. 이 방식은 CPU 사용량을 줄이고, 게임의 속도를 일정하게 유지하는 데 도움이 됩니다.

---

## 4. 색상과 좌표계

Pygame의 색상은 RGB 튜플로 표현합니다.

- `(0, 0, 0)`: 검정
- `(255, 255, 255)`: 흰색
- `(255, 0, 0)`: 빨강
- `(0, 255, 0)`: 초록
- `(0, 0, 255)`: 파랑
- `(255, 255, 0)`: 노랑

좌표계는 수학 시간에 배운 좌표계와 다릅니다.

1. 원점 `(0, 0)`은 화면의 왼쪽 위입니다.
2. 오른쪽으로 갈수록 `x` 값이 커집니다.
3. 아래로 갈수록 `y` 값이 커집니다.

즉, Pygame에서는 `y`가 아래 방향으로 증가한다는 점을 꼭 기억해 두세요.

---

## 5. Rect 클래스 이해하기

Pygame에서 위치와 크기를 함께 다룰 때는 `Rect` 클래스를 자주 사용합니다.

```python
import pygame
from pygame import Rect

r = Rect(30, 20, 60, 40)

print(r.x, r.y)
print(r.width, r.height)
print(r.center)
print(r.bottomleft)
```

### Rect를 만드는 방법

```python
Rect(left, top, width, height)
Rect((left, top), (width, height))
```

### 자주 쓰는 프로퍼티

- `x`, `y`
- `top`, `left`, `bottom`, `right`
- `center`, `centerx`, `centery`
- `width`, `height`
- `topleft`, `bottomleft`, `topright`, `bottomright`

### 자주 쓰는 메서드

- `move(x, y)`: 이동한 새 Rect를 반환합니다.
- `move_ip(x, y)`: 자기 자신을 직접 이동합니다.
- `collidepoint(x, y)`: 점이 Rect 안에 있는지 검사합니다.
- `colliderect(other)`: 다른 Rect와 충돌하는지 검사합니다.

`_ip`가 붙은 메서드는 객체 자체를 직접 바꾸는 메서드라고 이해하면 됩니다.

---

## 6. 기본 도형 그리기

Pygame은 `pygame.draw` 모듈로 여러 도형을 그릴 수 있습니다.

### 6-1. 직사각형 그리기

```python
import sys
import pygame
from pygame.locals import QUIT, Rect

pygame.init()
surface = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        surface.fill((255, 255, 255))

        pygame.draw.rect(surface, (255, 0, 0), (10, 20, 100, 50))
        pygame.draw.rect(surface, (255, 0, 0), (150, 10, 100, 30), 3)
        pygame.draw.rect(surface, (0, 255, 0), ((100, 80), (80, 50)))

        rect0 = Rect(200, 60, 140, 80)
        pygame.draw.rect(surface, (0, 0, 255), rect0)

        rect1 = Rect((30, 160), (100, 50))
        pygame.draw.rect(surface, (255, 255, 0), rect1)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
```

### 6-2. 원 그리기

```python
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
surface = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        surface.fill((255, 255, 255))

        pygame.draw.circle(surface, (255, 0, 0), (50, 50), 20)
        pygame.draw.circle(surface, (255, 0, 0), (150, 50), 20, 10)
        pygame.draw.circle(surface, (0, 255, 0), (50, 150), 10)
        pygame.draw.circle(surface, (0, 255, 0), (150, 150), 20)
        pygame.draw.circle(surface, (0, 255, 0), (250, 150), 30)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
```

### 6-3. 타원 그리기

```python
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
surface = pygame.display.set_mode((400, 250))
clock = pygame.time.Clock()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        surface.fill((255, 255, 255))

        pygame.draw.ellipse(surface, (255, 0, 0), (50, 50, 140, 60))
        pygame.draw.ellipse(surface, (255, 0, 0), (250, 30, 90, 90))
        pygame.draw.ellipse(surface, (0, 255, 0), (50, 150, 110, 60), 5)
        pygame.draw.ellipse(surface, (0, 255, 0), ((250, 130), (90, 90)), 20)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
```

### 6-4. 선과 다각형 그리기

```python
import sys
from math import sin, cos, radians
import pygame
from pygame.locals import QUIT

pygame.init()
surface = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        surface.fill((0, 0, 0))

        pygame.draw.line(surface, (255, 0, 0), (10, 80), (200, 80))
        pygame.draw.line(surface, (255, 0, 0), (10, 150), (200, 150), 15)
        pygame.draw.line(surface, (0, 255, 0), (250, 30), (250, 200))

        start_pos = (300, 30)
        end_pos = (380, 200)
        pygame.draw.line(surface, (0, 0, 255), start_pos, end_pos, 10)

        pointlist0 = []
        pointlist1 = []

        for theta in range(0, 360, 72):
            rad = radians(theta)
            pointlist0.append((cos(rad) * 70 + 100, sin(rad) * 70 + 150))
            pointlist1.append((cos(rad) * 70 + 300, sin(rad) * 70 + 150))

        pygame.draw.lines(surface, (255, 255, 255), True, pointlist0, 3)
        pygame.draw.polygon(surface, (200, 200, 0), pointlist1)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
```

---

## 7. 마우스 입력 처리하기

이번에는 마우스를 누른 상태에서 움직인 궤적을 그려 보겠습니다.

```python
import sys
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP

pygame.init()
surface = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()


def main():
    mouse_positions = []
    mouse_down = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_down = True
            elif event.type == MOUSEMOTION:
                if mouse_down:
                    mouse_positions.append(event.pos)
            elif event.type == MOUSEBUTTONUP:
                mouse_down = False
                mouse_positions.clear()

        surface.fill((255, 255, 255))

        if len(mouse_positions) > 1:
            pygame.draw.lines(surface, (255, 0, 0), False, mouse_positions, 3)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
```

### 핵심 설명

1. `MOUSEBUTTONDOWN`은 마우스 버튼을 눌렀을 때 발생합니다.
2. `MOUSEMOTION`은 마우스를 움직일 때 발생합니다.
3. `event.pos`에는 현재 마우스 좌표가 들어 있습니다.
4. `pygame.draw.lines()`를 사용하면 좌표 목록을 이어서 선을 그릴 수 있습니다.

---

## 8. 키보드 입력 처리하기

이번에는 방향키로 사각형을 움직여 보겠습니다. 원문에서는 이미지를 이동했지만, 실습이 더 쉽도록 도형 버전으로 정리했습니다.

```python
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN

pygame.init()
pygame.key.set_repeat(5, 5)
surface = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()


def main():
    rect = pygame.Rect(180, 130, 40, 40)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    rect.x -= 5
                elif event.key == K_RIGHT:
                    rect.x += 5
                elif event.key == K_UP:
                    rect.y -= 5
                elif event.key == K_DOWN:
                    rect.y += 5

        rect.x %= 400
        rect.y %= 300

        surface.fill((225, 225, 225))
        pygame.draw.rect(surface, (30, 120, 255), rect)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
```

### 핵심 설명

1. `KEYDOWN` 이벤트는 키를 눌렀을 때 발생합니다.
2. `event.key`로 어떤 키가 눌렸는지 확인합니다.
3. `pygame.key.set_repeat(5, 5)`는 키를 계속 누르고 있을 때 반복 입력이 들어오도록 도와줍니다.
4. `%` 연산을 사용하면 화면 바깥으로 나간 도형이 반대편에서 다시 나타나게 만들 수 있습니다.

---

## 9. 매 프레임마다 화면을 다시 그리는 이유

게임 화면은 보통 매 프레임마다 다음 순서로 처리합니다.

1. 배경을 지웁니다.
2. 현재 상태를 기준으로 모든 요소를 다시 그립니다.
3. 화면에 반영합니다.

예를 들어 아래 코드는 거의 모든 Pygame 프로그램에서 반복됩니다.

```python
surface.fill((0, 0, 0))

# 게임 오브젝트 그리기

pygame.display.update()
```

이 과정을 생략하면 이전 프레임의 그림이 화면에 남아서 잔상이 생길 수 있습니다.

---

## 10. 종합 실습: 방향키로 움직이는 플레이어 만들기

지금까지 배운 내용을 한 번에 정리하는 실습입니다. 이 예제는 게임의 기본 구조를 가장 명확하게 보여 줍니다.

```python
import sys
import pygame
from pygame.locals import QUIT, K_LEFT, K_RIGHT, K_UP, K_DOWN

WIDTH = 640
HEIGHT = 480
FPS = 60
BG_COLOR = (20, 20, 30)
PLAYER_COLOR = (80, 220, 160)
PLAYER_SPEED = 5


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Basic Loop")
    clock = pygame.time.Clock()

    player = pygame.Rect(300, 220, 40, 40)

    while True:
        ### 1. 이벤트 처리
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        ### 2. 상태 업데이트
        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            player.x -= PLAYER_SPEED
        if keys[K_RIGHT]:
            player.x += PLAYER_SPEED
        if keys[K_UP]:
            player.y -= PLAYER_SPEED
        if keys[K_DOWN]:
            player.y += PLAYER_SPEED

        player.x = max(0, min(player.x, WIDTH - player.width))
        player.y = max(0, min(player.y, HEIGHT - player.height))

        ### 3. 화면 그리기
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, PLAYER_COLOR, player)
        pygame.display.update()

        ### 4. 프레임 속도 제어
        clock.tick(FPS)


if __name__ == "__main__":
    main()
```

### 이 예제로 꼭 확인할 점

1. 초기화는 `pygame.init()`에서 시작합니다.
2. 화면 설정은 `pygame.display.set_mode()`가 담당합니다.
3. 메인 루프 안에서 이벤트 처리, 상태 업데이트, 그리기를 반복합니다.
4. `pygame.key.get_pressed()`를 사용하면 현재 눌린 키 상태를 계속 확인할 수 있습니다.
5. `Rect`를 사용하면 플레이어 위치와 크기를 간단하게 관리할 수 있습니다.

---

## 11. 정리

이번 장에서 익혀야 할 핵심은 다음과 같습니다.

1. Pygame 프로그램은 메인 루프 중심으로 동작합니다.
2. 이벤트 처리는 `pygame.event.get()`으로 수행합니다.
3. 프레임 레이트는 `pygame.time.Clock()`으로 제어합니다.
4. 위치와 크기는 `Rect`로 다루면 편리합니다.
5. 그리기는 `pygame.draw`와 `Surface.blit()`를 중심으로 이루어집니다.
6. 게임은 결국 `입력 처리 -> 상태 변경 -> 화면 갱신`의 반복입니다.

이제 여기까지의 예제를 직접 실행하고, 색상이나 속도, 좌표, 도형 크기를 바꿔 보세요. 직접 수정해 보면서 익히는 것이 가장 빠른 학습 방법입니다.
