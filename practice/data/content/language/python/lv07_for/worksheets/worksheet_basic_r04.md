---
id: "py_lv07_for_basic_r04"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_for"
title: "Python for문 기초 4회차"
round: 4
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python for문 기초 4회차

### Q1. Trace 1. 입력 위치와 누적

각 반복 직후 i, num, sum을 표에 채우세요.

```c
n = 3
sumv = 0
for i in range(n):
    num = int(input())
    sumv += num
```

---

### Q2. Trace 2. 0 포함 경계

range(0, n+1)에서 n=2일 때 i와 output을 표에 채우세요.

```c
n = 2
for i in range(0, n + 1):
    print('%d' % i)
```

---

### Q3. Reverse 1. n 추론

아래 코드의 출력(sumv)이 9일 때 n 값을 쓰세요.

```c
sumv = 0
for i in range(1, n + 1):
    if i % 2 == 1:
        sumv += i
print('%d' % sumv)
```

---

### Q4. Short 1. step 방향 판단

다음 코드의 본문은 몇 번 실행되나요?

```c
for i in range(5, 0, 1):
    print(i)
```

---

### Q5. Code 1. 루프 안 입력

반복문 안에서 정수 하나를 입력받아 sumv에 더하는 코드를 작성하세요.

```c
sumv = 0
for i in range(n):
    # TODO
    sumv += num
```

---
