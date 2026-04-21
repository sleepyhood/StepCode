---
id: "py_lv15_array2d"
contentType: "lesson"
track: "language"
lang: "python"
categoryId: "py_array2d"
title: "Python Lv15 2차원 배열"
status: "active"
order: 215
audience: "common"
recommendedSetId: "py_lv15_array2d_b01"
relatedSetIds: ["py_lv15_array2d_b01", "py_lv15_array2d_b02", "py_lv15_array2d_b03", "py_lv15_array2d_c01", "py_lv15_array2d_c02"]
prerequisites: ["py_lv10_array"]
nextConcepts: []
priority: 3
---
# 2차원 배열 핵심 이론

## 1) 2차원 배열이 하는 일

2차원 배열은 값을 "행(row)"과 "열(column)" 구조로 저장합니다.

- 1차원 배열이 한 줄이라면, 2차원 배열은 표(격자) 형태입니다.
- 값 하나를 꺼낼 때는 인덱스 두 개가 필요합니다. (`arr[r][c]`)
- 초급 단계에서는 "첫 번째 인덱스=행, 두 번째 인덱스=열" 규칙을 고정하는 것이 핵심입니다.

---

## 2) 실행 흐름

2차원 배열 코드는 아래 순서로 읽으면 실수가 줄어듭니다.

1. 배열 준비(행/열 구조 확인)
2. `arr[r][c]`로 특정 칸 접근
3. 중첩 반복문으로 전체 순회
4. 누적/탐색(합, 최댓값 등) 처리

핵심은 "**행 인덱스와 열 인덱스를 분리해서 추적해야 한다**"는 점입니다.

---

## 3) 가장 자주 쓰는 패턴

### 패턴 A: 특정 위치 값 접근

{lang:python}
```python
a = [[1, 2], [3, 4]]
print("%d" % a[1][0])
print("%d" % a[0][1])
```

{lang:c}
```c
int a[2][2] = {{1, 2}, {3, 4}};
printf("%d\n", a[1][0]);
printf("%d\n", a[0][1]);
```

{lang:java}
```java
int[][] a = {{1, 2}, {3, 4}};
System.out.printf("%d\n", a[1][0]);
System.out.printf("%d\n", a[0][1]);
```

```io
input:
(없음)
output:
3
2
```

아래 표는 **접근 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 1. arr[r][c] 접근
lang: python,c,java
columns: 순서, r, c, 값
rows:
1 | 1 | 0 | 3
2 | 0 | 1 | 2
```

### 패턴 B: 전체 순회 (행 우선)

{lang:python}
```python
a = [[1, 2], [3, 4]]
for r in range(2):
    for c in range(2):
        print("%d" % a[r][c])
```

{lang:c}
```c
int a[2][2] = {{1, 2}, {3, 4}};
for (int r = 0; r < 2; r++) {
    for (int c = 0; c < 2; c++) {
        printf("%d\n", a[r][c]);
    }
}
```

{lang:java}
```java
int[][] a = {{1, 2}, {3, 4}};
for (int r = 0; r < 2; r++) {
    for (int c = 0; c < 2; c++) {
        System.out.printf("%d\n", a[r][c]);
    }
}
```

```io
input:
(없음)
output:
1
2
3
4
```

아래 표는 **각 출력 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 2. 2x2 순회 순서
lang: python,c,java
columns: 순서, r, c, a[r][c]
rows:
1 | 0 | 0 | 1
2 | 0 | 1 | 2
3 | 1 | 0 | 3
4 | 1 | 1 | 4
```

### 패턴 C: 합계/최댓값 추적

{lang:python}
```python
a = [[1, 5], [3, 2]]
sumv = 0
maxv = a[0][0]
for r in range(2):
    for c in range(2):
        sumv += a[r][c]
        if a[r][c] > maxv:
            maxv = a[r][c]
print("%d" % sumv)
print("%d" % maxv)
```

{lang:c}
```c
int a[2][2] = {{1, 5}, {3, 2}};
int sumv = 0;
int maxv = a[0][0];
for (int r = 0; r < 2; r++) {
    for (int c = 0; c < 2; c++) {
        sumv += a[r][c];
        if (a[r][c] > maxv) {
            maxv = a[r][c];
        }
    }
}
printf("%d\n", sumv);
printf("%d\n", maxv);
```

