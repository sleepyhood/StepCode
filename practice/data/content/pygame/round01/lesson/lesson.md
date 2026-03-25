---
id: "py_pygame_intro"
contentType: "lesson"
track: "pygame"
lang: "python"
categoryId: "py_pygame"
title: "Python Pygame 1주차 응용"
status: "active"
order: 275
audience: "common"
tags: [pygame, game, window, event, debug, application]
recommendedSetId: "py_pygame_a01"
relatedSetIds: ["py_pygame_b01", "py_pygame_a01"]
priority: 3
---

# Pygame 1주차 응용 수업

> [!goal]
> 오늘의 목표
> - 지난 시간에 만든 `pygame` 창과 이벤트 코드를 다시 읽을 수 있다.
> - 고장난 코드를 보고 왜 안 되는지 설명할 수 있다.
> - 규칙 1개를 직접 바꾸며 게임을 확장할 수 있다.

## 1) 응용 회차의 중심 구조

이번 회차는 `복사해서 완성`이 아니라 아래 3단계를 한 세트로 묶습니다.

1. 코드 읽기
2. 오류 판단과 수정
3. 규칙 1개 변경

핵심은 "어떤 줄을 써야 하는가"보다 "`왜` 그 줄이 필요한가"를 회수하는 것입니다.

## 2) 이번 회차에서 다시 잡을 개념

원본 1회차 수업에서 실제로 다시 사용하게 되는 개념은 아래 6개입니다.

- `pygame.display.set_mode((가로, 세로))`
- `SURFACE.fill((R, G, B))`
- `for event in pygame.event.get():`
- `if event.type == QUIT:`
- `pygame.display.update()`
- `clock.tick(FPS)`

## 3) 읽기 단계에서 볼 코드

```python
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((400, 300))
pygame.display.set_caption("game")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    SURFACE.fill((255, 255, 255))
    pygame.display.update()
```

이 코드를 읽을 때는 아래 순서로 확인합니다.

1. 창이 언제 만들어지는가
2. 이벤트를 어디서 읽는가
3. 화면을 언제 다시 그리는가
4. 종료 코드는 어떤 조건에서 실행되는가

## 4) 자주 넣기 좋은 오류

응용 회차에서는 아래 같은 오류를 의도적으로 섞는 것이 좋습니다.

- 이벤트 반복문이 빠진 경우
- `pygame.display.update()`가 빠진 경우
- 충돌 대상을 잘못 비교한 경우
- 그리기 순서가 뒤집힌 경우
- `clock.tick()`이 빠진 경우

## 5) 50분 운영 예시

- 10분: 핵심 코드 읽기와 실행 결과 예측
- 20분: 고장난 코드 수정
- 15분: 규칙 1개 바꾸기
- 5분: 오늘 수정한 이유 정리

## 6) 이번 세트의 마무리 질문

마지막에는 반드시 아래 질문을 다시 말하게 합니다.

- 왜 이벤트 처리는 반복문 안에 있어야 하는가?
- 왜 화면 변경 뒤에 `pygame.display.update()`가 필요한가?
- 내가 바꾼 규칙은 어떤 변수나 조건식으로 구현했는가?
