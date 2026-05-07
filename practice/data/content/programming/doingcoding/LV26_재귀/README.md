이 단원은 **재귀(Recursion)를 기초부터 심화까지 단계별로 학습할 수 있도록 구성되어 있습니다.
단순히 함수가 자신을 호출하는 것을 넘어, 실행 흐름의 중첩(Stack)과 상태 공간의 탐색(Branching)을 익히는 것이 목표입니다.

> **파일 명명 규칙**: `ALLvXXXXX_{db_id}` (수업) / `SALLvXXXXX_{db_id}` (숙제)  
> **`legacy_id`**: 이전 버전 파일명 또는 외부 출처 (`bj_*`: 백준, `[A-Z]+\d*[v]\d+`: 기존 시스템)

### 📋 범례 (Legend)
- **ID**: `v05` (단일 호출/선형), `v10` (다중 호출/구조적)
- **db_id**: 웹 DB 고유 번호 (**LOCAL**은 업로드 예정 항목)
- **Status**: `[ ]` 대기, `[/]` 작성 중, `[x]` 검증 완료
- **핵심 포인트**: 해당 문제에서 반드시 익혀야 할 기술적 목표

---

## 🚀 재귀 구조의 진화: Linear에서 Structural로

재귀는 문제의 상태를 어떻게 분할하느냐에 따라 두 가지 핵심 단계로 나뉩니다.

```mermaid
graph TD
    subgraph "v05: 선형 재귀 (Linear Flow)"
    A1[Start] --> B1[State n] --> C1[State n-1] --> D1[Base Case]
    D1 -.-> C1 -.-> B1 -.-> A1
    end

    subgraph "v10: 구조적 재귀 (Structural Branching)"
    A2[Start] --> B2[Branch L]
    A2 --> C2[Branch R]
    B2 --> D2[Leaf]
    B2 --> E2[Leaf]
    C2 --> F2[Leaf]
    C2 --> G2[Leaf]
    end

    v05 -->|상태 공간 확장| v10 -->|유망성 검사 도입| lv29[백트래킹]
```

---

## 1. [v05 시리즈] 선형 재귀의 정수 (7개 Set)

v05 시리즈는 재귀의 가장 기본적인 형태인 **선형 재귀(Linear Recursion)**를 다룹니다.
스택의 원리, 매개변수 전달, 반환값 누적의 완벽한 이해를 목표로 합니다.

| **Set** | **구분** | **주제 (Topic)** | **문제 제목 (파일명)** | **id** | **db_id** | **Legacy/Source** | **Status** | **핵심 포인트** |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **01** | 수업 | **원리** | [재귀함수 튜토리얼](02_workspace/ALLv05001_519.md) | `ALLv05001` | **519** | `ALLv05001` | `[ ]` | 탈출 조건과 스택 기초 |
| | 숙제 | | [1부터 n까지 역순 출력](02_workspace/SALLv05001_520.md) | `SALLv05001` | **520** | `SP301v2601` | `[ ]` | 호출 이후의 실행 |
| **02** | 수업 | **조건** | [두 수 사이 홀수](02_workspace/ALLv05002_521.md) | `ALLv05002` | **521** | `P301v2602` | `[ ]` | 매개변수 상태 전달 |
| | 숙제 | | [두 수 사이 짝수](02_workspace/SALLv05002_721.md) | `SALLv05002` | **721** | `SP301v2602` | `[ ]` | 조건부 재귀 호출 |
| **03** | 수업 | **시각화** | [재귀 챗봇](02_workspace/ALLv05003_LOCAL.md) | `ALLv05003` | **LOCAL** | `bj_17478` | `[x]` | **[필수]** 호출 전/후 실행 흐름 |
| | 숙제 | | [마트료시카](02_workspace/SALLv05003_LOCAL.md) | `SALLv05003` | **LOCAL** | _(신규)_ | `[x]` | 깊이에 따른 변화 |
| **04** | 수업 | **합산** | [1부터 n까지 합](02_workspace/ALLv05004_522.md) | `ALLv05004` | **522** | `P301v2603` | `[ ]` | return을 통한 상향식 누적 |
| | 숙제 | | [팩토리얼 계산](02_workspace/SALLv05004_523.md) | `SALLv05004` | **523** | `SP301v2603` | `[ ]` | 계승의 재귀적 정의 |
| **05** | 수업 | **제어** | [우박수 (3n+1)](02_workspace/ALLv05005_526.md) | `ALLv05005` | **526** | `P301v2605` | `[ ]` | 불규칙한 상태 추적 |
| | 숙제 | | [우박수 (3n+1)(rev)](02_workspace/SALLv05005_527.md) | `SALLv05005` | **527** | `SP301v2605` | `[ ]` | 도달 경로 역추적 |
| **06** | 수업 | **변환** | [N진수 변환](02_workspace/ALLv05006_LOCAL.md) | `ALLv05006` | **LOCAL** | _(신규)_ | `[ ]` | 나머지 역순 처리 |
| | 숙제 | | [2진수 변환](02_workspace/SALLv05006_525.md) | `SALLv05006` | **525** | `SP301v2604` | `[ ]` | 진법 변환의 원리 |
| **07** | 수업 | **브릿지** | [N자리 수 만들기](02_workspace/ALLv05007_LOCAL.md) | `ALLv05007` | **LOCAL** | _(신규)_ | `[ ]` | 탐색 트리의 첫 발걸음 |
| | 숙제 | | [숫자 만들기](02_workspace/SALLv05007_1501.md) | `SALLv05007` | **1501** | `SALLv05014` | `[ ]` | 상태 공간 생성 체험 |

