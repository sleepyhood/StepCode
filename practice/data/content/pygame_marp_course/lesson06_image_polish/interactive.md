---
id: "pygame_u06"
contentType: "lesson"
track: "pygame_project"
lang: "python"
categoryId: "pygame_project_ship_u06"
title: "6차시. 이미지로 만드는 진짜 게임 (Final Polish)"
status: "active"
order: 106
audience: "common"
tags: ["pygame", "image", "blit", "scale"]
---

# 6차시. 이미지로 만드는 진짜 게임 (Final Polish)

---

# 목차

- **6.1. 이미지 불러오기와 크기 조절**
  - 안전한 경로 처리와 리소스 로딩
- **6.2. 화면에 이미지 그리기 (Blit)**
  - 사각형을 스킨(이미지)으로 교체하기
- **6.3. [심화] 무한 스크롤 배경 (Scrolling)**
  - 끊김 없이 흐르는 우주 배경 구현
- **6.4. [버그 수정] 전역 변수와 UI**
  - UnboundLocalError 해결 및 게임 오버 문구 복구
- **6.5. 최종 졸업 체크리스트**

![우주선 예시](assets/output_animation.gif)

---

# 실습 파일 구조

<div class="code-window">

```python
# [step6_student.py 주요 구조]
def load_assets():
    # TODO: 이미지 로드 및 크기 조절
    pass

def draw_background(surface):
    # TODO: 배경 이미지 출력 (스크롤)
    pass

def draw_ship(surface):
    # TODO: 우주선 blit
    pass

def draw_meteors(surface):
    # TODO: 운석 blit
    pass

def main():
    # TODO: 전역 변수 선언 및 게임 오버 UI 출력
    pass
```

</div>

---

# 6.1. 이미지 불러오기와 크기 조절

사각형은 컴퓨터가 직접 그리지만, 이미지는 외부 파일(`.png`)을 불러와 메모리에 올려야 합니다. 이때 실행 위치에 상관없이 파일을 찾으려면 **절대 경로**를 사용하는 것이 안전합니다.

### 이미지 로딩과 크기 최적화

- `os.path.join(assets_path, "파일명")`: 폴더와 이름을 안전하게 합칩니다.
- `pygame.transform.scale(이미지, (가로, 세로))`: 이미지 크기를 사각형(Rect) 크기와 맞춥니다.

---

### 💻 실습 미션 1: 안전하게 이미지 불러오기

`load_assets()` 함수 내부에 우주선, 운석, 배경 이미지를 불러오고 크기를 조절하는 코드를 작성하세요.

<div class="code-window">

```python
def load_assets():
    global img_ship, img_meteor, img_bg
    
    # [A] 이미지 파일 로드 (convert_alpha는 투명도 처리를 도와줍니다)
    img_ship = pygame.image.load(os.path.join(assets_path, "ship.png")).convert_alpha()
    img_meteor = pygame.image.load(os.path.join(assets_path, "meteor.png")).convert_alpha()
    img_bg = pygame.image.load(os.path.join(assets_path, "background.png")).convert()
    
    # [B] 이미지 크기를 실제 Rect 크기에 맞게 조정
    img_ship = pygame.transform.scale(img_ship, (50, 50))
    img_meteor = pygame.transform.scale(img_meteor, (40, 40))
    img_bg = pygame.transform.scale(img_bg, (800, 600))
```

</div>

---

# 6.2. 화면에 이미지 그리기 (Blit)

Pygame에서 이미지를 화면에 그릴 때는 `blit(이미지, 좌표)` 함수를 사용합니다. 여기서 좌표 대신 우리가 사용해온 `Rect` 변수를 넣으면 이미지가 사각형을 따라다닙니다.

---

### 💻 실습 미션 2: 객체 스킨 교체

`draw_ship`과 `draw_meteors` 함수를 수정하여 사각형 대신 이미지가 보이게 하세요.

<div class="code-window">

```python
def draw_ship(surface):
    if img_ship:
        surface.blit(img_ship, ship_rect) # 사각형 위치에 이미지 그리기
    else:
        pygame.draw.rect(surface, (0, 255, 255), ship_rect)

def draw_meteors(surface):
    for m in meteors:
        if img_meteor:
            # 운석은 m(Rect)의 크기에 맞게 실시간으로 스케일링하여 그립니다.
            scaled = pygame.transform.scale(img_meteor, (m.width, m.height))
            surface.blit(scaled, m)
```

</div>

---

# 6.3. [심화] 무한 스크롤 배경 (Scrolling)

배경을 아래로 계속 흐르게 만들어 우주선이 전진하는 느낌을 줍니다. 배경 이미지를 위아래로 두 장 이어 붙여서 그리는 것이 핵심입니다.

<div class="code-window">

```python
def draw_background(surface):
    global bg_y
    if img_bg:
        if not game_over:
            bg_y += 2 # 아래로 흐르는 속도
        if bg_y >= 600: bg_y = 0 # 한 바퀴 돌면 좌표 리셋
            
        # 두 개의 이미지를 위아래로 이어 붙여 그리기
        surface.blit(img_bg, (0, bg_y))
        surface.blit(img_bg, (0, bg_y - 600))
```

</div>

---

# 6.4. [버그 수정] 전역 변수와 UI

파이썬 함수 안에서 바깥에 있는 변수(game_over 등)에 값을 대입하려면 반드시 `global` 선언이 필요합니다. 또한, 게임 오버 시 문구가 다시 나타나도록 코드를 보완해야 합니다.

---

### 💻 실습 미션 3: 메인 루프 보완

`main()` 함수와 그리기 구역을 수정하여 에러를 막고 UI를 복구하세요.

<div class="code-window">

```python
def main():
    # [A] 수정 권한 부여 (UnboundLocalError 방지)
    global game_over, score, difficulty, lives
    
    # ... (게임 루프 생략) ...
    
    # [B] 그리기 구역 하단에 게임 오버 UI 추가
    draw_hud(screen)
    if game_over:
        draw_game_over(screen) # 누락된 게임 오버 문구 호출!
```

</div>

---

# 6.5. 최종 졸업 체크리스트

<div class="callout tip">

- [ ] 우주선과 운석이 사각형이 아닌 이미지로 나타나나요?
- [ ] 배경 우주 공간이 아래로 부드럽게 흐르나요?
- [ ] 부딪혔을 때 "GAME OVER" 문구가 정상적으로 표시되나요?
- [ ] 에러 메시지(UnboundLocalError) 없이 게임이 잘 실행되나요?

</div>

### 🎉 축하합니다!
이제 여러분은 로직부터 디자인까지 모두 갖춘 **완벽한 파이썬 게임 개발자**가 되었습니다!
