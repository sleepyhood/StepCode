---
id: "pygame_l01_ship"
contentType: "lesson"
track: "pygame_course"
lang: "python"
categoryId: "pygame_l01"
title: "1차시. 우주선 좌우 이동하기"
status: "active"
order: 101
audience: "common"
tags: ["pygame", "ship", "movement"]
---

# 1차시. 우주선 좌우 이동하기

---

# 1.0. 목차

- **1.1. 실습 준비와 좌표계**
  - 파일 구조 확인 및 화면 좌표 이해
- **1.2. 우주선 첫 시동 걸기 (Move)**
  - 화살표 키 입력과 좌표 이동 로직
- **1.3. 화면 이탈 버그 막기 (Boundary)**
  - if 조건문을 이용한 경계 제한 처리
- **1.4. 게임 엔진 작동 원리**
  - 무한 반복 루프와 애니메이션의 마법

![우주선 예시](assets/real_ship_demo.png)

---

# 1.1. 실습 준비와 좌표계

---

# 1.1.1. 실습 파일 구조 확인

- **학생 작업 구역:** 우리가 코드를 채울 `move_ship(keys)` 함수입니다.
- **게임 엔진 구역:** 배경을 지우고, 캐릭터를 그려주는 '심장'입니다. (절대 수정 금지!)

<div class="code-window">

```python
import pygame
import sys

# =========================================================
# 🧑‍💻 [학생 작업 구역] 1차시: 우주선 좌우 이동하기
# =========================================================


def move_ship(keys):
    """
    키보드 입력에 따라 우주선을 좌우로 움직입니다.
    화면 밖으로 나가지 않도록 제한합니다.
    """
    global ship_rect

    speed = 5

    # TODO: [1] 왼쪽(pygame.K_LEFT) 화살표 키를 누르면 왼쪽으로 speed만큼 이동하게 작성하세요.
    pass

    # TODO: [2] 오른쪽(pygame.K_RIGHT) 화살표 키를 누르면 오른쪽으로 speed만큼 이동하게 작성하세요.
    pass

    # TODO: [3] 우주선이 화면 밖으로 나가지 않게 제한해보세요.
    # 힌트: 화면 가로 크기는 800, ship_rect.left 와 ship_rect.right 를 활용하세요.
    pass


# =========================================================
# ⚙️ [게임 엔진 구역] 건드리지 마세요!
# =========================================================

# --- 초기화 ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("우주선 운석 피하기 - 학생 실습본")
clock = pygame.time.Clock()

# --- 게임 상태 변수 ---
# 초보자 배려: 이미지가 없어도 실행되도록 사각형으로 우주선 대체
ship_color = (0, 255, 255)  # 청록색
ship_rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 50)


def draw_ship(surface):
    pygame.draw.rect(surface, ship_color, ship_rect)


def main():
    running = True
    while running:
        # 1. 이벤트 확인
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. 사용자 입력 확인
        keys = pygame.key.get_pressed()

        # 3. 우주선 이동 (학생 작성 함수 호출)
        move_ship(keys)

        # 4. 화면 그리기
        screen.fill((30, 30, 50))  # 어두운 남색 배경
        draw_ship(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

```

</div>

---

# 1.1.2. 컴퓨터의 좌표계 (X, Y)

- **(0,0):** 화면의 **왼쪽 위**가 기준점입니다.
- **X축 (가로):** 오른쪽으로 갈수록 숫자가 커집니다. `+=`
- **Y축 (세로):** 아래로 갈수록 숫자가 커집니다. `+=`
- **이동 원리:** `x` 값을 조금씩 바꾸면 우리 눈에는 움직이는 것처럼 보입니다.

![좌표계 이동](assets/coordinate_system.drawio.svg)

---

# 1.2. 우주선 첫 시동 걸기 (Move)

---

# 1.2.1. 화살표 키 인식하기

- `keys[...]`: 현재 어떤 키가 눌렸는지 확인하는 '장부'입니다. [A]
- `pygame.K_LEFT`: 왼쪽 화살표 키의 이름표입니다. [B]
- **논리:** "만약 왼쪽 키가 눌렸다면, X 좌표를 줄여라!"

<div class="code-window">

```python
def move_ship(keys):
    # [A] 장부에서 [B] 키 상태 확인
    if keys[pygame.K_LEFT]:
        ship_rect.x -= speed

    if keys[pygame.K_RIGHT]:
        ship_rect.x += speed
```

</div>

---

# 1.2.2. [Mission] 우주선 움직이기

- **Logic Hole:** 오른쪽으로 가려면 X를 어떻게 해야 할까요?
- **힌트:** `K_RIGHT`와 `+=`

<div class="theory-mini-check-card" data-answer="ship_rect.x += speed">
  <input type="text" class="stage-key-input" placeholder="정답 코드(ship_rect.x ??? speed) 입력...">
  <button class="stage-unlock-btn">제출하고 다음으로</button>
</div>

---

# 1.3. 화면 이탈 버그 막기 (Boundary)

---

# 1.3.1. 왜 화면 밖으로 나갈까요?

- 컴퓨터는 우리가 "멈춰!"라고 말하기 전까지 좌표를 무한히 증가시킵니다.
- **경계 조건:** X가 0보다 작아지거나, 800보다 커지는 순간을 감시해야 합니다.
- `ship_rect.left`와 `ship_rect.right` 테두리 센서를 사용합니다.

![경계선 넘어가는 우주선](assets/boundary_0_800.svg)

---

# 1.3.2. 방어벽 로직 (if 조건문)

- **Check:** 왼쪽 테두리가 0을 넘었는지 확인합니다. [A]
- **Fix:** 넘었다면 강제로 0에 고정시킵니다. [B]
- 이 과정을 통해 우주선이 화면에 갇히게 됩니다.

![방어벽 로직](assets/boundary_logic.drawio.svg)

---

# 1.3.3. [Mission] 방어벽 완성하기

- 화면 오른쪽 끝(800)을 넘지 못하게 막는 코드를 완성하세요.
- **Logic Hole:** 오른쪽 벽의 기준은 무엇일까요?

<div class="theory-mini-check-card" data-answer="ship_rect.right = 800">
  <input type="text" class="stage-key-input" placeholder="정답 코드(ship_rect.right = ???) 입력...">
  <button class="stage-unlock-btn">제출하고 다음으로</button>
</div>

---

# 1.4. 게임 엔진 작동 원리

---

# 1.4.1. 애니메이션의 마법

- **무한 반복:** 엔진이 `while` 루프 안에서 우리가 만든 함수를 초당 60번씩 부릅니다.
- **조금씩 이동:** 한 번 부를 때마다 5px씩 이동합니다.
- **결과:** 우리 눈에는 아주 부드러운 움직임으로 보입니다! (60 FPS)

![이동 개요](assets/move_ship_overview.svg)

---

# 1.5. 1차시 완성 체크리스트

<div class="callout tip">

- [ ] 화살표 키를 누를 때 우주선이 반응하나요?
- [ ] 왼쪽 벽(0)을 뚫고 지나가지 않나요?
- [ ] 오른쪽 벽(800)을 뚫고 지나가지 않나요?
- [ ] `speed` 숫자를 바꿨을 때 속도가 변하나요?

</div>

---

# 다음 시간에는...

**2차시: 운석 낙하와 리스트 관리**
하늘에서 쏟아지는 운석을 만들고 리스트로 관리하는 법을 배웁니다.