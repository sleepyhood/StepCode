---
id: "py_lv03_input"
contentType: "lesson"
track: "language"
lang: "python"
categoryId: "py_input"
title: "Python Lv3 입력"
status: "active"
order: 203
audience: "common"
recommendedSetId: "py_input_b1"
relatedSetIds: ["py_input_b1", "py_input_b2", "py_input_b3", "py_input_c1"]
prerequisites: ["py_lv02_var"]
nextConcepts: ["py_lv04_operator"]
priority: 2
---
# 입력 핵심 이론

## 1) 입력이 하는 일

입력은 사용자에게 값을 받아 변수에 저장하는 과정입니다.

- 프로그램은 입력값을 받아 계산/판단/출력을 진행합니다.
- 입력값은 "그대로 쓰는 값"이 아니라, 보통 **원하는 타입으로 변환**해서 사용합니다.
- 초급 단계에서는 "입력 -> 변환 -> 저장 -> 출력" 순서를 먼저 익히는 것이 중요합니다.

---

## 2) 실행 흐름

입력 코드는 아래 4단계로 읽으면 실수가 줄어듭니다.

1. 입력 읽기
2. 타입 변환 (`int`, `float` 등)
3. 변수에 저장
4. 출력/연산에 사용

핵심은 "**변환하지 않으면 문자열로 남을 수 있다**"는 점입니다.

---

## 3) 가장 자주 쓰는 패턴

### 패턴 A: 한 개 정수 입력

{lang:python}
```python
n = int(input())
print("%d" % (n + 1))
```

{lang:c}
```c
int n;
scanf("%d", &n);
printf("%d\n", n + 1);
```

{lang:java}
```java
import java.util.Scanner;

Scanner sc = new Scanner(System.in);
int n = sc.nextInt();
System.out.printf("%d\n", n + 1);
```

```io
input:
7
output:
8
```

아래 표는 **입력 후 변수 상태가 확정된 직후**를 기록한 것입니다.

```tracegrid
title: Trace 1. 한 개 정수 입력
lang: python,c,java
columns: 단계, raw 입력, n(변환 후), 출력
rows:
1 | "7" | 7 | 8
```

### 패턴 B: 한 줄에 두 값 입력 (split + 개별 변환)

{lang:python}
```python
a_str, b_str = input().split()
a = int(a_str)
b = float(b_str)
print("%d %.1f" % (a, b))
```

{lang:c}
```c
int a;
float b;
scanf("%d %f", &a, &b);
printf("%d %.1f\n", a, b);
```

{lang:java}
```java
import java.util.Scanner;

Scanner sc = new Scanner(System.in);
int a = sc.nextInt();
float b = sc.nextFloat();
System.out.printf("%d %.1f\n", a, b);
```

```io
input:
3 2.5
output:
3 2.5
```

아래 표는 **입력 후 변수 상태가 확정된 직후**를 기록한 것입니다.

```tracegrid
title: Trace 2. split + 타입 변환
lang: python,c,java
columns: 단계, 입력 줄, a(int), b(float), 출력
rows:
1 | "3 2.5" | 3 | 2.5 | 3 2.5
```

### 패턴 C: Python에서 map으로 한 줄 입력 처리

{lang:python}
```python
a, b = map(int, input().split())
print("%d" % (a + b))
```

{lang:c}
```c
int a, b;
scanf("%d %d", &a, &b);
printf("%d\n", a + b);
```

{lang:java}
```java
import java.util.Scanner;

Scanner sc = new Scanner(System.in);
int a = sc.nextInt();
int b = sc.nextInt();
System.out.printf("%d\n", a + b);
```

```io
input:
10 20
output:
30
```

---

## 4) 값 변환 포인트 (입력 단원 핵심)

입력 단원에서 가장 중요한 지점은 "어떤 타입으로 쓸지"를 먼저 정하는 것입니다.

- 정수 계산: `int`
- 소수 포함 계산: `float`
- 섞여 있다면 각 변수마다 타입을 분리해서 변환

예를 들어 Python에서 `input().split()` 결과는 문자열 목록이므로, 각 값에 `int()`/`float()`를 적용해야 합니다.

---

## 5) 자주 틀리는 포인트

1. 변환 누락
   Python에서 `n = input()`만 쓰면 문자열입니다.

2. 타입 불일치
   실수인데 `int`로 변환하거나, 정수인데 실수 형식으로만 처리하는 실수.

3. 입력 개수 불일치
   두 개 입력이 필요한데 한 변수만 받는 경우.

4. 출력 형식 혼동
   초급 단계에서는 서식문자 출력(`%d`, `%.1f`)을 기준으로 통일해 연습합니다.

---

## 5-1) 언어별 실전 팁

{lang:python} 기본 입력은 `input()`입니다. 한 줄에 여러 값이 오면 `input().split()`으로 먼저 나눕니다.

{lang:python} 나눈 값은 문자열이므로, 각 변수마다 `int()`나 `float()`를 적용합니다.

{lang:python} `map`을 쓰면 한 줄로 변환까지 처리할 수 있습니다. 예: `a, b = map(int, input().split())`

{lang:python,c,java} 초급 입력 단원에서는 출력을 서식문자 기반으로 통일합니다. (`%d`, `%.1f`)

{lang:c} `scanf`에서 변수 앞 `&`를 빼먹지 않도록 확인합니다.

{lang:java} `Scanner`의 `nextInt`, `nextFloat`처럼 타입에 맞는 입력 메서드를 사용합니다.

---

## 6) 미니 체크 문제

### Q1

입력값을 계산에 사용하려면 먼저 무엇을 확인해야 하나요?  
정답: `현재 타입과 필요한 타입(변환 필요 여부)`

### Q2

`n`개 입력 반복에서 `i`와 `num`은 각각 무엇을 의미하나요?  
정답: ``i``는 반복 인덱스, ``num``은 실제 입력값

### Q3 (언어별)

{lang:python} 한 줄 입력 `"3 4"`를 두 정수로 받는 대표 형태는 무엇인가요?  
정답: ``a, b = map(int, input().split())``

{lang:c} C에서 정수와 실수를 한 줄에서 받는 기본 형식은 무엇인가요?  
정답: ``scanf("%d %f", &a, &b);``

{lang:java} Java `Scanner`로 정수 2개를 받을 때 주로 쓰는 메서드는 무엇인가요?  
정답: ``nextInt()``

---
## 7) 다음 학습

- 기본 문제: `py_input_b1` / `c_input_b1`
- 심화 문제: `py_input_c1` / `c_input_c1`
- 다음 개념: `operator` (입력값을 이용한 연산)
