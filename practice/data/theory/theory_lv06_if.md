# 조건문 핵심 이론

## 1) 조건문이 하는 일

조건문은 조건식의 참/거짓에 따라 실행 경로를 나누는 문법입니다.

- 같은 입력이라도 조건 결과에 따라 다른 출력이 나옵니다.
- `if`, `elif/else if`, `else`로 분기를 구성합니다.
- 조건 단원부터는 "어느 줄이 실제로 실행됐는지"를 추적하는 습관이 중요합니다.

---

## 2) 실행 흐름

조건문은 아래 순서로 읽습니다.

1. 첫 조건식 검사
2. 참이면 해당 블록 실행 후 종료
3. 거짓이면 다음 조건식 검사
4. 어떤 조건도 참이 아니면 `else` 실행

핵심은 "**위에서 아래 순서로 조건을 검사하고, 참이 되는 첫 분기만 실행된다**"는 점입니다.

---

## 3) 가장 자주 쓰는 패턴

### 패턴 A: 단일 if

조건이 참일 때만 특정 동작 1개를 실행하는 가장 기본 패턴입니다.
거짓일 때는 아무것도 실행하지 않는 흐름을 확인하세요.

{lang:python}
```python
n = 5
if n > 0:
    print("양수")
```

{lang:c}
```c
int n = 5;
if (n > 0) {
    printf("양수\n");
}
```

{lang:java}
```java
int n = 5;
if (n > 0) {
    System.out.println("양수");
}
```

```io
input:
5
output:
양수
```

아래 표는 **각 조건식 검사 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 1. 단일 if 흐름
lang: python,c,java
columns: 단계, 조건식, 결과, 실행 블록, 출력
rows:
1 | n=5, n > 0  | true  | if 본문 | 양수
2 | n=-1, n > 0 | false | 실행 없음 | 출력 없음
```

### 패턴 B: if - else

참/거짓 두 경우를 반드시 하나씩 처리하는 양자 분기 패턴입니다.
둘 중 정확히 한 블록만 실행된다는 점이 핵심입니다.

{lang:python}
```python
n = -2
if n >= 0:
    print("0 이상")
else:
    print("음수")
```

{lang:c}
```c
int n = -2;
if (n >= 0) {
    printf("0 이상\n");
} else {
    printf("음수\n");
}
```

{lang:java}
```java
int n = -2;
if (n >= 0) {
    System.out.println("0 이상");
} else {
    System.out.println("음수");
}
```

```io
input:
-2
output:
음수
```

아래 표는 **각 조건식 검사 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 2. if-else 흐름
lang: python,c,java
columns: 단계, 조건식, 결과, 실행 블록, 출력
rows:
1 | n >= 0 | false | else | 음수
```

### 패턴 C: if - elif(else if) - else

여러 조건 중 처음으로 참이 되는 분기만 실행하는 다중 분기 패턴입니다.
조건 순서가 바뀌면 결과도 바뀔 수 있으므로 검사 순서를 함께 추적해야 합니다.

{lang:python}
```python
score = 78
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C")
```

{lang:c}
```c
int score = 78;
if (score >= 90) {
    printf("A\n");
} else if (score >= 80) {
    printf("B\n");
} else {
    printf("C\n");
}
```

{lang:java}
```java
int score = 78;
if (score >= 90) {
    System.out.println("A");
} else if (score >= 80) {
    System.out.println("B");
} else {
    System.out.println("C");
}
```

```io
input:
78
output:
B
```

아래 표는 **각 조건식 검사 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 3. 다중 분기 흐름
lang: python,c,java
columns: 단계, 검사한 조건식, 결과, 다음 동작
rows:
1 | score >= 90 | false | 다음 조건 검사
2 | score >= 80 | true | B 출력 후 종료
```

경계값은 아래처럼 별도로 확인하면 실수를 줄일 수 있습니다.

```tracegrid
title: Trace 4. 경계값(score=90,80,79)
lang: python,c,java
columns: 입력 score, score>=90, score>=80, 실행 분기, 출력
rows:
90 | true  | 검사 안 함 | if          | A
80 | false | true  | elif/else if | B
79 | false | false | else          | C
```

### 패턴 D: 복합 조건(범위 검사)

범위 조건은 논리 연산으로 한 번에 표현할 수 있습니다.
단, 양쪽 조건이 각각 무엇을 검사하는지 분리해서 읽는 습관이 필요합니다.

{lang:python}
```python
x = 7
if (x >= 1) and (x <= 10):
    print("범위 안")
