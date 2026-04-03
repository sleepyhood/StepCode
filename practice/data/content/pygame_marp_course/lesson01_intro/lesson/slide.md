---
marp: true
theme: pygame-marp-base
paginate: true
title: Pygame 반완성형 1차시 - 시작과 화면 구성
description: 실행 환경, 창 생성, 기본 게임 루프 도입
---

# Pygame 반완성형 1차시

## 시작과 화면 구성

- 오늘의 목표: 창을 띄우고, 닫고, 반복 구조를 이해한다.
- 수업 방식: 완성 코드 전달이 아니라 빈칸과 수정 포인트를 함께 채운다.

---

# 교사용 진행 흐름

- 왜 `while` 반복이 필요한지 먼저 말로 설명한다.
- 학생이 `창이 계속 살아 있는 이유`를 코드 없이 추측하게 한다.
- 마지막에 최소 실행 예제를 함께 완성한다.

---

# 최소 실행 예제

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
```
