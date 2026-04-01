# Pygame 운영 기준

이 문서는 `practice/data/content/pygame/` 폴더를
어떻게 운영하고 유지하는지 설명하는 기준 문서입니다.

즉, 이 README는 `수업 소개`보다 아래 내용을 다룹니다.

- 이 폴더의 운영 철학
- 실제 소스 오브 트루스 경로
- 폴더 구조와 각 폴더의 역할
- 이름 규칙과 표시 규칙
- generated 인덱스 재생성 원칙
- `roundXX`와 `weekXX`의 관계

모듈별 교육 목표와 상세 커리큘럼은
`practice/data/content/pygame/커리큘럼.md`에서 관리합니다.

## 운영 목적

이 폴더의 pygame 콘텐츠는 `개념 분해형 강의안`보다
`오픈북/수정형 응용 문제 세트`를 제작하고 운영하는 데 초점을 둡니다.

즉, 목표는 새로운 문법을 길게 설명하는 것이 아니라
학생이 제시된 코드를 읽고,
왜 고장났는지 찾고,
필요한 줄을 수정해서 원하는 동작으로 복구하도록 만드는 것입니다.

핵심 운영 원칙은 아래와 같습니다.

- 응용 문제 중심 운영
- 고장난 코드 읽기/수정 중심
- 새 개념 강의보다 문제 세트 운영 우선
- `코드 입력형`, `빈칸형`, `복수정답 객관식형` 중심
- `짧은 개념 확인 -> 고장난 코드 수정 -> 응용 문제 풀이 -> 결과 비교` 흐름 유지

## 현재 운영 범위

현재 실제 운영 루트는 `week01~week10`입니다.
각 주차 폴더는 웹 카드, lesson, interactive, worksheet가 하나의 묶음으로 연결됩니다.

현재 모듈 목록은 아래와 같습니다.

- `week01`: `모듈 01 · 화면 구성과 좌표`
- `week02`: `모듈 02 · 이미지 출력과 회전 중심`
- `week03`: `모듈 03 · 마우스 입력과 그리기 규칙`
- `week04`: `모듈 04 · 이동, FPS, 값 변화`
- `week05`: `모듈 05 · 이벤트와 상태 분기`
- `week06`: `모듈 06 · 미니게임 종합 응용`
- `week07`: `모듈 07 · 랜덤 규칙과 등장 제어`
- `week08`: `모듈 08 · 시간 규칙과 간격 제어`
- `week09`: `모듈 09 · 삼각함수와 궤적 이동`
- `week10`: `모듈 10 · 클래스와 코드 구조화`

`weekXX` 폴더명은 내부 운영 경로이고,
웹 카드와 상세 화면에는 정규화된 `모듈 XX · 제목` 규칙을 사용합니다.

## 이름 규칙

이 pygame 콘텐츠는 아래 규칙으로 맞춥니다.

- 폴더명: `week01` ~ `week10`
- category ID: `py_pygame_w01` ~ `py_pygame_w10`
- lesson ID: `py_pygame_w01_intro` 형식
- set ID: `py_pygame_w01_b01` 형식
- worksheet ID: `py_pygame_w01_basic_r01` 형식

표시 규칙은 아래로 고정합니다.

- 카드 표시명: `모듈 01 · 화면 구성과 좌표`
- 상세 lesson 제목: `Python Pygame 모듈 01 · 화면 구성과 좌표`
- interactive/worksheet 제목도 같은 규칙을 따릅니다.

즉, `주차`라는 표현은 내부 폴더 구분 용도로만 남고,
실제 화면 표기와 generated 제목은 `모듈 XX · 주제명` 형식으로 관리합니다.

## 폴더 구조

각 모듈은 아래 구조를 기본으로 사용합니다.

```text
weekXX/
  category.meta.yml
  lesson/
  interactive/
  worksheets/
  problem_review_*.md
```

필요한 경우 아래가 함께 포함될 수 있습니다.

- `problems/`
- `reference_images/`

역할은 아래와 같습니다.

- `category.meta.yml`: 카드 제목과 generated 카테고리 메타의 source of truth
- `lesson/`: 해당 모듈의 진입 문서
- `interactive/`: 웹 문제 세트 메타
- `worksheets/`: 출력용 문제지와 정답
- `problem_review_*.md`: 검수 원본
- `problems/`: 실제 기준 코드 또는 운영 참고 코드
- `reference_images/`: 문제 설명용 참고 이미지/GIF

## 생성 흐름

이 폴더의 source of truth는 `practice/data/content/pygame/**` 입니다.
`practice/data/generated/*`는 직접 수정하지 않고,
항상 원본 메타를 수정한 뒤 재생성합니다.

생성 흐름은 아래와 같습니다.

1. `practice/data/content/pygame/weekXX/**`에서 원본 문서와 메타를 수정
2. 필요하면 `problem_review_*.md`에서 세트 JSON 생성
3. `scripts/generate_content_indexes.py`로 generated 인덱스 재생성

문제 세트 생성 예시:

```powershell
python scripts/generate_pygame_set_from_review.py `
  --source practice/data/content/pygame/week01/problem_review_round01.md `
  --output practice/data/sets/py_pygame_w01_b01.json `
  --set-id py_pygame_w01_b01 `
  --title "Python Pygame 모듈 01 · 화면 구성과 좌표" `
  --category-id py_pygame_w01
```

인덱스 재생성:

```powershell
python scripts/generate_content_indexes.py
```

즉, 아래 원칙을 유지합니다.

- `practice/data/generated/*`는 직접 수정하지 않음
- `practice/data/content/pygame/**`를 수정한 뒤 재생성
- 세트 JSON은 가능한 한 검수 원본 markdown에서 생성

## round 폴더 취급

- `round01`, `round02`, `round03`은 웹 직접 노출 루트가 아닙니다.
- 이 폴더들은 원본 수업 자료, 초안, 검수 기록, 보관 문맥으로 유지합니다.
- 실제 운영과 웹 노출은 `weekXX` 기준으로 해석합니다.

특히 `round01`은 더 이상 `1주차 전체`를 뜻하지 않습니다.
현재 기준에서는 아래처럼 해석합니다.

- `1~4번`: 모듈 01 핵심 응용 문제
- `5번`: 모듈 02 확장 응용
- `6번`: 모듈 03 확장 응용

즉, 기존의 `1주차 1~6번` 해석은 사용하지 않습니다.

## 커리큘럼 문서와의 분리

이 README에는 아래 내용을 길게 넣지 않습니다.

- 각 모듈의 학습 목표 상세
- 주차별 교수 흐름
- 1~10모듈의 세부 교육 설명
- 후속 심화 운영 판단

이 내용은 `practice/data/content/pygame/커리큘럼.md`가 담당합니다.

정리하면 역할은 아래와 같습니다.

- `README.md`: 운영 규칙, 구조, 이름 규칙, 생성 흐름
- `커리큘럼.md`: 교육 내용, 모듈별 주제, 학습 목표

## 원본 `py_*.py` 파일 취급 기준

- 원본 `py_*.py` 게임 파일은 수업용 응용 문제를 만들기 위한 후보 소스입니다.
- 바로 웹에 연결하는 최종 자료가 아니라, 모듈 목표에 맞게 줄이고 재구성해서 사용합니다.
- 기준은 `완성된 예제 설명`보다 `문제화하기 좋은 고장난 코드/수정 포인트`가 있는지입니다.
