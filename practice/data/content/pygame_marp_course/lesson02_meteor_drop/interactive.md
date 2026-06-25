---
id: "pygame_u02"
contentType: "lesson"
track: "pygame_project"
lang: "python"
categoryId: "pygame_project_ship_u02"
title: "2차시. 운석 낙하와 리스트 관리"
status: "active"
order: 102
audience: "common"
tags: ["pygame", "meteor", "list", "random"]
---

# 2차시. 운석 낙하와 리스트 관리

---

# 목차

- **2.1. 운석 공장 가동하기 (Spawn)**
  - 무작위 위치 설정 및 리스트 추가
- **2.2. 무한 낙하와 메모리 청소 (Update)**
  - 다중 객체 이동 및 화면 밖 삭제
- **2.3. 엔진의 심장: 타이머 (Engine)**
  - 주기적인 이벤트 발생 원리 이해

![우주선 예시](assets/output_animation.gif)

---

# 실습 파일 구조

<div class="code-window">

```python
import pygame
import sys
import random

# =========================================================
# 🧑‍💻 [학생 작업 구역] 1차시 코드 (완성) + 2차시: 운석 생성과 낙하
# =========================================================

# --- 1차시 완성 코드 ---
def move_ship(keys):
    global ship_rect
    speed = 5
    if keys[pygame.K_LEFT]:
        ship_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        ship_rect.x += speed
    if ship_rect.left < 0:
        ship_rect.left = 0
    if ship_rect.right > 800:
        ship_rect.right = 800

# --- 2차시 작업 목표 ---
def spawn_meteor():
    """
    화면 맨 위(y=-meteor_size)의 임의의 위치(x)에 운석을 새롭게 생성합니다.
    """
    global meteors
    meteor_size = 40
    
    # TODO: [1] 화면 가로(800) 범위 내 임의의 x좌표를 고르세요.
    pass
    
    # TODO: [2] 새로운 운석 사각형(pygame.Rect)을 만드세요.
    pass
    
    # TODO: [3] 만든 운석을 meteors 리스트에 추가(append) 하세요!
    pass

def update_meteors():
    """
    모든 운석을 아래로 떨어뜨리고 화면 밖은 제거합니다.
    """
    global meteors
    meteor_speed = 7
    
    # TODO: [4] 모든 운석을 아래로 이동시키세요. (안전한 삭제를 위해 복사본[:] 순회 활용)
    pass
        
    # TODO: [5] 화면 밖(top > 600) 운석은 삭제하여 메모리를 절약하세요.
    pass


# =========================================================
# ⚙️ [게임 엔진 구역] 건드리지 마세요!
# =========================================================

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("우주선 운석 피하기 - 학생 실습본 (2차시)")
clock = pygame.time.Clock()

# 상태 관리 변수
ship_rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 50)
meteors = []

# 운석 생성 타이머 (0.6초마다 신호 발생)
SPAWN_METEOR_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_METEOR_EVENT, 600)

def main():
    # ... 메인 루프 (엔진 구역)
    pass
```

</div>

---

# 2.1. 운석을 만드는 원리

- **무작위 위치:** `random.randint`를 사용하여 매번 다른 X 좌표를 고릅니다.
- **사각형 제작:** `pygame.Rect`를 사용하여 운석의 크기와 위치를 정의합니다.
- **창고 보관:** 생성한 운석을 `meteors` 리스트에 보관합니다.

> [!NOTE]
> **왜 함수 안에 `global meteors`를 쓰나요?**
> 파이썬에서는 함수 내부에서 외부(전역)에 선언된 변수나 리스트를 수정하거나 재할당하려면 해당 변수 앞에 `global` 키워드를 명시해야 합니다. `meteors` 리스트를 관리하기 위해 꼭 필요합니다.

![운석 생성 원리](assets/meteor_spawn_logic.drawio.svg)

---

### 📝 Checkpoint 1: 무작위 범위 계산

<div class="theory-mcq-card">
  <h3>화면 너비가 800이고 운석 크기가 40일 때, <code>random.randint(0, ?)</code>에 들어갈 올바른 최대값은 무엇일까요?</h3>
  <div class="mcq-options">
    <div class="mcq-option" data-correct="false" data-hint="800으로 설정하면, 운석의 x좌표가 800이 되어 오른쪽 화면 밖에서 나타날 수 있습니다.">
      <code>800</code>
    </div>
    <div class="mcq-option" data-correct="true">
      <code>760</code>
    </div>
    <div class="mcq-option" data-correct="false" data-hint="40은 운석의 크기입니다. 오른쪽 끝에서 나타나려면 화면 너비에서 크기를 빼야 합니다.">
      <code>40</code>
    </div>
  </div>
  <div class="mcq-hint"></div>
</div>

---

### 💻 실습 미션 1: 운석 공장 조립하기

`spawn_meteor()` 함수를 완성하여 하늘에서 운석이 생성되게 만드세요.

<div class="code-window">

```python
def spawn_meteor():
    global meteors
    meteor_size = 40

    # [A] 무작위 X 좌표 결정 (화면 밖으로 나가지 않게 760까지)
    random_x = random.randint(0, 800 - meteor_size)

    # [B] 운석 사각형 생성 (y 좌표는 화면 위쪽인 -meteor_size)
    new_meteor = pygame.Rect(random_x, -meteor_size, meteor_size, meteor_size)

    # [C] 리스트에 추가
    meteors.append(new_meteor)
```

