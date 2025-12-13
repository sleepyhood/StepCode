# StepCode – 실행추적 · MCQ · 코드수정 연습

로컬에서 가볍게 돌릴 수 있는 **실행추적/MCQ/코드 작성 연습장**입니다.  
이 문서는 특히 **새로운 문제 세트를 JSON으로 추가할 때 따라야 할 규칙**에 초점을 맞춥니다.

---

## 1. 폴더 구조

`practice/` 폴더 기준 구조는 다음과 같습니다.

```text
practice/
  index.html            # 메인 목록 페이지
  practice.html         # 실제 문제 풀이 페이지
  index.js
  practice.js
  main.css
  practice.css

  data/
    categories.json     # 카테고리 목록 (C-조건문, Python-for 등)
    sets.index.json     # 세트(회차) 메타데이터 목록
    sets/
      c_if_b1.json      # C 조건문 기초 1회차
      c_if_c1.json      # C 조건문 챌린지 1회차
      c_for_b1.json     # C for문 기초 1회차
      c_for_c1.json     # C for문 챌린지 1회차
      py_input_b1.json  # Python 입력 기초 1회차
      py_if_b1.json     # Python 조건문 기초 1회차
      py_for_b1.json    # Python for문 기초 1회차
      py_for_c1.json    # Python for문 챌린지 1회차
      py_while_b1.json  # Python while문 기초 1회차
      java_if_b1.json   # Java 조건문 기초 1회차
```

> **실전에서 자주 수정하는 파일**
>
> * 카테고리/세트 추가 : `data/categories.json`, `data/sets.index.json`
> * 실제 문제 내용 : `data/sets/*.json`

---

## 2. 실행 방법 (로컬 테스트)

브라우저의 보안 정책 때문에 **파일을 그냥 더블클릭해서** 열면 JSON을 못 불러옵니다.
반드시 간단한 로컬 서버를 띄운 뒤 접속합니다.

### 2.1 Python 내장 서버 사용

```bash
cd practice
python -m http.server 8000
```

그 다음 브라우저에서:

* 메인: `http://localhost:8000/index.html`
* 문제풀이: 세트 선택 후 자동 이동 (`practice.html?set=...`)

VSCode Live Server, Web Server for Chrome 등 다른 정적 서버를 써도 됩니다.

---

## 3. 데이터 구조

### 3.1 `categories.json` – 카테고리 목록

각 카테고리(과목/단원)에 대한 메타데이터입니다.

필드:

* `id` : 내부용 고유 ID (영문 소문자 + `_`)
* `name` : 메인 화면에 보여줄 이름
* `order` : 정렬 순서 (작을수록 위에 표시)

현재 예시:

```json
[
  { "id": "c_if",      "name": "C - 조건문",               "order": 10 },
  { "id": "c_for",     "name": "C - Lv7 반복1(for)",       "order": 20 },
  { "id": "py_input",  "name": "Python - Lv3 입력",        "order": 30 },
  { "id": "py_if",     "name": "Python - Lv6 조건",        "order": 40 },
  { "id": "py_for",    "name": "Python - Lv7 반복1(for)",  "order": 50 },
  { "id": "py_while",  "name": "Python - Lv8 반복2(while)","order": 60 },
  { "id": "java_if",   "name": "Java - 조건문",            "order": 70 }
]
```

> 새 단원을 만들 때는 여기에 항목을 하나 추가하고, `id`를 이후 세트/문제에서 `categoryId`로 사용합니다.

---

### 3.2 `sets.index.json` – 세트(회차) 목록

한 줄이 “연습장 1회차”에 해당합니다. 메인 페이지에서 이 파일을 읽어 **카테고리별 세트 버튼**을 만듭니다.

필드:

* `id` : 세트 고유 ID (파일명, practice.html 쿼리스트링에 모두 사용)
* `categoryId` : 위 `categories.json` 중 하나의 `id`
* `title` : 버튼에 표시할 전체 제목
* `round` : 회차 번호 (1, 2, 3…)
* `difficulty` : 난이도. **현재는 `basic` / `challenge` 두 종류만 사용**
* `numProblems` : 해당 세트 JSON에 들어 있는 문제 개수
* `file` : 실제 세트 JSON 파일 이름 (`data/sets/` 기준)

