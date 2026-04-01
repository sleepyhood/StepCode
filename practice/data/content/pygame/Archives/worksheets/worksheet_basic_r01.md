---
id: "py_pygame_basic_r01"
contentType: "worksheet"
track: "pygame"
lang: "python"
categoryId: "py_pygame"
title: "Python Pygame 기초 1회차"
round: 1
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---

# Python Pygame 기초 1회차

아래 문제는 `완성 코드 복사`가 아니라 `핵심 부분 채우기`를 목표로 합니다.

### Q1. 게임창 만들기

빈칸을 채워 게임 창이 열리도록 만드세요.

```python
import sys
import pygame
from pygame.locals import ______

pygame.init()
SURFACE = pygame.display.set_mode((____, ____))
pygame.display.set_caption("________")

while True:
    for event in pygame.event.get():
        if event.type == ______:
            pygame.quit()
            sys.exit()

    pygame.display.________()
```

### Q2. 배경색 바꾸기

화면이 초록색이 되도록 RGB 빈칸을 채우세요.

```python
SURFACE.fill((____, ____, ____))
```

### Q3. 종료 이벤트 이해하기

아래 코드의 빈칸을 채우세요.

```python
for event in pygame.event.get():
    if event.type == ______:
        pygame.quit()
        sys.exit()
```

### Q4. 화면 업데이트

화면 변경 사항이 실제로 보이도록 함수 이름을 채우세요.

```python
SURFACE.fill((255, 255, 0))
pygame.display.________()
```

### Q5. 도전 과제

Q1 코드를 바탕으로 아래 2가지를 직접 바꾸세요.

1. 창 크기를 `(300, 500)`으로 바꾸기
2. 제목을 본인 이름이 들어가게 바꾸기
