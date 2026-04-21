---
id: "py_lv07_for_challenge_r02"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_for"
title: "Python for문 챌린지 1회차"
round: 2
difficulty: "challenge"
status: "active"
audience: "common"
printDefault: true
---
# Python for문 챌린지 1회차

### Q1. Trace 1. n개 입력 중 짝수만 더하기

입력이 `3, 8, 4, 1, 6`일 때, 각 반복 직후의 i, num, sum을 표에 채우세요.

```c
n = 5
sumv = 0
for i in range(1, n + 1):
    num = int(input())
    if num % 2 == 0:
        sumv += num
```

---

### Q2. Trace 2. n개 입력 중 홀수들의 평균

입력이 `9, 4, 7, 3, 8`일 때, 홀수만 이용해 평균을 구합니다. 각 반복 직후의 i, num, sum, count를 표에 채우세요.

```c
n = 5
sumv = 0
count = 0
for i in range(1, n + 1):
    num = int(input())
    if num % 2 != 0:
        sumv += num
        count += 1
avg = sumv // count
```

---

### Q3. Reverse 1. 1부터 n까지의 평균 역추론

아래 코드의 출력(avg)이 `5`였습니다. 단, `1 <= n <= 10`일 때 가능한 n 중 가장 큰 값을 쓰세요.

```c
sumv = 0
for i in range(1, n + 1):
    sumv += i
avg = sumv // n
print(avg)
```

---

### Q4. Short 1. 최댓값과 종료 직후 값

입력이 `8, 3, 12, 7, 10`일 때, 출력되는 `i max`를 공백으로 구분해 쓰세요.

```c
maxv = int(input())
for i in range(2, 6):
    num = int(input())
    if num > maxv:
        maxv = num
print(i + 1, maxv)
```

---

### Q5. Code 1. 짝수 판별 조건식

입력값 num이 짝수일 때만 sumv에 더하려고 합니다. `if`의 조건식을 한 줄로 작성하세요.

```c
if ____:
    sumv += num
```

---

### Q6. Code 2. 최댓값 갱신 조건식

새 입력값 num이 현재 최댓값 maxv보다 클 때만 갱신하려고 합니다. `if`의 조건식을 한 줄로 작성하세요.

```c
if ____:
    maxv = num
```

---
