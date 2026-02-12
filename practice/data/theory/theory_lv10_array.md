# 배열 핵심 이론

## 1) 배열이 하는 일

배열은 같은 타입의 값을 "순서"대로 저장하는 자료구조입니다.

- 여러 값을 변수 하나로 묶어서 관리할 수 있습니다.
- 각 값은 인덱스(index)로 접근합니다.
- 초급 단계에서는 "인덱스는 0부터 시작"한다는 규칙을 가장 먼저 고정해야 합니다.

---

## 2) 실행 흐름

배열 코드는 아래 순서로 읽으면 실수가 줄어듭니다.

1. 배열 준비(선언/생성)
2. 값 저장(초기화 또는 입력)
3. 인덱스로 접근/수정
4. 반복문으로 순회하여 출력/누적/탐색

핵심은 "**값 자체가 아니라 인덱스를 통해 접근한다**"는 점입니다.

---

## 3) 가장 자주 쓰는 패턴

### 패턴 A: 인덱스로 값 접근

{lang:python}
```python
arr = [10, 20, 30]
print("%d" % arr[0])
print("%d" % arr[2])
```

{lang:c}
```c
int arr[3] = {10, 20, 30};
printf("%d\n", arr[0]);
printf("%d\n", arr[2]);
```

{lang:java}
```java
int[] arr = {10, 20, 30};
System.out.printf("%d\n", arr[0]);
System.out.printf("%d\n", arr[2]);
```

```io
input:
(없음)
output:
10
30
```

아래 표는 **접근 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 1. 인덱스 접근
lang: python,c,java
columns: 순서, 접근 식, 꺼낸 값
rows:
1 | arr[0] | 10
2 | arr[2] | 30
```

### 패턴 B: 반복문으로 전체 순회

{lang:python}
```python
arr = [5, 7, 9]
for i in range(len(arr)):
    print("%d" % arr[i])
```

{lang:c}
```c
int arr[3] = {5, 7, 9};
for (int i = 0; i < 3; i++) {
    printf("%d\n", arr[i]);
}
```

{lang:java}
```java
int[] arr = {5, 7, 9};
for (int i = 0; i < arr.length; i++) {
    System.out.printf("%d\n", arr[i]);
}
```

```io
input:
(없음)
output:
5
7
9
```

아래 표는 **각 반복이 끝난 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 2. 배열 순회(i, arr[i])
lang: python,c,java
columns: 반복, i, arr[i], 출력
rows:
1 | 0 | 5 | 5
2 | 1 | 7 | 7
3 | 2 | 9 | 9
```

### 패턴 C: 배열 누적 합과 최댓값

{lang:python}
```python
arr = [4, 1, 8, 3]
sumv = 0
maxv = arr[0]
for i in range(len(arr)):
    sumv += arr[i]
    if arr[i] > maxv:
        maxv = arr[i]
print("%d" % sumv)
print("%d" % maxv)
```

{lang:c}
```c
int arr[4] = {4, 1, 8, 3};
int sumv = 0;
int maxv = arr[0];
for (int i = 0; i < 4; i++) {
    sumv += arr[i];
    if (arr[i] > maxv) {
        maxv = arr[i];
    }
}
printf("%d\n", sumv);
printf("%d\n", maxv);
```

{lang:java}
```java
int[] arr = {4, 1, 8, 3};
int sumv = 0;
int maxv = arr[0];
for (int i = 0; i < arr.length; i++) {
    sumv += arr[i];
    if (arr[i] > maxv) {
        maxv = arr[i];
    }
}
System.out.printf("%d\n", sumv);
System.out.printf("%d\n", maxv);
```

```io
input:
(없음)
output:
16
8
```

아래 표는 **각 반복이 끝난 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 3. sum/max 추적
lang: python,c,java
columns: 반복, i, arr[i], sumv, maxv
rows:
1 | 0 | 4 | 4 | 4
2 | 1 | 1 | 5 | 4
3 | 2 | 8 | 13 | 8
4 | 3 | 3 | 16 | 8
```

---

## 4) 인덱스 추적 포인트 (배열 단원 핵심)

배열 단원에서 가장 중요한 것은 "인덱스 범위"를 정확히 지키는 것입니다.

- 길이가 `n`이면 유효 인덱스는 `0`부터 `n-1`까지입니다.
- 마지막 인덱스는 `length-1`입니다.
- 인덱스를 한 칸 잘못 쓰면 런타임 오류 또는 잘못된 값이 나옵니다.

---

## 5) 자주 틀리는 포인트

1. 범위 밖 인덱스 접근
   예: 길이 3 배열에서 `arr[3]` 접근은 오류입니다.

2. 길이와 마지막 인덱스 혼동
   길이 5 배열의 마지막 인덱스는 4입니다.

3. 반복 범위 실수
   `i <= len(arr)`처럼 쓰면 마지막에서 한 번 더 돌아 오류가 날 수 있습니다.

4. max 초기값 실수
   `maxv = 0`으로 고정하면 음수 배열에서 오답이 될 수 있습니다.

5. sum/max 초기화 위치 실수
   초기화를 반복문 안에 두면 매번 리셋되어 누적이 깨집니다.

---

## 5-1) 언어별 실전 팁

{lang:python} 배열 길이는 `len(arr)`로 구하고, 순회는 `range(len(arr))`를 기본으로 익힙니다.

{lang:c} 배열 길이는 선언 시 정한 크기를 기준으로 루프 범위를 직접 관리해야 합니다.

{lang:java} 배열 길이는 `arr.length`로 구하며, `i < arr.length`를 기본 루프 조건으로 사용합니다.

{lang:python,c,java} 배열 문제는 값만 보지 말고 `i`와 `arr[i]`를 같이 표로 추적하면 정확도가 크게 올라갑니다.

---

## 6) 미니 체크 문제

### Q1

길이가 4인 배열의 마지막 인덱스는 무엇인가요?  
정답: `3`

### Q2

배열 순회에서 인덱스 범위를 벗어나지 않으려면 무엇을 먼저 확인해야 하나요?  
정답: `배열 길이와 루프 조건`

### Q3 (언어별)

{lang:python} Python에서 배열 길이를 구하는 함수는 무엇인가요?  
정답: ``len(arr)``

{lang:c} C에서 길이 5 배열의 마지막 유효 인덱스는 무엇인가요?  
정답: ``4``

{lang:java} Java에서 배열 길이를 나타내는 속성은 무엇인가요?  
정답: ``arr.length``

---
## 7) 다음 학습

- 기본 문제: `py_lv10_array_b01` / `c_lv10_array_b01` / `java_lv10_array_b01`
- 심화 문제: `py_lv10_array_c01` / `c_lv10_array_c01` / `java_lv10_array_c01`
- 다음 개념: `array2d` (행/열 구조로 확장)

