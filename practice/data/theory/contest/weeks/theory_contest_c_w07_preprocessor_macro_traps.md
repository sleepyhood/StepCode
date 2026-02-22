# C 경시대회 W07 - 전처리기/매크로 함정

## 메타
- week: W07
- slug: preprocessor_macro_traps
- audience: common, elementary, middle, high

## 학습 목표
- `problem_c_w07.md`와 `problem_c_w07_map.md` 문항을 매크로 치환 관점으로 정확히 해석하는 것이 목표입니다.
- 함수형 매크로의 괄호 부재로 생기는 우선순위 함정을 빠르게 검출하는 것이 목표입니다.

## 문항-개념 빠른 연결
- 개념 1) `#define` 치환 규칙: 매크로가 함수 호출이 아니라 텍스트 치환이라는 점을 적용하는 문항
- 개념 2) 매크로 괄호와 부작용: `x*x`, `x+1` 같은 매크로의 우선순위 문제를 계산하는 문항
- 개념 3) 조건부 컴파일 읽기: 전처리 조건에 따라 실제 컴파일되는 코드 구간을 판별하는 개념

## 공통 이론 (COMMON)
<!-- audience:common -->
### 개념 1) `#define` 치환 규칙
- 개념 정의: 전처리 단계에서 매크로 인자가 그대로 치환된 뒤 컴파일된다는 규칙을 적용하는 개념입니다.
- 판별 규칙: 매크로는 함수처럼 실행되지 않고, 먼저 문자열 치환된다.
- 판별 규칙: 치환 후 식을 다시 C 연산 우선순위로 계산한다.
- 추적 절차: 원식 작성 -> 치환식 전개 -> 우선순위 계산 순서로 푼다.
- 오답 포인트: "매크로 = 함수"로 가정하면 `f(a+1)`을 `(a+1)*(a+1)`로 잘못 계산합니다.

| 단계 | 확인 내용 | 계산 체크 |
| --- | --- | --- |
| 1. 호출식 확인 | `M(a+1)` 같은 원식 기록 | 인자 표현을 그대로 보존 |
| 2. 치환식 전개 | `x` 자리에 인자 문자열 대입 | 괄호가 자동 추가되지 않음을 확인 |
| 3. 우선순위 적용 | `*`, `+` 순으로 계산 | 전개식 기준으로만 계산 |
| 4. 결과 검산 | 괄호 보강 버전과 비교 | 왜 차이가 나는지 설명 |

![define 매크로 치환 전개와 계산 순서 다이어그램](./data/theory/images/contest_w07_define_expansion_flow.svg)

예시 (기본):
```c
#include <stdio.h>
#define M(x) x*x
int main(void) {
    int a = 3;
    printf("%d", M(a));
    return 0;
}
```
```io
input:
(없음)
output:
9
```

예시 (변형):
```c
#include <stdio.h>
#define M(x) x*x
int main(void) {
    int a = 3;
    printf("%d", M(a+1));
    return 0;
}
```
```io
input:
(없음)
output:
7
```

예시 (함정):
```text
M(a+1) -> a+1*a+1 로 치환된다.
곱셈이 먼저 계산되어 a + a + 1이 된다.
```

### 개념 2) 매크로 괄호와 부작용
- 개념 정의: 매크로 본문/인자 괄호 유무가 계산 결과를 바꾸는 현상을 다루는 개념입니다.
- 판별 규칙: 안전한 매크로는 보통 `#define F(x) ((x) * (x))`처럼 작성한다.
- 판별 규칙: `#define f(x) x+1`을 곱셈과 함께 쓰면 치환 후 결합 순서가 바뀐다.
- 추적 절차: 치환식에 괄호를 직접 보강해 비교 -> 실제 식과 차이 확인 -> 출력 계산 순으로 푼다.
- 오답 포인트: `f(a)*f(a)`를 `(a+1)*(a+1)`로 자동 해석하면 오답입니다.

| 매크로 형태 | 호출 예 | 치환 결과 형태 | 위험도 |
| --- | --- | --- | --- |
| `#define f(x) x+1` | `f(a)*f(a)` | `a+1*a+1` | 높음 |
| `#define g(x) (x+1)` | `g(a)*g(a)` | `(a+1)*(a+1)` | 중간 |
| `#define h(x) ((x)+1)` | `h(a)*h(a)` | `((a)+1)*((a)+1)` | 낮음 |
| `#define sq(x) ((x)*(x))` | `sq(a+1)` | `((a+1)*(a+1))` | 낮음 |

![매크로 괄호 유무에 따른 계산 결과 비교 다이어그램](./data/theory/images/contest_w07_macro_parentheses_compare.svg)

예시 (기본):
```c
#include <stdio.h>
#define f(x) x+1
int main(void) {
    int a = 5;
    printf("%d", f(a)*f(a));
    return 0;
}
```
```io
input:
(없음)
output:
11
```

예시 (변형):
```c
#include <stdio.h>
#define g(x) ((x)+1)
int main(void) {
    int a = 5;
    printf("%d", g(a)*g(a));
    return 0;
}
```
```io
input:
(없음)
output:
36
```