{lang:java}
```java
int[][] a = {{1, 5}, {3, 2}};
int sumv = 0;
int maxv = a[0][0];
for (int r = 0; r < 2; r++) {
    for (int c = 0; c < 2; c++) {
        sumv += a[r][c];
        if (a[r][c] > maxv) {
            maxv = a[r][c];
        }
    }
}
System.out.printf("%d\n", sumv);
System.out.printf("%d\n", maxv);
```

```io
input:
(없음)
output:
11
5
```

아래 표는 **각 칸 처리 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 3. sum/max 추적
lang: python,c,java
columns: 순서, r, c, 값, sumv, maxv
rows:
1 | 0 | 0 | 1 | 1 | 1
2 | 0 | 1 | 5 | 6 | 5
3 | 1 | 0 | 3 | 9 | 5
4 | 1 | 1 | 2 | 11 | 5
```

---

## 4) 행/열 인덱스 추적 포인트 (2차원 배열 단원 핵심)

2차원 배열 단원에서는 "행 길이"와 "열 길이"를 분리해서 생각해야 합니다.

- `arr[r][c]`에서 `r`은 행 번호, `c`는 열 번호입니다.
- 행 수와 열 수가 다를 수 있으므로 루프 범위를 각각 확인합니다.
- 특히 인덱스 범위를 넘지 않도록 `r`/`c`를 따로 추적해야 합니다.

---

## 5) 자주 틀리는 포인트

1. 행/열 인덱스 뒤바꿈
   `arr[c][r]`처럼 바꿔 쓰면 다른 값을 읽게 됩니다.

2. 루프 범위 실수
   행 루프/열 루프에 같은 길이를 넣어 범위를 넘는 경우가 많습니다.

3. max 초기값 실수
   `maxv = 0` 고정은 음수 데이터에서 오답이 될 수 있습니다.

4. 누적 변수 초기화 위치 실수
   `sumv`를 반복문 안에서 초기화하면 누적이 깨집니다.

5. 줄 단위 출력 위치 실수
   표 모양 출력 시 줄바꿈 위치가 안쪽/바깥쪽 루프에 따라 달라집니다.

---

## 5-1) 언어별 실전 팁

{lang:python} 2차원 리스트 순회는 `for r in range(len(a))`, `for c in range(len(a[r]))` 형태로 길이를 분리해 쓰는 습관이 안전합니다.

{lang:c} 선언 시 행/열 크기를 명확히 두고, 루프 조건도 같은 크기로 맞춥니다.

{lang:java} `a.length`는 행 개수, `a[r].length`는 해당 행의 열 개수입니다.

{lang:python,c,java} 2차원 배열 문제는 `r, c, a[r][c]` 3개를 표로 같이 적어 추적하면 정확도가 크게 올라갑니다.

---

## 6) 미니 체크 문제

### Q1

`arr[r][c]`에서 첫 번째 인덱스와 두 번째 인덱스는 각각 무엇을 의미하나요?  
정답: `첫 번째는 행, 두 번째는 열`

### Q2

2행 3열 배열의 유효 열 인덱스 범위는 무엇인가요?  
정답: `0~2`

### Q3 (언어별)

{lang:python} Python에서 2차원 리스트의 열 길이를 현재 행 기준으로 구할 때 무엇을 쓰나요?  
정답: ``len(a[r])``

{lang:c} C에서 `int a[2][3]` 선언일 때 행 반복 범위는 무엇인가요?  
정답: ``r = 0..1``

{lang:java} Java에서 전체 행 개수와 r행 열 개수를 구하는 속성은 각각 무엇인가요?  
정답: ``a.length``, ``a[r].length``

---
## 7) 다음 학습

- 기본 문제: `py_lv15_array2d_b01` / `java_lv15_array2d_b01`
- 심화 문제: `py_lv15_array2d_c01` / `java_lv15_array2d_c01`
- 다음 개념: 2차원 배열 응용(탐색/변환/좌표 문제)
