---
id: "py_lv15_array2d_challenge_r04"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_array2d"
title: "Python 2차원 배열 LV15 챌린지 1회차"
round: 4
difficulty: "challenge"
status: "active"
audience: "common"
printDefault: true
---
# Python 2차원 배열 LV15 챌린지 1회차

### Q1. MCQ 1. 열 길이 버그 찾기

다음 중 2차원 배열을 순회할 때 발생하기 쉬운 버그 설명으로 가장 적절한 것은 무엇인가요?

- **A**: 행 반복이 필요 없는데 하고 있다
- **B**: 열 반복에서 `len(a)`를 사용해 열 길이가 아닌 행 길이를 사용했다
- **C**: sum_ 초기화가 잘못됐다
- **D**: i와 j를 바꿔야 한다

---

### Q2. Code 1. 경계 조건 고치기

아래 코드에서 주석 위치에 들어갈 **for문 한 줄**을 작성하세요.
(예외가 나지 않도록 고쳐야 합니다.)

```c
a = [[0] * 4 for _ in range(3)]
cnt = 0
# TODO: 예외가 나지 않도록 for문 한 줄을 작성하세요.
# (잘못된 예) for i in range(len(a) + 1):
    cnt += 1
print('%d' % cnt)
```

---

### Q3. Short 1. 발생하는 예외

아래 코드에서 발생하는 예외의 이름을 쓰세요.

```c
a = [[0] * 2 for _ in range(2)]
print('%d' % a[2][0])
```

---

### Q4. MCQ 2. 최댓값 tie-break(나중 좌표)

다음 중 최댓값을 찾되, **동점이면 더 나중 좌표(행 큰 것 → 열 큰 것)**를 선택하는 조건으로 올바른 것은 무엇인가요?

- **A**: a[i][j] > max_v
- **B**: a[i][j] >= max_v
- **C**: a[i][j] > max_v or (a[i][j] == max_v and (i > mr or (i == mr and j > mc)))
- **D**: a[i][j] >= max_v and i >= mr and j >= mc

---

### Q5. Code 2. 최댓값 갱신 + tie-break(한 줄)

아래 코드에서 주석 위치에 들어갈 **한 줄**을 작성하세요.
조건이 참일 때 `max_v`, `mr`, `mc`를 갱신해야 합니다. (동점이면 더 나중 좌표 선택)

```c
a = [
    [5, 7],
    [7, 1]
]
max_v = a[0][0]
mr, mc = 0, 0
for i in range(len(a)):
    for j in range(len(a[0])):
        if a[i][j] > max_v or (a[i][j] == max_v and (i > mr or (i == mr and j > mc))):
            # TODO: max_v, mr, mc 갱신
print('%d %d %d' % (max_v, mr, mc))
```

---

### Q6. MCQ 3. 2×2 블록 합 반복 범위

R×C 배열에서 2×2 블록 합을 모두 검사하려면 (0-index 기준) i, j 반복 범위는 무엇이 적절한가요?

- **A**: i: 0..R-1, j: 0..C-1
- **B**: i: 0..R-2, j: 0..C-2
- **C**: i: 1..R-1, j: 1..C-1
- **D**: i: 0..R, j: 0..C

---

### Q7. Code 3. 2×2 블록 합의 최댓값

아래 코드에서 주석 위치에 들어갈 **한 줄**을 작성하세요.
(각 2×2 블록 합을 계산해 best를 갱신합니다.)

```c
a = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
R, C = len(a), len(a[0])
best = -10**18

for i in range(R - 1):
    for j in range(C - 1):
        # TODO: 2×2 합으로 best 갱신
print('%d' % best)
```

---

### Q8. Short 2. 2×2 최댓값 결과

아래 2차원 배열에서 2×2 블록 합의 최댓값은 얼마인가요?

```
1 2 3
4 5 6
7 8 9
```

---

### Q9. Code 4. 대칭 행렬 판별(정사각형)

아래 코드에서 주석 위치에 들어갈 **한 줄**을 작성하세요.
(대칭 조건을 위반하면 ok를 False로 바꿉니다.)

```c
a = [
    [1, 2, 3],
    [2, 4, 5],
    [3, 5, 6]
]
ok = True
for i in range(len(a)):
    for j in range(i + 1, len(a)):
        # TODO: 대칭 조건 위반이면 ok를 False로
print('%s' % ok)
```

---