</div>

---

# 2.2. 무한 낙하와 메모리 청소 (Update)

- **Update:** 모든 운석의 Y 좌표를 증가시켜 낙하시킵니다.
- **Check:** 화면 끝(600)을 넘었는지 확인합니다.
- **Remove:** 넘었다면 목록에서 지워 메모리를 절약합니다.

> [!NOTE]
> **왜 `y > 600`이 아니라 `top > 600`을 쓸까요?**
> 운석 사각형 `Rect`에서 `y`나 `top`은 사각형의 **가장 윗부분** y좌표입니다. `meteor.top > 600`으로 검사해야 운석의 가장 윗부분(즉, 전체 크기)이 화면 아래 경계(600)를 완전히 넘어갔을 때 삭제되어 화면에서 자연스럽게 사라집니다.

![리스트 업데이트](assets/list_update_process.drawio.svg)

---

### 📝 Checkpoint 2: 복사본 순회의 이유

<div class="theory-mcq-card">
  <h3><code>for m in meteors[:]:</code>와 같이 리스트 뒤에 <code>[:]</code>를 붙여 복사본을 만드는 이유는 무엇일까요?</h3>
  <div class="mcq-options">
    <div class="mcq-option" data-correct="false" data-hint="속도와는 무관하며, 복사본 생성은 메모리를 아주 약간 더 사용합니다.">
      <span>운석이 떨어지는 속도를 높이기 위해서</span>
    </div>
    <div class="mcq-option" data-correct="true">
      <span>순회 도중 요소를 삭제할 때, 리스트의 인덱스가 꼬이는 오류를 방지하기 위해서</span>
    </div>
    <div class="mcq-option" data-correct="false" data-hint="단순 순회는 [:]가 없어도 가능합니다. 핵심은 '안전한 삭제'입니다.">
      <span>리스트 안의 모든 운석을 빠짐없이 이동시키기 위해서</span>
    </div>
  </div>
  <div class="mcq-hint"></div>
</div>

---

### 💻 실습 미션 2: 운석 낙하와 삭제

모든 운석을 아래로 떨어뜨리고, 화면 밖으로 나간 운석을 리스트에서 제거하는 로직을 완성하세요.

<div class="code-window">

```python
def update_meteors():
    global meteors
    meteor_speed = 7
    
    # [A] 안전한 삭제를 위해 복사본[:]을 순회합니다.
    for meteor in meteors[:]:
        # [B] 아래 방향으로 이동
        meteor.y += meteor_speed

        # [C] 바닥(600)을 넘어가면 목록에서 제거
        if meteor.top > 600:
            meteors.remove(meteor)
```

</div>

---

# 2.3. 엔진의 심장: 타이머와 함수 호출 (Engine)

- 매 프레임(1/60초)마다 운석을 만들면 화면이 순식간에 운석으로 가득 찹니다.
- **타이머 이벤트:** 우리가 정한 시간 간격(0.6초)으로만 생성 신호를 보냅니다.

---

### 💻 실습 미션 3: 운석 함수 호출하기

우리가 완성한 `spawn_meteor()`와 `update_meteors()` 함수가 게임 속에서 실제로 실행될 수 있도록, **메인 루프(Main Loop)** 내부의 올바른 위치에서 호출해 주세요.

1. **운석 생성 (`spawn_meteor`):** 이벤트 처리 구역에서 0.6초마다 타이머 이벤트(`SPAWN_METEOR_EVENT`)가 발생할 때 호출합니다.
2. **운석 업데이트 (`update_meteors`):** 키 입력 및 상태 업데이트 구역에서 매 프레임(반복문이 돌 때마다) 호출하여 운석을 떨어뜨립니다.

<div class="code-window">

```python
# [Main Loop] 메인 게임 루프
running = True
while running:
    # --- [1] 이벤트 처리 구역 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # ⏰ 0.6초마다 신호가 오면 운석 생성 함수 호출
        if event.type == SPAWN_METEOR_EVENT:
            spawn_meteor()  # <--- [호출] 운석 생성!

    # --- [2] 키 입력 및 게임 상태 업데이트 구역 ---
    keys = pygame.key.get_pressed()
    move_ship(keys)      # 1차시 우주선 이동 함수
    
    # ☄️ 매 프레임마다 운석 위치 업데이트 및 화면 밖 제거 함수 호출
    update_meteors()     # <--- [호출] 운석 이동 및 삭제!

    # --- [3] 화면 그리기 구역 ---
    screen.fill((30, 30, 50))
    draw_ship(screen)
    draw_meteors(screen) # 운석 그리기 함수 (엔진 내부)
    
    pygame.display.flip()
    clock.tick(60)
```

</div>

---

# 2차시 완성 체크리스트

<div class="callout tip">

- [ ] `random.randint`를 사용하여 운석이 매번 다른 위치에서 나오나요?
- [ ] 운석이 끊김 없이 아래로 부드럽게 떨어지나요?
- [ ] 화면 밖으로 나간 운석이 리스트에서 정상적으로 사라지나요?
- [ ] 우주선과 운석이 겹쳐도 아직은 죽지 않습니다. (3차시 예고!)

</div>

---

# 다음 시간에는...

**3차시: 충돌 판정과 게임 오버**
운석에 부딪히면 게임이 멈추고 "Game Over"를 띄우는 법을 배웁니다.
