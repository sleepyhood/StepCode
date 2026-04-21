---
id: "py_lv02_var_basic_r03"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_var"
title: "Python 변수 기초 3회차"
round: 3
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python 변수 기초 3회차

### Q1. MCQ 1. // 와 %

아래 코드의 출력으로 알맞은 것을 고르세요.

```c
a = 7
b = 2
print('%d %d' % (a // b, a % b))
```

- **A**: 3 1
- **B**: 3 2
- **C**: 4 1
- **D**: 오류

---

### Q2. MCQ 2. 우선순위

아래 코드에서 x의 값으로 알맞은 것을 고르세요.

```c
x = 2 + 3 * 4
print('%d' % x)
```

- **A**: 14
- **B**: 20
- **C**: 24
- **D**: 오류

---

### Q3. MCQ 3. 괄호의 효과

아래 코드에서 x의 값으로 알맞은 것을 고르세요.

```c
x = (2 + 3) * 4
print('%d' % x)
```

- **A**: 14
- **B**: 20
- **C**: 24
- **D**: 오류

---

### Q4. MCQ 4. 분:초 변환

입력으로 초(seconds) n이 주어집니다.
아래 코드에서 입력이 130일 때 출력으로 알맞은 것은?
(출력: 분 초)

```c
n = int(input())
m = n // 60
s = n % 60
print('%d %d' % (m, s))
```

- **A**: 2 10
- **B**: 1 70
- **C**: 130 0
- **D**: 오류

---

### Q5. MCQ 5. 마지막 자리

아래 코드의 출력으로 알맞은 것을 고르세요.

```c
n = 123
print('%d' % (n % 10))
```

- **A**: 3
- **B**: 2
- **C**: 123
- **D**: 오류

---

### Q6. Short 1. 분:초 변환 결과

아래 프로그램에서 입력이 1000일 때, 출력되는 한 줄을 그대로 쓰세요.
(출력: 분 초)

```c
n = int(input())
m = n // 60
s = n % 60
print('%d %d' % (m, s))
```

---

### Q7. Short 2. 평균(몫) 구하기

아래 프로그램에서 입력이 "9 10"일 때, 출력되는 한 줄을 그대로 쓰세요.

```c
a, b = map(int, input().split())
avg = (a + b) // 2
print('%d' % avg)
```

---

### Q8. Code 1. 몫 계산하기

초 n이 주어질 때, m에 '분'을 저장하려고 합니다.
아래 TODO에 들어갈 코드를 한 줄 작성하세요.

```c
n = int(input())
m = 0
# TODO: m에 n의 '분'을 저장하세요.
print('%d' % m)
```

---

### Q9. Code 2. 마지막 자리 저장하기

정수 n의 마지막 자리를 변수 last에 저장하려고 합니다.
아래 TODO에 들어갈 코드를 한 줄 작성하세요.

```c
n = int(input())
last = 0
# TODO: last에 마지막 자리를 저장하세요.
print('%d' % last)
```

---
