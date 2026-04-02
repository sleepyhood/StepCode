---
id: "py_lv10_array_challenge_r05"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_array"
title: "Python 배열 Lv10 챌린지 2회차"
round: 5
difficulty: "challenge"
status: "active"
audience: "common"
printDefault: true
---
# Python 배열 Lv10 챌린지 2회차

### Q1. Trace 1. prefix 배열 추적

코드를 실행해 prefix 값이 채워지는 과정을 표로 작성하세요.

```c
arr = [2, 1, 3, 4]
prefix = [0] * len(arr)
prefix[0] = arr[0]
for i in range(1, len(arr)):
    prefix[i] = prefix[i - 1] + arr[i]
print(prefix)
```

---

### Q2. Code 1. 빈도 증가

값 x가 나왔을 때 해당 빈도를 1 증가시키는 한 줄을 작성하세요.

```c
# freq 배열 길이는 101
# TODO: x의 빈도 1 증가
```

---

### Q3. Short 1. 값의 등장 횟수

arr에서 값 1이 몇 번 등장하는지 쓰세요.

```c
arr = [1,2,1,3,2,1]
```

---

### Q4. Code 2. 최빈값 갱신(2줄)

후보 값 v의 빈도 f가 더 좋을 때 best, bestF를 갱신하는 2줄을 작성하세요.

```c
if f > bestF:
    # TODO
```

---

### Q5. Reverse 1. prefix로 원소 복원

prefix가 [2, 3, 6, 10]일 때 arr[2] 값을 쓰세요.

```c
arr[i] = prefix[i] - prefix[i-1] (i>0)
```

---

### Q6. Code 3. 단순 등수 계산

scores에서 target보다 큰 점수를 만나면 rank를 증가시키는 코드를 작성하세요.

```c
rank = 1
for s in scores:
    # TODO
```

---

### Q7. Code 4. prefix 채우기

prefix 배열을 누적합으로 채우는 한 줄을 작성하세요.

```c
for i in range(1, n):
    # TODO
```

---

### Q8. Short 2. prefix 구간합

prefix=[2,3,6,10]일 때 1~3 구간합을 쓰세요.

```c
sum(1..3) = prefix[3] - prefix[0]
```

---

### Q9. MCQ 1. 빈도 배열 길이

값의 범위가 0~100(포함)일 때 필요한 freq 배열 길이를 고르세요.

```c
# value in [0, 100]
```

- **A**: 100
- **B**: 101
- **C**: 99
- **D**: 102

---
