---
id: "py_pygame_application_r01"
contentType: "worksheet"
track: "pygame"
lang: "python"
categoryId: "py_pygame"
title: "Python Pygame 응용 1회차"
round: 1
difficulty: "application"
status: "active"
audience: "common"
printDefault: true
---

# Python Pygame 응용 1회차

이번 회차는 `읽기 -> 버그 수정 -> 규칙 변경` 순서로 진행합니다.
정답만 쓰지 말고, 왜 그렇게 고쳤는지도 함께 설명해 보세요.

### Q1. 이동 코드 읽기

아래 코드를 읽고, 각 입력이 끝난 직후 `velocity_x`와 `player_x` 값을 표에 채우세요.

```python
player_x = 100
velocity_x = 0
events = ["RIGHT", "RIGHT", "LEFT"]

for key in events:
    if key == "RIGHT":
        velocity_x = 10
    elif key == "LEFT":
        velocity_x = -10

    player_x += velocity_x
```

| 입력 | velocity_x | player_x |
|---|---:|---:|
| RIGHT |  |  |
| RIGHT |  |  |
| LEFT |  |  |

### Q2. 그리기 순서 예측

아래 코드는 같은 위치 `(100, 100)`에 두 이미지를 차례로 그립니다.
화면 맨 위에 보이는 이미지는 무엇인지 쓰세요.

```python
SURFACE.fill((255, 255, 255))
SURFACE.blit(player_img, (100, 100))
SURFACE.blit(enemy_img, (100, 100))
pygame.display.update()
```

### Q3. 이벤트 처리 버그 수정

아래 코드는 창 닫기 버튼을 눌러도 정상 종료되지 않습니다.
`# TODO` 위치에 한 줄을 추가해 문제를 고치세요.

```python
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((400, 300))

while True:
    SURFACE.fill((0, 0, 0))
    # TODO: 여기에 한 줄 작성
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
```

### Q4. 충돌 판정 버그 수정

의도는 `총알이 적과 부딪히면 점수가 1 올라간다`입니다.
하지만 현재 코드는 잘못된 두 대상을 비교하고 있습니다.
`if` 한 줄을 올바르게 고치세요.

```python
if player_rect.colliderect(bullet_rect):
    score += 1
```

### Q5. 규칙 변경 미션

점수가 10점 이상이면 적 속도를 `7`로 올리려고 합니다.
아래 `if`문의 조건식 부분만 작성하세요.

```python
score = 12
enemy_speed = 4

if __________________:
    enemy_speed = 7
```

### Q6. 마무리 체크

아래 질문에 짧게 답하세요.

1. `for event in pygame.event.get():`가 반복문 안에 있어야 하는 이유는 무엇인가요?
2. `pygame.display.update()`를 빼면 화면에서 어떤 문제가 생기나요?
