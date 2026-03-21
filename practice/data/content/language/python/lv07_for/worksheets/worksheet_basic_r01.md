---
id: "py_lv07_for_basic_r01"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_for"
title: "Python for문 기초 1회차"
round: 1
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---

# Python for문 기초 1회차

### Q1. Trace 1. 기본 반복 흐름

각 반복 직후 i와 output을 표에 채우세요.

```python
for i in range(3):
    print('%d' % i)
```

### Q2. Trace 2. 누적 합

각 반복 직후 i와 sum을 표에 채우세요.

```python
sumv = 0
for i in range(1, 5):
    sumv += i
print('%d' % sumv)
```

### Q3. Reverse 1. 끝값 추론

출력이 1, 2, 3, 4일 때 n 값을 쓰세요.

```python
for i in range(1, n + 1):
    print('%d' % i)
```

### Q4. Short 1. 종료 직후 i

다음 코드 실행 후 출력되는 i 값을 쓰세요.

```python
for i in range(5):
    pass
print('%d' % i)
```

### Q5. Code 1. 1부터 n까지 출력

주석 위치에 들어갈 for문 한 줄을 작성하세요.

```python
n = int(input())
# TODO: 1부터 n까지 출력하는 for문 한 줄 작성
    print('%d' % i)
```