else:
    print("범위 밖")
```

{lang:c}
```c
int x = 7;
if ((x >= 1) && (x <= 10)) {
    printf("범위 안\n");
} else {
    printf("범위 밖\n");
}
```

{lang:java}
```java
int x = 7;
if ((x >= 1) && (x <= 10)) {
    System.out.println("범위 안");
} else {
    System.out.println("범위 밖");
}
```

```tracegrid
title: Trace 5. 복합 조건 범위 검사
lang: python,c,java
columns: x, x>=1, x<=10, 최종 조건, 출력
rows:
7  | true  | true  | true  | 범위 안
12 | true  | false | false | 범위 밖
```

---

## 4) 분기 추적 포인트 (if 단원 핵심)

조건 단원부터는 결과만 보지 말고 "검사 순서"를 같이 추적해야 합니다.

- 어떤 조건이 먼저 검사되는지 확인합니다.
- 참이 된 시점에서 나머지 분기는 검사하지 않는지 확인합니다.
- `else`는 "앞의 모든 조건이 거짓"일 때만 실행됩니다.

중첩 if에서 `else` 결합 위치도 반드시 확인해야 합니다.

```python
if a > 0:
    if b > 0:
        print("P")
    else:
        print("Q")
```

```tracegrid
title: Trace 6. 중첩 if의 else 결합
lang: python,c,java
columns: a, b, 바깥 if(a>0), 안쪽 if(b>0), 실행 출력
rows:
1 | 1  | true  | true  | P
1 | -1 | true  | false | Q
-1 | 1 | false | 검사 안 함 | 출력 없음
```

---

## 5) 자주 틀리는 포인트

1. 조건 순서 실수
   범위가 겹치면 더 큰 기준(좁은 조건)을 먼저 검사해야 합니다.

2. 경계값 실수
   `<`와 `<=`, `>`와 `>=` 차이로 결과가 달라집니다.

3. `=`와 `==` 혼동
   `=`는 대입, `==`는 비교입니다.

4. else 연결 위치 실수
   중첩 조건에서 `else`가 어떤 `if`에 붙는지 주의해야 합니다.

---

## 5-1) 언어별 실전 팁

{lang:python} Python은 `if/elif/else` 뒤에 콜론(`:`)을 쓰고 들여쓰기로 블록을 구분합니다.

{lang:c} C는 조건식을 괄호로 감싸고 블록은 `{}`로 묶습니다.

{lang:java} Java도 C와 동일하게 괄호/중괄호를 사용합니다.

{lang:python,c,java} 조건문은 "정답 출력"보다 "어느 분기가 실행됐는지"를 먼저 추적해 확인합니다.

---

## 6) 미니 체크 문제

### Q1

`n = 0`일 때 `if n > 0 ... else ...` 구조에서 실행되는 블록은 무엇인가요?  
정답: `else`

### Q2

`if -> elif/else if -> else` 구조에서 조건이 처음으로 참이 되면 그 뒤 분기는 어떻게 되나요?  
정답: `검사/실행하지 않고 종료합니다.`

### Q3 (언어별)

{lang:python} 아래 코드에서 `n = -1`일 때 실행되는 출력은 무엇인가요?  
`if n > 0: print("P")`  
`elif n == 0: print("Z")`  
`else: print("N")`  
정답: ``N``

{lang:c} 아래 코드에서 `n = 0`일 때 실행되는 출력은 무엇인가요?  
`if (n > 0) printf("P\n");`  
`else if (n == 0) printf("Z\n");`  
`else printf("N\n");`  
정답: ``Z``

{lang:java} 아래 코드에서 `n = 2`일 때 실행되는 출력은 무엇인가요?  
`if (n > 0) System.out.println("P");`  
`else if (n == 0) System.out.println("Z");`  
`else System.out.println("N");`  
정답: ``P``

### Q4

아래 두 코드는 항상 같은 결과를 내나요?  
코드 A: `if score >= 90: A / elif score >= 80: B / else: C`  
코드 B: `if score >= 80: B / elif score >= 90: A / else: C`  
정답: `아니오. 조건 순서가 달라 결과가 달라질 수 있습니다.`

---
## 7) 다음 학습

- 기본 문제: `py_if_b1` / `c_if_b1`
- 심화 문제: `py_if_c1` / `c_if_c1`
- 다음 개념: `for` (반복 + 분기 추적)