예시 (함정):
```text
S(q+q)에서 S(x)=x*x 이면 q+q*q+q 가 된다.
q=4일 때 4+16+4 = 24다.
```

### 개념 3) 조건부 컴파일 읽기
- 개념 정의: `#if`, `#ifdef`, `#ifndef`로 인해 실제로 컴파일되는 코드 블록을 판별하는 개념입니다.
- 판별 규칙: 거짓 조건 블록은 컴파일 대상에서 제외된다.
- 판별 규칙: 매크로 정의 유무에 따라 포함 블록이 달라진다.
- 추적 절차: 전처리 조건값 확정 -> 활성 블록 표시 -> 남은 코드만 실행 추적 순으로 푼다.
- 오답 포인트: 실행 단계만 보고 추적하면, 전처리에서 제거된 코드까지 계산하는 실수가 납니다.

| 전처리 지시문 | 참이 되는 기준 | 자주 하는 실수 |
| --- | --- | --- |
| `#if X` | `X`가 0이 아닌 값으로 평가 | 정의만 되어 있으면 참이라고 오해 |
| `#ifdef X` | `X`가 정의되어 있음 | 값이 0이면 거짓이라고 오해 |
| `#ifndef X` | `X`가 정의되어 있지 않음 | `#ifdef`와 의미 반대로 읽지 못함 |
| `#if MODE == 1` | 수치 비교식이 참 | 비교식 대신 정의 여부만 확인 |

![조건부 컴파일에서 활성 코드 블록 판별 다이어그램](./data/theory/images/contest_w07_conditional_compile_map.svg)

예시 (기본):
```c
#include <stdio.h>
#define MODE 1
int main(void) {
#if MODE == 1
    printf("A");
#else
    printf("B");
#endif
    return 0;
}
```
```io
input:
(없음)
output:
A
```

예시 (변형):
```c
#include <stdio.h>
#define DEBUG
int main(void) {
#ifdef DEBUG
    printf("D");
#else
    printf("R");
#endif
    return 0;
}
```
```io
input:
(없음)
output:
D
```

예시 (함정):
```text
#ifdef X 와 #if X 는 다르다.
X가 정의만 되어 있어도 #ifdef X는 참이다.
```

### 실전 풀이 루틴 (W07 공통)
1. 매크로 호출식을 먼저 전처리 치환식으로 풀어쓴다.
2. 치환식에서 곱셈/덧셈 우선순위를 적용해 중간값을 계산한다.
3. 괄호가 있었다면 결과가 어떻게 달라지는지 함께 검산한다.
4. 조건부 컴파일이 있으면 활성 블록만 남겨서 실행 흐름을 다시 본다.
5. 최종 출력 형식(공백 포함)을 확인해 선택지와 대조한다.

### 공통 미니 체크 (필수 제출)
문항:
1. `#define f(x) x*x`에서 `f(2+1)` 결과를 쓰세요.
2. 안전한 제곱 매크로 형태를 쓰세요.
3. `#ifdef A`와 `#if A`의 차이를 한 줄로 쓰세요.

답안 작성:
1. 정답: [ ] / 근거: [ ]
2. 정답: [ ] / 근거: [ ]
3. 정답: [ ] / 근거: [ ]

## 초등 트랙 (ELEMENTARY)
<!-- audience:elementary -->
### 초등 포인트
- 치환식 전개를 습관화해 기본 매크로 함정을 피합니다.

### 초등 연계 실습
실습 목표:
- `x*x` 매크로의 괄호 부재 문제를 직접 계산합니다.

실습 문제:
```c
#include <stdio.h>
#define S(x) x*x
int main(void) {
    int n = 3;
    printf("%d", S(n+2));
    return 0;
}
```

체크포인트:
1. 치환식을 먼저 적었는가?
2. 우선순위 적용 순서를 기록했는가?

## 중등 트랙 (MIDDLE)
<!-- audience:middle -->
### 중등 포인트
- 동일 매크로를 여러 식에 재사용할 때 결과 차이를 비교합니다.

### 중등 연계 실습
실습 목표:
- 괄호 있는/없는 매크로를 비교합니다.

실습 문제:
```c
#include <stdio.h>
#define A(x) x+1
#define B(x) ((x)+1)
int main(void) {
    int a = 4;
    printf("%d %d", A(a)*A(a), B(a)*B(a));
    return 0;
}
```

체크포인트:
1. 두 매크로의 치환식을 각각 적었는가?
2. 두 결과가 왜 다른지 설명했는가?

## 고등 트랙 (HIGH)
<!-- audience:high -->
### 고등 포인트
- 전처리 단계와 실행 단계를 분리해 해석합니다.

### 고등 연계 실습
실습 목표:
- 조건부 컴파일 + 함수형 매크로를 함께 추적합니다.

실습 문제:
```c
#include <stdio.h>
#define MODE 1
#define F(x) x+1
int main(void) {
#if MODE
    int a = 5;
    printf("%d", F(a)*F(a));
#else
    printf("0");
#endif
    return 0;
}
```

체크포인트:
1. 활성 블록을 먼저 확정했는가?
2. 치환 후 우선순위를 적용해 출력을 계산했는가?
