---
id: "py_lv07_for"
contentType: "lesson"
track: "language"
lang: "python"
categoryId: "py_for"
title: "Python Lv7 for문"
status: "active"
order: 207
audience: "common"
tags: [for, loop, range]
recommendedSetId: "py_lv07_for_b01"
relatedSetIds: ["py_lv07_for_b01"]
prerequisites: ["py_lv06_if"]
nextConcepts: ["py_lv08_while"]
priority: 3
---

# for문 핵심 이론

> [!goal]
> 오늘의 목표
> - `for` 반복문의 기본 흐름을 이해한다.
> - `range`의 경계를 실수 없이 읽는다.
> - 누적 패턴과 입력 반복 패턴을 구분한다.

## 1) for문이 하는 일

`for`는 **반복 횟수가 대체로 정해져 있을 때** 가장 먼저 쓰는 반복문입니다.

- 같은 작업을 여러 번 실행한다.
- 반복마다 바뀌는 값(인덱스, 누적합, 개수)을 다룬다.
- 이후 배열/리스트 순회로 확장할 때도 같은 반복 원리가 사용된다.

---

## 2) 실행 흐름

for문을 읽을 때는 아래 4단계를 고정으로 보세요.

1. 초기화
2. 조건 확인
3. 본문 실행
4. 증감(다음 반복 준비)

핵심은 "**조건이 참일 때만 본문이 실행된다**"는 점입니다.

![for 실행 흐름도](./data/theory/images/for_flow.svg)

---

## 3) 가장 자주 쓰는 패턴

### 패턴 A: 0부터 n-1까지 반복

`range(n)`은 0부터 `n-1`까지 정확히 `n`번 반복하는 기본 형태입니다.
반복 횟수와 각 반복에서의 `i` 값을 함께 추적하는 연습에 적합합니다.

```python
for i in range(n):
    print(i)
```

```c
for (int i = 0; i < n; i++) {
    printf("%d\n", i);
}
```

```java
for (int i = 0; i < n; i++) {
    System.out.println(i);
}
```

![range 경계 시각화](./data/theory/images/for_range_boundary.svg)

```io
input:
3
output:
0
1
2
```

```tracegrid
title: Trace 1. 기본 반복 흐름 (range(3))
lang: python,c,java
columns: 반복, i, output
rows:
1 | 0 | 0
2 | 1 | 1
3 | 2 | 2
```

### 패턴 B: 1부터 n까지 반복

```python
for i in range(1, n + 1):
    print(i)
```

```c
for (int i = 1; i <= n; i++) {
    printf("%d\n", i);
}
```

```java
for (int i = 1; i <= n; i++) {
    System.out.println(i);
}
```

```io
input:
4
output:
1
2
3
4
```

```tracegrid
title: Trace 2. 1부터 n까지 반복
lang: python,c,java
columns: 반복, i, output
rows:
1 | 1 | 1
2 | 2 | 2
3 | 3 | 3
4 | 4 | 4
```

## 4) 누적 패턴 (sum / count)

### 합계(sum)

```python
sumv = 0
for i in range(1, n + 1):
    sumv += i
```

```tracegrid
title: Trace 3. sum 누적
lang: python,c,java
columns: 반복, i, sum
rows:
1 | 1 | 1
2 | 2 | 3
3 | 3 | 6
4 | 4 | 10
```

> [!key]
> 핵심 개념
> `sumv`, `cnt` 같은 누적 변수는 반복문 밖에서 한 번만 초기화해야 합니다.

## 5) 자주 틀리는 포인트

1. `< n`과 `<= n`의 차이
2. 증가/감소 방향과 조건의 불일치
3. 종료 직후 반복 변수 값 착각
4. 입력 위치 실수

## 6) 언어별 실전 팁

{lang:python} `range(start, end)`에서 `end`는 포함되지 않습니다. `1..n`은 `range(1, n+1)`로 씁니다.

{lang:c} `for` 헤더의 세미콜론 2개를 꼭 확인하세요: `for (초기화; 조건; 증감)`.

{lang:java} Java도 C와 동일하게 `for (초기화; 조건; 증감)` 문법이며, 출력은 `System.out.println(...)`를 사용합니다.

{lang:python,c,java} 누적 변수(`sum`, `count`) 초기화는 반드시 반복문 **밖**에서 시작합니다.

## 7) 다음 학습

- 기본 문제: `py_lv07_for_b01`
- 다음 개념: `while`
