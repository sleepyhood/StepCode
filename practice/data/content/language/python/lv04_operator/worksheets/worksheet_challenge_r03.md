---
id: "py_lv04_operator_challenge_r03"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_operator"
title: "Python 연산자 LV04 챌린지 1회차"
round: 3
difficulty: "challenge"
status: "active"
audience: "common"
printDefault: true
---
# Python 연산자 LV04 챌린지 1회차

### Q1. MCQ 1. not과 괄호

다음 요구사항을 만족하는 코드를 고르세요.

- 입력받은 a, b가 같지 않으면 True, 같으면 False를 출력한다.
- 반드시 not 연산자를 사용한다.
- 출력은 서식문자(%)를 사용한다.

- **A**: a = int(input()) b = int(input()) print('%s' % (not (a == b)))
- **B**: a = int(input()) b = int(input()) print('%s' % ((not a) == b))
- **C**: a = int(input()) b = int(input()) print('%s' % (not (a != b)))
- **D**: a = int(input()) b = int(input()) print('%s' % (a != b))

---

### Q2. MCQ 2. 우선순위 함정(산술+비교)

다음 코드의 출력으로 올바른 것을 고르세요.

- 출력은 서식문자(%)를 사용한다.

```c
a = 5
b = 2
print('%s' % (a + b * 2 == 9))
print('%s' % ((a + b) * 2 == 14))
```

- **A**: True True
- **B**: True False
- **C**: False True
- **D**: False False

---

### Q3. MCQ 3. 음수 나머지(%)

다음 코드의 출력으로 올바른 것을 고르세요.

- 파이썬에서 `%`는 항상 0 이상 b 미만이 되도록 나머지를 만든다.
- 출력은 서식문자(%)를 사용한다.

```c
print('%d' % (-7 % 3))
print('%d' % (-(7 % 3)))
```

- **A**: 2 -1
- **B**: -1 -1
- **C**: 2 -2
- **D**: -2 -1

---

### Q4. Short 1. 논리 연산 우선순위

아래 프로그램에서 출력되는 값(True/False)을 쓰시오.

```c
a = 1
b = 2
c = 3
print('%s' % (a < b and b < c or a == 0))
```

---

### Q5. Short 2. 드모르간(De Morgan)

아래 프로그램에서 출력되는 값(True/False)을 쓰시오.

```c
a = -1
b = 5
print('%s' % (not (a > 0 and b > 0)))
```

---

### Q6. Short 3. 연쇄 비교

아래 프로그램에서 출력되는 값(True/False)을 쓰시오.

```c
a = 3
b = 5
c = 4
print('%s' % (a < b < c))
```

---

### Q7. Code 1. 2 또는 3의 배수이지만 둘 다는 아님

정수 n을 입력받아 다음 조건의 결과(True/False)를 출력하세요.

- n이 2의 배수이거나 3의 배수이다.
- 하지만 2와 3의 공배수(둘 다 배수)인 경우는 False

힌트: (조건1) != (조건2) 를 사용할 수 있습니다.
출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 한 줄만 작성하세요.

```c
n = int(input())
# TODO: 조건을 만족하는지 출력하시오.
```

---

### Q8. Code 2. 몫과 나머지로 검증하기

정수 a, b를 입력받습니다. (b는 0이 아닙니다.)
다음 값을 한 줄에 하나씩 출력하세요.

- 1번째 줄: a를 b로 나눈 몫 (a//b)
- 2번째 줄: a를 b로 나눈 나머지 (a%b)
- 3번째 줄: (a//b)*b + (a%b) 의 값

출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 부분만 작성하세요.

```c
a = int(input())
b = int(input())
# TODO: 몫, 나머지, 검증식을 한 줄씩 출력하시오.
```

---

### Q9. Code 3. 정확히 하나만 양수인가?

정수 a, b, c를 입력받아 정확히 하나만 양수(>0)이면 True, 아니면 False를 출력하세요.

힌트: 파이썬에서 True는 1, False는 0처럼 더할 수 있습니다.
출력은 서식문자(%)를 사용해야 합니다.
아래 코드에서 TODO 한 줄만 작성하세요.

```c
a = int(input())
b = int(input())
c = int(input())
# TODO: 정확히 하나만 양수인지 출력하시오.
```

---