현재 예시:

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
  },
  {
    "id": "py_input_b1",
    "categoryId": "py_input",
    "title": "Python 입력 기초 1회차",
    "round": 1,
    "difficulty": "basic",
    "numProblems": 9,
    "file": "py_input_b1.json"
  },
  {
    "id": "py_for_b1",
    "categoryId": "py_for",
    "title": "Python for문 기초 1회차",
    "round": 1,
    "difficulty": "basic",
    "numProblems": 9,
    "file": "py_for_b1.json"
  },
  {
    "id": "py_for_c1",
    "categoryId": "py_for",
    "title": "Python for문 챌린지 1회차",
    "round": 2,
    "difficulty": "challenge",
    "numProblems": 9,
    "file": "py_for_c1.json"
  },
  {
    "id": "c_for_b1",
    "categoryId": "c_for",
    "title": "C for문 기초 1회차",
    "round": 1,
    "difficulty": "basic",
    "numProblems": 9,
    "file": "c_for_b1.json"
  },
  {
    "id": "c_for_c1",
    "categoryId": "c_for",
    "title": "C for문 챌린지 1회차",
    "round": 2,
    "difficulty": "challenge",
    "numProblems": 9,
    "file": "c_for_c1.json"
  },
  {
    "id": "py_while_b1",
    "categoryId": "py_while",
    "title": "Python while문 기초 1회차",
    "round": 1,
    "difficulty": "basic",
    "numProblems": 9,
    "file": "py_while_b1.json"
  }
]
```

---

### 3.3 `data/sets/*.json` – 실제 문제 세트

각 세트 파일은 다음과 같은 공통 구조를 가집니다.

필수 필드:

* `id` : 세트 ID (반드시 `sets.index.json`의 `id`와 동일)
* `title` : 세트 제목 (화면 상단에 표시)
* `categoryId` : 속한 카테고리 ID (`categories.json` 참고)
* `availableLanguages` : 이 세트에 사용되는 언어 목록 (예: `["c"]`, `["python"]`)
* `problems` : 문제 배열

예시 (Python while문 기초 세트 축약):

```json
{
  "id": "py_while_b1",
  "title": "Python while문 기초 1회차",
  "categoryId": "py_while",
  "availableLanguages": ["python"],
  "problems": [
    {
      "id": "mcq1",
      "type": "mcq",
      "level": "기초",
      "title": "MCQ 1. 1부터 n까지의 합",
      "description": "…",
      "code": "…",
      "options": [ "…", "…", "…", "…" ],
      "optionLabels": ["A","B","C","D"],
      "correctIndex": 1
    },
    {
      "id": "code1",
      "type": "code",
      "level": "코드 작성",
      "title": "Code 1. …",
      "description": "…",
      "code": "…",
      "expectedCode": "print('%d x %d = %d' % (n, i, n * i))",
      "hint": "print('%d x %d = %d' % (?, ?, ?)) 형태를 사용하세요."
    }
  ]
}
```

---

## 4. 문제 형식(Problem Schema)

### 4.1 공통 필드

모든 문제는 다음 공통 필드를 가집니다.

* `id` : 세트 내에서 고유한 ID (`"mcq1"`, `"short2"`, `"code1"` 등)
* `type` : `"mcq"`, `"short"`, `"code"` 중 하나
* `level` : 화면에 보여줄 난이도 라벨

  * 예시: `"기초"`, `"조금 응용"`, `"챌린지"`, `"단답형"`, `"코드 작성"`
  * 실질적인 정렬/채점에는 사용하지 않고 **설명용 텍스트**입니다.
* `title` : 문제 제목 (`"MCQ 1. Pass / Fail 프로그램"` 등)
* `description` : 문제 설명 (여러 줄일 경우 `\n`으로 줄바꿈)
* `code` : 문제 위에 보여줄 코드. 필요 없으면 `null` 사용.

이후 필드는 `type`에 따라 달라집니다.

---

### 4.2 `type: "mcq"` – 객관식

추가 필드:

* `options` : 보기 문자열 배열

  * 코드가 들어가는 보기라도 그대로 문자열로 작성합니다(`\n`으로 줄바꿈).
* `optionLabels` : 보기 라벨 배열 (보통 `["A", "B", "C", "D"]`)
* `correctIndex` : 정답 인덱스 (0부터 시작, 예: A=0, B=1, …)

예시:

```json
{
  "id": "mcq1",
  "type": "mcq",
  "level": "기초",
  "title": "MCQ 1. Pass / Fail 프로그램",
  "description": "다음 설명에 맞는 C 코드를 고르세요.\n\n- 정수 score를 하나 입력받는다.\n- score가 60 이상이면 \"Pass\"를 출력하고,\n  그렇지 않으면 \"Fail\"을 출력한다.",
  "code": null,
  "options": [
    "int score;\nscanf(\"%d\", score);\nif (score >= 60) {\n    printf(\"Pass\\n\");\n} else {\n    printf(\"Fail\\n\");\n}",
    "int score;\nscanf(\"%d\", &score);\nif (score > 60) {\n    printf(\"Pass\\n\");\n}\nif (score <= 60) {\n    printf(\"Fail\\n\");\n}",
    "int score;\nscanf(\"%d\", &score);\nif (score >= 60) {\n    printf(\"Pass\\n\");\n} else {\n    printf(\"Fail\\n\");\n}",
    "int score;\nscanf(\"%d\", &score);\nif (score = 60) {\n    printf(\"Pass\\n\");\n} else {\n    printf(\"Fail\\n\");\n}"
  ],
  "optionLabels": ["A", "B", "C", "D"],
  "correctIndex": 2
}
```

---

### 4.3 `type: "short"` – 단답형

추가 필드:

* `expectedText` : 정답 문자열 1개
* 또는 `expectedAnyOf` : 여러 정답 후보 문자열 배열

**채점 규칙(요약)**

* 앞뒤 공백 제거
* 중간의 공백 여러 개는 한 칸으로 처리
* 영문은 소문자/대문자 구분 없음 (필요시)

예시 1 – 한 개의 정답:

```json
{
  "id": "short1",
  "type": "short",
  "level": "단답형",
  "title": "Short 1. 범위 + if-else 결과",
  "description": "아래 프로그램에서 입력이 7일 때, 출력되는 내용을 그대로 쓰세요.\n(줄바꿈 없이 한 줄입니다.)",
  "code": "int n;\nscanf(\"%d\", &n);\nif (n >= 5 && n <= 10) {\n    printf(\"OK\\n\");\n} else {\n    printf(\"NG\\n\");\n}",
  "expectedText": "OK"
}
```

예시 2 – 여러 정답 중 하나:

```json
{
  "id": "short2",
  "type": "short",
  "level": "단답형",
  "title": "Short 2. 어떤 값을 넣으면 참이 될까?",
  "description": "다음 조건식이 참(true)이 되도록 n의 값을 하나만 쓰세요.\n(여러 개 중 아무거나 하나 맞으면 정답입니다.)",
  "code": "1 <= n && n <= 5",
  "expectedAnyOf": ["1", "2", "3", "4", "5"]
}
```

---

### 4.4 `type: "code"` – 코드 작성/수정

추가 필드:

* `expectedCode` : 정답 코드 문자열 (학생이 작성해야 하는 부분)
* `hint` : 선택 사항. 힌트 문자열 (없으면 `""` 또는 생략)

**채점 규칙(요약)**

`expectedCode`와 학생 입력을 `normalizeCode()`로 정규화한 뒤, 문자열 비교합니다.

정규화에서 하는 일 (요약):

* 줄바꿈 통일 (`\r\n` → `\n`)
* 한 줄/여러 줄 주석 제거
* 연속된 공백을 한 칸으로 축소
* `(`, `)`, `;`, `,`, 연산자 주변의 불필요한 공백 제거

→ 즉,

* 들여쓰기, 탭/스페이스 차이
* 연산자 주변 공백 (`n*i` vs `n * i`)
* 줄 나누는 위치
* 주석 유무

정도는 **모두 허용**됩니다.
단, **토큰(변수명/연산자/순서)**이 바뀌면 오답입니다.

예시:

```json
{
  "id": "code2",
  "type": "code",
  "level": "코드 작성",
  "title": "Code 2. 두 정수 입력 받기",
  "description": "정수 변수 a, b에 값을 각각 입력받는 scanf 문을 한 줄로 작성하세요.\n(두 수는 공백으로 구분해서 들어옵니다.)",
  "code": "int a, b;\n// 여기에 scanf 한 줄을 작성하세요.",
  "expectedCode": "scanf(\"%d %d\", &a, &b);",
  "hint": "서로 다른 두 변수를 &a, &b 순서로 넣어야 합니다."
}
```

---

## 5. 동작 흐름(요약)

1. **index.html**

   * `categories.json` → 카테고리 목록 렌더링
   * `sets.index.json` → 세트 목록 렌더링
   * 세트 버튼 클릭 시 `practice.html?set=세트ID` 로 이동

2. **practice.html + practice.js**

   * 쿼리스트링의 `set` 값으로 해당 세트 JSON(`data/sets/…`) 로드
   * 문제 리스트 렌더링, HUD(타이머/네비게이션 등) 초기화
   * 사용자가 푼 답안을 `localStorage`에 저장하여, **뒤로 갔다가 다시 들어와도 이전 답안을 복원** (개발 내용 기준)

3. **채점**

   * MCQ : `correctIndex` 비교
   * Short : `expectedText` 또는 `expectedAnyOf`와 정규화 비교
   * Code : `expectedCode`와 `normalizeCode()` 비교

---

## 6. 새 문제 / 새 세트 / 새 카테고리 추가 가이드

### 6.1 기존 세트에 “문제 하나 더” 추가

1. `data/sets/<세트ID>.json` 파일을 연다.
2. `problems` 배열 맨 끝 또는 원하는 위치에 새 문제 객체를 추가한다.
3. **`sets.index.json`에서 해당 세트의 `numProblems` 값을 1 증가**시킨다.

> 문제 ID는 `"mcq6"`, `"short3"`, `"code3"`처럼 간단히 번호를 이어가면 됩니다.

---

### 6.2 새 세트 추가 (예: Python while문 챌린지 1회차)

1. **세트 JSON 파일 만들기**

   * `data/sets/py_while_c1.json` 같은 이름으로 새 파일 생성.
   * 최소 구조:

   ```json
   {
     "id": "py_while_c1",
     "title": "Python while문 챌린지 1회차",
     "categoryId": "py_while",
     "availableLanguages": ["python"],
     "problems": [
       {
         "id": "mcq1",
         "type": "mcq",
         "level": "챌린지",
         "title": "…",
         "description": "…",
         "code": "…",
         "options": [ "…", "…", "…", "…" ],
         "optionLabels": ["A","B","C","D"],
         "correctIndex": 1
       }
       // 나머지 문제들 …
     ]
   }
   ```

2. **`sets.index.json`에 메타데이터 추가**

   ```json
   {
     "id": "py_while_c1",
     "categoryId": "py_while",
     "title": "Python while문 챌린지 1회차",
     "round": 2,
     "difficulty": "challenge",
     "numProblems": 9,
     "file": "py_while_c1.json"
   }
   ```

3. 브라우저에서 새로고침 후 메인 화면에서 카테고리/세트가 잘 보이는지 확인.

---

### 6.3 새 카테고리 추가 (예: Python - Lv9 함수)

1. **`categories.json`에 항목 추가**

   ```json
   { "id": "py_func", "name": "Python - Lv9 함수", "order": 90 }
   ```

2. **`sets.index.json`에 이 카테고리를 사용하는 세트 정보 추가**

   ```json
   {
     "id": "py_func_b1",
     "categoryId": "py_func",
     "title": "Python 함수 기초 1회차",
     "round": 1,
     "difficulty": "basic",
     "numProblems": 8,
     "file": "py_func_b1.json"
   }
   ```

3. `data/sets/py_func_b1.json` 파일을 만들어 문제들을 채운다.

---

## 7. 언어별 출제 스타일 규칙

### 7.1 C 언어

* 입력 : `scanf("%d", &n);` 형식 사용

* 출력 : 항상 `printf("...\n");` 형태로 개행 포함

* 전체 프로그램이 필요한 경우:

  ```c
  #include <stdio.h>

  int main(void) {
      int n;
      scanf("%d", &n);
      ...
      return 0;
  }
  ```

* 부분 코드만 필요하면 `#include` / `main`은 생략하고 필요한 부분만 `code`/`options`에 넣는다.

### 7.2 Python

* 입력 : `n = int(input())` / `a, b = map(int, input().split())` 형태 사용

* **출력은 통일성 때문에 모두 C 스타일 서식문자 사용**:

  * 한 값: `print('%d' % n)`
  * 두 값: `print('%d %d' % (a, b))`
  * 식 표현: `print('%d + %d = %d' % (a, b, a + b))`
  * 반복문 예: `print('%d x %d = %d' % (n, i, n * i))`

* 힌트는 다음 문구를 기본 형식으로 사용:

  * `print('%d x %d = %d' % (?, ?, ?)) 형태를 사용하세요.`

> 이렇게 맞춰두면 학생들이 **입력/출력 패턴을 그대로 연습**할 수 있고, 코드 채점도 안정적입니다.

### 7.3 Java

* 입력 : `Scanner sc = new Scanner(System.in);`
* 출력 : `System.out.println()` 또는 `System.out.printf()` 사용
* 예시:

  ```java
  import java.util.Scanner;

  public class Main {
      public static void main(String[] args) {
          Scanner sc = new Scanner(System.in);
          int n = sc.nextInt();
          if (n >= 60) {
              System.out.println("Pass");
          } else {
              System.out.println("Fail");
          }
      }
  }
  ```

---

## 8. 난이도 규칙

세트 단위 난이도(`sets.index.json`의 `difficulty`)는 **두 가지**만 사용합니다.

* `"basic"` : 처음 배우는 학생용.

  * 단순한 조건/반복, 실행 추적, 기본 입출력 위주
* `"challenge"` : 어느 정도 익숙한 학생용.

  * 실수하기 좋은 부분, 복합 조건, 약간의 응용 로직 포함

문제 객체의 `level` 필드는 세트 안에서 **설명용 레이블**이므로 자유롭게 써도 되지만,
가능하면 다음 정도로 통일합니다.

* `"기초"` / `"조금 응용"` / `"챌린지"` / `"단답형"` / `"코드 작성"`

---

## 9. 앞으로 문제를 만들 때 최소 체크리스트

1. **어느 카테고리에 넣을지 결정**

   * 기존 카테고리 사용 or `categories.json`에 새 카테고리 추가

2. **세트 ID와 파일명 정하기**

   * 규칙: `<언어>_<파트>_<난이도><회차>`

     * 예: `py_if_b1`, `c_for_c1`, `py_while_b1`

3. **`data/sets/<id>.json` 작성**

   * 루트 필드: `id`, `title`, `categoryId`, `availableLanguages`, `problems`
   * 각 문제는 `type`에 맞게 필드 세팅

4. **`sets.index.json`에 세트 정보 한 줄 추가**

   * `id`, `categoryId`, `title`, `round`, `difficulty`, `numProblems`, `file`

5. **로컬 서버에서 테스트**

   * 메인 목록에 잘 뜨는지
   * 모든 문제 렌더링/채점이 정상 동작하는지 확인

이 규칙만 지키면, 나중에 서버로 옮겨도 **JSON 구조는 그대로 재사용**할 수 있습니다.

