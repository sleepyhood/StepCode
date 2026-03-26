# JSON Schema Guide for Problem Sets

## 1. 목적

이 문서는 `practice/data/sets/` 아래에서 사용하는 문제지 JSON의 공통 규칙을 정의한다.

이 가이드는 다음 목표를 가진다.

- 과목별 JSON 구조를 가능한 한 일관되게 유지한다.
- `language`, `unity`, `contest` 영역에서 공통으로 해석 가능한 필드를 정리한다.
- 문제 유형(`mcq`, `short`, `code`)별 필수/선택 필드를 명확히 구분한다.
- 프론트엔드 뷰어와 데이터 제작자가 같은 기준으로 파일을 읽고 작성할 수 있게 한다.
- 향후 자동 검증(JSON Schema, lint, 빌드 검증)으로 확장할 수 있는 기반을 만든다.

이 문서는 "모든 JSON이 완전히 동일한 모양이어야 한다"는 의미가 아니라, "공통 뼈대는 통일하고, 문제 유형별 확장은 허용한다"는 원칙을 따른다.

---

## 2. 적용 범위

이 가이드는 다음 경로의 문제지 세트 JSON에 적용한다.

- `practice/data/sets/language/*.json`
- `practice/data/sets/unity/*.json`
- `practice/data/sets/contest/**/*.json`
- `practice/data/sets/*.json` 중 문제지 세트로 간주되는 JSON

적용 대상은 "문항 여러 개를 묶은 세트 파일"이다. 단일 문제 원본, 메타 캐시, 임시 생성 파일은 필요 시 별도 규칙을 둘 수 있다.

---

## 3. 기본 설계 원칙

### 3.1 공통 메타와 문제 데이터는 분리한다

세트 파일은 크게 두 층으로 나눈다.

- 세트 메타데이터
- 문제 목록

즉, 최상위에는 세트 전체를 설명하는 정보가 오고, 실제 채점/출력 정보는 `problems` 배열 안에 둔다.

### 3.2 문제 유형별 정답 구조를 분리한다

문항은 공통 필드를 공유하지만, 정답 관련 필드는 `type`별로 달라진다.

- `mcq`: 선택지와 정답 인덱스 중심
- `short`: 단답 또는 표 입력 중심
- `code`: 코드 한 줄 또는 코드 조각 정답 중심

정답 구조를 무리하게 하나로 합치지 않는다. 대신 공통 키와 유형별 허용 키를 문서로 통제한다.

### 3.3 사람이 읽기 쉬운 JSON을 우선한다

현재 프로젝트의 JSON은 직접 작성과 수동 검토 비중이 높다. 따라서 다음 원칙을 따른다.

- 의미가 분명한 필드명을 사용한다.
- 축약보다 명확성을 우선한다.
- 동일 의미의 중복 필드는 가급적 만들지 않는다.
- 프론트엔드가 추론해야 하는 숨은 규칙을 줄인다.

### 3.4 실제 운영 중인 필드를 우선 표준화한다

이 가이드는 추상적인 이상형보다, 현재 저장소에서 이미 사용 중인 필드를 기준으로 정리한다. 확인된 주요 필드는 다음과 같다.

- 세트 공통: `id`, `title`, `categoryId`, `availableLanguages`, `concepts`, `problems`
- 문제 공통: `id`, `type`, `level`, `title`, `description`, `code`, `teacherExplainMd`, `conceptRef`, `conceptRefs`, `hint`, `ioExample`
- `mcq`: `options`, `optionLabels`, `correctIndex`
- `short`: `expectedText`, `expectedAnyOf`, `answerUi`, `expectedGrid`
- `code`: `expectedCode`, `expectedCodes`

---

## 4. 최상위 세트 구조

### 4.1 권장 형태

```json
{
  "id": "py_lv07_for_b01",
  "title": "Python for문 기초 1회차",
  "categoryId": "py_for",
  "availableLanguages": ["python"],
  "concepts": [],
  "problems": []
}
```

### 4.2 최상위 필드 규칙

| 필드                 | 타입     | 필수 여부 | 설명                             |
| -------------------- | -------- | --------- | -------------------------------- |
| `id`                 | string   | 필수      | 세트 고유 ID                     |
| `title`              | string   | 필수      | 세트 제목                        |
| `categoryId`         | string   | 필수      | 프론트엔드 분류 또는 묶음 ID     |
| `availableLanguages` | string[] | 필수      | 해당 세트에서 허용되는 언어 목록 |
| `concepts`           | object[] | 선택      | 개념 설명 목록                   |
| `problems`           | object[] | 필수      | 문제 목록                        |

