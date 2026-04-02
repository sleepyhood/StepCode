---
set_id: py_lv07_for_b02
category_id: py_for
title: Python for문 기초 2회차
round: 2
difficulty: basic
lang: python
---

# Review Source - Python for문 기초 2회차

This markdown is the primary review source for this set.
Edit this file first, then regenerate JSON.

## Problem 1
id: t_range_step
type: short
level: 기초
title: Trace 1. 감소 step

### prompt
각 반복 직후 i와 output을 표에 채우세요.

### starter
```python
for i in range(5, 0, -2):
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
      "5",
      "5"
    ],
    [
      "3",
      "3"
    ],
    [
      "1",
      "1"
    ]
  ]
}
```

## Problem 2
id: t_input_sum
type: short
level: 기초
title: Trace 2. 중간 상태 복원

### prompt
sum += i 코드에서 3회 반복 직후 i와 sum을 표에 채우세요.

### starter
```python
sumv = 0
for i in range(1, 7):
    sumv += i
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
    ]
  ]
}
```

## Problem 3
id: r_find_n_even_sum
type: short
level: 기초
title: Reverse 1. 시작값/step 추론

### prompt
출력이 2, 4, 6, 8일 때 start와 step을 공백으로 구분해 쓰세요.

### starter
```python
for i in range(start, 9, step):
    print('%d' % i)
```

### choices
- (none)

### answer
```json
{
  "expectedText": "2 2"
}
```

## Problem 4
id: s_even_count
type: short
level: 기초
title: Short 1. 경계 비교

### prompt
for i in range(5) 본문은 몇 번 실행되나요?

### starter
```python
for i in range(5):
    pass
```

### choices
- (none)

### answer
```json
{
  "expectedText": "5"
}
```

## Problem 5
id: code2
type: code
level: 기초
title: Code 1. 조건식 한 줄

### prompt
1부터 n까지 수 중 짝수만 sumv에 더하려고 합니다. if문의 조건식 한 줄을 작성하세요.

### starter
```python
sumv = 0
for i in range(1, n + 1):
    if ____:
        sumv += i
```

### choices
- (none)

### answer
```json
{
  "expectedCode": "i % 2 == 0"
}
```
