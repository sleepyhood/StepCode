# Pygame Marp 슬라이드 작성 및 운영 가이드

## 1. 목적과 적용 범위

이 문서는 `practice/data/content/pygame_marp_course/` 아래에서 실제 수업자료를 어떻게 관리하고 확장할지 정리한 운영 가이드다.

이 코스에서 `lesson01_ship_movement`부터 `lesson05_extensions`까지의 `lesson0*_` 폴더는 모두 실제 수업에 사용하는 lesson 자료다.

적용 범위:

- `lesson01_ship_movement/`
- `lesson02_meteor_drop/`
- `lesson03_collision/`
- `lesson04_score_difficulty/`
- `lesson05_extensions/`
- 공용 테마 `shared/themes/pygame_theme.css`
- 공용 자산 `shared/assets/`
- 공용 재사용 조각 `shared/snippets/`

이 가이드의 목적은 다음과 같다.

- lesson01~05를 하나의 연속된 수업 흐름으로 운영한다.
- 차시별 자료 구조와 역할을 혼동하지 않도록 기준을 명확히 둔다.
- Marp 슬라이드와 코드 자료가 함께 있는 lesson 자료를 일관된 방식으로 관리한다.
- 앞으로 slide 자산을 확장할 때도 현재 lesson 운영 흐름과 충돌하지 않게 한다.

---

## 2. 현재 폴더 구조와 역할

현재 루트 구조:

```text
pygame_marp_course/
  README.md
  curriculum.md
  marp_slide_guide.md
  marp_example.md
  shared/
    assets/
    snippets/
    themes/
  lesson01_ship_movement/
    assets/
    lesson/
      slide.md
    src/
  lesson02_meteor_drop/
    src/
  lesson03_collision/
    src/
  lesson04_score_difficulty/
    src/
  lesson05_extensions/
    src/
  Archives/
```

파일과 폴더의 역할:

- `README.md`
  - 코스 루트의 운영 원칙과 source of truth 범위를 설명한다.
- `curriculum.md`
  - 현재 운영 중인 5차시의 목표, 산출물, 수업 흐름을 개요 수준에서 정리한다.
- `marp_slide_guide.md`
  - lesson 자료 운영 방식과 Marp 슬라이드 작성 원칙을 설명한다.
- `marp_example.md`
  - 슬라이드 레이아웃과 CSS 리듬을 참고할 때 보는 예시 자료다.
- `lesson01_ship_movement/`
  - 현재 가장 완성도가 높은 lesson 기준 사례다.
  - `lesson/slide.md`, `assets/`, `src/`를 함께 사용한다.
- `lesson02_meteor_drop/` ~ `lesson05_extensions/`
  - 현재는 `src/` 기반 수업자료로 운영한다.
  - 이후 필요하면 lesson01과 같은 방식으로 `lesson/slide.md`와 lesson 전용 `assets/`를 확장할 수 있다.
- `shared/themes/`
  - 공용 Marp 테마와 관련 CSS를 둔다.
- `shared/assets/`
  - 둘 이상의 차시에서 반복 사용할 수 있는 공용 자산을 둔다.
- `shared/snippets/`
  - 둘 이상의 차시에서 반복 사용할 수 있는 문구, 코드 프레임, 재사용 조각을 둔다.
- `Archives/`
  - 더 이상 쓰지 않는 초안이나 이전 버전을 보관한다.

운영 해석 원칙:

- 현재 구조 설명에서는 존재하지 않는 `teacher_notes/`, `category.meta.yml` 같은 폴더/파일을 전제하지 않는다.
- `lesson/slide.md`는 현재 lesson01에 실체가 있는 구조이며, 다른 lesson에도 같은 패턴으로 확장 가능하다.
- `src/`는 각 차시의 실행 가능한 코드 자료를 담는 실제 수업자료다.

---

## 3. lesson 자료 운영 기준

이 코스의 lesson 자료는 `슬라이드 자료`와 `코드 자료`를 함께 포함할 수 있다.

### 3.1 lesson01 기준 사례

`lesson01_ship_movement/`는 현재 기준 사례다.

- `lesson/slide.md`
  - 실제 수업에서 보여주는 Marp 슬라이드 원본
- `assets/`
  - lesson01 슬라이드에서 직접 사용하는 이미지, 도식, 스크린샷
- `src/`
  - 학생용/교사용/복구용 코드 자료

즉, lesson01은 `슬라이드 + 시각 자료 + 코드`가 함께 갖춰진 완성형 lesson 자료로 본다.

### 3.2 lesson02~05 운영 현실

`lesson02_meteor_drop`부터 `lesson05_extensions`까지는 현재 `src/` 중심으로 운영되는 lesson 자료다.