### 4.3 최상위 필드 상세

#### `id`

- 세트 파일 전체에서 유일해야 한다.
- 파일명과 동일하게 맞추는 것을 강력 권장한다.
- 확장자 `.json`을 제외한 파일명과 `id`가 일치해야 한다.

좋은 예:

```json
{
  "id": "unity_u03_function_syntax"
}
```

피해야 할 예:

```json
{
  "id": "set1"
}
```

이유:

- 검색이 어렵다.
- 도메인/주제/회차 정보가 드러나지 않는다.
- 파일명과 불일치할 가능성이 높아진다.

#### `title`

- 사용자에게 직접 보일 수 있는 자연어 제목이다.
- 약어만 나열하지 말고, 과목/주제/레벨/회차를 식별 가능하게 쓴다.
- 지나치게 짧거나 내부용 코드만 들어간 제목은 피한다.

#### `categoryId`

- 프론트엔드 분류 및 필터링 기준으로 사용한다.
- 동일한 주제군이면 여러 세트가 같은 `categoryId`를 가질 수 있다.
- UI 분류체계와 맞닿는 값이므로, 작성 전에 기존 카테고리 규칙과 충돌하지 않는지 확인한다.

#### `availableLanguages`

- 최소 1개 이상이어야 한다.
- 문자열 배열로 둔다.
- 단일 언어 세트라도 배열 형식을 유지한다.

좋은 예:

```json
{
  "availableLanguages": ["python"]
}
```

권장 언어 값 예시:

- `python`
- `c`
- `java`
- `csharp`

#### `concepts`

- 세트에 연결된 개념 설명이 있을 때만 사용한다.
- 없는 경우 생략 가능하다.
- 문제에서 `conceptRef`나 `conceptRefs`를 사용한다면, 해당 ID를 `concepts` 안에서 찾을 수 있어야 한다.

#### `problems`

- 문제는 반드시 배열로 관리한다.
- 순서 자체가 출력 순서가 되므로, 배열 순서를 의도적으로 관리한다.
- 비어 있는 배열은 허용하지 않는 것을 권장한다.

---

## 5. `concepts` 구조

### 5.1 목적

`concepts`는 세트 안의 문제들이 어떤 개념과 연결되는지 설명하는 메타 정보다.

대표 용도:

- 학습 포인트 묶음
- 이론 문서 연결
- 문제와 개념의 참조 관계 표현
- 향후 개념 카드 UI 렌더링

### 5.2 권장 형태

```json
{
  "concepts": [
    {
      "id": "range_len",
      "title": "range와 len",
      "summary": "`range(len(lst))`는 0부터 `len(lst)-1`까지 반복합니다."
    }
  ]
}
```

### 5.3 개념 객체 필드

| 필드              | 타입     | 필수 여부 | 설명                |
| ----------------- | -------- | --------- | ------------------- |
| `id`              | string   | 필수      | 개념 고유 ID        |
| `title`           | string   | 필수      | 개념 제목           |
| `summary`         | string   | 필수      | 개념 요약           |
| `example`         | string   | 선택      | 예시 코드/텍스트    |
| `algorithm`       | string   | 선택      | 단계형 설명         |
| `media`           | object[] | 선택      | 이미지 등 보조 자료 |
| `relatedProblems` | string[] | 선택      | 관련 문제 ID 목록   |

### 5.4 개념 관련 규칙

- `id`는 세트 내부에서 유일해야 한다.
- `relatedProblems`는 실제 `problems[].id`를 참조해야 한다.
- `media`를 사용할 때는 경로가 실제 자산 위치와 맞아야 한다.
- `conceptRef`와 `conceptRefs`를 동시에 사용할 수 있으나, 의미 충돌이 없어야 한다.

### 5.5 `conceptRef`와 `conceptRefs`

문제 객체에서 사용하는 참조 방식은 두 가지를 허용한다.

- `conceptRef`: 대표 개념 1개
- `conceptRefs`: 관련 개념 여러 개

권장 기준:

- 주 개념이 1개면 `conceptRef`
- 주 개념 1개와 보조 개념이 더 있으면 `conceptRef` + `conceptRefs`
- 복수 개념만 중요하고 대표 1개를 정하기 어렵다면 `conceptRefs`

