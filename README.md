# StepCode

**StepCode**는 프로그래밍 학원용 **실행 추적 · 객관식(MCQ) · 코드 작성/수정 연습** 플랫폼입니다.  
지금은 **로컬에서 정적 파일만으로** 돌리지만,  
나중에 학원 사이트(Flask 등)와 쉽게 연동할 수 있도록 구조를 나눠두었습니다.

---

## 1. 폴더 구조

```text
StepCode/
└─ practice/
   ├─ index.html              # 문제 목록 페이지 (카테고리/회차 리스트)
   ├─ practice.html           # 실제 문제 푸는 연습장 화면
   ├─ assets/
   │  ├─ css/
   │  │  ├─ main.css          # 공통 레이아웃 + 목록(index.html) 스타일
   │  │  └─ practice.css      # 연습장(practice.html) 문제 카드/채점 스타일
   │  └─ js/
   │     ├─ config.js         # APP_CONFIG(mode, data 경로 등 공통 설정)
   │     ├─ index.js          # index.html용 JS (카테고리/세트 목록 렌더)
   │     ├─ practice.js       # practice.html용 JS (문제 렌더 + 채점)
   │     └─ services/
   │        └─ problemService.local.js  # JSON에서 문제 읽는 서비스
   └─ data/
      ├─ categories.json      # 카테고리 목록 (C-조건문, Python-조건문 등)
      ├─ sets.index.json      # 세트(회차) 메타데이터 목록
      └─ sets/
         ├─ c_if_b1.json      # C 조건문 기초 1회차 세트
         ├─ c_if_c1.json      # C 조건문 챌린지 1회차 세트
         ├─ py_if_b1.json     # Python 조건문 기초 1회차 세트
         └─ java_if_b1.json   # Java 조건문 기초 1회차 세트
```

---

## 2. 실행 방법 (로컬 서버)

브라우저 보안 정책 때문에, `file://` 로 직접 열면 JSON을 `fetch()` 할 수 없습니다.
반드시 **간단한 HTTP 서버**를 띄운 다음, `http://` 로 접속해야 합니다.

1. `practice` 폴더로 이동
   (예: `C:\...\StepCode\practice`)

2. 해당 폴더에서 터미널(cmd/PowerShell) 열기 후:

   ```bash
   python -m http.server 8000
   ```

3. 브라우저에서 접속:

   ```text
   http://localhost:8000/index.html
   ```

이제:

* `index.html`: 카테고리/세트 목록 화면
* 각 세트 링크 클릭 → `practice.html?set=세트ID` 로 연습장 화면 이동

---

## 3. 데이터 구조

### 3.1 카테고리 목록: `data/categories.json`

카테고리(언어+주제)를 정의합니다.

```json
[
  { "id": "c_if",    "name": "C - 조건문",        "order": 10 },
  { "id": "c_loop",  "name": "C - 반복문",        "order": 20 },
  { "id": "py_if",   "name": "Python - 조건문",   "order": 30 },
  { "id": "java_if", "name": "Java - 조건문",     "order": 40 }
]
```

* `id`      : 카테고리 고유 ID (세트에서 `categoryId`로 참조)
* `name`    : index 화면에 표시되는 이름
* `order`   : 카테고리 표시 순서 (작을수록 위에 배치)

---

### 3.2 세트 목록: `data/sets.index.json`

각 세트(회차)에 대한 메타데이터입니다.

```json
[
  {
    "id": "c_if_b1",
    "categoryId": "c_if",
    "title": "C 조건문 기초 1회차",
    "round": 1,
    "difficulty": "basic",
    "numProblems": 9,
    "file": "c_if_b1.json"
  },
  {
    "id": "c_if_c1",
    "categoryId": "c_if",
    "title": "C 조건문 챌린지 1회차",
    "round": 2,
    "difficulty": "challenge",
    "numProblems": 8,
    "file": "c_if_c1.json"
  },
  {
    "id": "py_if_b1",
    "categoryId": "py_if",
    "title": "Python 조건문 기초 1회차",
    "round": 1,
    "difficulty": "basic",
    "numProblems": 9,
    "file": "py_if_b1.json"
  },
  {
    "id": "java_if_b1",
    "categoryId": "java_if",
    "title": "Java 조건문 기초 1회차",
    "round": 1,
    "difficulty": "basic",
    "numProblems": 9,
    "file": "java_if_b1.json"
  }
]
```

* `id`          : 세트 ID (`?set=id` 로 사용)
* `categoryId`  : `categories.json`의 `id` 와 연결
* `title`       : 세트 제목 (학생이 보는 이름)
* `round`       : 회차 번호 (카테고리 안에서 정렬 기준)
* `difficulty`  : 난이도 태그 (예: `basic`, `challenge`)
* `numProblems` : 문제 개수 (표시용)
* `file`        : 실제 세트 JSON 파일명 (`data/sets/{file}`)

