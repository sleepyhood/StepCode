---
id: "py_lv02_var_basic_r02"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_var"
title: "Python 변수 기초 2회차"
round: 2
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python 변수 기초 2회차

### Q1. MCQ 1. 변수 값 갱신

변수 x의 값을 1 증가시키는 코드로 알맞은 것은?

- **A**: x = x + 1
- **B**: x + 1
- **C**: x == x + 1
- **D**: x =+ 1

---

### Q2. MCQ 2. += 의미

아래 코드의 출력으로 알맞은 것을 고르세요.

```c
x = 7
x += 3
print('%d' % x)
```

- **A**: 10
- **B**: 7
- **C**: 6
- **D**: 오류

---

### Q3. MCQ 3. 교환(swap) 결과

아래 코드의 출력으로 알맞은 것을 고르세요.

```c
a = 2
b = 9
tmp = a
a = b
b = tmp
print('%d %d' % (a, b))
```

- **A**: 9 2
- **B**: 2 9
- **C**: 9 9
- **D**: 2 2

---

### Q4. MCQ 4. 잘못된 swap

아래 코드는 a와 b를 바꾸려는 코드입니다.
출력으로 알맞은 것을 고르세요.

```c
a = 2
b = 9
a = b
b = a
print('%d %d' % (a, b))
```

- **A**: 9 2
- **B**: 2 9
- **C**: 9 9
- **D**: 오류

---

### Q5. MCQ 5. 같은 의미 찾기

다음 중 `x += 5`와 같은 의미인 것은?

- **A**: x = x + 5
- **B**: x = 5
- **C**: x == x + 5
- **D**: x =+ 5

---

### Q6. Short 1. 갱신 결과 예측

아래 프로그램에서 입력이 4일 때, 출력되는 한 줄을 그대로 쓰세요.

```c
n = int(input())
n *= 2
print('%d' % n)
```

---

### Q7. Short 2. 두 값 교환 결과 예측

아래 프로그램에서 입력이 "3 7"일 때, 출력되는 한 줄을 그대로 쓰세요.

```c
a, b = map(int, input().split())
tmp = a
a = b
b = tmp
print('%d %d' % (a, b))
```

---

### Q8. Code 1. 1 증가시키기

아래 코드에서 TODO 한 줄에 들어갈 코드를 작성하세요.
(한 줄만 제출)

```c
x = 10
# TODO: x를 1 증가시키세요.
print('%d' % x)
```

---

### Q9. Code 2. swap의 첫 단계

임시변수 tmp를 이용해 a와 b를 교환하려고 합니다.
아래 코드에서 TODO 한 줄에 들어갈 코드를 작성하세요.
(한 줄만 제출)

```c
a = 2
b = 9
tmp = 0
# TODO: tmp에 a를 저장하세요.
a = b
b = tmp
print('%d %d' % (a, b))
```

---
