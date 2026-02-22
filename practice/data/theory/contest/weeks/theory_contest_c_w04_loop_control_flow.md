# C 경시대회 W04 - 반복문/제어흐름

## 메타
- week: W04
- slug: loop_control_flow
- audience: common, elementary, middle, high

## 학습 목표
- `problem_c_w04.md`와 `problem_c_w04_map.md` 문항을 반복 흐름 관점으로 안정적으로 추적하는 것이 목표입니다.
- 종료 조건, 분기 제어, 중첩 반복의 영향을 분리해 계산하는 습관을 만드는 것이 목표입니다.

## 문항-개념 빠른 연결
- 개념 1) for/while 종료 조건 추적: 반복 횟수와 누적값 계산형 문항
- 개념 2) break/continue 영향 범위: 루프 탈출/건너뛰기 적용 범위 판별형 문항
- 개념 3) 중첩 반복 총 실행 횟수: 다중 루프와 플래그 제어 추적형 문항


## 공통 이론 (COMMON)
<!-- audience:common -->
### 개념 1) for/while 종료 조건 추적
- 개념 정의: 반복문의 시작값, 종료조건, 증감식이 만드는 실행 횟수와 누적 결과를 계산하는 개념입니다.
- 판별 규칙: `for(init; cond; step)`는 `cond`가 거짓이 되는 순간 종료한다.
- 판별 규칙: `while(cond)`는 본문 진입 전에 `cond`를 검사한다.
- 추적 절차: 초기값 기록 -> 각 반복의 변수 변화 기록 -> 종료 시점 확인 -> 출력 검산 순서로 푼다.
- 오답 포인트: 마지막 반복 포함 여부(`<=` vs `<`)를 잘못 보면 결과가 1회 어긋납니다.

종료 조건 체크표:

| 항목 | 체크 질문 | 빠른 판정 |
| --- | --- | --- |
| 시작값 | 첫 회차 값이 무엇인가 | 초기값 그대로 시작 |
| 종료 비교 | `<`인지 `<=`인지 | `<=`면 경계값 포함 |
| 증감 | 한 회차마다 얼마나 변하는가 | 증가/감소 방향 확인 |
| while 진입 | 조건 검사 시점은 언제인가 | 본문 진입 전에 검사 |


![for while 종료 조건과 반복 횟수 추적 흐름 다이어그램](./data/theory/images/contest_w04_loop_termination_flow.svg)

예시 (기본):
```c
#include <stdio.h>
int main(void) {
    int s = 0;
    for (int i = 2; i <= 10; i += 2) s += i;
    printf("%d", s);
    return 0;
}
```
```io
input:
(없음)
output:
30
```

예시 (변형):
```c
#include <stdio.h>
int main(void) {
    int a = 14, b = 5;
    while (a > 0) {
        a -= 4;
        b += 2;
    }
    printf("%d", b);
    return 0;
}
```
```io
input:
(없음)
output:
13
```

예시 (함정):
```c
#include <stdio.h>
int main(void) {
    int c = 0;
    for (int i = 0; i < 5; i++) c += 1;
    printf("%d", c);
    return 0;
}
```
```io
input:
(없음)
output:
5
```

### 개념 2) break/continue 영향 범위
- 개념 정의: `break`와 `continue`가 어떤 반복문 레벨에 작동하는지 판별하는 개념입니다.
- 판별 규칙: `break`는 가장 가까운 반복문 1개만 즉시 종료한다.
- 판별 규칙: `continue`는 가장 가까운 반복문의 현재 회차만 건너뛰고 다음 회차로 간다.
- 판별 규칙: 중첩 루프 전체 탈출이 필요하면 플래그 변수 또는 추가 조건이 필요하다.
- 추적 절차: 현재 실행 중인 루프 레벨 표시 -> `break/continue` 발생 위치 표시 -> 다음 실행 위치 확인 순으로 푼다.
- 오답 포인트: 내부 루프 `break`가 외부 루프까지 종료한다고 가정하면 오답입니다.

제어문 적용 범위표:

| 구문 | 즉시 효과 | 적용 범위 |
| --- | --- | --- |
| `continue` | 현재 회차 나머지 생략 | 가장 가까운 루프 1개 |
| `break` | 루프 즉시 종료 | 가장 가까운 루프 1개 |
| `flag + break` | 내부 종료 후 외부 조건 종료 | 설계한 외부 루프까지 확장 가능 |


![break와 continue가 적용되는 루프 범위 비교 다이어그램](./data/theory/images/contest_w04_break_continue_scope.svg)

예시 (기본):
```c
#include <stdio.h>
int main(void) {
    int n = 0;
    for (int i = 0; i < 4; i++) {
        if (i == 2) continue;
        n += i;
    }
    printf("%d", n);
    return 0;
}
```
```io
input:
(없음)
output:
4
```

예시 (변형):
```c
#include <stdio.h>
int main(void) {
    int n = 0;
    for (int i = 0; i < 5; i++) {
        if (i == 3) break;
        n += i;
    }
    printf("%d", n);
    return 0;
}
```
```io
input:
(없음)
output:
3
```

예시 (함정):
```text
내부 루프에서 break를 써도 외부 루프는 계속 돈다.
외부까지 멈추려면 flag + 외부 조건 확인이 필요하다.
```