---

### 3.3 세트 JSON: `data/sets/*.json`

각 세트 파일은 공통 구조를 갖습니다.

```json
{
  "id": "c_if_b1",
  "title": "C 조건문 기초 1회차",
  "categoryId": "c_if",
  "availableLanguages": ["c"],
  "problems": [
    { /* problem 1 */ },
    { /* problem 2 */ }
  ]
}
```

* `id`, `title`, `categoryId` : `sets.index.json`과 일관성 유지
* `availableLanguages`        : 이 세트에서 사용하는 언어 목록 (현재는 단일 언어)
* `problems`                  : 문제 배열

---

## 4. 문제 형식(Problem Schema)

`problems` 배열 안의 각 문제는 `type`에 따라 구조가 조금씩 다릅니다.

### 4.1 MCQ (객관식)

```json
{
  "id": "mcq1",
  "type": "mcq",
  "level": "기초",
  "title": "MCQ 1. Pass / Fail 프로그램",
  "description": "요구사항 설명...",
  "code": "int n;\nscanf(\"%d\", &n);\nif (n >= 60) { ... }",
  "options": [
    "보기 A 코드 또는 텍스트",
    "보기 B ...",
    "보기 C ...",
    "보기 D ..."
  ],
  "optionLabels": ["A", "B", "C", "D"],
  "correctIndex": 2
}
```

* `code`         : 공통 코드 (보기 위에 보여줄 원본 코드), 없으면 `null` 가능
* `options`      : 각 보기 문자열 (코드/출력/설명 등)
* `optionLabels` : 보기에 표시할 라벨 (A/B/C/D)
* `correctIndex` : 정답 보기 인덱스 (0부터 시작)

렌더링 시:

* 라디오 버튼 + 보기 카드 형태로 표시
* `correctIndex`를 기준으로 채점

---

### 4.2 short (단답형)

#### 단일 정답:

```json
{
  "id": "short1",
  "type": "short",
  "level": "단답형",
  "title": "Short 1. 출력 결과 쓰기",
  "description": "입력이 7일 때 출력 한 줄을 쓰세요.",
  "code": "int n;\nscanf(\"%d\", &n);\nif (n >= 5 && n <= 10) { ... }",
  "expectedText": "OK"
}
```

#### 여러 정답 중 하나 허용:

```json
{
  "id": "short2",
  "type": "short",
  "level": "단답형",
  "title": "Short 2. 조건을 만족하는 n",
  "description": "1 <= n && n <= 5 를 참으로 만드는 n의 값 하나를 쓰세요.",
  "code": "1 <= n && n <= 5",
  "expectedAnyOf": ["1", "2", "3", "4", "5"]
}
```

채점:

* 공백/대소문자를 정규화하여 비교
* `expectedAnyOf`가 있으면 그 배열 안의 어떤 값과 일치해도 정답
* 없으면 `expectedText`와 비교

---

### 4.3 code (코드 작성/수정)

```json
{
  "id": "code1",
  "type": "code",
  "level": "코드 작성",
  "title": "Code 1. 1 이상 10 이하 조건식 작성",
  "description": "/* 여기에 조건식 작성 */ 부분에 들어갈 코드를 쓰세요.",
  "code": "int n;\nscanf(\"%d\", &n);\nif ( /* 여기에 작성 */ ) {\n    printf(\"InRange\\n\");\n}",
  "expectedCode": "n >= 1 && n <= 10",
  "hint": "공백은 크게 상관 없습니다. && 연산자를 사용하세요."
}
```

채점:

* `normalizeCode`로 사용자 입력과 `expectedCode`를 모두 정규화
  (개행, 공백, 주석, 연산자 주변 공백 제거 등)
* 구조가 동일하면 정답 처리 (공백/줄 바뀜에 덜 민감함)

---

## 5. 동작 흐름 요약

### 5.1 index.html

* `assets/js/index.js` 에서:

  ```js
  const [categories, sets] = await Promise.all([
    ProblemService.listCategories(),
    ProblemService.listSets()
  ]);
  ```

* `categories`를 `order` 기준으로 정렬 후,

* `sets`를 `categoryId`별로 묶어서,

* 각 세트는 `practice.html?set=세트ID` 링크로 렌더링

---

### 5.2 practice.html

* URL에서 `set` 파라미터 읽기:

  ```js
  const setId = new URLSearchParams(location.search).get("set");
  currentSetData = await ProblemService.loadSet(setId);
  ```

