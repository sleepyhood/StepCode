---
id: "py_lv07_for_basic_r02"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_for"
title: "Python for문 기초 2회차"
round: 2
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---

# Python for문 기초 2회차

### Q1. Trace 1. 역순 반복

각 반복 직후 i와 output을 표에 채우세요.

```python
for i in range(4, 0, -1):
    print('%d' % i)
```

### Q2. Trace 2. 짝수 누적

각 반복 직후 i와 sum을 표에 채우세요.

```python
sumv = 0
for i in range(2, 9, 2):
    sumv += i
print('%d' % sumv)
```

### Q3. Reverse 1. 반복 횟수 추론

아래 코드의 출력이 0, 1, 2, 3, 4일 때 n 값을 쓰세요.

```python
for i in range(n):
    print('%d' % i)
```

### Q4. Short 1. 종료 직후 i

다음 코드 실행 후 출력되는 i 값을 쓰세요.

```python
for i in range(2, 8, 2):
    pass
print('%d' % i)
```

### Q5. Code 1. 0부터 n-1까지 반복

주석 위치에 들어갈 for문 한 줄을 작성하세요.

```python
n = int(input())
# TODO: 0부터 n-1까지 반복하는 for문 한 줄 작성
    print('%d' % i)
```
