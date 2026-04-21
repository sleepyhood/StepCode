---
id: "py_lv05_cast"
contentType: "lesson"
track: "language"
lang: "python"
categoryId: "py_cast"
title: "Python Lv5 자료형 변환"
status: "active"
order: 205
audience: "common"
recommendedSetId: "py_lv05_cast_b01"
relatedSetIds: ["py_lv05_cast_b01", "py_lv05_cast_b02", "py_lv05_cast_c01"]
prerequisites: ["py_lv04_operator"]
nextConcepts: ["py_lv06_if"]
priority: 2
---
# 자료형 변환 핵심 이론

## 1) 자료형 변환이 하는 일

자료형 변환(cast)은 값을 원하는 타입으로 바꾸는 작업입니다.

- 같은 값이라도 타입이 다르면 연산 결과가 달라질 수 있습니다.
- 문자열을 숫자로 바꿔야 계산이 가능합니다.
- 초급 단계에서는 "지금 값의 타입이 무엇인지" 먼저 확인하는 습관이 중요합니다.

---

## 2) 실행 흐름

형변환 코드는 아래 4단계로 읽으면 이해가 쉽습니다.

1. 현재 값과 타입 확인
2. 목표 타입 결정 (`int`, `float`/`double` 등)
3. 변환 실행
4. 변환 후 연산/출력

핵심은 "**변환 전 타입과 변환 후 타입은 다를 수 있다**"는 점입니다.

---

## 3) 가장 자주 쓰는 패턴

### 패턴 A: 문자열 -> 정수 변환

{lang:python}
```python
s = "12"
n = int(s)
print("%d" % (n + 3))
```

{lang:c}
```c
char s[] = "12";
int n = atoi(s);
printf("%d\n", n + 3);
```

{lang:java}
```java
String s = "12";
int n = Integer.parseInt(s);
System.out.printf("%d\n", n + 3);
```

```io
input:
(없음)
output:
15
```

아래 표는 **각 변환/대입문이 끝난 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 1. 문자열을 정수로 변환
lang: python,c,java
columns: 단계, 값, 타입, 출력
rows:
1 | "12" | string | 
2 | 12 | int | 15
```

### 패턴 B: 정수 나눗셈을 실수 나눗셈으로 변환

{lang:python}
```python
a = 7
b = 2
x = float(a) / b
print("%.1f" % x)
```

{lang:c}
```c
int a = 7;
int b = 2;
double x = (double)a / b;
printf("%.1f\n", x);
```

{lang:java}
```java
int a = 7;
int b = 2;
double x = (double)a / b;
System.out.printf("%.1f\n", x);
```

```io
input:
(없음)
output:
3.5
```

아래 표는 **각 연산문이 끝난 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 2. 정수 나눗셈 vs 실수 나눗셈
lang: python,c,java
columns: 단계, 식, 결과, 타입
rows:
1 | 7 / 2(정수 기준) | 3 또는 3.0 | int 또는 float
2 | 변환 후 7 / 2 | 3.5 | float/double
```

### 패턴 C: 실수를 정수로 변환

{lang:python}
```python
x = 3.9
n = int(x)
print("%d" % n)
```

{lang:c}
```c
double x = 3.9;
int n = (int)x;
printf("%d\n", n);
```

{lang:java}
```java
double x = 3.9;
int n = (int)x;
System.out.printf("%d\n", n);
```

```io
input:
(없음)
output:
3
```

---

## 4) 형변환 포인트 (cast 단원 핵심)

cast 단원의 핵심은 "연산 전에 타입을 맞춰야 원하는 결과가 나온다"는 점입니다.

- 문자열은 숫자로 바꾼 뒤 계산합니다.
- 정수 나눗셈은 필요하면 실수 타입으로 먼저 변환합니다.
- 실수 -> 정수 변환은 소수점 아래가 버려질 수 있습니다.

---

## 5) 자주 틀리는 포인트

1. 문자열 덧셈 vs 숫자 덧셈 혼동
   `"12" + "3"`은 문자열 결합, `12 + 3`은 숫자 계산입니다.

2. 정수 나눗셈 결과 착각
   언어/타입에 따라 `7 / 2`가 `3` 또는 `3.5`가 될 수 있습니다.

3. 변환 시점 실수
   연산 후 변환이 아니라, 필요한 경우 연산 전에 변환해야 합니다.

4. 변환 실패 상황 미고려
   숫자가 아닌 문자열을 숫자로 바꾸려 하면 오류가 날 수 있습니다.

---

## 5-1) 언어별 실전 팁

{lang:python} 문자열 -> 정수는 `int(s)`, 문자열 -> 실수는 `float(s)`를 사용합니다.

{lang:c} 정수를 실수 계산에 쓰려면 `(double)` 캐스트를 명시해 계산 타입을 올립니다.

{lang:java} 문자열 -> 정수는 `Integer.parseInt(s)`, 문자열 -> 실수는 `Double.parseDouble(s)`를 사용합니다.

{lang:python,c,java} 초급 단원에서는 출력 형식을 서식문자 기반(`%d`, `%.1f`)으로 통일해 연습합니다.

---

## 6) 미니 체크 문제

### Q1

문자열 값을 숫자 계산에 쓰려면 먼저 무엇을 해야 하나요?  
정답: `숫자 타입으로 변환(cast/parse)`

### Q2

정수 나눗셈을 실수 결과로 얻고 싶을 때 핵심 원칙은 무엇인가요?  
정답: `연산 전에 피연산자 중 하나를 실수 타입으로 변환`

### Q3 (언어별)

{lang:python} Python에서 문자열 `"20"`을 정수로 바꾸는 코드는 무엇인가요?  
정답: ``int("20")``

{lang:c} C에서 `a / b`를 실수 계산으로 만들 때 자주 쓰는 캐스트는 무엇인가요?  
정답: ``(double)a``

{lang:java} Java에서 문자열을 정수로 변환하는 메서드는 무엇인가요?  
정답: ``Integer.parseInt(s)``

---
## 7) 다음 학습

- 기본 문제: `py_lv05_cast_b01`
- 심화 문제: `py_lv05_cast_c01`
- 다음 개념: `if` (조건에 따라 분기)