* `currentSetData.problems` 를 순회하며 문제 카드 렌더:

  * `type === "mcq"` → 라디오 + 보기 카드
  * `type === "short"` → 단답형 textarea
  * `type === "code"` → 코드 입력 textarea

* `채점하기` 버튼 클릭 시:

  * 각 문제 유형별로 정답 비교
  * 카드 하단 `feedback` 영역에 ✅/❌ 보여주고
  * 상단 `score` 영역에 전체 정답 개수 표시

---

### 5.3 ProblemService 레이어 (local 버전)

`assets/js/config.js`:

```js
const APP_CONFIG = {
  mode: "local",
  dataBasePath: "./data"
};
```

`assets/js/services/problemService.local.js`:

```js
const ProblemService = {
  async listCategories() {
    const res = await fetch(`${APP_CONFIG.dataBasePath}/categories.json`);
    if (!res.ok) throw new Error("failed to load categories");
    return res.json();
  },

  async listSets() {
    const res = await fetch(`${APP_CONFIG.dataBasePath}/sets.index.json`);
    if (!res.ok) throw new Error("failed to load sets index");
    return res.json();
  },

  async loadSet(setId) {
    const sets = await this.listSets();
    const meta = sets.find((s) => s.id === setId);
    if (!meta) {
      throw new Error(`Unknown setId: ${setId}`);
    }

    const res = await fetch(
      `${APP_CONFIG.dataBasePath}/sets/${meta.file}`
    );
    if (!res.ok) throw new Error(`failed to load set: ${meta.file}`);
    return res.json();
  }
};
```

나중에 학원 서버 API로 연동할 때는,
이 인터페이스를 유지한 채 `fetch("/api/...")`를 사용하는 `problemService.api.js`로 교체하면 됨.

---

## 6. 새 문제 / 새 세트 추가 가이드

### 6.1 기존 세트에 문제 추가

1. `data/sets/{세트ID}.json` 파일 열기
   (예: `data/sets/c_if_b1.json`)
2. `problems` 배열 끝에 새로운 문제 객체 추가

   * `id`는 세트 내에서 고유하게
   * `type`에 맞춰 `mcq` / `short` / `code` 템플릿 사용
3. (선택) `sets.index.json`에서 해당 세트의 `numProblems` 업데이트

---

### 6.2 새 세트(회차) 추가

예: `C 조건문 챌린지 1회차` → `c_if_c1`

1. `data/sets/c_if_c1.json` 생성:

   ```json
   {
     "id": "c_if_c1",
     "title": "C 조건문 챌린지 1회차",
     "categoryId": "c_if",
     "availableLanguages": ["c"],
     "problems": [
       /* 문제들... */
     ]
   }
   ```

2. `data/sets.index.json` 에 메타데이터 추가:

   ```json
   {
     "id": "c_if_c1",
     "categoryId": "c_if",
     "title": "C 조건문 챌린지 1회차",
     "round": 2,
     "difficulty": "challenge",
     "numProblems": 8,
     "file": "c_if_c1.json"
   }
   ```

3. 서버 실행 후 `index.html` 에서 C - 조건문 아래에 2회차 세트가 보이는지 확인

---

### 6.3 새 언어/카테고리 추가 (예: Python, Java)

1. `data/categories.json` 에 새 카테고리 추가:

   ```json
   { "id": "py_if", "name": "Python - 조건문", "order": 30 }
   ```

2. `data/sets/py_if_b1.json` 등 세트 파일 추가

3. `data/sets.index.json` 에 세트 메타데이터 추가:

   ```json
   {
     "id": "py_if_b1",
     "categoryId": "py_if",
     "title": "Python 조건문 기초 1회차",
     "round": 1,
     "difficulty": "basic",
     "numProblems": 9,
     "file": "py_if_b1.json"
   }
   ```

---

## 7. 향후 확장 방향 (초기 설계 의도)

* **제출/점수 저장**

  * 로그인된 학생 정보와 함께 `POST /api/.../submit` 형태로 점수 기록
  * DB에 `user_id`, `quiz_id`, `score`, `detail_json` 등을 저장
* **1회 제출 제한**

  * 서버에서 `UNIQUE (user_id, quiz_id)` 제약 또는 `attempt` 카운트
* **언어별 코드 통합**

  * 현재는 세트 단위로 언어를 분리했지만,
  * 나중에는 문제 단위에 `codeByLang` 구조를 도입해
    같은 개념을 언어별로 스위칭하는 연습도 가능

현재 구조(HTML/JS/JSON 분리 + ProblemService 레이어)는
이런 확장을 고려한 초석 역할을 합니다.
