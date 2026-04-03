---
marp: true
theme: pygame-marp-base
paginate: true
title: Pygame 반완성형 2차시 - 입력과 반복 업데이트
description: 키 입력 처리와 위치 갱신의 기본 구조
---

# Pygame 반완성형 2차시

## 입력과 반복 업데이트

- 오늘의 목표: 입력 처리와 상태 갱신을 분리해서 이해한다.
- 수업 방식: 방향키 이동 코드를 반완성형으로 함께 채운다.

---

# 교사용 진행 흐름

- 이벤트 처리와 위치 계산이 서로 다른 역할이라는 점을 먼저 구분한다.
- 학생이 `한 번 누르면 왜 계속 움직이지 않는지`를 질문하도록 유도한다.
- 마지막에 `속도 변수`를 넣어 코드 구조를 한 단계 확장한다.

---

# 예제 뼈대

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
x = 100
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        x += 5

    screen.fill((30, 30, 40))
    pygame.draw.rect(screen, (80, 180, 255), (x, 250, 60, 60))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```
