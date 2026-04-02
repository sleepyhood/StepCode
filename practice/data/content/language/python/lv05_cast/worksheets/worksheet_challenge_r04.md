---
id: "py_lv05_cast_challenge_r04"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_cast"
title: "Python 자료형 변환 LV05 챌린지 1회차"
round: 4
difficulty: "challenge"
status: "active"
audience: "common"
printDefault: true
---
# Python 자료형 변환 LV05 챌린지 1회차

### Q1. MCQ 1. int(float(...)) 순서

다음 요구사항을 만족하는 코드를 고르세요.

- 문자열로 입력된 실수 s를 입력받는다. (예: 3.99)
- s의 정수 부분만 출력한다. (예: 3)
- 출력은 서식문자(%)를 사용한다.

- **A**: s = input() print('%d' % int(float(s)))
- **B**: s = input() print('%d' % int(s))
- **C**: s = input() print('%.0f' % int(float(s)))
- **D**: s = input() print('%d' % float(int(s)))

---

### Q2. MCQ 2. 음수에서 정수 부분

다음 요구사항을 만족하는 코드를 고르세요.

- 실수 x를 입력받는다. (음수도 가능)
- x의 정수 부분을 출력한다. (파이썬의 int()는 0쪽으로 버림)
- 출력은 서식문자(%)를 사용한다.

- **A**: x = float(input()) print('%d' % int(x))
- **B**: x = float(input()) print('%d' % (x // 1))
- **C**: x = float(input()) print('%.0f' % (x // 1))
- **D**: x = float(input()) print('%d' % (x / 1))

---

### Q3. MCQ 3. 문자열 더하기 버그 수정

다음 요구사항을 만족하는 코드를 고르세요.

- 정수 a, b를 입력받아 합을 출력한다.
- 아래의 잘못된 코드를 올바르게 고친 버전을 고르세요.

잘못된 코드:
```
a = input()
b = input()
print('%d' % (a + b))
```

- 출력은 서식문자(%)를 사용한다.

- **A**: a = input() b = input() print('%d' % (int(a) + int(b)))
- **B**: a = int(input()) b = int(input()) print('%d' % a + b)
- **C**: a = input() b = input() print('%d' % (a + b))
- **D**: a = int(input()) b = int(input()) print(a + b)

---

### Q4. Short 1. int(float('3.99'))

다음 프로그램에서 출력되는 값(한 줄)을 쓰시오.

```c
print('%d' % (int(float('3.99'))))
```

---

### Q5. Short 2. int(-2.7)

다음 프로그램에서 출력되는 값(한 줄)을 쓰시오.

```c
print('%d' % int(-2.7))
```

---

### Q6. Short 3. float(int(7.9))

다음 프로그램에서 출력되는 값(한 줄)을 쓰시오.

```c
print('%.2f' % (float(int(7.9))))
```

---

### Q7. Code 1. 실수의 정수 부분 출력

실수 x를 입력받아 x의 정수 부분만 출력하세요.

- 파이썬의 int()는 0쪽으로 버립니다.
- 출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 부분만 작성하세요.

```c
x = float(input())
# TODO: x의 정수 부분을 출력하시오.
```

---

### Q8. Code 2. 세 정수의 평균

정수 a, b, c를 입력받아 평균을 소수점 첫째 자리까지 출력하세요.

- 평균 = (a+b+c)/3
- 출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 부분만 작성하세요.

```c
a = int(input())
b = int(input())
c = int(input())
# TODO: 평균을 소수점 첫째 자리까지 출력하시오.
```

---

### Q9. Code 3. 세금 계산(버림)

정수 price(가격)와 실수 rate(세율, %)를 입력받아 아래를 출력하세요.

- 1번째 줄: 세금 = price * rate / 100 의 결과를 정수로 변환한 값(int로 버림)
- 2번째 줄: price + 세금

출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 부분만 작성하세요.

```c
price = int(input())
rate = float(input())
# TODO: 세금(정수)과 총액을 각각 한 줄씩 출력하시오.
```

---
