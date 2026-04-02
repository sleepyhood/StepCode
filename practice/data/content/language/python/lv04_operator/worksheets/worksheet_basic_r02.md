---
id: "py_lv04_operator_basic_r02"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_operator"
title: "Python 연산자 LV04 기초 2회차"
round: 2
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python 연산자 LV04 기초 2회차

### Q1. MCQ 1. 비교 연산(1)

다음 요구사항을 만족하는 코드를 고르세요.

- a=3, b=5일 때 `a < b`의 결과를 출력한다.
- 출력은 서식문자(%)를 사용한다.

- **A**: a = 3 b = 5 print('%s' % (a < b))
- **B**: a = 3 b = 5 print('%d' % (a < b))
- **C**: a = 3 b = 5 print('%s' % (a = b))
- **D**: a = 3 b = 5 print('%s' % (a > b))

---

### Q2. MCQ 2. and / or / not

다음 코드의 출력으로 올바른 것을 고르세요.

- 출력은 서식문자(%)를 사용한다.

```c
a = 2
b = 0
print('%s' % ((a > 0) and (b > 0)))
print('%s' % ((a > 0) or (b > 0)))
print('%s' % (not (a > 0)))
```

- **A**: True True False
- **B**: False True False
- **C**: False False True
- **D**: True False True

---

### Q3. MCQ 3. not으로 같지 않음 만들기

다음 요구사항을 만족하는 코드를 고르세요.

- a=3, b=5일 때 두 수가 같지 않으면 True를 출력한다.
- 반드시 not 연산자를 사용한다.
- 출력은 서식문자(%)를 사용한다.

- **A**: a = 3 b = 5 print('%s' % (not (a == b)))
- **B**: a = 3 b = 5 print('%s' % (not (a != b)))
- **C**: a = 3 b = 5 print('%s' % ((not a) == b))
- **D**: a = 3 b = 5 print('%s' % (a != b))

---

### Q4. Short 1. 짝수 판별

아래 프로그램에서 출력되는 값(True/False)을 쓰시오.

```c
n = 12
print('%s' % (n % 2 == 0))
```

---

### Q5. Short 2. 범위 판별

아래 프로그램에서 출력되는 값(True/False)을 쓰시오.

```c
x = 7
print('%s' % (1 <= x and x <= 10))
```

---

### Q6. Short 3. 세 값 중 하나라도 같음

아래 프로그램에서 출력되는 값(True/False)을 쓰시오.

```c
a = 3
b = 5
c = 3
print('%s' % (a == b or a == c or b == c))
```

---

### Q7. Code 1. 두 수가 같은가?

정수 a, b를 입력받아 두 수가 같으면 True, 아니면 False를 출력하세요.

- 출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 한 줄만 작성하세요.

```c
a = int(input())
b = int(input())
# TODO: 두 수가 같은지 비교한 결과를 출력하시오.
```

---

### Q8. Code 2. 두 수 모두 양수인가?

정수 a, b를 입력받아 두 수가 모두 양수이면 True, 아니면 False를 출력하세요.

- 출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 한 줄만 작성하세요.

```c
a = int(input())
b = int(input())
# TODO: 두 수가 모두 양수인지 출력하시오.
```

---

### Q9. Code 3. 10 이상 99 이하인가?

정수 n을 입력받아 n이 10 이상 99 이하이면 True, 아니면 False를 출력하세요.

- 출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 한 줄만 작성하세요.

```c
n = int(input())
# TODO: 10 이상 99 이하인지 출력하시오.
```

---
