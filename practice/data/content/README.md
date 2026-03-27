# `practice/data/content` 표준

이 문서는 `practice/data/content/` 아래에서 사용하는 **원본 콘텐츠 구조 표준**을 정의한다.
목표는 다음 3가지를 고정하는 것이다.

1. 사람이 직접 수정하는 원본은 어디인가
2. 웹이 읽는 산출물은 어디인가
3. 폴더명, 파일명, ID를 어떤 규칙으로 통일할 것인가

---

## 1. 기본 원칙

### 1.1 원본과 산출물의 역할

- `practice/data/content/`
  - 사람이 직접 편집하는 **원본(source of truth)** 이다.
  - 문제지, 해설, 이론, 커리큘럼, 문제 매핑, 메타데이터를 이곳에서 관리한다.

- `practice/data/generated/`
  - `content/`를 바탕으로 생성되는 **파생 메타/인덱스** 이다.
  - 예: `categories.json`, `sets.index.json`, `theory.index.json`

- `practice/data/sets/`
  - 웹 문제 풀이 화면이 직접 읽는 **실행용 세트 JSON** 이다.
  - 사람이 직접 고치는 원본이 아니라, `content/`에서 생성되는 결과물로 본다.

### 1.2 운영 규칙

- 새 콘텐츠는 먼저 `content/`에 만든다.
- `generated/`와 `sets/`는 직접 수정하지 않고 생성 스크립트로 갱신하는 것을 원칙으로 한다.
- 레거시 파일을 유지하더라도 기준 원본은 `content/` 하나만 사용한다.
- 같은 의미의 데이터를 `content/`와 `generated/`에 동시에 수동으로 관리하지 않는다.

---

## 2. 최상위 구조

권장 구조는 다음과 같다.

```text
practice/data/
  content/
    contest/
      c/
      python/
    pygame/
      pygame/
  generated/
    categories.json
    sets.index.json
    theory.index.json
  sets/
    *.json
```

의미:

- `content/`: 편집 원본
- `generated/`: 웹이 읽는 인덱스/연결 정보
- `sets/`: 웹이 읽는 최종 문제 세트

---

## 3. 경로 축

`content/` 아래의 기본 경로 축은 다음과 같다.

```text
content/<track>/<subject>/...
```

필드 의미:

- `track`: 운영 트랙
  - 예: `contest`, `pygame`
- `subject`: 과목 또는 주제 단위
  - 예: `c`, `python`, `pygame`

예시:

- `content/contest/c/`
- `content/contest/python/`
- `content/pygame/pygame/`

주의:

- `pygame`처럼 트랙과 과목이 사실상 같은 경우에도 2단 구조를 유지한다.
- 상위 축을 고정해 두면 이후 `unity`, `web`, `java` 등을 추가해도 구조가 흔들리지 않는다.

---

## 4. 표준 폴더 구조

### 4.1 Contest 계열

```text
content/contest/c/
  category.meta.yml
  curriculum/
    index.md
    elem.md
    mid.md
    high.md
  units/
    c_w01/
      lesson.md
      worksheet.basic.r01.md
      answer.basic.r01.md
      set.meta.yml
      assets/
    c_w02/
      ...
```

```text
content/contest/python/
  category.meta.yml
  curriculum/
    index.md
    elem.md
    mid.md
    high.md
  units/
    py_w01/
      ...
```

### 4.2 Pygame 계열

```text
content/pygame/pygame/
  category.meta.yml
  curriculum/
    index.md
  rounds/
    round01/
      lesson.md
      worksheet.basic.r01.md
      answer.basic.r01.md
      set.meta.yml
      problem_map.json
      problems/
      missions/
      assets/
    round02/
      ...
```

구조 원칙:

- `curriculum/`은 과정 설계 문서를 둔다.
- `units/` 또는 `rounds/`는 실제 학습/출제 묶음을 둔다.
- 각 묶음 폴더 안에 이론, 문제지, 해설, 메타, 자산을 함께 둔다.
- 트랙별 특수 자산은 해당 묶음 폴더 내부에만 둔다.

---

## 5. 파일 역할

### 5.1 공통 파일

- `category.meta.yml`
  - 카테고리 단위 메타데이터
  - 웹 카테고리, 생성 순서, 제목 등을 정의한다.

- `lesson.md`
  - 해당 단원/회차의 이론 원본
  - 최종 `theory.index.json`과 이론 페이지 연결의 출발점이 된다.

- `worksheet.basic.r01.md`
  - 학생용 문제지 원본
  - 난이도와 회차가 파일명에 드러나야 한다.

- `answer.basic.r01.md`
  - 교사용 해설 원본

- `set.meta.yml`
  - 세트 ID, 카테고리 ID, 난이도, 회차, lesson 연결 등 세트 생성용 메타데이터

- `assets/`
  - 이미지, gif, 보조 파일 등 해당 단원 전용 자산

### 5.2 선택 파일

- `problem_map.json`
  - 출제 재구성 규칙 또는 출처 매핑
  - 특히 `pygame`처럼 여러 코드 조각을 묶어 문제지를 구성할 때 사용

- `missions/`
  - 실습형 트랙의 원본 미션 코드

- `problems/`
  - 대문항/예제 코드 등 출제 재료

---

## 6. 파일명 규칙

### 6.1 공통 규칙

- 소문자 영문, 숫자, `_`, `.`만 사용한다.
- 공백은 사용하지 않는다.
- 회차 번호는 두 자리 `01`, `02`처럼 0패딩을 사용한다.
- 같은 역할의 파일은 프로젝트 전체에서 같은 이름 패턴을 사용한다.