---

## 2. [v10 시리즈] 구조적 재귀의 정수 (6개 Set)

v10 시리즈는 한 함수에서 **자신을 여러 번 호출**하는 구조를 통해 프랙탈(Fractal)과 상태 공간 탐색(State Space Search)을 배웁니다.

| **Set** | **구분** | **주제 (Topic)** | **문제 제목 (파일명)** | **id** | **db_id** | **Legacy/Source** | **Status** | **핵심 포인트** |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **01** | 수업 | **분기** | [재귀함수 튜토리얼3](02_workspace/ALLv10001_816.md) | `ALLv10001` | **816** | `ALLv05005` | `[ ]` | 한 함수 내 다중 호출 |
| | 숙제 | | [정사면체 주사위](02_workspace/SALLv10001_1510.md) | `SALLv10001` | **1510** | `SP301v2606` | `[ ]` | 호출 분기 이해 |
| **02** | 수업 | **대칭** | [알파벳 트리](02_workspace/ALLv10002_LOCAL.md) | `ALLv10002` | **LOCAL** | _(신규)_ | `[ ]` | 분할 정복과 대칭 프랙탈 |
| | 숙제 | | [재귀적 눈금 그리기](02_workspace/SALLv10002_LOCAL.md) | `SALLv10002` | **LOCAL** | _(신규)_ | `[ ]` | 프랙탈 1D 구조 |
| **03** | 수업 | **조합** | [로또](02_workspace/ALLv10003_2136.md) | `ALLv10003` | **2136** | `ALLv10005` | `[ ]` | **[필수]** 조건부 탐색 완성 (nCr) |
| | 숙제 | | [국가대표 선발 (nCr)](02_workspace/SALLv10003_LOCAL.md) | `SALLv10003` | **LOCAL** | _(신규)_ | `[ ]` | 조합 생성 실습 |
| **04** | 수업 | **분할** | [프랙탈 크로스 그리기](02_workspace/ALLv10004_LOCAL.md) | `ALLv10004` | **LOCAL** | _(신규)_ | `[ ]` | 2D 공간 분할 기초 |
| | 숙제 | | [쿼드트리 번호 매기기](02_workspace/SALLv10004_LOCAL.md) | `SALLv10004` | **LOCAL** | _(신규)_ | `[ ]` | 2D 4분할 쿼드트리 |
| **05** | 수업 | **경로** | [격자이동](02_workspace/ALLv10005_1509.md) | `ALLv10005` | **1509** | `P301v2612` | `[ ]` | 2D 재귀 이동 + 장애물 |
| | 숙제 | | [미로 탐색 기초](02_workspace/SALLv10005_LOCAL.md) | `SALLv10005` | **LOCAL** | _(신규)_ | `[ ]` | 도달 가능성 탐색 |
| **06** | 수업 | **효율** | [재귀의 귀재 (호출 측정)](02_workspace/ALLv10006_LOCAL.md) | `ALLv10006` | **LOCAL** | `bj_25501` | `[ ]` | 호출 폭발과 성능 분석 |
| | 숙제 | | [재귀의 함정 (카운트)](02_workspace/SALLv10006_LOCAL.md) | `SALLv10006` | **LOCAL** | _(신규)_ | `[ ]` | 백트래킹/DP 필요성 체감 |

---

## 🚫 제외된 문제 목록 (Excluded Problems)

단원 간소화 및 핵심 원리 집중을 위해 다음 문제들은 정규 커리큘럼에서 제외되었습니다.

