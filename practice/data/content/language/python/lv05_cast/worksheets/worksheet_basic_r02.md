---
id: "py_lv05_cast_basic_r02"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_cast"
title: "Python 자료형 변환 LV05 기초 2회차"
round: 2
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python 자료형 변환 LV05 기초 2회차

### Q1. MCQ 1. 실수 입력과 소수점 2자리 출력

다음 요구사항을 만족하는 코드를 고르세요.

- 실수 x를 입력받아 `x*2`를 소수점 둘째 자리까지 출력한다.
- 출력은 서식문자(%)를 사용한다.

- **A**: x = float(input()) print('%d' % (x * 2))
- **B**: x = float(input()) print('%.2f' % (x * 2))
- **C**: x = input() print('%.2f' % (x * 2))
- **D**: x = float(input()) print('%.2f' % x * 2)

---

### Q2. MCQ 2. 평균을 실수로 출력

다음 요구사항을 만족하는 코드를 고르세요.

- 정수 a, b를 입력받아 평균을 소수점 둘째 자리까지 출력한다.
- 출력은 서식문자(%)를 사용한다.

- **A**: a = int(input()) b = int(input()) print('%.2f' % ((a + b) // 2))
- **B**: a = int(input()) b = int(input()) print('%.2f' % ((a + b) / 2))
- **C**: a = input() b = input() print('%.2f' % ((a + b) / 2))
- **D**: a = int(input()) b = int(input()) print('%d' % ((a + b) / 2))

---

### Q3. MCQ 3. 서식문자와 괄호

다음 요구사항을 만족하는 코드를 고르세요.

- `1/2`의 결과를 소수점 첫째 자리까지 출력한다.
- 출력은 서식문자(%)를 사용한다.

- **A**: print('%.1f' % (1/2))
- **B**: print('%.1f' % 1/2)
- **C**: print('%.1f' % (1//2))
- **D**: print('%.1f' % (1%2))

---

### Q4. Short 1. float 변환 후 덧셈

다음 프로그램에서 출력되는 값(한 줄)을 쓰시오.

```c
x = float('3')
y = float('2.5')
print('%.1f' % (x + y))
```

---

### Q5. Short 2. 나눗셈 결과 출력

다음 프로그램에서 출력되는 값(한 줄)을 쓰시오.

```c
a = 3
b = 2
print('%.2f' % (a / b))
```

---

### Q6. Short 3. 소수점 둘째 자리 반올림

다음 프로그램에서 출력되는 값(한 줄)을 쓰시오.

```c
n = 10
print('%.2f' % (n / 3))
```

---

### Q7. Code 1. 할인된 가격

정수 price(가격)와 실수 rate(할인율, %)를 입력받아 할인된 가격을 소수점 둘째 자리까지 출력하세요.

- 할인된 가격 = price * (1 - rate/100)
- 출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 부분만 작성하세요.

```c
price = int(input())
rate = float(input())
# TODO: 할인된 가격을 소수점 둘째 자리까지 출력하시오.
```

---

### Q8. Code 2. 섭씨 → 화씨

실수 c(섭씨)를 입력받아 화씨 f를 소수점 첫째 자리까지 출력하세요.

- f = c * 9/5 + 32
- 출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 부분만 작성하세요.

```c
c = float(input())
# TODO: 화씨 온도를 소수점 첫째 자리까지 출력하시오.
```

---

### Q9. Code 3. 나눗셈 몫을 소수 3자리로

정수 a, b를 입력받아 `a/b`를 소수점 셋째 자리까지 출력하세요.

출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 부분만 작성하세요.

```c
a = int(input())
b = int(input())
# TODO: a/b를 소수점 셋째 자리까지 출력하시오.
```

---
