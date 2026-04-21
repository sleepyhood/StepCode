---
id: "py_lv05_cast_basic_r01"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_cast"
title: "Python 자료형 변환 LV05 기초 1회차"
round: 1
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python 자료형 변환 LV05 기초 1회차

### Q1. MCQ 1. 입력을 정수로 변환

다음 요구사항을 만족하는 코드를 고르세요.

- 정수 n을 입력받아 `n+10`을 출력한다.
- 출력은 서식문자(%)를 사용한다.

- **A**: n = input() print('%d' % (n + 10))
- **B**: n = int(input()) print('%d' % (n + 10))
- **C**: n = int(input()) print('%d' % n + 10)
- **D**: n = float(input()) print('%d' % (n + 10))

---

### Q2. MCQ 2. 몫과 나머지

다음 요구사항을 만족하는 코드를 고르세요.

- 정수 a, b를 입력받는다.
- 1번째 줄에 `a//b`(몫), 2번째 줄에 `a%b`(나머지)를 출력한다.
- 출력은 서식문자(%)를 사용한다.

- **A**: a = int(input()) b = int(input()) print('%d' % (a / b)) print('%d' % (a % b))
- **B**: a = int(input()) b = int(input()) print('%d' % (a // b)) print('%d' % (a % b))
- **C**: a = input() b = input() print('%d' % (a // b)) print('%d' % (a % b))
- **D**: a = int(input()) b = int(input()) print('%d' % (b // a)) print('%d' % (b % a))

---

### Q3. MCQ 3. 마지막 자리 출력

다음 요구사항을 만족하는 코드를 고르세요.

- 정수 n(0 이상)을 입력받아 마지막 자리(일의 자리)를 출력한다.
- 출력은 서식문자(%)를 사용한다.

- **A**: n = int(input()) print('%d' % (n // 10))
- **B**: n = int(input()) print('%d' % (n % 10))
- **C**: n = input() print('%d' % (n % 10))
- **D**: n = int(input()) print(n % 10)

---

### Q4. Short 1. 문자열을 정수로 변환

다음 프로그램에서 출력되는 값(한 줄)을 쓰시오.

```c
a = '7'
b = int(a)
print('%d' % (b + 3))
```

---

### Q5. Short 2. int(양수 실수)

다음 프로그램에서 출력되는 값(한 줄)을 쓰시오.

```c
x = 3.9
print('%d' % int(x))
```

---

### Q6. Short 3. int(음수 실수)

다음 프로그램에서 출력되는 값(한 줄)을 쓰시오.

```c
x = -3.9
print('%d' % int(x))
```

---

### Q7. Code 1. 십의 자리와 일의 자리

정수 n(0 이상)을 입력받아 아래 형식대로 출력하세요.

- 1번째 줄: `n//10` (십의 자리 이상)
- 2번째 줄: `n%10` (일의 자리)

출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 부분만 작성하세요.

```c
n = int(input())
# TODO: 십의 자리 이상과 일의 자리를 각각 한 줄씩 출력하시오.
```

---

### Q8. Code 2. (a+b)*(a-b)

정수 a, b를 입력받아 `(a+b)*(a-b)`의 값을 출력하세요.

출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 부분만 작성하세요.

```c
a = int(input())
b = int(input())
# TODO: (a+b)*(a-b)를 출력하시오.
```

---

### Q9. Code 3. 초를 분/초로 변환

정수 s(초)를 입력받아 아래 형식대로 출력하세요.

- 1번째 줄: 분(= s//60)
- 2번째 줄: 남은 초(= s%60)

출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 부분만 작성하세요.

```c
s = int(input())
# TODO: 분과 남은 초를 각각 한 줄씩 출력하시오.
```

---
