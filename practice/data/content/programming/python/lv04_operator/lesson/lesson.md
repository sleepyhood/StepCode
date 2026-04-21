---
id: "py_lv04_operator"
contentType: "lesson"
track: "language"
lang: "python"
categoryId: "py_operator"
title: "Python Lv4 연산자"
status: "active"
order: 204
audience: "common"
recommendedSetId: "py_lv04_operator_b01"
relatedSetIds: ["py_lv04_operator_b01", "py_lv04_operator_b02", "py_lv04_operator_c01"]
prerequisites: ["py_lv03_input"]
nextConcepts: ["py_lv05_cast"]
priority: 2
---
# 연산자 핵심 이론

## 1) 연산자가 하는 일

연산자는 값을 계산하거나 비교할 때 사용하는 기호입니다.

- 산술 연산: `+ - * / %`
- 비교 연산: `== != < <= > >=`
- 논리 연산: and/or/not 또는 `&& || !`

초급 단계에서는 "연산 결과 타입(숫자/참거짓)"을 구분하는 습관이 중요합니다.

---

## 2) 실행 흐름

연산 코드는 아래 순서로 읽습니다.

1. 피연산자(값/변수) 확인
2. 연산자 의미 확인
3. 연산 결과 계산
4. 결과를 출력/저장

핵심은 "**같은 숫자라도 어떤 연산자를 쓰느냐에 따라 결과가 달라진다**"는 점입니다.

---

## 3) 가장 자주 쓰는 패턴

### 패턴 A: 산술 연산

{lang:python}
```python
a = 7
b = 3
print("%d" % (a + b))
print("%d" % (a % b))
```

{lang:c}
```c
int a = 7;
int b = 3;
printf("%d\n", a + b);
printf("%d\n", a % b);
```

{lang:java}
```java
int a = 7;
int b = 3;
System.out.printf("%d\n", a + b);
System.out.printf("%d\n", a % b);
```

```io
input:
(없음)
output:
10
1
```

아래 표는 **각 출력문이 실행된 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 1. 산술 연산 결과
lang: python,c,java
columns: 단계, 식, 결과
rows:
1 | a + b | 10
2 | a % b | 1
```

### 패턴 B: 비교 연산

{lang:python}
```python
a = 7
b = 3
print(a > b)
print(a == b)
```

{lang:c}
```c
int a = 7;
int b = 3;
printf("%d\n", a > b);
printf("%d\n", a == b);
```

{lang:java}
```java
int a = 7;
int b = 3;
System.out.println(a > b);
System.out.println(a == b);
```

```io
input:
(없음)
output:
true/1
false/0
```

아래 표는 **각 출력문이 실행된 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 2. 비교 연산 결과
lang: python,c,java
columns: 단계, 식, 결과
rows:
1 | a > b | true/1
2 | a == b | false/0
```

### 패턴 C: 논리 연산

{lang:python}
```python
x = 5
print((x >= 1) and (x <= 10))
```

{lang:c}
```c
int x = 5;
printf("%d\n", (x >= 1) && (x <= 10));
```

{lang:java}
```java
int x = 5;
System.out.println((x >= 1) && (x <= 10));
```

```io
input:
(없음)
output:
true/1
```

아래 표는 **조건식이 계산되는 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 3. 논리 연산(and) 평가
lang: python,c,java
columns: 단계, x, 왼쪽식(x>=1), 오른쪽식(x<=10), 최종 결과
rows:
1 | 5  | true/1 | true/1  | true/1
2 | 12 | true/1 | false/0 | false/0
```

### 패턴 D: 부정 연산 (`not`, `!`)

{lang:python}
```python
x = 5
print(x >= 1)
print(not (x >= 1))
```

{lang:c}
```c
int x = 5;
printf("%d\n", x >= 1);
printf("%d\n", !(x >= 1));
```

{lang:java}
```java
int x = 5;
System.out.println(x >= 1);
System.out.println(!(x >= 1));
```

```io
input:
(없음)
output:
true/1
false/0
```

아래 표는 **조건식과 부정식이 계산된 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 4. not/! 평가
lang: python,c,java
columns: 단계, x, 원래 조건(x>=1), 부정(not/!), 최종 출력
rows:
1 | 5  | true/1  | false/0 | false/0
2 | -1 | false/0 | true/1  | true/1
```

---

## 4) 연산 순서 포인트 (연산자 단원 핵심)

연산자 단원에서는 "어떤 연산이 먼저 계산되는가"를 확인해야 합니다.

- 괄호가 있으면 괄호 안을 먼저 계산합니다.
- 산술/비교/논리 연산이 섞이면 결과 타입이 바뀔 수 있습니다.
- 예: `a + b > 10`은 먼저 `a + b`를 계산한 뒤, 비교 결과(true/false 또는 1/0)를 만듭니다.
- 논리 결과는 언어/출력 방식에 따라 `true/false` 또는 `1/0`으로 보일 수 있습니다.

---

## 5) 자주 틀리는 포인트

1. `=`와 `==` 혼동
   `=`는 저장, `==`는 같은지 비교입니다.

2. 정수 나눗셈 오해
   정수끼리 나누면 소수점이 버려질 수 있습니다.

3. `%`(나머지) 의미 혼동
   `%`는 퍼센트가 아니라 나머지 연산입니다.

4. 논리식 괄호 누락
   조건이 길어지면 괄호를 써서 의도를 명확히 해야 합니다.

---

## 5-1) 언어별 실전 팁

{lang:python} 논리 연산자는 `and`, `or`, `not`을 사용합니다.

{lang:c} 논리 연산자는 `&&`, `||`, `!`를 사용하며, 참/거짓 출력은 보통 `1/0`입니다.

{lang:java} Java 논리 연산자는 C와 동일하게 `&&`, `||`, `!`를 사용하며 출력은 `true/false`입니다.

{lang:python,c,java} 초급 단원에서는 숫자 출력을 서식문자 기반(`%d`, `%.1f`)으로 통일해 연습합니다.

---

## 6) 미니 체크 문제

### Q1

`a = 8`, `b = 3`일 때 `a % b` 값은 무엇인가요?  
정답: `2`

### Q2

`x = 12`일 때 `x >= 1 and x <= 10`의 결과는 무엇인가요?  
정답: `false` (C 출력은 `0`)

### Q3 (언어별)

{lang:python} Python에서 `x >= 1`의 부정을 쓰는 형태는 무엇인가요?  
정답: ``not (x >= 1)``

{lang:c} C에서 `x >= 1`의 부정을 쓰는 형태는 무엇인가요?  
정답: ``!(x >= 1)``

{lang:java} Java에서 논리 AND를 쓰는 연산자는 무엇인가요?  
정답: ``&&``

---
## 7) 다음 학습

- 기본 문제: `py_lv04_operator_b01`
- 심화 문제: `py_lv04_operator_c01`
- 다음 개념: `cast` (형변환)