단, 다음 규칙을 권장한다.

- `conceptRef`가 있으면 `conceptRefs`에도 그 값을 포함하는 편이 일관성 측면에서 좋다.
- 둘 중 하나만 써도 되지만, 같은 세트 안에서 지나치게 혼용하지 않는다.

---

## 6. 문제 객체 공통 구조

### 6.1 권장 형태

```json
{
  "id": "p01",
  "type": "mcq",
  "level": "basic",
  "title": "예시 문제",
  "description": "문제 설명",
  "code": "print('hello')",
  "teacherExplainMd": "해설",
  "conceptRef": "intro"
}
```

### 6.2 공통 필드 표

| 필드               | 타입           | 필수 여부 | 설명                     |
| ------------------ | -------------- | --------- | ------------------------ |
| `id`               | string         | 필수      | 문제 고유 ID             |
| `type`             | string         | 필수      | 문제 유형                |
| `level`            | string         | 필수      | 난이도 또는 학습 단계    |
| `title`            | string         | 필수      | 문제 제목                |
| `description`      | string         | 필수      | 문제 설명                |
| `code`             | string or null | 선택      | 코드 블록 또는 제시 코드 |
| `teacherExplainMd` | string         | 권장      | 교사용 해설 마크다운     |
| `conceptRef`       | string         | 선택      | 대표 개념 ID             |
| `conceptRefs`      | string[]       | 선택      | 관련 개념 ID 목록        |
| `hint`             | string         | 선택      | 힌트                     |
| `ioExample`        | object         | 선택      | 입력/출력 예시           |

### 6.3 공통 필드 상세

#### `id`

- 세트 내부에서 유일해야 한다.
- 프론트엔드가 키로 사용할 수 있으므로, 수정 시 영향 범위를 확인한다.

권장 패턴 예시:

- `p01`, `p02`
- `mcq1`, `trace1`, `code1`
- `t_range_basic`, `short_last_index`

중요한 것은 "세트 내에서 일관된 네이밍"이다.

#### `type`

현재 표준 유형은 다음 3개다.

- `mcq`
- `short`
- `code`

이 세 유형 외 확장이 필요하면, 먼저 뷰어와 채점 로직이 해당 유형을 이해하는지 확인해야 한다.

#### `level`

현재 저장소에는 다음처럼 혼재된 값이 보인다.

- `기초`
- `단답형`
- `코드 작성`
- `basic`
- `challenge`
- `고`

즉, 현재 `level`은 "난이도", "문항 성격", "학년/대상" 의미가 섞여 있다. 장기적으로는 정리하는 것이 좋다.

권장 방향은 두 가지 중 하나를 택해 통일하는 것이다.

1. 난이도 중심

- `basic`
- `intermediate`
- `advanced`
- `challenge`

2. 한글 중심

- `기초`
- `기본`
- `심화`
- `도전`

주의:

- `단답형`, `코드 작성`은 사실상 `type` 정보와 겹친다.
- `고`, `중`, `초`는 난이도보다 대상군에 가깝다.

따라서 새 파일부터는 `level`을 난이도 의미로 제한하는 것을 권장한다.

#### `title`

- 사용자에게 직접 노출되는 제목이다.
- 문제 번호, 유형, 핵심 포인트를 적절히 반영한다.

권장 예시:

- `MCQ 1. 경계값 선택`
- `Trace 1. 기본 반복 흐름`
- `Code 2. 마지막 3개 역순 출력`

#### `description`

- 문제 풀이에 필요한 설명을 자연어로 적는다.
- 조건, 입력 상황, 요구 사항을 분명히 적는다.
- 여러 줄 텍스트를 허용한다.

#### `code`

- 제시 코드가 있을 경우 문자열로 저장한다.
- 줄바꿈은 `\n`으로 표현한다.
- 코드가 아예 없는 문제는 `null` 또는 생략을 허용하되, 같은 세트 안에서는 한쪽 방식으로 통일하는 것이 좋다.

권장:

- 제시 코드가 없는 경우 `code: null` 또는 필드 생략 중 하나로 프로젝트 전체 기준을 정한다.
- 신규 작성에서는 "없으면 생략"보다 "없으면 `null`"이 더 명시적일 수 있다. 다만 기존 렌더러가 어느 쪽을 더 안정적으로 처리하는지 확인해야 한다.

#### `teacherExplainMd`