### 6.2 고정 파일명

- `category.meta.yml`
- `lesson.md`
- `set.meta.yml`
- `problem_map.json`
- `index.md`
- `elem.md`
- `mid.md`
- `high.md`

### 6.3 패턴 파일명

- `worksheet.<difficulty>.rNN.md`
  - 예: `worksheet.basic.r01.md`
  - 예: `worksheet.challenge.r02.md`

- `answer.<difficulty>.rNN.md`
  - 예: `answer.basic.r01.md`
  - 예: `answer.challenge.r02.md`

단, 특정 트랙에서 `basic/challenge` 외의 난이도 체계를 쓰더라도 파일명 패턴은 유지한다.

---

## 7. 폴더명 규칙

- `track` 폴더: `contest`, `pygame`
- `subject` 폴더: `c`, `python`, `pygame`
- `unit` 폴더:
  - contest 계열은 `c_w01`, `c_w02`, `py_w01`처럼 사용
  - round 계열은 `round01`, `round02`처럼 사용

규칙:

- 주차성 단원은 `wNN`
- 회차성 묶음은 `roundNN`
- 언어 접두가 필요한 경우 `c_w01`, `py_w01`처럼 subject를 드러낸다

---

## 8. ID 규칙

ID는 파일명/폴더명과 가능한 한 직접 대응되게 만든다.

### 8.1 Category ID

형식:

```text
<track>_<subject>
```

예:

- `contest_c`
- `contest_python`
- `pygame_pygame`

### 8.2 Unit ID

형식:

```text
<subject>_wNN
<subject>_roundNN
```

예:

- `c_w01`
- `py_w03`
- `pygame_round01`

### 8.3 Lesson ID

형식:

```text
theory_<track>_<subject>_<unit>
```

예:

- `theory_contest_c_c_w01`
- `theory_contest_python_py_w03`
- `theory_pygame_pygame_pygame_round01`

참고:

- lesson ID는 다소 길어도 괜찮다.
- 충돌보다 명시성을 우선한다.

### 8.4 Set ID

형식:

```text
<track>_<subject>_<audience?>_<year?>_<unit?>_<difficulty>_rNN
```

예:

- `contest_c_elem_2024_w03_basic_r01`
- `contest_python_mid_2024_w05_challenge_r01`
- `pygame_pygame_round01_basic_r01`

프로젝트 사정상 레거시 ID를 유지해야 한다면:

- 기존 ID를 `set.meta.yml`의 `id`로 유지할 수 있다.
- 단, 새로 만드는 세트는 위 패턴을 우선 사용한다.

---

## 9. 메타데이터 표준 예시

### 9.1 `category.meta.yml`

```yml
id: contest_c
track: contest
subject: c
title: C 경시대회
order: 300
sourceOfTruth: content
```

### 9.2 `set.meta.yml`

```yml
id: contest_c_elem_2024_w03_basic_r01
categoryId: contest_c
track: contest
subject: c
unitId: c_w03
title: C 경시대회 초등 3주차 기초 1회차
difficulty: basic
round: 1
audience: elementary
lessonRef: theory_contest_c_c_w03
worksheetFile: worksheet.basic.r01.md
answerFile: answer.basic.r01.md
```

### 9.3 `lesson.md` front matter 예시

```md
---
id: theory_contest_c_c_w03
categoryId: contest_c
track: contest
subject: c
unitId: c_w03
title: C 경시대회 3주차 핵심 개념
---
```

---

## 10. 생성 규칙

`content/`를 기준으로 아래 결과를 생성한다.

- `generated/categories.json`
- `generated/sets.index.json`
- `generated/theory.index.json`
- `sets/*.json`

생성기의 책임:

1. `category.meta.yml`에서 카테고리 목록 생성
2. `lesson.md` 메타에서 이론 인덱스 생성
3. `set.meta.yml`와 `worksheet.*.md`에서 세트 인덱스 생성
4. 문제지 원본을 웹 실행용 `sets/*.json`으로 변환

원칙:

- 생성 결과를 수동 수정하지 않는다.
- 수동 수정이 필요하면 원본(`content/`)을 수정한 뒤 다시 생성한다.

---

## 11. 마이그레이션 규칙

기존 파일을 옮길 때는 다음 기준을 따른다.

- 기존 `practice/data/curriculum/**/*`
  - `content/<track>/<subject>/curriculum/` 아래로 이동

- 기존 `practice/data/theory/**/*`
  - 실제 편집 원본인 경우 `content/.../lesson.md` 또는 관련 문서로 재배치
  - 배포용 사본이라면 제거 대상 후보로 본다

- 기존 `practice/data/sets/*.json`
  - 직접 수정하지 않고, 대응하는 `worksheet.*.md`와 `set.meta.yml` 원본을 만든다

- 기존 별도 메모/초안 문서
  - 특정 unit/round에 종속되면 해당 폴더 내부로 이동
  - 공통 운영 메모면 별도 문서 폴더를 둔다

---

## 12. 최종 판단 기준

다음 조건을 만족하면 구조 정규화가 된 것으로 본다.

- 새 콘텐츠를 만들 때 `content/`만 수정하면 된다.
- `generated/`와 `sets/`는 생성 스크립트로만 갱신된다.
- 폴더명만 보고도 트랙, 과목, 단원 성격을 알 수 있다.
- 파일명만 보고도 이론, 문제지, 해설, 메타를 구분할 수 있다.
- 레거시 JSON과 원본 MD 사이의 기준점이 하나로 고정된다.