- 각 lesson은 실제 수업 흐름을 반영한 코드 단계를 갖고 있다.
- 현재는 slide 자산이 없더라도 lesson 폴더 자체는 실제 수업자료다.
- 이후 슬라이드를 추가할 때는 lesson01의 구조와 작성 원칙을 참고해 확장한다.

즉, 이 코스에서 “실제 lesson 자료”의 기준은 `slide.md가 있느냐`가 아니라 `현재 수업에 사용되는 차시 자료인가`이다.

### 3.3 공용 자산과 lesson 전용 자산

- 한 차시에서만 쓰는 자료는 해당 lesson 폴더 안에 둔다.
- 둘 이상의 차시에서 반복 사용할 것이 분명할 때만 `shared/`로 올린다.
- 현재 lesson01의 시각 자료처럼 특정 차시에 종속된 도식은 lesson 전용 자산으로 유지한다.

---

## 4. Marp 슬라이드 작성 기준

현재 이 코스의 Marp 슬라이드 작성 기준은 lesson01을 기준 사례로 삼는다.

기본 원칙:

- 슬라이드는 수업 설명서가 아니라 수업 진행 스크립트로 작성한다.
- 학생이 오늘 완성할 기능을 초반에 명확히 이해할 수 있어야 한다.
- `top-down` 구조를 유지한다.
- `slide-title`, `slide-section`, `slide-part` 클래스를 중심으로 슬라이드 흐름을 잡는다.
- 공용 레이아웃과 표현 규칙은 `shared/themes/pygame_theme.css`에서 관리한다.

권장 흐름:

1. 타이틀 슬라이드
2. 목차 또는 전체 지도
3. 오늘 완성할 기능 또는 산출물 소개
4. 파트 전환 슬라이드
5. 개념/코드/시각 자료 슬라이드
6. 완성 체크리스트 또는 실습 시작 안내

lesson01에서 검증된 핵심 패턴:

- `move_ship(keys)`처럼 오늘 완성할 핵심 함수를 초반에 선언한다.
- TODO 조립 순서를 먼저 보여주고 세부 코드로 내려간다.
- 결과 이미지, 개념 도식, 버그 화면의 역할을 구분한다.
- 마지막에 학생이 스스로 확인할 수 있는 체크리스트를 둔다.

---

## 5. 공용 CSS와 클래스 사용 규칙

공용 인터페이스:

```md
<!-- _class: slide-title -->
<!-- _class: slide-section -->
<!-- _class: slide-part -->
```

공용 레이아웃 클래스:

```html
<div class="slide-2column ratio-64">...</div>
<div class="slide-2column ratio-55">...</div>
<div class="slide-2column ratio-46">...</div>
```

공용 콜아웃 클래스:

```html
<div class="callout tip">...</div>
<div class="callout warn">...</div>
<div class="callout ok">...</div>
```

사용 기준:

- `slide-title`
  - 차시 시작 또는 엔딩 타이틀
- `slide-section`
  - 일반 설명 슬라이드
- `slide-part`
  - 큰 흐름 전환
- `.slide-2column`
  - 텍스트와 이미지, 코드와 설명 등 역할이 다른 두 블록을 나눌 때
- `.callout`
  - 보조 설명, 경고, 완료 조건 강조

금지:

- 슬라이드 루트에 직접 `<section>`을 쓰는 방식으로 구조를 새로 만들지 않는다.
- lesson마다 제각각 인라인 레이아웃 규칙을 늘리지 않는다.
- 현재 없는 공용 클래스 계약을 개별 lesson에서 임의로 표준처럼 만들지 않는다.

---

## 6. 작성 전후 체크리스트

### 작성 전

- 이 lesson이 현재 어떤 차시 목표를 담당하는가
- 학생이 수업 끝에 완성해야 할 기능은 무엇인가
- lesson 전용 자료와 shared 자료를 어떻게 구분할 것인가
- 슬라이드가 필요한 lesson인지, 코드 자료 중심 lesson인지
- lesson01 구조를 어느 정도까지 재사용할 것인지

### 작성 후

- 문서 설명이 실제 lesson 폴더 구조와 충돌하지 않는가
- lesson 전용 자료가 shared로 잘못 올라가지 않았는가
- slide를 추가했다면 `pygame_theme.css`의 공용 클래스 계약만 사용했는가
- lesson01~05가 모두 실제 수업자료라는 운영 전제를 깨지 않았는가
- 새 문서를 읽는 사람이 현재 운영 구조를 오해하지 않는가

---

## 7. 앞으로 확장할 때의 기준