- 매우 권장되는 필드다.
- 정답 해설, 교사용 설명, 출제 의도, 흔한 오답 포인트를 마크다운으로 담는다.
- `contest`와 `unity` 계열에서 이미 적극 사용되고 있으므로, 장기적으로는 전 영역 공통 권장 필드로 본다.

권장 내용:

- 정답 근거
- 핵심 개념
- 계산/추론 과정
- 실수 포인트

#### `hint`

- 학생용 또는 제작자용 힌트를 짧게 제공할 때 사용한다.
- `code` 문제에서 유용하다.

#### `ioExample`

- 입출력 예시가 문제 이해에 필요한 경우 사용한다.
- 최소 구조는 다음처럼 단순하게 둘 수 있다.

```json
{
  "ioExample": {
    "input": "10 20 30"
  }
}
```

필요 시 확장 예:

```json
{
  "ioExample": {
    "input": "3\n10 20 30",
    "output": "60"
  }
}
```

---

## 7. 문제 유형별 규칙

### 7.1 `mcq` 타입

#### 목적

보기 중 하나를 고르는 객관식 문제.

#### 필수 필드

| 필드           | 타입     | 필수 여부 | 설명               |
| -------------- | -------- | --------- | ------------------ |
| `options`      | string[] | 필수      | 선택지 목록        |
| `optionLabels` | string[] | 필수      | 보기 라벨          |
| `correctIndex` | number   | 필수      | 정답 선택지 인덱스 |

#### 권장 형태

```json
{
  "id": "mcq1",
  "type": "mcq",
  "level": "basic",
  "title": "MCQ 1. 경계값 선택",
  "description": "설명",
  "code": "for i in range( ??? ):",
  "options": ["len(lst) + 1", "len(lst)", "len(lst) - 1", "1, len(lst)"],
  "optionLabels": ["A", "B", "C", "D"],
  "correctIndex": 1
}
```

#### 규칙

- `options.length`와 `optionLabels.length`는 반드시 같아야 한다.
- `correctIndex`는 `0`부터 시작한다.
- `correctIndex`는 반드시 `options` 범위 안에 있어야 한다.
- `optionLabels`는 프론트엔드 출력 순서와 동일해야 한다.

#### 권장 라벨 규칙

- 4지선다: `["A", "B", "C", "D"]`
- 5지선다: `["A", "B", "C", "D", "E"]`

현재 프로젝트는 영문 대문자 라벨을 주로 사용한다. 새 파일도 동일 규칙을 권장한다.

#### 작성 시 주의

- 정답 텍스트를 `options`와 `teacherExplainMd`에 이중으로 적을 때 서로 모순되지 않게 한다.
- 코드 조각이 긴 선택지는 줄바꿈과 들여쓰기를 보존한다.
- "정답 기준: B"처럼 해설에 라벨을 직접 적는 경우, `correctIndex` 변경 시 해설도 함께 수정해야 한다.

---

### 7.2 `short` 타입

#### 목적

단답형 또는 추적표 입력형 문항.

#### 허용되는 주요 정답 구조

`short`는 실제로 두 하위 패턴이 존재한다.

1. 단일 텍스트 정답
2. 표(grid) 기반 정답

둘을 모두 `short` 안에서 허용한다.

#### A. 단일 텍스트 정답형

##### 주요 필드

| 필드            | 타입     | 필수 여부   | 설명             |
| --------------- | -------- | ----------- | ---------------- |
| `expectedText`  | string   | 조건부 필수 | 대표 정답 텍스트 |
| `expectedAnyOf` | string[] | 선택        | 복수 허용 정답   |

##### 권장 형태

```json
{
  "id": "short1",
  "type": "short",
  "level": "basic",
  "title": "Short 1. 마지막 인덱스",
  "description": "리스트 길이가 n일 때 마지막 인덱스 값을 쓰세요.",
  "code": "n = 8",
  "expectedText": "7"
}
```

##### 규칙

- 정확히 하나의 대표 정답이 있으면 `expectedText`를 사용한다.
- 여러 답이 모두 허용되면 `expectedAnyOf`를 사용한다.
- `expectedText`와 `expectedAnyOf`를 동시에 둘 수는 있지만, 의미가 중복되지 않도록 주의한다.

권장 방식:

- 하나만 정답이면 `expectedText`
- 여러 개가 허용되면 `expectedAnyOf`

예시:

