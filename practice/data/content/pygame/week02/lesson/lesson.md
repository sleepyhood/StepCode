---
id: "py_pygame_w02_intro"
contentType: "lesson"
track: "pygame"
lang: "python"
categoryId: "py_pygame_w02"
title: "Python Pygame 모듈 02 · 이미지 출력과 회전 중심"
status: "active"
order: 276
audience: "common"
tags: [pygame, image, rotate, center, blit]
recommendedSetId: "py_pygame_w02_b01"
relatedSetIds: ["py_pygame_w02_b01"]
priority: 2
---

# Python Pygame 모듈 02 · 이미지 출력과 회전 중심

이번 차시는 이미지 출력과 회전 결과를 다시 읽고,
서로 다른 네 개의 프로젝트 안에서 고장난 코드를 직접 수정하는 데 초점을 둡니다.

## 이번 모듈에서 다룰 핵심

- `SURFACE.blit(...)`
- `pygame.transform.rotate(...)`
- 이미지 출력 좌표와 겹침 순서
- `(0, 0)` 기준 출력이 만드는 화면 결과
- `rect.center`
- `get_rect(center=...)`
- 회전 결과의 중심 보정과 속도 비교

## 학습 방식

이번 모듈은 `round01`의 5번 문제를 바탕으로,
정적 이미지 출력 프로젝트 1개와
회전 프로젝트 3개를 각각 독립적으로 읽고 수정하는 흐름으로 진행합니다.

핵심은 새로운 기능을 많이 추가하는 것이 아니라,
이미 있는 코드를 읽고
출력 위치, 중심 좌표, 속도와 방향을 어떻게 고쳐야 하는지 설명하는 데 있습니다.

## 학습 시작

- 주제: 독립 프로젝트형 이미지 출력과 회전 중심 응용
- 형태: 코드 수정형 + 빈칸형 + 복수정답 객관식형
- 기준 문제: `week02` 1번
- 검수 원본: `practice/data/content/pygame/week02/problem_review_week02.md`
