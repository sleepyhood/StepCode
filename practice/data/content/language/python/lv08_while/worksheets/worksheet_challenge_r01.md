---
id: "py_lv08_while_challenge_r01"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_while"
title: "Python while문 챌린지 1회차"
round: 1
difficulty: "challenge"
status: "active"
audience: "common"
printDefault: true
---
# Python while문 챌린지 1회차

### Q1. MCQ 1. 이전 값이 필요한 이유

아래 프로그램에서 입력이 순서대로 3, 5, 4, 6, 0 일 때 출력으로 알맞은 것을 고르세요.

```c
prev = int(input())
cnt = 0
while True:
    x = int(input())
    if x == 0:
        break
    if x > prev:
        cnt = cnt + 1
    prev = x
print('%d' % cnt)
```

- **A**: 0
- **B**: 1
- **C**: 2
- **D**: 3

---

### Q2. MCQ 2. off-by-one (n개 입력)

아래 코드의 목적은 '정수 n을 입력받고, n개의 정수를 더해 합을 출력'하는 것입니다.

입력이 n개일 때 이 코드는 몇 개를 더하려고 시도하나요?

```c
n = int(input())
i = 1
s = 0
while i <= n + 1:
    x = int(input())
    s = s + x
    i = i + 1
print('%d' % s)
```

- **A**: n-1개
- **B**: n개
- **C**: n+1개
- **D**: 무한히

---

### Q3. MCQ 3. 센티넬 루프 디버깅(갱신 위치)

아래 코드는 '0이 나올 때까지 입력받아 합을 출력'하려고 합니다.

이 코드가 정상 동작하도록 하려면 반복문 안에 어떤 한 줄을 추가해야 하나요?

```c
s = 0
x = int(input())
while x != 0:
    s = s + x
print('%d' % s)
```

- **A**: x = 0
- **B**: x = int(input())
- **C**: s = 0
- **D**: break

---

### Q4. MCQ 4. 찾으면 종료, 없으면 -1

다음 중 정수 n을 입력받고, 이어서 n개의 정수를 입력받아 **처음으로 음수가 나온 위치(1부터 시작)** 를 출력하는 코드로 올바른 것을 고르세요.
음수가 한 번도 없다면 -1을 출력합니다.
(출력은 서식문자를 사용한다.)

- **A**: n = int(input()) pos = -1 i = 1 while i <= n:     x = int(input())     if x < 0 and pos == -1:         pos = i         break     i = i + 1 print('%d' % pos)
- **B**: n = int(input()) pos = -1 i = 1 while i <= n:     x = int(input())     if x < 0:         pos = i     i = i + 1 print('%d' % pos)
- **C**: n = int(input()) pos = -1 i = 1 while i <= n:     x = int(input())     if x < 0:         break     i = i + 1 print('%d' % pos)
- **D**: n = int(input()) pos = -1 i = 0 while i < n:     x = int(input())     if x < 0 and pos == -1:         pos = i         break     i = i + 1 print('%d' % pos)

---

### Q5. MCQ 5. continue와 갱신 순서

아래 프로그램에서 입력이 4일 때 출력으로 알맞은 것을 고르세요.

```c
n = int(input())
i = 0
s = 0
while i < n:
    i = i + 1
    if i % 2 == 0:
        continue
    s = s + i
print('%d' % s)
```

- **A**: 4
- **B**: 6
- **C**: 8
- **D**: 10

---

### Q6. Short 1. continue가 있을 때 출력

아래 프로그램에서 입력이 5일 때 출력되는 값을 쓰시오.

```c
n = int(input())
i = 0
s = 0
while i < n:
    i = i + 1
    if i == 3:
        continue
    s = s + i
print('%d' % s)
```

---

### Q7. Short 2. n이 1이 될 때까지 나누기

아래 프로그램에서 입력이 20일 때 출력되는 값을 쓰시오.

```c
n = int(input())
cnt = 0
while n > 1:
    n = n // 2
    cnt = cnt + 1
print('%d' % cnt)
```

---

### Q8. Code 1. 첫 양수의 위치 (조건식 채우기)

정수 n을 입력받고, 이어서 n개의 정수를 입력받습니다.
그 중 **처음으로 양수가 나온 위치(1부터 시작)** 를 출력하세요.
양수가 한 번도 없다면 -1을 출력합니다.

아래 코드에서 주석 위치에 들어갈 조건식 한 줄만 작성하면 됩니다.

```c
n = int(input())
pos = -1
i = 1
while i <= n:
    x = int(input())
    if  # TODO: x가 양수이고 아직 pos가 -1일 때만 실행되도록 조건식을 작성하시오.
        pos = i
        break
    i = i + 1
print('%d' % pos)
```

---

### Q9. Code 2. 2로 나누는 횟수 (조건식 채우기)

정수 n을 입력받아, n이 1이 될 때까지 2로 나누었습니다. (정수 나눗셈 사용)
몇 번 나누었는지 출력하세요.

아래 코드에서 주석 위치에 들어갈 while 조건식 한 줄만 작성하면 됩니다.

```c
n = int(input())
cnt = 0
while  # TODO: n이 1보다 큰 동안만 반복하도록 조건식을 작성하시오.
    n = n // 2
    cnt = cnt + 1
print('%d' % cnt)
```

---