```json
{
  "expectedAnyOf": ["10", "11", "12"]
}
```

#### B. 그리드 정답형

##### 주요 필드

| 필드           | 타입       | 필수 여부   | 설명               |
| -------------- | ---------- | ----------- | ------------------ |
| `answerUi`     | object     | 조건부 필수 | 답안 입력 UI 구조  |
| `expectedGrid` | string[][] | 조건부 필수 | 행/열 기반 정답 값 |

##### 권장 형태

```json
{
  "id": "trace1",
  "type": "short",
  "level": "basic",
  "title": "Trace 1. 반복 흐름 추적",
  "description": "각 반복 직후 값을 표에 채우세요.",
  "code": "for i in range(3):\n    print(i)",
  "answerUi": {
    "kind": "grid",
    "rows": ["1", "2", "3"],
    "columns": ["i", "output"],
    "rowSep": "\n",
    "colSep": " "
  },
  "expectedGrid": [
    ["0", "0"],
    ["1", "1"],
    ["2", "2"]
  ]
}
```

#### `answerUi` 세부 규칙

| 필드                 | 타입     | 필수 여부 | 설명                 |
| -------------------- | -------- | --------- | -------------------- |
| `kind`               | string   | 필수      | 현재는 `grid` 사용   |
| `rows`               | string[] | 필수      | 행 라벨              |
| `columns`            | string[] | 필수      | 열 라벨              |
| `narrowAnswerColumn` | boolean  | 선택      | 답안 열 폭 축소 여부 |
| `rowSep`             | string   | 선택      | 행 구분자            |
| `colSep`             | string   | 선택      | 열 구분자            |

#### 그리드 규칙

- `answerUi.kind`는 현재 `grid`만 표준으로 본다.
- `expectedGrid.length`는 `answerUi.rows.length`와 같아야 한다.
- 각 행의 칸 수는 `answerUi.columns.length`와 같아야 한다.
- 모든 셀 값은 문자열로 저장하는 것을 권장한다.

왜 문자열을 권장하는가:

- 숫자, 기호, 코드 토큰을 혼합해도 일관성이 유지된다.
- 프론트엔드에서 텍스트 렌더링이 단순해진다.
- `"0"`과 `0` 혼용으로 인한 비교 오류를 줄일 수 있다.

#### `short` 타입 작성 시 주의

- `expectedText`와 `expectedGrid`를 동시에 넣지 않는 것을 권장한다.
- 추적표 문제는 `answerUi`와 `expectedGrid`를 한 쌍으로 본다.
- 여러 답 허용 문제는 `expectedAnyOf`를 사용하고, 해설에도 허용 범위를 설명하는 편이 좋다.

---

### 7.3 `code` 타입

#### 목적

학생이 특정 코드 한 줄 또는 짧은 코드 조각을 작성하는 문제.

#### 주요 필드

| 필드            | 타입     | 필수 여부   | 설명           |
| --------------- | -------- | ----------- | -------------- |
| `expectedCode`  | string   | 조건부 필수 | 대표 정답 코드 |
| `expectedCodes` | string[] | 선택        | 추가 허용 정답 |

#### 권장 형태

```json
{
  "id": "code1",
  "type": "code",
  "level": "basic",
  "title": "Code 1. 입력을 리스트로 저장",
  "description": "정수들을 리스트 lst로 저장하는 한 줄을 작성하세요.",
  "code": "n = int(input())\n# TODO",
  "expectedCode": "lst = list(map(int, input().split()))"
}
```

#### 복수 정답 허용 형태

```json
{
  "id": "code2",
  "type": "code",
  "level": "basic",
  "title": "Code 2. 조건식 완성",
  "description": "조건식을 작성하세요.",
  "code": "if (/* TODO */) { }",
  "expectedCode": "score >= 80",
  "expectedCodes": ["80 <= score"]
}
```

#### 규칙

- 대표 정답은 `expectedCode`에 둔다.
- 동등한 대체 정답이 있으면 `expectedCodes`에 추가한다.
- `expectedCodes`를 둘 경우, `expectedCode`와 의미가 동등해야 한다.
- `expectedCodes` 안에 `expectedCode`를 중복으로 넣지 않는다.

#### 작성 시 주의