- 새 차시는 `lessonXX_topic` 형식으로 추가한다.
- 새 차시도 실제 수업자료로 운영할 수 있어야 한다.
- 처음에는 `src/` 중심으로 시작해도 되며, 필요하면 `lesson/slide.md`와 lesson 전용 `assets/`를 확장한다.
- lesson01은 Marp 슬라이드 구조의 기준 사례로 삼되, 모든 lesson이 당장 같은 수준의 자산을 갖고 있어야 하는 것은 아니다.
- 문서를 업데이트할 때는 “현재 존재하는 구조”와 “앞으로 확장 가능한 구조”를 혼동하지 않는다.

---

## 8. lesson01 검수를 통한 실전 작성 원칙

아래 사항은 `lesson01_ship_movement/lesson/slide.md`를 실제로 작성하고 검수하는 과정에서 도출한 실전 기준이다. 이후 차시 작성 시 반드시 참고한다.

### 8.1. 슬라이드 계층 번호 체계

- 대묶음 파트는 `1.1`, `1.2`처럼 **점이 하나**인 번호를 쓴다.
- 실제 콘텐츠 슬라이드는 `1.1.1`, `1.1.2`처럼 **점이 두 개**인 번호를 쓴다.
- 목차의 번호와 본문 슬라이드의 `<h1>` 번호는 **반드시 1:1로 일치**시킨다.
- `slide-part` 슬라이드의 제목은 직접 텍스트가 아닌 `# 제목` 형태(h1)로 써야 CSS 프리미엄 타이포그래피가 적용된다.

```md
<!-- _class: slide-part -->

# 1.1. 우주선 첫 시동 걸기
```

### 8.2. 코드 블록 사용 기준

- Marp 내 일반 코드 블록은 기본 다크 박스로 렌더링된다.
- 학생이 **직접 조립하거나 집중해야 하는 핵심 실습 코드**는 `<div class="code-window">` 로 감싸 Mac OS 창 스타일을 적용한다.
- 단순 출력 결과나 한 줄짜리 예시에는 `code-window`를 쓰지 않는다.

### 8.3. SVG 자산 제작 규칙

- 모든 SVG는 반드시 **`viewBox="0 0 W H"` 형태로 원점 `(0,0)` 기준**으로 설계한다.
- `viewBox`가 실제 콘텐츠 좌표와 어긋나면 텍스트가 잘리거나 불필요한 여백이 생긴다.
- SVG는 자동 줄바꿈이 없으므로 긴 문장은 **`<text>` 두 줄로 분할**한다.
- 박스(`<rect>`) 높이는 내부 텍스트 줄 수  약 36px를 기준으로 여유있게 설정한다.
- 화살표 끝점과 레이블 텍스트의 `x` 좌표가 겹치지 않도록 레이블은 화살표 끝 너머에 배치한다.

### 8.4. 슬라이드 밀도 기준

| 유형 | 권장 조합 |
|---|---|
| 개념 설명 슬라이드 | 본문 텍스트 + SVG 이미지 **또는** 코드 블록 하나 |
| 실습 코드 슬라이드 | `code-window` 하나 + callout 1~2개 |
| Big Picture 슬라이드 | 완성 코드 + 다이어그램 이미지 (callout 1개 이내) |
| 전환 슬라이드(`slide-part`) | `# h1` 제목만. 부연 설명 없음 |

- **과밀:** 2컬럼 안에 callout이 2개 이상이면 다음 슬라이드로 분리한다.
- **과소:** 텍스트 2줄 이하이고 이미지도 없으면 callout 1개 이상을 추가해 맥락을 보완한다.
- 이미지가 주석 처리(`<!-- -->`)된 슬라이드는 반드시 callout 등으로 그 자리를 채운다.

### 8.5. Marp CSS 우선순위 원칙

- Marp 내장 테마가 먼저 적용되므로, 커스텀 CSS가 무시될 때는 **선택자 계층 구체화 + `!important`** 를 함께 사용한다.
- `section pre` 보다 `section .code-window pre`처럼 래퍼를 중간에 넣어야 우선순위가 보장된다.
- 래퍼 클래스는 **전역 스타일을 오염시키지 않도록** 반드시 부모 선택자를 좁혀서 정의한다.

### 8.6. 목차-슬라이드 동기화 원칙

- 목차의 항목명과 실제 슬라이드 `<h1>` 제목을 글자 하나까지 일치시킨다.
- 목차 구조를 수정한 후에는 반드시 본문 슬라이드 제목을 전수 확인하여 동기화한다.
- `ratio-55`, `ratio-46` 등 비율 선택은 왼쪽/오른쪽 텍스트 양을 보고 시각적 균형에 맞춰 결정한다.
