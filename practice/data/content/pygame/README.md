# Pygame 콘텐츠 구조

현재 웹 노출 기준은 `week01` ~ `week06`입니다.
각 주차는 웹 카드와 실제 콘텐츠 루트가 1:1로 매핑됩니다.

## 폴더 규칙

- `week01/`
- `week02/`
- `week03/`
- `week04/`
- `week05/`
- `week06/`

각 주차 폴더는 아래 구조를 기본으로 사용합니다.

```text
weekXX/
  category.meta.yml
  lesson/
  interactive/
  worksheets/
```

### 역할

- `category.meta.yml`: 웹 카드와 generated 인덱스에 반영되는 주차 메타
- `lesson/`: 해당 주차의 진입 lesson
- `interactive/`: 해당 주차의 연습 세트 메타
- `worksheets/`: 출력용 활동지와 정답

## 주차 매핑

- `week01`: 창 생성과 화면 갱신 기초
- `week02`: 세트 1 응용
- `week03`: 이벤트 큐와 정상 종료
- `week04`: 세트 2 응용
- `week05`: FPS, 좌표, 값 변화
- `week06`: 세트 3 응용

## round 폴더 취급

- `round01`, `round02`, `round03`은 삭제하지 않고 보존합니다.
- 다만 웹의 직접 노출 단위나 generated 인덱스 기준 루트로는 더 이상 사용하지 않습니다.
- `roundXX`는 원본 수업 자료, 검수 기록, 레퍼런스 보관 위치로 유지합니다.

## 현재 상태

- `week01`은 기존 1주차 실데이터를 주차형 ID와 경로로 이관한 상태입니다.
- `week02` ~ `week06`은 lesson 안내 페이지와 기본 메타를 갖춘 최소 스캐폴드입니다.
- 후속 작업에서 각 주차의 실제 문제 세트와 출력물을 채웁니다.

## week01 문제 생성 파이프라인

- 검수 원본: `week01/problem_review_round01.md`
- 생성 스크립트: `scripts/generate_pygame_set_from_review.py`
- 생성 결과: `practice/data/sets/py_pygame_w01_b01.json`

즉, `problem_review_round01.md`는 사람이 직접 웹에서 읽는 파일이 아니라
세트 JSON을 생성하는 운영 원본으로 사용합니다.

예시 명령:

```powershell
python scripts/generate_pygame_set_from_review.py `
  --source practice/data/content/pygame/week01/problem_review_round01.md `
  --output practice/data/sets/py_pygame_w01_b01.json `
  --set-id py_pygame_w01_b01 `
  --title "Python Pygame 1주차" `
  --category-id py_pygame_w01
```

## 원본 `py_*.py` 게임 파일 취급 기준

- 원본 `py_*.py` 게임 파일은 수업용 주차 자료를 만들기 위한 후보 소스입니다.
- 즉시 웹에 연결하는 최종 자료가 아니라, 주차 목표에 맞춰 줄인 수업용 버전으로 재구성해 사용합니다.