- 공백, 줄바꿈, 들여쓰기 차이를 채점에서 어떻게 다룰지 아직 구현에 따라 달라질 수 있으므로, 문서 작성자는 가능한 한 표준형 한 가지를 제시한다.
- 여러 줄 정답이 필요한 경우 문자열 안에 줄바꿈을 포함할 수 있지만, 가능하면 문제 설계를 한 줄 또는 짧은 블록 기준으로 단순화한다.
- 언어별 문법 변형이 많다면 `expectedCodes`로 보완한다.

---

## 8. 필수/선택 필드 요약

### 8.1 세트 레벨

| 필드                 | 상태 |
| -------------------- | ---- |
| `id`                 | 필수 |
| `title`              | 필수 |
| `categoryId`         | 필수 |
| `availableLanguages` | 필수 |
| `problems`           | 필수 |
| `concepts`           | 선택 |

### 8.2 문제 공통

| 필드               | 상태 |
| ------------------ | ---- |
| `id`               | 필수 |
| `type`             | 필수 |
| `level`            | 필수 |
| `title`            | 필수 |
| `description`      | 필수 |
| `code`             | 선택 |
| `teacherExplainMd` | 권장 |
| `conceptRef`       | 선택 |
| `conceptRefs`      | 선택 |
| `hint`             | 선택 |
| `ioExample`        | 선택 |

### 8.3 타입별 정답 필드

| `type`  | 필수/조건부 필드                                                     |
| ------- | -------------------------------------------------------------------- |
| `mcq`   | `options`, `optionLabels`, `correctIndex`                            |
| `short` | `expectedText` 또는 `expectedAnyOf` 또는 `answerUi` + `expectedGrid` |
| `code`  | `expectedCode`                                                       |

---

## 9. 명명 규칙

### 9.1 세트 파일명과 `id`

파일명과 `id`는 동일하게 맞춘다.

예시:

- 파일명: `py_lv07_for_b01.json`
- `id`: `py_lv07_for_b01`

예시:

- 파일명: `unity_u03_function_syntax.json`
- `id`: `unity_u03_function_syntax`

### 9.2 세트 ID 권장 패턴

도메인에 따라 다음처럼 읽히는 이름을 권장한다.

- 언어 학습형: `{lang}_lv{NN}_{topic}_{round}`
- 유니티형: `unity_u{NN}_{topic}`
- 경시형: `contest_{lang}_{group}_{year}_{round}_{batch}`

예시:

- `py_lv07_for_b01`
- `c_lv06_if_b03`
- `unity_u03_function_syntax`
- `contest_py_high_2024_r3_b01`

### 9.3 문제 ID 권장 패턴

두 가지 스타일 중 하나를 세트 단위로 고정한다.

1. 역할형

- `mcq1`
- `trace1`
- `short2`
- `code1`

2. 의미형

- `t_range_basic`
- `short_last_index`
- `code_input_list`

중요한 것은 같은 세트 안에서 섞더라도 의도적으로 섞어야 하며, 무질서하게 섞지 않는 것이다.

---

## 10. 값 표준화 권장안

### 10.1 `level`

새 파일부터는 아래 둘 중 하나를 택해 통일할 것을 권장한다.

영문 중심:

- `basic`
- `intermediate`
- `advanced`
- `challenge`

한글 중심:

- `기초`
- `기본`
- `심화`
- `도전`

권장:

- 뷰어/UI가 다국어를 크게 요구하지 않으면 한글 중심도 가능하다.
- 다만 외부 도구, 자동화, 정렬, 필터링까지 고려하면 영문 소문자가 더 안정적이다.

### 10.2 `availableLanguages`

프로젝트 전체에서 소문자 식별자를 유지한다.

예:

- `python`
- `c`
- `java`
- `csharp`

### 10.3 `type`

현재는 다음 세 값만 표준으로 유지한다.

- `mcq`
- `short`
- `code`

새 타입을 도입하기 전에 다음을 먼저 확인해야 한다.

- 뷰어 렌더링 지원 여부
- 채점 로직 지원 여부
- 작성자 문서 업데이트 여부

---

## 11. 금지 또는 비권장 패턴

### 11.1 의미가 겹치는 필드 남용

비권장:

- 난이도 대신 `level`에 문제 유형을 넣는 것
- 같은 의미를 `description`과 `teacherExplainMd`에 중복해서 적는 것

### 11.2 타입과 맞지 않는 정답 필드 혼합

비권장:

- `mcq` 문제에 `expectedText` 추가
- `code` 문제에 `correctIndex` 추가
- `short` 텍스트형 문제에 `expectedGrid` 추가

