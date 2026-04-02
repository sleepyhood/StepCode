---
set_id: py_lv07_for_b01
category_id: py_for
title: Python for문 기초 1회차
round: 1
difficulty: basic
lang: python
---

# Review Source - Python for문 기초 1회차

This markdown is the primary review source for this set.
Edit this file first, then regenerate JSON.

## Problem 1
id: t_range_basic
type: short
level: 기초
title: Trace 1. 기본 반복 흐름

### prompt
각 반복 직후 i와 output을 표에 채우세요.

### starter
```python
for i in range(3):
    print('%d' % i)
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
      "3"
    ],
    "columns": [
      "i",
      "output"
    ],
    "rowSep": "\\n",
    "colSep": " "
  },
  "expectedGrid": [
    [
      "0",
      "0"
    ],
    [
      "1",
      "1"
    ],
    [
      "2",
      "2"
    ]
  ]
}
```

## Problem 2
id: t_sum_flow
type: short
level: 기초
title: Trace 2. 누적 합

### prompt
각 반복 직후 i와 sum을 표에 채우세요.

### starter
```python
sumv = 0
for i in range(1, 5):
    sumv += i
print('%d' % sumv)
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
      "sum"
    ],
    "rowSep": "\\n",
    "colSep": " "
  },
  "expectedGrid": [
    [
      "1",
      "1"
    ],
    [
      "2",
      "3"
    ],
    [
      "3",
      "6"
    ],
    [
      "4",
      "10"
    ]
  ]
}
```

## Problem 3
id: r_find_n
type: short
level: 기초
title: Reverse 1. 끝값 추론

### prompt
출력이 1, 2, 3, 4일 때 n 값을 쓰세요.

### starter
```python
for i in range(1, n + 1):
    print('%d' % i)
```

### choices
- (none)

### answer
```json
{
  "expectedText": "4"
}
```

## Problem 4
id: s_odds
type: short
level: 기초
title: Short 1. 종료 직후 i

### prompt
다음 코드 실행 후 출력되는 i 값을 쓰세요.

### starter
```python
for i in range(5):
    pass
print('%d' % i)
```

### choices
- (none)

### answer
```json
{
  "expectedText": "4"
}
```

## Problem 5
id: code1
type: code
level: 기초
title: Code 1. 1부터 n까지 출력

### prompt
주석 위치에 들어갈 for문 한 줄을 작성하세요.

### starter
```python
n = int(input())
# TODO: 1부터 n까지 출력하는 for문 한 줄 작성
    print('%d' % i)
```

### choices
- (none)

### answer
```json
{
  "expectedCode": "for i in range(1, n + 1):"
}
```
