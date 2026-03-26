---
id: "py_pygame_round01_problem_sheet_teacher"
contentType: "worksheet"
track: "pygame"
lang: "python"
categoryId: "py_pygame"
title: "Python Pygame Round01 대문항형 문제지 교사용 해설"
round: 1
difficulty: "application"
status: "draft"
audience: "teacher"
printDefault: false
---

# Python Pygame Round01 대문항형 문제지 교사용 해설

## 사용 목적

이 문서는 [문제지_round01_대문항형.md](./문제지_round01_대문항형.md)에
대응하는 교사용 해설서입니다.
정답을 한 가지로만 고정하기보다,
학생이 `실행 -> 관찰 -> 수정 -> 재실행` 흐름을
제대로 수행했는지 확인하는 기준으로 사용합니다.

채점 또는 피드백 시 아래 세 가지를 우선 봅니다.

- 문제 원인을 실제 동작과 연결해서 설명했는가
- 수정 코드가 목표 동작을 만들었는가
- 수정 이유를 말로 설명할 수 있는가

---

## 1번. 창 만들기와 기본 화면 구성

### 핵심 개념

- `pygame.init()`
- `pygame.display.set_mode()`
- `fill()`
- 도형 좌표 `(x, y, width, height)`
- RGB 색상값

### 문항 의도

- 창 생성과 화면 갱신의 기본 구조를 읽는지 확인
- 좌표를 바꾸면 도형 위치가 달라진다는 점을 확인
- 숫자 수정이 곧바로 화면 변화로 이어진다는 경험 제공

### 예시 답안

#### 1.1

- `SURFACE.fill((255, 255))`는 색상값 개수가 잘못되어
  실행 오류가 난다.
- 올바른 예:

```python
SURFACE.fill((255, 255, 255))
```

- 핵심은 `fill()`에 전달하는 색상값 형식을 이해하는 것이다.

#### 1.2

- 중앙 배치를 위한 대표 수정 예:

```python
pygame.draw.rect(SURFACE, (255, 120, 120), (120, 105, 160, 90))
```

- 핵심은 도형의 시작 좌표를 `(0, 0)`에서
  중앙 근처로 옮기는 것이다.
- 완전한 수학적 중앙이 아니어도 의도가 맞으면 인정 가능.

#### 1.3

- 예:
  - 창 크기 `(600, 400)`으로 수정
  - 배경색 `(240, 240, 255)`로 수정
- 이유를 "도형이 더 잘 보이도록",
  "여백이 부족해서",
  "배경과 도형 색 대비를 주기 위해" 등으로 설명하면 적절하다.

### 채점 포인트

- 좌표의 의미를 이해했는가
- 창 크기와 배경색 변경이 실제 코드 수정으로 이어졌는가
- 색상값 오류를 파악했는가
- 결과를 관찰한 뒤 말로 정리했는가

---

## 2번. 도형 그리기 순서와 겹침

### 핵심 개념

- 그리기 순서
- 겹침
- 좌표 조정

### 문항 의도

- 나중에 그린 도형이 위에 보인다는 원리를 확인
- 단순 암기가 아니라 직접 순서를 바꾸며 화면 차이를 보게 함

### 예시 답안

#### 2.1

- 원칙: 보통 나중에 그린 도형이 더 위에 보인다.
- 이유: 화면은 순서대로 덮어 그려지기 때문이다.

#### 2.2

- 예시 수정:

```python
pygame.draw.circle(SURFACE, (80, 140, 255), (250, 170), 85)
pygame.draw.rect(SURFACE, (255, 120, 120), (140, 90, 170, 130))
```

- 또는 좌표를 바꾸어
  더 많이 겹치게 만든 뒤 관찰하게 할 수 있다.

#### 2.3

- 예시:

```python
pygame.draw.circle(SURFACE, (40, 220, 120), (250, 170), 35)
```

- 새 도형을 가장 마지막에 그리면 된다.

### 채점 포인트

- "나중에 그린다"와 "위에 보인다"를 연결했는가
- 실제 draw 순서를 바꾸거나,
  마지막 draw에 새 도형을 두었는가
- 결과를 관찰 언어로 설명했는가

---

## 3번. 이벤트 처리와 정상 종료

### 핵심 개념

- `pygame.event.get()`
- `QUIT`
- 종료 처리

### 문항 의도

- 이벤트 반복문이 없으면 종료 입력을 처리할 수 없다는 점을
  이해시키기 위함

### 예시 답안

#### 3.1

- 종료 이벤트를 읽는 반복문이 없기 때문에
  `X` 버튼을 눌러도 `QUIT` 이벤트를 처리하지 못한다.
- `if False:`는 절대 실행되지 않으므로
  종료 코드가 동작하지 않는다.

#### 3.2

```python
for event in pygame.event.get():
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
```

- 이 코드가 반복문 안에 있어야 한다.

#### 3.3

- 예시:

```python
from pygame.locals import QUIT, KEYDOWN, K_SPACE
```

```python
color = (255, 210, 80)

for event in pygame.event.get():
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == KEYDOWN and event.key == K_SPACE:
        color = (80, 200, 255)
```

