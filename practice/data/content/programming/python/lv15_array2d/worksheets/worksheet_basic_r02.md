---
id: "py_lv15_array2d_basic_r02"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_array2d"
title: "Python 2차원 배열 LV15 기초 2회차"
round: 2
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python 2차원 배열 LV15 기초 2회차

### Q1. MCQ 1. 입력 저장 위치

다음 중 `input()`으로 입력받은 값을 2차원 배열에 저장하는 올바른 한 줄을 고르세요.
(중첩 반복문 안에서 i, j가 유효하다고 가정)

- **A**: x = int(input())
- **B**: a[i] = int(input())
- **C**: a[i][j] = int(input())
- **D**: a[j][i] = int(input())

---

### Q2. Code 1. R×C 배열 입력 받기

아래 코드에서 주석 위치에 들어갈 **입력 한 줄**을 작성하세요.
(R행 C열의 모든 값을 입력 받아 `a`에 저장해야 합니다.)

```c
R, C = map(int, input().split())
a = [[0] * C for _ in range(R)]

for i in range(R):
    for j in range(C):
        # TODO: 입력을 받아 a[i][j]에 저장
```

---

### Q3. Short 1. 행 합 출력

아래 코드가 출력하는 내용을 그대로 쓰세요. (줄바꿈 포함)

```c
a = [
    [1, 2, 3],
    [4, 5, 6]
]
for i in range(len(a)):
    s = 0
    for j in range(len(a[0])):
        s += a[i][j]
    print('%d' % s)
```

---

### Q4. MCQ 2. 평균의 나눗셈

다음 중 전체 평균을 **실수**로 올바르게 계산하는 코드를 고르세요. (`sum_`은 정수)

- **A**: avg = sum_ // (R * C)
- **B**: avg = float(sum_ // (R * C))
- **C**: avg = sum_ / (R * C)
- **D**: avg = sum_ / float(R) * C

---

### Q5. Code 2. 최댓값과 좌표 찾기

아래 코드에서 주석 위치에 들어갈 **한 줄**을 작성하세요.
`max_v`와 그 위치 `(mr, mc)`를 갱신해야 합니다. (동점이면 먼저 나온 좌표 유지)

```c
a = [
    [3, 9, 1],
    [8, 9, 2]
]
max_v = a[0][0]
mr, mc = 0, 0

for i in range(len(a)):
    for j in range(len(a[0])):
        if a[i][j] > max_v:
            # TODO: max_v와 mr, mc 갱신
print('%d %d %d' % (max_v, mr, mc))
```

---

### Q6. Short 2. 최댓값 동점 처리

아래 코드는 최댓값의 좌표를 찾습니다. 출력 결과를 쓰세요. (한 줄)
(동점이면 더 먼저 나온 좌표를 유지합니다.)

```c
a = [
    [5, 7],
    [7, 1]
]
max_v = a[0][0]
mr, mc = 0, 0
for i in range(len(a)):
    for j in range(len(a[0])):
        if a[i][j] > max_v:
            max_v, mr, mc = a[i][j], i, j
print('%d %d' % (mr, mc))
```

---

### Q7. MCQ 3. 열 합 구하기 반복문

다음 중 각 열의 합을 구해 한 줄씩 출력하는 코드로 올바른 것은 무엇인가요?

- **A**: for i in range(R):     s = 0     for j in range(C):         s += a[i][j]     print('%d' % s)  # 행 합
- **B**: for j in range(C):     s = 0     for i in range(R):         s += a[i][j]     print('%d' % s)  # 열 합
- **C**: for i in range(R):     for j in range(C):         print('%d' % a[i][j])  # 원소 출력
- **D**: for j in range(R):     s = 0     for i in range(C):         s += a[i][j]     print('%d' % s)  # 잘못된 범위

---

### Q8. Code 3. 특정 값 개수(열 기준)

아래 코드에서 주석 위치에 들어갈 **한 줄**을 작성하세요.
(각 열에서 **짝수의 개수**를 세어 `evenCnt`에 저장합니다.)

```c
a = [
    [2, 3, 4],
    [6, 7, 8]
]
C = len(a[0])

for j in range(C):
    evenCnt = 0
    for i in range(len(a)):
        # TODO: a[i][j]가 짝수면 evenCnt 증가
    print('%d' % evenCnt)
```

---

### Q9. MCQ 4. 최댓값 tie-break(행/열 작은 순)

다음 중 최댓값을 찾되, **동점이면 (행이 작은 것 → 열이 작은 것)**을 선택하는 조건으로 올바른 것은 무엇인가요?

- **A**: (a[i][j] >= max_v) and (i <= mr) and (j <= mc)
- **B**: a[i][j] > max_v or (a[i][j] == max_v and (i < mr or (i == mr and j < mc)))
- **C**: a[i][j] > max_v and (i < mr or j < mc)
- **D**: a[i][j] == max_v and i < mr and j < mc

---