### 개념 3) 중첩 반복 총 실행 횟수
- 개념 정의: 2중/3중 반복문에서 실제 실행된 회차 수와 조건 통과 횟수를 계산하는 개념입니다.
- 판별 규칙: 전체 실행 횟수는 각 루프의 유효 반복 횟수 곱으로 시작해, `continue`/`break`를 반영해 줄인다.
- 판별 규칙: 조건문이 내부에서 가지치기를 만들면, "실행된 회차"와 "누적된 회차"를 분리해 계산한다.
- 추적 절차: 루프 범위 확정 -> 가지치기 조건 기록 -> 플래그 변경 시점 기록 -> 최종 출력 확인 순으로 푼다.
- 오답 포인트: 중첩 루프 문제에서 출력 직전 탈출 조건을 놓치면 완전히 다른 값을 얻습니다.

중첩 반복 검산표:

| 단계 | 계산 대상 | 체크 포인트 |
| --- | --- | --- |
| 1 | 기본 조합 수 | 각 루프 유효 횟수 곱으로 계산 |
| 2 | 가지치기(`continue`) | 건너뛴 회차를 별도 차감 |
| 3 | 탈출(`break`) | 어느 레벨에서 멈췄는지 표시 |
| 4 | 최종값 | 출력 직전 상태를 한 줄로 확인 |


![중첩 반복의 실행 횟수와 가지치기 추적 다이어그램](./data/theory/images/contest_w04_nested_loop_count_trace.svg)

예시 (기본):
```c
#include <stdio.h>
int main(void) {
    int cnt = 0;
    for (int i = 1; i <= 3; i++) {
        for (int j = 1; j <= 3; j++) {
            if (i == j) continue;
            cnt++;
        }
    }
    printf("%d", cnt);
    return 0;
}
```
```io
input:
(없음)
output:
6
```

예시 (변형):
```c
#include <stdio.h>
int main(void) {
    int flag = 0, ans = -1;
    for (int i = 1; i <= 9; i++) {
        for (int j = 1; j <= 9; j++) {
            if (i * j == 21) { ans = i + j; flag = 1; break; }
        }
        if (flag) break;
    }
    printf("%d", ans);
    return 0;
}
```
```io
input:
(없음)
output:
10
```

예시 (함정):
```text
3중 루프에서 break가 가장 안쪽 루프에만 적용되는지 항상 표시하고 계산한다.
```

### 실전 풀이 루틴 (W04 공통)
1. 반복문마다 `(초기값, 조건, 증감)`을 한 줄 표로 먼저 적는다.
2. `break/continue`가 어느 레벨 루프에 적용되는지 옆에 표시한다.
3. 누적 변수와 제어 변수(`flag`)를 분리해 추적한다.
4. 종료 조건이 만족되는 "첫 시점"을 명시하고 그 이후 실행을 차단한다.
5. 최종 출력값을 선택지와 대조해 검산한다.


### 공통 미니 체크 (필수 제출)
문항:
1. `for(i=100; i<=2024; i+=100)`의 반복 횟수를 쓰세요.
2. 내부 루프 `break`가 외부 루프에 미치는 영향을 한 줄로 쓰세요.
3. 3중 루프에서 오답을 줄이는 기록 항목 2가지를 쓰세요.

답안 작성:
1. 정답: [ ] / 근거: [ ]
2. 정답: [ ] / 근거: [ ]
3. 정답: [ ] / 근거: [ ]

## 초등 트랙 (ELEMENTARY)
<!-- audience:elementary -->
### 초등 포인트
- 개념 1을 중심으로 반복 횟수와 누적값을 정확히 계산합니다.


### 초등 연계 실습
실습 목표:
- for 반복 횟수를 계산해 누적값으로 연결합니다.

실습 문제:
```c
#include <stdio.h>
int main(void) {
    int s = 0;
    for (int i = 50; i <= 300; i += 50) s += 1;
    printf("%d", s);
    return 0;
}
```

체크포인트:
1. `i`의 실제 방문값을 모두 적었는가?
2. 마지막 방문값이 조건을 만족하는지 확인했는가?

## 중등 트랙 (MIDDLE)
<!-- audience:middle -->
### 중등 포인트
- 개념 2, 3을 함께 사용해 중첩 반복의 실제 실행 경로를 추적합니다.


### 중등 연계 실습
실습 목표:
- `continue`/`break`가 누적 횟수에 미치는 영향을 계산합니다.

실습 문제:
```c
#include <stdio.h>
int main(void) {
    int c = 0;
    for (int i = 1; i <= 4; i++) {
        for (int j = 1; j <= 4; j++) {
            if (i == j) continue;
            if (i + j >= 6) break;
            c++;
        }
    }
    printf("%d", c);
    return 0;
}
```

체크포인트:
1. `continue`로 건너뛴 회차를 표시했는가?
2. `break` 이후 같은 루프 레벨의 실행이 멈췄는지 확인했는가?

## 고등 트랙 (HIGH)
<!-- audience:high -->
### 고등 포인트
- while 내부의 복합 갱신(`*=`, `/=`, `+=`)을 반복 횟수와 함께 추적합니다.


### 고등 연계 실습
실습 목표:
- 반복마다 변수 쌍의 상태 변화를 표로 검산합니다.

실습 문제:
```c
#include <stdio.h>
int main(void) {
    int a = 18, b = 40;
    while (a > 0) {
        a -= 5;
        b = b * 2 / 3;
    }
    printf("%d", b);
    return 0;
}
```

체크포인트:
1. 각 반복 후 `(a, b)`를 순서대로 기록했는가?
2. 종료 직전 반복이 포함되는지 조건으로 검산했는가?
