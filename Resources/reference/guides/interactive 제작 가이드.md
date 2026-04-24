# Interactive Lesson 제작 가이드

본 문서는 StepCode의 새로운 스크롤형 인터랙티브 실습 콘텐츠(`interactive.md`)를 작성하기 위한 표준 가이드라인입니다. 
기존 슬라이드(Marp) 방식과 이론 중심 문서의 장점을 결합하여, 학생들이 스크롤하며 자연스럽게 개념을 학습하고 코드를 검증할 수 있도록 설계되었습니다.

---

## 1. 프론트메터 (Frontmatter) 규격

파일 최상단에 반드시 YAML 형식의 메타데이터를 포함해야 합니다.

```yaml
---
id: "pygame_l01_ship"         # 고유 식별자 (과정명_레벨_주제)
contentType: "lesson"         # 반드시 "lesson"으로 설정
track: "pygame_course"        # 소속 트랙명
lang: "python"                # 주 사용 언어 (python, c, java)
categoryId: "pygame_l01"      # 단원 카테고리 ID
title: "1차시. 우주선 좌우 이동하기" # 화면 상단에 표시될 제목
status: "active"              # active 또는 draft
order: 101                    # 정렬 순서
audience: "common"            # 대상 (common, student 등)
tags: ["pygame", "ship", "movement"] # 관련 태그
---
```

---

## 2. 문서 구조 및 스크롤 디자인

스크롤 환경에서 학생의 주의를 집중시키기 위해 적절한 구획 분리가 필요합니다.

### 2.1. 목차 (1.0.)
- 항상 시작 부분에 목차를 제공하여 앞으로 배울 내용을 예고합니다.
- 동적 목차 플로팅 위젯(TOC)이 h1, h2 태그를 기반으로 자동 생성되므로, **헤더 계층 구조를 명확히** 유지하세요.

### 2.2. 슬라이드 구분선 (`---`)
- `---`는 시각적인 카드(Section Card) 분리 단위로 렌더링됩니다.
- 한 가지 핵심 개념이나 하나의 미션이 끝날 때마다 `---`를 넣어 여백을 확보하세요.

---

## 3. 인터랙티브 컴포넌트

학생이 단순히 글만 읽는 것을 방지하기 위해 제공되는 컴포넌트들입니다.

### 3.1. 객관식 체크 카드 (`theory-mcq-card`) [권장]
수업 운영 시 교사가 정답을 일일이 확인하기 힘든 경우, 자동 채점과 피드백을 제공하는 객관식 미션을 권장합니다.

**작성 템플릿:**
```html
<div class="theory-mcq-card">
  <h3>Q. 우주선을 오른쪽으로 이동시키는 올바른 코드는 무엇일까요?</h3>
  <div class="mcq-options">
    <div class="mcq-option" data-correct="false" data-hint="x 좌표를 빼면 왼쪽으로 이동하게 됩니다.">
      <code>ship_rect.x -= speed</code>
    </div>
    <div class="mcq-option" data-correct="true">
      <code>ship_rect.x += speed</code>
    </div>
  </div>
  <div class="mcq-hint"></div>
</div>
```
- `data-correct="true"`: 정답 옵션에 부여합니다.
- `data-hint="..."`: 오답 선택 시 학생에게 보여줄 맞춤형 힌트 메시지입니다.
- `.mcq-hint`: 선택 결과 메시지가 출력될 빈 공간입니다. 반드시 포함하세요.

### 3.2. 단답형 체크 카드 (`theory-mini-check-card`)
직접 코드를 타이핑하게 만들고 싶을 때 제한적으로 사용합니다.

**작성 템플릿:**
```html
<div class="theory-mini-check-card" data-answer="ship_rect.right = 800">
  <input type="text" class="stage-key-input" placeholder="정답 코드(ship_rect.right = ???) 입력...">
  <button class="stage-unlock-btn">제출하고 다음으로</button>
</div>
```
- `data-answer`: 정답 문자열. 대소문자를 구분하지 않으며, 띄어쓰기는 자동 무시되어 비교됩니다.

---

## 4. 교사용 수업 운영 기능

### 4.1. 교사용 정답 모드 (Teacher Mode)
수업 중 교사가 빠른 확인이나 화면 시연을 위해 정답을 미리 볼 수 있습니다.
- **접속 방법:** 이론 페이지 URL 끝에 `?teacher=1` 파라미터를 붙여 접속합니다.
- **기능:** 우측 하단에 **[👁️ 정답 보기 ON/OFF]** 플로팅 버튼이 생성됩니다.
- **효과:** `theory-mcq-card`의 정답 옵션이 강조되고, `theory-mini-check-card`의 입력창에 정답이 미리 채워집니다.

### 4.2. 진행도 저장
학생이 푼 `mcq-card`나 `mini-check-card`의 결과는 브라우저 `localStorage`에 자동 저장됩니다.
새로고침을 하거나 다음 날 수업을 이어가더라도 이전에 완료한 미션은 '완료(Solved)' 상태로 유지됩니다.

---

## 5. 작성 시 주의사항 (Pedagogy)

1. **용어의 일관성**: 같은 대상을 지칭할 때는 하나의 용어만 사용하세요. (예: `x` 좌표와 `left`가 동일한 위치를 의미한다면, 문서 내에서 이를 명시적으로 짚어주어야 합니다.)
2. **Logic Hole 방지**: 미션의 질문("무엇을 해야 할까요?")과 요구하는 정답(코드 작성) 사이에 논리적 비약이 없도록 힌트나 설명 코드를 충분히 제공하세요.
3. **코드 스니펫**: 부분적인 코드 작성 과제를 줄 때는 앞뒤 문맥을 파악할 수 있도록 전체 `if` 블록 등 뼈대 코드를 먼저 보여주는 것이 좋습니다.
