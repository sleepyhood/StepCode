# for문 핵심 이론

## 1) for문이 하는 일

`for`는 **반복 횟수가 대체로 정해져 있을 때** 가장 먼저 쓰는 반복문입니다.

- 같은 작업을 여러 번 실행한다.
- 반복마다 바뀌는 값(인덱스, 누적합, 개수)을 다룬다.
- 배열/리스트 순회와 궁합이 좋다.

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

### 패턴 C: 감소 반복

```python
for i in range(5, 0, -1):
    print(i)
```

```c
for (int i = 5; i > 0; i--) {
    printf("%d\n", i);
}
```

```java
for (int i = 5; i > 0; i--) {
    System.out.println(i);
}
```

```io
input:
(없음)
output:
5
4
3
2
1
```

```tracegrid
title: Trace 3. 감소 반복
lang: python,c,java
columns: 반복, i, output
rows:
1 | 5 | 5
2 | 4 | 4
3 | 3 | 3
4 | 2 | 2
5 | 1 | 1
```

---

## 4) 누적 패턴 (sum / count)

### 합계(sum)

```python
sumv = 0
for i in range(1, n + 1):
    sumv += i
```

```c
int sumv = 0;
for (int i = 1; i <= n; i++) {
    sumv += i;
}
printf("%d\n", sumv);
```

![sum 누적 변화 표](./data/theory/images/for_accumulate_sum.svg)

```io
input:
4
output:
10
```

```tracegrid
title: Trace 4. sum 누적
lang: python,c,java
columns: 반복, i, sum
rows:
1 | 1 | 1
2 | 2 | 3
3 | 3 | 6
4 | 4 | 10
```

### 개수(count)

```python
cnt = 0
for i in range(1, n + 1):
    if i % 2 == 0:
        cnt += 1
```

```c
int cnt = 0;
for (int i = 1; i <= n; i++) {
    if (i % 2 == 0) {
        cnt += 1;
    }
}
printf("%d\n", cnt);
```

```io
input:
6
output:
3
```

```tracegrid
title: Trace 5. 짝수 개수 누적
lang: python,c,java
columns: 반복, i, i%2==0, cnt
rows:
1 | 1 | false | 0
2 | 2 | true  | 1
3 | 3 | false | 1
4 | 4 | true  | 2
5 | 5 | false | 2
6 | 6 | true  | 3
```

포인트:

- `sumv`, `cnt`의 **초기화 위치는 반복문 밖**이어야 합니다.
- 초기화를 반복문 안에 두면 값이 매번 리셋됩니다.

---

## 5) 자주 틀리는 포인트

1. 경계 실수  
   `< n`과 `<= n`은 반복 횟수가 1회 차이납니다.

2. step 방향 실수  
   증가해야 하는데 감소 step을 쓰거나, 그 반대.

3. 종료 직후 값 착각  
   반복이 끝난 직후의 `i`는 마지막 출력값과 다를 수 있습니다.

4. 입력 위치 실수  
   `n`번 입력 받아야 하는데 루프 밖에서 한 번만 입력받는 경우.

---

## 5-1) 언어별 실전 팁

{lang:python} `range(start, end)`에서 `end`는 포함되지 않습니다. `1..n`은 `range(1, n+1)`로 씁니다.

{lang:c} `for` 헤더의 세미콜론 2개를 꼭 확인하세요: `for (초기화; 조건; 증감)`.

{lang:java} Java도 C와 동일하게 `for (초기화; 조건; 증감)` 문법이며, 출력은 `System.out.println(...)`를 사용합니다.

{lang:python,c,java} 누적 변수(`sum`, `count`) 초기화는 반드시 반복문 **밖**에서 시작합니다.

---

## 6) 미니 체크 문제

### Q1

`for i in range(2, 7):`에서 `i`는 몇 번 반복되나요?  
정답: `5번` (2, 3, 4, 5, 6)

### Q2

`for (int i = 1; i <= 3; i++)`의 출력값은?  
정답: `1 2 3`

### Q3

`for i in range(5, 0, 1)` 본문은 몇 번 실행되나요?  
정답: `0번` (증가 step인데 시작이 끝보다 큼)

---

## 7) 다음 학습

- 기본 문제: `py_lv07_for_b01` / `c_lv07_for_b01`
- 심화 문제: `py_lv07_for_c01` / `c_lv07_for_c01`
- 다음 개념: `while` (반복 횟수가 정해지지 않은 경우)
