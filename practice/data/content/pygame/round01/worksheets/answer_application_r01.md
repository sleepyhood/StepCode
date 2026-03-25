# Python Pygame 응용 1회차 정답

## Q1. 이동 코드 읽기

| 입력 | velocity_x | player_x |
|---|---:|---:|
| RIGHT | 10 | 110 |
| RIGHT | 10 | 120 |
| LEFT | -10 | 110 |

핵심은 `velocity_x`가 먼저 바뀌고, 그 다음 `player_x += velocity_x`가 실행된다는 점입니다.

## Q2. 그리기 순서 예측

- 정답: `enemy_img`

나중에 그린 이미지가 화면 맨 위에 보입니다.

## Q3. 이벤트 처리 버그 수정

- 정답:

```python
for event in pygame.event.get():
```

이 줄이 없으면 `event`를 읽지 못하고, 종료 버튼 입력도 처리할 수 없습니다.

## Q4. 충돌 판정 버그 수정

- 정답:

```python
if enemy_rect.colliderect(bullet_rect):
```

의도는 `플레이어-총알`이 아니라 `적-총알` 충돌입니다.

## Q5. 규칙 변경 미션

- 정답: `score >= 10`

완성 형태:

```python
if score >= 10:
    enemy_speed = 7
```

## Q6. 마무리 체크

1. 이벤트는 매 프레임 계속 새로 들어오므로 반복문 안에서 계속 읽어야 합니다.
2. 화면 변경 사항이 실제 창에 반영되지 않아, 색이나 위치가 바뀌어도 보이지 않습니다.