가능하더라도, 뷰어와 작성자 모두 혼란스러워진다.

### 11.3 참조 무결성 없는 개념 연결

비권장:

- `conceptRef` 값이 `concepts`에 존재하지 않는 경우
- `relatedProblems`에 존재하지 않는 문제 ID를 넣는 경우

### 11.4 라벨 길이 불일치

비권장:

```json
{
  "options": ["A", "B", "C", "D"],
  "optionLabels": ["A", "B", "C"]
}
```

### 11.5 파일명과 `id` 불일치

비권장:

- 파일명: `py_lv07_for_b01.json`
- `id`: `py_for_round_1`

이 패턴은 검색, 디버깅, 자동화에서 지속적으로 문제를 만든다.

---

## 12. 작성 체크리스트

새 JSON을 만들거나 수정할 때 아래 순서로 검토한다.

### 12.1 세트 수준 체크

- 파일명과 `id`가 같은가
- `title`이 자연어 제목으로 읽히는가
- `categoryId`가 기존 분류 규칙과 충돌하지 않는가
- `availableLanguages`가 배열인가
- `problems`가 비어 있지 않은가

### 12.2 개념 연결 체크

- `concepts[].id`가 중복되지 않는가
- `conceptRef`와 `conceptRefs`가 실제 개념 ID를 가리키는가
- `relatedProblems`가 실제 문제 ID를 가리키는가

### 12.3 문제 공통 체크

- 각 문제 `id`가 유일한가
- `type`이 표준값인가
- `level` 값이 세트 내에서 일관적인가
- `title`, `description`이 비어 있지 않은가
- `code`가 필요 없는 문제면 `null` 또는 생략 규칙을 지켰는가

### 12.4 타입별 체크

`mcq`

- `options`와 `optionLabels` 길이가 같은가
- `correctIndex`가 범위 안인가

`short`

- `expectedText`, `expectedAnyOf`, `expectedGrid` 중 문제 의도에 맞는 구조를 골랐는가
- 그리드형이면 `rows`, `columns`, `expectedGrid` 차원이 일치하는가

`code`

- `expectedCode`가 존재하는가
- `expectedCodes`가 있다면 실제로 동등 정답만 담고 있는가

### 12.5 해설 체크

- `teacherExplainMd`가 있다면 정답과 모순되지 않는가
- 해설 안의 정답 라벨이 `correctIndex`와 일치하는가
- 설명에 있는 코드/출력 값이 실제 정답과 일치하는가

---

## 13. 권장 예시

### 13.1 최소형 세트 예시

```json
{
  "id": "py_lv07_for_b01",
  "title": "Python for문 기초 1회차",
  "categoryId": "py_for",
  "availableLanguages": ["python"],
  "problems": [
    {
      "id": "mcq1",
      "type": "mcq",
      "level": "basic",
      "title": "MCQ 1. 반복 범위 선택",
      "description": "리스트의 모든 원소를 정확히 한 번씩 출력하려면 무엇이 들어가야 하는지 고르세요.",
      "code": "for i in range( ??? ):\n    print(lst[i])",
      "options": ["len(lst) + 1", "len(lst)", "len(lst) - 1", "1, len(lst)"],
      "optionLabels": ["A", "B", "C", "D"],
      "correctIndex": 1,
      "teacherExplainMd": "정답은 B입니다. `range(len(lst))`는 0부터 마지막 인덱스까지 정확히 한 번씩 순회합니다."
    }
  ]
}
```

### 13.2 개념 포함 세트 예시

```json
{
  "id": "unity_u03_function_syntax",
  "title": "Unity U03 함수/static 기초",
  "categoryId": "unity_u03_function_syntax",
  "availableLanguages": ["csharp"],
  "concepts": [
    {
      "id": "static_context",
      "title": "static 문맥",
      "summary": "static 메서드는 인스턴스 없이 호출되며, 인스턴스 필드에 직접 접근할 수 없습니다."
    }
  ],
  "problems": [
    {
      "id": "p01",
      "type": "mcq",
      "level": "basic",
      "title": "static 문맥 오류 수정",
      "description": "빈칸에 들어갈 키워드를 고르세요.",
      "code": "public class Example : MonoBehaviour\n{\n    [ ① ] float statFloat = 0;\n    private static void ThisStat()\n    {\n        statFloat = 1;\n    }\n}",
      "options": ["`static`", "`const`", "`readonly`", "`private`"],
      "optionLabels": ["A", "B", "C", "D"],
      "correctIndex": 0,
      "conceptRef": "static_context",
      "teacherExplainMd": "static 메서드에서 접근하려면 필드도 static이어야 합니다."
    }
  ]
}
```

