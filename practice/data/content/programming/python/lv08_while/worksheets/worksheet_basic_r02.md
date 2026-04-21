---
id: "py_lv08_while_basic_r02"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_while"
title: "Python while문 기초 2회차"
round: 2
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python while문 기초 2회차

### Q1. MCQ 1. 센티넬(0 종료) - pre-read 패턴

다음 중 정수를 계속 입력받다가 0이 입력되면 종료하고, 입력된 수들의 합을 출력하는 코드로 올바른 것을 고르세요.
(출력은 서식문자를 사용한다.)

- **A**: s = 0 x = int(input()) while x != 0:     s = s + x print('%d' % s)
- **B**: s = 0 x = int(input()) while x != 0:     s = s + x     x = int(input()) print('%d' % s)
- **C**: s = 0 while x != 0:     x = int(input())     s = s + x print('%d' % s)
- **D**: s = 0 x = int(input()) while x == 0:     s = s + x     x = int(input()) print('%d' % s)

---

### Q2. MCQ 2. 최댓값 변수 필요

다음 중 정수 n을 입력받고, 이어서 n개의 정수를 입력받아 **최댓값**을 출력하는 코드로 올바른 것을 고르세요.
(출력은 서식문자를 사용한다.)

- **A**: n = int(input()) i = 1 x = int(input()) mx = x while i < n:     x = int(input())     if x > mx:         mx = x     i = i + 1 print('%d' % mx)
- **B**: n = int(input()) i = 1 mx = 0 while i <= n:     x = int(input())     if x > mx:         mx = x     i = i + 1 print('%d' % mx)
- **C**: n = int(input()) i = 1 mx = -1 while i <= n:     x = int(input())     mx = x     i = i + 1 print('%d' % mx)
- **D**: n = int(input()) i = 1 x = int(input()) mx = x while i <= n:     x = int(input())     if x > mx:         mx = x     i = i + 1 print('%d' % mx)

---

### Q3. MCQ 3. 합이 목표 이상이 되는 최소 k

아래 프로그램에서 입력이 10일 때 출력으로 알맞은 것을 고르세요.

```c
t = int(input())
s = 0
k = 1
while s < t:
    s = s + k
    k = k + 1
print('%d' % (k - 1))
```

- **A**: 3
- **B**: 4
- **C**: 5
- **D**: 6

---

### Q4. MCQ 4. 입력을 한 번 더 읽는 실수

아래 코드의 목적은 '정수 n을 입력받고, 그 다음 줄부터 n개의 정수를 더해 합을 출력'하는 것입니다.

그런데 이 코드는 어떤 문제가 있나요?

```c
n = int(input())
i = 1
s = 0
while i <= n:
    x = int(input())
    s = s + x
    i = i + 1
x = int(input())
print('%d' % s)
```

- **A**: n개의 수를 더하기 전에 i를 0으로 초기화해야 한다
- **B**: 마지막에 불필요하게 입력을 한 번 더 받는다
- **C**: s가 실수로 계산된다
- **D**: while 조건이 항상 거짓이어서 한 번도 반복되지 않는다

---

### Q5. MCQ 5. 감소 while 조건

다음 중 5부터 1까지를 한 줄에 하나씩 출력하는 코드로 올바른 것을 고르세요.
(출력은 서식문자를 사용한다.)

- **A**: i = 5 while i < 1:     print('%d' % i)     i = i - 1
- **B**: i = 5 while i > 1:     print('%d' % i)     i = i - 1 print('%d' % i)
- **C**: i = 5 while i >= 1:     print('%d' % i)     i = i - 1
- **D**: i = 5 while i != 1:     print('%d' % i)     i = i - 1

---

### Q6. Short 1. 최댓값 추적

아래 프로그램에서 입력이 순서대로 4, 2, 9, 3, 7 일 때 출력되는 값을 쓰시오.

```c
n = int(input())
i = 1
x = int(input())
mx = x
while i < n:
    x = int(input())
    if x > mx:
        mx = x
    i = i + 1
print('%d' % mx)
```

---

### Q7. Short 2. 조건에 맞는 개수 세기

아래 프로그램에서 입력이 순서대로 5, 3, 8, 2, 9, 1 일 때 출력되는 값을 쓰시오.

```c
n = int(input())
i = 1
cnt = 0
while i <= n:
    x = int(input())
    if x >= 5:
        cnt = cnt + 1
    i = i + 1
print('%d' % cnt)
```

---

### Q8. Code 1. 0이 나올 때까지 합 (조건식 채우기)

정수를 계속 입력받다가 0이 입력되면 종료하고, 입력된 수들의 합을 출력하는 프로그램을 완성하세요.

아래 코드에서 주석 위치에 들어갈 while 조건식 한 줄만 작성하면 됩니다.

```c
x = int(input())
s = 0
while  # TODO: 0이 아닐 때만 반복하도록 조건식을 작성하시오.
    s = s + x
    x = int(input())
print('%d' % s)
```

---

### Q9. Code 2. 합이 목표 이상이 되는 최소 k (조건식 채우기)

정수 t를 입력받아, 1부터 더해가며 합이 t 이상이 되는 **최소 k**를 출력하세요.

아래 코드에서 주석 위치에 들어갈 while 조건식 한 줄만 작성하면 됩니다.

```c
t = int(input())
s = 0
k = 1
while  # TODO: 합이 t보다 작은 동안만 반복하도록 조건식을 작성하시오.
    s = s + k
    k = k + 1
print('%d' % (k - 1))
```

---
