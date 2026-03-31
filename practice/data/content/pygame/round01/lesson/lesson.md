---
id: "py_pygame_intro"
contentType: "lesson"
track: "pygame"
lang: "python"
categoryId: "py_pygame"
title: "Python Pygame 1주차"
status: "active"
order: 275
audience: "common"
tags: [pygame, game, window, display, fill, update]
recommendedSetId: "py_pygame_b01"
relatedSetIds: ["py_pygame_b01"]
priority: 3
---

# Pygame 1주차 운영 메모

> [!goal]
> 오늘의 목표
>
> - `pygame` 창을 직접 만들고 실행 확인까지 마칠 수 있다.
> - 창 크기, 창 제목, 배경색이 각각 어떤 코드와 연결되는지 설명할 수 있다.
> - 화면 변경 뒤 `pygame.display.update()`가 왜 필요한지 확인할 수 있다.

## 1) 이번 차시의 위치

이 문서는 `세트 1. 창 생성과 화면 갱신 기초`의 `1주차 개념 수업` 운영 메모다.
이번 차시에서는 창 생성과 화면 갱신까지만 다룬다.

아래 항목은 이번 차시의 메인 범위에서 제외한다.

- 종료 이벤트 처리
- FPS 제한
- 도형 그리기
- 이미지 출력과 회전
- 마우스 입력

## 2) 이번 차시 핵심 개념 5개

이번 시간에는 아래 5개만 정확히 잡는다.

- `pygame.init()`
- `pygame.display.set_mode((가로, 세로))`
- `pygame.display.set_caption("제목")`
- `SURFACE.fill((R, G, B))`
- `pygame.display.update()`

설명 순서는 반드시 위 순서를 유지하는 편이 좋다.
새 개념 수를 늘리지 말고, 각 줄이 화면에서 어떤 변화를 만드는지만 확인한다.

## 3) 핵심 코드 1개

학생이 오늘 완성해야 하는 기준 코드는 아래 수준으로 고정한다.

```python
import pygame

pygame.init()
SURFACE = pygame.display.set_mode((400, 300))
pygame.display.set_caption("game")

SURFACE.fill((255, 255, 255))
pygame.display.update()
```

이 코드의 역할은 아래 정도만 설명하면 충분하다.

1. `pygame.init()`은 `pygame` 사용 준비
2. `set_mode()`는 창 크기 결정
3. `set_caption()`은 창 제목 설정
4. `fill()`은 화면 색 채우기
5. `update()`는 변경된 화면 반영

이번 시간에는 위 코드를 먼저 완성하고,
그 다음에 숫자와 색만 바로 바꿔 보게 한다.

## 4) 90분 운영 흐름

- 10분: `pygame` 실행 확인과 오늘 만들 결과 화면 제시
- 20분: 핵심 코드 1줄씩 입력하며 창 생성 확인
- 20분: `set_mode()` 숫자를 바꿔 창 크기 비교
- 15분: `fill()` 색을 바꿔 배경색 비교
- 10분: `update()`를 지웠을 때와 넣었을 때 차이 확인
- 10분: 학생별 수정 결과 점검
- 5분: 오늘 사용한 코드 5줄 다시 읽기

핵심은 `설명 -> 바로 실행 -> 값 1개 수정 -> 다시 실행` 흐름을 반복하는 것이다.
새 개념 설명을 길게 끌지 않는다.

## 5) 즉시 수정 실습 포인트

이번 차시에서 바로 바꿔 보게 할 항목은 아래 정도면 충분하다.

- 창 크기를 `(400, 300)`에서 `(300, 300)`으로 바꾸기
- 창 제목을 `"game"`에서 다른 이름으로 바꾸기
- 배경색을 흰색에서 초록색이나 파란색으로 바꾸기
- `update()`를 잠시 지운 뒤 왜 화면 반영이 안 되는지 말해 보기

수정 실습은 "정답 찾기"보다 "값을 바꾸면 화면이 어떻게 달라지는가"에 초점을 둔다.

## 6) 원본 자료 사용 범위

[md_1회차_파이썬으로_게임만들기.md](c:/Users/osw/Desktop/Workspace/#Projects/StepCode/practice/data/content/pygame/round01/source/md_1회차_파이썬으로_게임만들기.md)는 범위가 넓다.
이번 1주차에서는 아래 부분만 사용한다.

- `pygame` 설치와 실행 확인
- `pygame.init()`
- `set_mode()`
- `set_caption()`
- `fill()`
- `pygame.display.update()`

이벤트, FPS, 도형, 이미지, 마우스 입력 설명은 이번 차시에서 본문 중심으로 다루지 않는다.

## 7) 문제 자료와의 연결

[problem_review_round01.md](c:/Users/osw/Desktop/Workspace/#Projects/StepCode/practice/data/content/pygame/round01/problem_review_round01.md)는 `round01` 전체를 기준으로 정리된 검수 문서다.
그중 `1~4번을 필수`, `5~6번을 심화 또는 다음 세트 이관 후보`로 보는 기준은 유지한다.

다만 이번 1주차 lesson에서는 문제 풀이 중심 운영을 하지 않는다.
문제 검수 문서는 `2주차 응용` 또는 `세트 확장 운영`에 연결하는 자료로 본다.

## 8) 수업 마무리 확인 질문

마지막에는 아래 질문만 확인하면 된다.

- 창 크기를 바꾸는 코드는 어느 줄인가
- 창 제목을 바꾸는 코드는 어느 줄인가
- 배경색을 바꾸는 코드는 어느 줄인가
- 화면 변경 뒤 `update()`가 왜 필요한가

학생이 이 네 가지를 말할 수 있으면 1주차 목표는 달성한 것으로 본다.

## 9) 다음 회차 예고

다음 회차에서는 이번에 만든 창을 바탕으로 아래 내용을 이어서 다룬다.

- 종료 버튼을 눌렀을 때 정상적으로 닫기
- 이벤트 큐 읽기
- 화면 갱신을 반복문 안에서 다루기
- 오픈북 복습과 간단한 수정 문제
