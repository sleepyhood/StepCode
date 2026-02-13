# for문 핵심 이론

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

아래 표는 **각 반복이 끝난 직후 상태**를 기록한 것입니다.

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

시작값을 1로 두고 끝값 `n`을 포함하는 패턴입니다.
`<`와 `<=`(또는 `range`의 끝값 처리) 차이로 반복 횟수가 달라지는 점을 확인하세요.

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

증가가 아니라 감소 방향으로 반복할 때 쓰는 형태입니다.
step(증감식) 방향이 조건과 맞지 않으면 본문이 0번 실행될 수 있다는 점이 핵심입니다.

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

반복마다 값을 더해 누적 합을 만드는 가장 기본적인 누적 패턴입니다.
`sumv` 초기화는 반복문 밖에서 한 번만 해야 합니다.

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

```java
int sumv = 0;
for (int i = 1; i <= n; i++) {
    sumv += i;
}
System.out.println(sumv);
```


```io
input:
4
output:
10
```

아래 표는 **각 반복이 끝난 직후 상태**를 기록한 것입니다.

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

조건을 만족한 횟수만 세는 패턴입니다.
조건문(`if`)이 참일 때만 `cnt`를 갱신한다는 흐름을 추적하세요.

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

```java
int cnt = 0;
for (int i = 1; i <= n; i++) {
    if (i % 2 == 0) {
        cnt += 1;
    }
}
System.out.println(cnt);
```

```io
input:
6
output:
3
```

아래 표는 **각 반복이 끝난 직후 상태**를 기록한 것입니다.

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

### n개 입력 처리 (입력값 + 누적)

반복 인덱스(`i`)와 실제 입력값(`num`)을 함께 다루는 실전 패턴입니다.
`i`는 순서 추적용, `num`은 계산 대상이라는 역할 구분이 중요합니다.

```python
n = int(input())
sumv = 0
for i in range(n):
    num = int(input())
    sumv += num
print("%d" % sumv)
```

```c
int n, num;
int sumv = 0;
scanf("%d", &n);
for (int i = 0; i < n; i++) {
    scanf("%d", &num);
    sumv += num;
}
printf("%d\n", sumv);
```

```java
int n = sc.nextInt();
int sumv = 0;
for (int i = 0; i < n; i++) {
    int num = sc.nextInt();
    sumv += num;
}
System.out.printf("%d\n", sumv);
```

```io
input:
3
4
1
5
output:
10
```

아래 표는 **각 반복이 끝난 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 6. n개 입력 합계
lang: python,c,java
columns: 반복, i, 입력값 num, sumv
rows:
1 | 0 | 4 | 4
2 | 1 | 1 | 5
3 | 2 | 5 | 10
```

### 최대값/최소값 구하기

여러 입력 중 최댓값/최솟값을 동시에 추적하는 패턴입니다.
입력값 `num`이 `-1000` 이상 `1000` 이하라고 가정하고, 초기값을 경계 밖으로 둡니다.
즉, `maxv = -1001`은 어떤 입력값보다 작고 `minv = 1001`은 어떤 입력값보다 큽니다.
그래서 첫 입력부터 `maxv/minv`가 반드시 갱신되어 안정적으로 시작할 수 있습니다.
반대로 입력 범위를 모를 때는 첫 입력값으로 `maxv/minv`를 초기화하는 방법이 더 안전합니다.

```python
n = int(input())
maxv = -1001
minv = 1001
for i in range(n):
    num = int(input())
    if num > maxv:
        maxv = num
    if num < minv:
        minv = num
print("%d %d" % (maxv, minv))
```

```c
int n, num, maxv, minv;
scanf("%d", &n);
maxv = -1001;
minv = 1001;
for (int i = 0; i < n; i++) {
    scanf("%d", &num);
    if (num > maxv) maxv = num;
    if (num < minv) minv = num;
}
printf("%d %d\n", maxv, minv);
```

```java
int n = sc.nextInt();
int maxv = -1001;
int minv = 1001;
for (int i = 0; i < n; i++) {
    int num = sc.nextInt();
    if (num > maxv) maxv = num;
    if (num < minv) minv = num;
}
System.out.printf("%d %d\n", maxv, minv);
```

```io
input:
4
3
9
1
7
output:
9 1
```

아래 표는 **각 반복이 끝난 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 7. max/min 추적
lang: python,c,java
columns: 반복, i, 입력값 num, maxv, minv
rows:
초기 | - | - | -1001 | 1001
1 | 0 | 3 | 3 | 3
2 | 1 | 9 | 9 | 3
3 | 2 | 1 | 9 | 1
4 | 3 | 7 | 9 | 1
```

포인트:

- `sumv`, `cnt`의 **초기화 위치는 반복문 밖**이어야 합니다.
- 초기화를 반복문 안에 두면 값이 매번 리셋됩니다.
- 입력 반복에서는 `i`(반복 인덱스)와 `num`(입력값)을 분리해서 추적해야 합니다.
- 입력 범위가 주어지면 max/min 초기값을 경계 밖 값으로 두는 방식도 안정적으로 동작합니다.

---

## 5) 자주 틀리는 포인트

1. 경계 실수  
   `< n`과 `<= n`은 반복 횟수가 1회 차이납니다.

2. step 방향 실수  
   증가해야 하는데 감소 step을 쓰거나, 그 반대.

3. 종료 직후 값 착각  
   반복이 끝난 직후의 `i`는 마지막 출력값과 다를 수 있습니다.
   예: `for (int i = 1; i <= 3; i++)`는 출력이 `1 2 3`이어도 종료 직후 `i`는 `4`입니다.

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

`for` 반복에서 종료 직후 반복 변수 값이 마지막 출력값과 다를 수 있나요?  
정답: `네, 다를 수 있습니다.`

### Q2

`n`개 입력 처리에서 `i`와 `num`을 분리해서 추적해야 하는 이유는 무엇인가요?  
정답: ``i``는 반복 횟수, ``num``은 입력 데이터이기 때문

### Q3 (언어별)

{lang:python} Python에서 `1..n` 반복을 만드는 기본 형태는 무엇인가요?  
정답: ``for i in range(1, n + 1):``

{lang:c} C에서 `0..n-1` 반복을 만드는 for 헤더는 무엇인가요?  
정답: ``for (int i = 0; i < n; i++)``

{lang:java} Java에서 `for` 문의 구조를 순서대로 쓰면 무엇인가요?  
정답: ``for (초기화; 조건; 증감)``

---
## 7) 다음 학습

- 기본 문제: `py_lv07_for_b01` / `c_lv07_for_b01`
- 심화 문제: `py_lv07_for_c01` / `c_lv07_for_c01`
- 다음 개념: `while` (반복 횟수가 정해지지 않은 경우)

