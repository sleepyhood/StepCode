---
id: "py_lv08_while"
contentType: "lesson"
track: "language"
lang: "python"
categoryId: "py_while"
title: "Python Lv8 while문"
status: "active"
order: 208
audience: "common"
recommendedSetId: "py_while_b1"
relatedSetIds: ["py_while_b1", "py_lv08_while_b02", "py_lv08_while_c01"]
prerequisites: ["py_lv07_for"]
nextConcepts: ["py_lv09_nfor"]
priority: 3
---
# while문 핵심 이론

## 1) while문이 하는 일

`while`은 조건이 참인 동안 같은 코드를 반복 실행하는 문법입니다.

- 반복 횟수를 미리 정확히 모를 때 자주 사용합니다.
- 매 반복마다 조건을 다시 검사합니다.
- 종료를 위해 반복문 안에서 상태(변수)가 바뀌어야 합니다.

---

## 2) 실행 흐름

while문은 아래 순서로 읽습니다.

1. 조건식 검사
2. 참이면 본문 실행
3. 상태 갱신(증감/입력 갱신)
4. 다시 조건식 검사

핵심은 "**조건 검사 -> 본문 -> 갱신** 흐름이 반복되며, 조건이 거짓이 되는 순간 종료된다"는 점입니다.

![while 실행 흐름도](./data/theory/images/while_flow.svg)

---

## 3) 가장 자주 쓰는 패턴

### 패턴 A: 기본 증가 반복

{lang:python}
```python
i = 1
while i <= 3:
    print("%d" % i)
    i += 1
```

{lang:c}
```c
int i = 1;
while (i <= 3) {
    printf("%d\n", i);
    i++;
}
```

{lang:java}
```java
int i = 1;
while (i <= 3) {
    System.out.printf("%d\n", i);
    i++;
}
```

```io
input:
(없음)
output:
1
2
3
```

아래 표는 **각 반복이 끝난 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 1. 기본 while 반복
lang: python,c,java
columns: 반복, i(반복 시작), 출력, i(갱신 후)
rows:
1 | 1 | 1 | 2
2 | 2 | 2 | 3
3 | 3 | 3 | 4
```

### 패턴 B: 누적 합 while

{lang:python}
```python
i = 1
sumv = 0
while i <= 4:
    sumv += i
    i += 1
print("%d" % sumv)
```

{lang:c}
```c
int i = 1;
int sumv = 0;
while (i <= 4) {
    sumv += i;
    i++;
}
printf("%d\n", sumv);
```

{lang:java}
```java
int i = 1;
int sumv = 0;
while (i <= 4) {
    sumv += i;
    i++;
}
System.out.printf("%d\n", sumv);
```

```io
input:
(없음)
output:
10
```

아래 표는 **각 반복이 끝난 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 2. while 누적 합
lang: python,c,java
columns: 반복, i, sumv(갱신 후)
rows:
1 | 1 | 1
2 | 2 | 3
3 | 3 | 6
4 | 4 | 10
```

### 패턴 C: 센티넬 입력 반복

센티넬 값(예: `0`)은 반복 종료를 위한 값이며, 입력은 되지만 출력 대상은 아닙니다.

{lang:python}
```python
num = int(input())
while num != 0:
    print("%d" % num)
    num = int(input())
```

{lang:c}
```c
int num;
scanf("%d", &num);
while (num != 0) {
    printf("%d\n", num);
    scanf("%d", &num);
}
```

{lang:java}
```java
import java.util.Scanner;

Scanner sc = new Scanner(System.in);
int num = sc.nextInt();
while (num != 0) {
    System.out.printf("%d\n", num);
    num = sc.nextInt();
}
```

```io
input:
5
3
0
output:
5
3
```

아래 표는 **각 반복이 끝난 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 3. 센티넬 while
lang: python,c,java
columns: 반복, num(검사 시점), 출력, num(다음 입력)
rows:
1 | 5 | 5 | 3
2 | 3 | 3 | 0
```

---

## 4) 종료 추적 포인트 (while 단원 핵심)

while 단원에서는 "언제 종료되는지"를 반드시 추적해야 합니다.

- 조건이 거짓이 되는 값을 확인합니다.
- 종료 직후 변수 값은 마지막 출력값과 다를 수 있습니다.
- 예: `i <= 3` 반복 종료 직후 `i`는 `4`입니다.

한 줄 체크: `i = 1`에서 시작해 `while i <= 3` 동안 `i += 1`이면 종료 직후 `i`는 `4`입니다.

---

## 5) 자주 틀리는 포인트

1. 갱신 누락
   `i += 1` 또는 입력 갱신이 없으면 무한 루프가 됩니다.

2. 경계값 실수
   `<`와 `<=` 차이로 반복 횟수가 달라집니다.

3. 갱신 위치 실수
   갱신이 조건 검사와 너무 멀면 추적이 어려워지고 오답이 늘어납니다.

4. 센티넬 처리 실수
   종료값(예: `0`)도 출력해버리는 실수를 자주 합니다.

---

## 5-1) 언어별 실전 팁

{lang:python} while 헤더 뒤 콜론(`:`)과 들여쓰기를 함께 확인합니다.

{lang:c} 조건은 괄호, 본문은 `{}` 블록으로 묶고 갱신문 위치를 명확히 둡니다.

{lang:java} Java도 C와 동일하게 while 조건 괄호/중괄호 블록을 사용합니다.

{lang:python,c,java} while 문제는 결과만 보지 말고 "조건값 변화"를 표로 추적해 확인합니다.

---

## 6) 미니 체크 문제

### Q1

`while`문에서 갱신(`i += 1` 등)이 없으면 어떤 문제가 생길 수 있나요?  
정답: `무한 루프 위험`

### Q2

`while` 종료를 정확히 판단하려면 무엇을 추적해야 하나요?  
정답: `조건식 값과 갱신 변수(i/num)가 언제 종료 조건을 만드는지`

### Q3 (언어별)

{lang:python} Python while문 헤더 끝에 반드시 필요한 기호는 무엇인가요?  
정답: ``:``

{lang:c} C에서 `while` 조건식을 감싸는 기호는 무엇인가요?  
정답: ``()``

{lang:java} Java에서 `while` 본문을 블록으로 묶는 기호는 무엇인가요?  
정답: ``{}``

---
## 7) 다음 학습

- 기본 문제: `py_lv08_while_b01` / `c_lv08_while_b01`
- 심화 문제: `py_lv08_while_c01` / `c_lv08_while_c01`
- 다음 개념: `nfor` 또는 `array` (반복 확장)