- 색 변경 규칙이 동작하면 충분하다.

### 채점 포인트

- `QUIT` 이벤트 처리 위치를 이해했는가
- `if False:`의 문제를 설명할 수 있는가
- 확장 규칙이 실제 입력과 연결되어 있는가

---

## 4번. 화면 갱신과 속도 제어

### 핵심 개념

- `pygame.display.update()`
- `clock.tick()`
- 프레임 속도와 체감 속도

### 문항 의도

- 화면 상태 변경과 실제 표시 갱신이 다르다는 점을 구분
- `tick` 값이 속도 체감에 영향을 준다는 점을 경험

### 예시 답안

#### 4.1

- 원인: 화면 색과 도형 위치는 메모리상에서 바뀌지만,
  화면 갱신 명령이 없어 보이지 않는다.

```python
pygame.display.update()
```

- 이 한 줄을 `draw` 뒤에 넣으면 된다.

#### 4.2

- 예시 관찰:
  - `tick(1)`: 매우 느리고 끊겨 보임
  - `tick(10)`: 느리지만 변화는 확인 가능
  - `tick(60)`: 자연스럽게 움직임
  - `tick(120)`: 더 부드럽게 느껴질 수 있음

- 학생 표현이 달라도 비교 관찰이 있으면 인정 가능.

#### 4.3

- 정답은 고정되지 않는다.
- 예:
  - `tick(30)`으로 조정
  - 또는 이동값 `xpos += 2`로 감소

### 채점 포인트

- `update()`와 `tick()`의 역할을 혼동하지 않았는가
- 실제로 숫자를 바꾸고 비교했는가
- 선택 이유가 논리적인가

---

## 5번. 회전과 중심 좌표

### 핵심 개념

- `pygame.transform.rotate()`
- 회전 후 크기 변화
- `get_rect(center=...)`

### 문항 의도

- 회전 결과 이미지의 크기가 달라질 수 있다는 점
- 원본 좌표와 회전 후 좌표를 따로 잡아야 한다는 점을 확인

### 예시 답안

#### 5.1

- 회전은 되지만 화면 왼쪽 위 `(0, 0)` 기준으로 붙어서 돈다.
- 중심 회전처럼 보이지 않고
  위치가 흔들리거나 치우쳐 보인다.

#### 5.2

```python
rotated = pygame.transform.rotate(sprite, theta)
rotated_rect = rotated.get_rect(center=(260, 160))
SURFACE.blit(rotated, rotated_rect)
```

- 핵심은 `blit` 좌표를 고정 숫자 `(0, 0)`로 두지 않고,
  회전된 이미지의 rect 중심을 맞추는 것이다.

#### 5.3

- 예:
  - `theta += 1`로 느리게 회전
  - 중심 좌표를 `(180, 160)`으로 변경

### 채점 포인트

- 회전 문제를 "중심 보정"으로 이해했는가
- `get_rect(center=...)` 또는 동등한 방식으로 해결했는가
- 결과를 중심 이동과 연결해 설명했는가

---

## 6번. 마우스 입력과 그리기 규칙

### 핵심 개념

- `MOUSEMOTION`
- 마우스 버튼 상태
- 조건 분기

### 문항 의도

- 입력 이벤트가 발생하는 조건과
  실제 저장 조건을 분리해 생각하게 함

### 예시 답안

#### 6.1

- 마우스를 움직일 때마다 `MOUSEMOTION` 이벤트가 발생하고,
  현재 코드는 그때마다
  무조건 `mouse_positions.append(event.pos)`를 수행한다.
- 그래서 점이 계속 그려진다.

#### 6.2

- 대표 수정 예:

```python
elif event.type == MOUSEMOTION and event.buttons[0]:
    mouse_positions.append(event.pos)
```

- 왼쪽 버튼이 눌린 상태일 때만 좌표를 저장한다.

#### 6.3

- 예시 1: 점 크기 변경

```python
pygame.draw.circle(SURFACE, (20, 20, 20), pos, 10)
```

- 예시 2: 색 변경

```python
pygame.draw.circle(SURFACE, (255, 80, 80), pos, 5)
```

- 예시 3: 키 입력으로 지우기 기능 추가

```python
from pygame.locals import QUIT, MOUSEMOTION, KEYDOWN, K_c
```

```python
elif event.type == KEYDOWN and event.key == K_c:
    mouse_positions.clear()
```

### 채점 포인트

- 이벤트 발생 조건과 그리기 조건을 구분했는가
- `event.buttons[0]` 또는 동등한 클릭 조건을 사용했는가
- 확장 기능이 실제로 동작 가능한 코드인가

---

## 운영 메모

- 1번과 2번은 비교적 빠르게 진행 가능
- 3번과 4번은 개념 설명이 필요해 시간이 더 걸릴 수 있음
- 5번은 중급 학생에게 강한 성취감을 주는 문항
- 6번은 마우스 이벤트를 다뤄 흥미 유발에 좋음

수업 시간 90분 기준 추천 운영:

1. 1번, 2번으로 진입
2. 3번, 4번에서 핵심 개념 정리
3. 5번, 6번 중 반 분위기에 맞게 깊이 조절