### 13.3 그리드형 `short` 예시

```json
{
  "id": "trace_demo",
  "title": "Trace Demo",
  "categoryId": "trace_demo",
  "availableLanguages": ["python"],
  "problems": [
    {
      "id": "trace1",
      "type": "short",
      "level": "basic",
      "title": "Trace 1. 누적합",
      "description": "각 반복 직후 값을 표에 채우세요.",
      "code": "sumv = 0\nfor i in range(1, 4):\n    sumv += i",
      "answerUi": {
        "kind": "grid",
        "rows": ["1", "2", "3"],
        "columns": ["i", "sumv"],
        "rowSep": "\n",
        "colSep": " "
      },
      "expectedGrid": [
        ["1", "1"],
        ["2", "3"],
        ["3", "6"]
      ]
    }
  ]
}
```

### 13.4 대체 정답 허용 `code` 예시

```json
{
  "id": "code_demo",
  "title": "Code Demo",
  "categoryId": "code_demo",
  "availableLanguages": ["c"],
  "problems": [
    {
      "id": "code1",
      "type": "code",
      "level": "basic",
      "title": "Code 1. 조건식 작성",
      "description": "B 구간 조건식을 작성하세요.",
      "code": "else if (/* TODO */) {\n    printf(\"B\\n\");\n}",
      "expectedCode": "score >= 80",
      "expectedCodes": ["80 <= score"],
      "hint": "앞선 if가 거짓이라는 사실을 이용하세요."
    }
  ]
}
```

---

## 14. 실무 운영 권장안

### 14.1 신규 파일 작성 기준

새로운 문제지 JSON은 다음 기준으로 작성하는 것을 권장한다.

- 최상위 필드: `id`, `title`, `categoryId`, `availableLanguages`, `problems`
- 필요 시 `concepts` 추가
- 모든 문제에 `id`, `type`, `level`, `title`, `description`
- 가능한 경우 `teacherExplainMd` 포함
- 정답 필드는 `type`에 맞는 것만 사용

### 14.2 기존 파일 점진 정리 기준

기존 파일은 한 번에 전부 바꾸기보다 아래 순서로 정리한다.

1. 파일명과 `id` 일치
2. `type`별 정답 필드 정리
3. `teacherExplainMd` 보강
4. `level` 값 표준화
5. `concepts`와 참조 무결성 정리

### 14.3 프론트엔드 구현 시 기대 동작

뷰어는 다음을 기본 가정으로 처리하는 것이 좋다.

- `concepts`는 없어도 된다.
- `code`는 없거나 `null`일 수 있다.
- `teacherExplainMd`는 없어도 된다.
- `short`는 텍스트형과 그리드형 둘 다 지원해야 한다.
- `code`는 `expectedCode` 외 `expectedCodes`까지 허용할 수 있다.

---

## 15. 향후 확장 제안

이 문서는 사람용 가이드다. 이후 자동 검증을 위해 아래를 추가할 수 있다.

- `practice/data/sets/schema/set.schema.json`
- `practice/data/sets/schema/problem.schema.json`
- `practice/data/sets/examples/`
- 검증 스크립트

권장 순서:

1. 이 문서 기준으로 수동 작성 규칙 통일
2. 대표 세트 몇 개를 샘플로 정리
3. JSON Schema 초안 추가
4. CI 또는 로컬 검증 스크립트 연결

---

## 16. 최종 원칙 요약

- 세트 구조는 통일하고, 문제 정답 구조는 `type`별로 분리한다.
- `id`, `title`, `categoryId`, `availableLanguages`, `problems`는 최상위 공통 필수다.
- 문제는 `id`, `type`, `level`, `title`, `description`를 공통 필수로 본다.
- `teacherExplainMd`는 전 영역 공통 권장 필드로 확대한다.
- `concepts`, `conceptRef`, `conceptRefs`는 선택 확장으로 유지한다.
- `short`는 텍스트형과 그리드형을 모두 허용한다.
- `code`는 `expectedCode`를 중심으로, 필요 시 `expectedCodes`로 대체 정답을 허용한다.
- 파일명과 `id`는 반드시 맞춘다.
