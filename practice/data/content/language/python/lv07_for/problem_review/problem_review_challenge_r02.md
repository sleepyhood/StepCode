---
set_id: py_lv07_for_c01
category_id: py_for
title: Python for문 챌린지 1회차
round: 2
difficulty: challenge
lang: python
---

# Review Source - Python for문 챌린지 1회차

This markdown is the primary review source for this set.
Edit this file first, then regenerate JSON.

## Problem 1
id: t_even_sum_inputs
type: short
level: 챌린지
title: Trace 1. n개 입력 중 짝수만 더하기

### prompt
입력이 `3, 8, 4, 1, 6`일 때, 각 반복 직후의 i, num, sum을 표에 채우세요.

### starter
```python
n = 5
sumv = 0
for i in range(1, n + 1):
    num = int(input())
    if num % 2 == 0:
        sumv += num
```

### choices
- (none)

### answer
```json
{
  "answerUi": {
    "kind": "grid",
    "rows": [
      "1",
      "2",
      "3",
      "4",
      "5"
    ],
    "columns": [
      "i",
      "num",
      "sum"
    ],
    "rowSep": "\\n",
    "colSep": " "
  },
  "expectedGrid": [
    [
      "1",
      "3",
      "0"
    ],
    [
      "2",
      "8",
      "8"
    ],
    [
      "3",
      "4",
      "12"
    ],
    [
      "4",
      "1",
      "12"
    ],
    [
      "5",
      "6",
      "18"
    ]
  ],
  "ioExample": {
    "input": "3\n8\n4\n1\n6"
  }
}
```

## Problem 2
id: t_odd_average_trace
type: short
level: 챌린지
title: Trace 2. n개 입력 중 홀수들의 평균

### prompt
입력이 `9, 4, 7, 3, 8`일 때, 홀수만 이용해 평균을 구합니다. 각 반복 직후의 i, num, sum, count를 표에 채우세요.

### starter
```python
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

### choices
- (none)

### answer
```json
{
  "answerUi": {
    "kind": "grid",
    "rows": [
      "1",
      "2",
      "3",
      "4",
      "5"
    ],
    "columns": [
      "i",
      "num",
      "sum",
      "count"
    ],
    "rowSep": "\\n",
    "colSep": " "
  },
  "expectedGrid": [
    [
      "1",
      "9",
      "9",
      "1"
    ],
    [
      "2",
      "4",
      "9",
      "1"
    ],
    [
      "3",
      "7",
      "16",
      "2"
    ],
    [
      "4",
      "3",
      "19",
      "3"
    ],
    [
      "5",
      "8",
      "19",
      "3"
    ]
  ],
  "ioExample": {
    "input": "9\n4\n7\n3\n8"
  }
}
```

## Problem 3
id: r_average_1_to_n
type: short
level: 챌린지
title: Reverse 1. 1부터 n까지의 평균 역추론

### prompt
아래 코드의 출력(avg)이 `5`였습니다. 단, `1 <= n <= 10`일 때 가능한 n 중 가장 큰 값을 쓰세요.

### starter
```python
sumv = 0
for i in range(1, n + 1):
    sumv += i
avg = sumv // n
print(avg)
```

### choices
- (none)

### answer
```json
{
  "expectedText": "10",
  "ioExample": {
    "output": "5"
  }
}
```

## Problem 4
id: s_max_after_loop
type: short
level: 챌린지
title: Short 1. 최댓값과 종료 직후 값

### prompt
입력이 `8, 3, 12, 7, 10`일 때, 출력되는 `i max`를 공백으로 구분해 쓰세요.

### starter
```python
maxv = int(input())
for i in range(2, 6):
    num = int(input())
    if num > maxv:
        maxv = num
print(i + 1, maxv)
```

### choices
- (none)

### answer
```json
{
  "expectedText": "6 12",
  "ioExample": {
    "input": "8\n3\n12\n7\n10"
  }
}
```

## Problem 5
id: code_even_condition
type: code
level: 챌린지
title: Code 1. 짝수 판별 조건식

### prompt
입력값 num이 짝수일 때만 sumv에 더하려고 합니다. `if`의 조건식을 한 줄로 작성하세요.

### starter
```python
if ____:
    sumv += num
```

### choices
- (none)

### answer
```json
{
  "expectedCode": "num % 2 == 0"
}
```

## Problem 6
id: code_max_condition
type: code
level: 챌린지
title: Code 2. 최댓값 갱신 조건식

### prompt
새 입력값 num이 현재 최댓값 maxv보다 클 때만 갱신하려고 합니다. `if`의 조건식을 한 줄로 작성하세요.

### starter
```python
if ____:
    maxv = num
```

### choices
- (none)

### answer
```json
{
  "expectedCode": "num > maxv"
}
```
