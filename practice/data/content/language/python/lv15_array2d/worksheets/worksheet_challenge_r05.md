---
id: "py_lv15_array2d_challenge_r05"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_array2d"
title: "Python 2차원 배열 LV15 챌린지 2회차"
round: 5
difficulty: "challenge"
status: "active"
audience: "common"
printDefault: true
---
# Python 2차원 배열 LV15 챌린지 2회차

### Q1. MCQ 1. 2차원 누적합 점화식

다음 중 1-indexed 2차원 누적합 ps의 점화식으로 올바른 것은 무엇인가요?

- **A**: ps[i][j] = a[i][j] + ps[i-1][j-1]
- **B**: ps[i][j] = a[i][j] + ps[i-1][j] + ps[i][j-1] + ps[i-1][j-1]
- **C**: ps[i][j] = a[i][j] + ps[i-1][j] + ps[i][j-1] - ps[i-1][j-1]
- **D**: ps[i][j] = ps[i-1][j] - ps[i][j-1] + a[i][j]

---

### Q2. Code 1. ps 채우기(한 줄)

아래 코드에서 주석 위치에 들어갈 **한 줄**을 작성하세요.
(1-indexed 2차원 누적합 ps를 계산)

```c
R, C = 3, 4
a = [[0] * (C + 1) for _ in range(R + 1)]
# (a에 값이 채워져 있다고 가정)
ps = [[0] * (C + 1) for _ in range(R + 1)]

for i in range(1, R + 1):
    for j in range(1, C + 1):
        # TODO: ps[i][j]를 계산하는 한 줄
```

---

### Q3. Short 1. 구간합 공식

누적합 ps를 이용한 구간합 공식(직사각형 합)을 그대로 쓰세요.

---

### Q4. MCQ 2. 구간합 인덱스 실수

2차원 누적합/구간합에서 흔한 실수로 올바른 설명을 고르세요.

- **A**: ps 배열을 (R+1)x(C+1)로 만들지 않는다
- **B**: ps를 만들 때 i와 j를 0부터 시작한다
- **C**: 구간합에서 r1-1 또는 c1-1을 사용하는 것을 빼먹는다
- **D**: 위 모두가 흔한 실수다

---

### Q5. Code 2. 구간합 한 줄

아래 코드에서 주석 위치에 들어갈 **한 줄**을 작성하세요.
(누적합 ps를 이용해 구간합을 s에 저장)

```c
r1, c1, r2, c2 = 2, 2, 3, 4
s = 0
# TODO: ps로 구간합 계산
print('%d' % s)
```

---

### Q6. MCQ 3. k×k 부분합 반복 범위

1-indexed ps를 사용해 k×k 부분합을 검사할 때, i, j 반복 범위로 가장 적절한 것은 무엇인가요?

- **A**: i: 0..R-1, j: 0..C-1
- **B**: i: k..R, j: k..C (1-indexed 기준)
- **C**: i: 1..R-k+1, j: 1..C-k+1
- **D**: i: 1..R, j: 1..C

---

### Q7. Code 3. k×k 부분합 최댓값

아래 코드에서 주석 위치에 들어갈 **한 줄**을 작성하세요.
(1-indexed ps를 이용해 k×k 구간합의 최댓값을 best에 갱신)

```c
# ps는 (R+1)×(C+1)이며 1-indexed로 채워져 있다고 가정
R, C = 3, 3
k = 2
best = -10**18

for i in range(k, R + 1):
    for j in range(k, C + 1):
        # TODO: (i-k+1, j-k+1) ~ (i, j) 구간합으로 best 갱신
print('%d' % best)
```

---

### Q8. Short 2. k×k 최댓값(예시)

아래 배열에서 k=2일 때 2×2 부분합의 최댓값은 얼마인가요?

```
1 2 3
4 5 6
7 8 9
```

---

### Q9. Code 4. 다중 질의 처리(한 줄)

여러 개의 구간합 질의를 처리하려고 합니다.
아래 코드에서 주석 위치에 들어갈 **출력 한 줄**을 작성하세요.
(질의마다 구간합 s를 계산해 출력)

```c
# Q, ps는 이미 준비되어 있다고 가정
for _ in range(Q):
    r1, c1, r2, c2 = map(int, input().split())
    s = ps[r2][c2] - ps[r1-1][c2] - ps[r2][c1-1] + ps[r1-1][c1-1]
    # TODO: s 출력
```

---
