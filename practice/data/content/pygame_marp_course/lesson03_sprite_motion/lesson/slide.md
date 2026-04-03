---
marp: true
theme: pygame-marp-base
paginate: true
title: Pygame 반완성형 3차시 - 스프라이트와 움직임 조합
description: 이미지 자산과 움직임을 결합하는 기본 흐름
---

# Pygame 반완성형 3차시

## 스프라이트와 움직임 조합

- 오늘의 목표: 이미지 자산을 불러오고 위치와 움직임을 함께 다룬다.
- 수업 방식: 완성본 제시보다 수정 포인트를 함께 찾는 방식으로 진행한다.

---

# 교사용 진행 흐름

- 도형에서 이미지로 바뀌어도 본질은 `좌표 + 업데이트`라는 점을 강조한다.
- 이미지가 보이지 않을 때 점검할 순서를 먼저 알려 준다.
- 필요하면 마지막에 간단한 충돌 판정의 감각만 소개한다.

---

# 예제 뼈대

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
player = pygame.image.load("player.png")
x, y = 100, 200
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x += 2

    screen.fill((245, 247, 250))
    screen.blit(player, (x, y))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```
