# Python Pygame 기초 1회차 정답

## Q1. 게임창 만들기

- `QUIT`
- `400, 300`
- 제목은 자유
- `QUIT`
- `update`

예시:

```python
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((400, 300))
pygame.display.set_caption("my game")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
```

## Q2. 배경색 바꾸기

- 초록색: `(0, 255, 0)`

## Q3. 종료 이벤트 이해하기

- 정답: `QUIT`

## Q4. 화면 업데이트

- 정답: `update`

## Q5. 도전 과제

- 정답 고정 없음
- 창 크기와 제목을 직접 바꾸었는지 확인
