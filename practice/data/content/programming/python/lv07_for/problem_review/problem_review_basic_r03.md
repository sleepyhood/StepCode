---
set_id: py_lv07_for_b03
category_id: py_for
title: Python for문 기초 3회차
round: 3
difficulty: basic
lang: python
---

# Review Source - Python for문 기초 3회차

This markdown is the primary review source for this set.
Edit this file first, then regenerate JSON.

## Problem 1
id: t_input_count
type: short
level: 기초
title: Trace 1. 입력 포함 count

### prompt
각 반복 직후 i, num, count를 표에 채우세요.

### starter
```python
n = 4
count = 0
for i in range(n):
    num = int(input())
    if num > 0:
        count += 1
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
      "4"
    ],
    "columns": [
      "i",
      "num",
      "count"
    ],
    "rowSep": "\\n",
    "colSep": " "
  },
  "expectedGrid": [
    [
      "0",
      "3",
      "1"
    ],
    [
      "1",
      "-1",
      "1"
    ],
    [
      "2",
      "5",
      "2"
    ],
    [
      "3",
      "0",
      "2"
    ]
  ],
  "ioExample": {
    "input": "3\n-1\n5\n0"
  }
}
```

## Problem 2
id: t_input_sum
type: short
level: 기초
title: Trace 2. 조건 누적 합

### prompt
짝수만 더할 때 i, num, sum 변화를 표에 채우세요.

### starter
```python
n = 4
sumv = 0
for i in range(n):
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
      "4"
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
      "0",
      "2",
      "2"
    ],
    [
      "1",
      "7",
      "2"
    ],
    [
      "2",
      "4",
      "6"
    ],
    [
      "3",
      "1",
      "6"
    ]
  ],
  "ioExample": {
    "input": "2\n7\n4\n1"
  }
}
```

## Problem 3
id: r_find_n_lines
type: short
level: 기초
title: Reverse 1. 누락 값 추론

### prompt
아래 코드의 출력(sumv)이 10이 되도록 ? 값을 쓰세요.

### starter
```python
n = 4
sumv = 0
for i in range(n):
    num = int(input())
    if num % 2 == 0:
        sumv += num
print('%d' % sumv)
```

### choices
- (none)

### answer
```json
{
  "expectedText": "4",
  "ioExample": {
    "input": "2\n?\n4\n1",
    "output": "10"
  }
}
```

## Problem 4
id: s_positive_count
type: short
level: 기초
title: Short 1. 종료 직후 i

### prompt
다음 코드 실행 후 출력되는 i 값을 쓰세요.

### starter
```python
for i in range(4):
    pass
print('%d' % i)
```

### choices
- (none)

### answer
```json
{
  "expectedText": "3"
}
```

## Problem 5
id: code1
type: code
level: 기초
title: Code 1. 조건식 한 줄

### prompt
n개의 정수를 입력받아 양수만 sumv에 더하려고 합니다.
if ____ 부분에 들어갈 조건식 한 줄을 작성하세요.

### starter
```python
sumv = 0
for i in range(n):
    num = int(input())
    if ____:
        sumv += num
```

### choices
- (none)

### answer
```json
{
  "expectedCode": "num > 0"
}
```
