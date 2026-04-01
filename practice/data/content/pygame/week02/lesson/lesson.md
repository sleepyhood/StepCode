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
recommendedSetId: ""
relatedSetIds: []
priority: 2
---

# Python Pygame 모듈 02 · 이미지 출력과 회전 중심

이번 차시는 이미지 출력과 회전 결과를 다시 읽고,
고장난 코드를 직접 수정하는 데 초점을 둡니다.

## 이번 모듈에서 다룰 핵심

- `SURFACE.blit(...)`
- `pygame.transform.rotate(...)`
- `(0, 0)` 기준 출력이 만드는 화면 결과
- `get_rect(center=...)`
- 회전 결과의 중심 보정

## 학습 방식

이번 모듈은 `round01`의 5번 문제를 바탕으로,
회전한 이미지가 왜 어색하게 보이는지 확인하고
필요한 줄을 바꿔 화면 결과를 정상적으로 복구하는 흐름으로 진행합니다.

핵심은 새로운 기능을 많이 추가하는 것이 아니라,
이미 있는 코드를 읽고
출력 위치와 중심 좌표를 어떻게 고쳐야 하는지 설명하는 데 있습니다.

## 학습 시작

- 주제: 이미지 출력과 회전 중심 응용
- 형태: 코드 수정형 + 빈칸형 + 복수정답 객관식형
- 기준 문제: `round01` 5번