### v05 (선형 재귀)
- `v05 Set 05`: 재귀함수 튜토리얼2 / 트리보나치 (`02_workspace/99_excluded/ALLv05005_524.md`, `02_workspace/99_excluded/SALLv05005_LOCAL.md`)
- `v05 Set 06`: 포비나치 / 가중치 피보나치 (`02_workspace/99_excluded/ALLv05006_1499.md`, `02_workspace/99_excluded/SALLv05006_LOCAL.md`)
- `v05 Set 08`: 기묘한 수열 / 계단식 재귀 (`02_workspace/99_excluded/ALLv05008_1029.md`, `02_workspace/99_excluded/SALLv05008_LOCAL.md`)
- `v05 Set 09`: 삼각형 / 역삼각형 (`02_workspace/99_excluded/ALLv05009_529.md`, `02_workspace/99_excluded/SALLv05009_LOCAL.md`)
- `v05 Set 10`: 직사각형 / 정사각형 타일 (`02_workspace/99_excluded/ALLv05010_2111.md`, `02_workspace/99_excluded/SALLv05010_LOCAL.md`)
- `v05 Set 12`: 문자열 거꾸로 / 재귀적 문자열 포장 (`02_workspace/99_excluded/ALLv05012_LOCAL.md`, `02_workspace/99_excluded/SALLv05012_LOCAL.md`)
- `v05 Set 13`: 8진수 변환 / 9진수 변환 (`02_workspace/99_excluded/ALLv05013_LOCAL.md`, `02_workspace/99_excluded/SALLv05013_2112.md`)

### v10 (구조적 재귀)
- `v10 Set 02`: 주사위 문자 / 단어 나누기 (`02_workspace/99_excluded/ALLv10002_1611.md`, `02_workspace/99_excluded/SALLv10002_2113.md`)
- `v10 Set 05`: 소 배치하기 / 암호 해독 (`02_workspace/99_excluded/ALLv10005_1031.md`, `02_workspace/99_excluded/SALLv10005_LOCAL.md`)
- `v10 Set 06`: 로마 숫자 만들기 / 숫자 카드 조합 (`02_workspace/99_excluded/ALLv10006_2139.md`, `02_workspace/99_excluded/SALLv10006_LOCAL.md`)
- `v10 Set 07`: 정사각형 쌓기 / 타일 채우기 (`02_workspace/99_excluded/ALLv10007_2137.md`, `02_workspace/99_excluded/SALLv10007_LOCAL.md`)
- `v10 Set 10`: 이상한 주사위 / 주사위 던지기(S) (`02_workspace/99_excluded/ALLv10010_1500.md`, `02_workspace/99_excluded/SALLv10010_LOCAL.md`)

---

## 3. 학습 경로 및 연계 지도

```mermaid
flowchart TD
    subgraph "Step 1: 기초 다지기 (v05)"
    A[선형 재귀 기초] --> B[데이터/진법 변환]
    B --> C[상태 공간 입문]
    end

    subgraph "Step 2: 구조적 확장 (v10)"
    C --> D{다중 분기}
    D --> E[조합론 & 상태 탐색]
    E --> F[프랙탈 & 격자 탐색]
    end

    subgraph "Step 3: 실전 응용"
    F --> G[lv29. 백트래킹]
    G --> H[lv30. 동적 계획법 기초]
    end

    style A fill:#f9f,stroke:#333
    style D fill:#bbf,stroke:#333
    style G fill:#bfb,stroke:#333
```

> [!TIP]
> `v10 Set 03~05`를 마치면 **lv29. 백트래킹** 단원의 유망성 검사(Pruning)와 방문 배열(`visited`)을 활용한 상태 관리 기법을 배울 준비가 완료됩니다.

---

## 🛠️ 문제 관리 지침 (Maintenance Guide)

이 커리큘럼 지도를 유지보수하거나 신규 문제를 추가할 때 다음의 **정합성 규칙**을 반드시 준수해야 합니다.

1.  **ID 명명 규칙**:
    *   `v05`: 재귀 호출이 1회 이하이거나 선형적 흐름인 경우.
    *   `v10`: 재귀 호출이 2회 이상이거나 분할 정복/프랙탈 구조인 경우.
2.  **데이터 동기화**:
    *   모든 Markdown 파일(`.md`)의 YAML Front-matter 내 `id`와 `db_id`는 본 테이블과 **100% 일치**해야 합니다.
    *   `LOCAL` 상태인 문제는 실제 파일 생성 시 이 테이블에 정의된 `id`를 파일명으로 사용합니다.
3.  **인덱스 갱신**:
    *   테이블의 내용이나 파일의 메타데이터를 수정한 후에는 반드시 `scripts/generate_content_indexes.py`를 실행하여 웹 엔진에 반영해야 합니다.
4.  **검증**:
    *   `db_id`가 있는 문제는 `scripts/check_sets_index.ps1`을 통해 중복 여부를 상시 체크합니다.
