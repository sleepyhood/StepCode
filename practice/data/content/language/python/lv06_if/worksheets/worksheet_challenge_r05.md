---
id: "py_lv06_if_challenge_r05"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_if"
title: "Python 조건문 챌린지 1회차"
round: 5
difficulty: "challenge"
status: "active"
audience: "common"
printDefault: true
---
# Python 조건문 챌린지 1회차

### Q1. MCQ 1. 성인 / 학생 분류

다음 요구사항을 만족하는 코드를 고르세요.

- 나이 age와 학생 여부 is_student("Y" 또는 "N")를 입력받는다.
- age가 20 이상이고 is_student가 "Y"이면 "성인 학생"을 출력한다.
- age가 20 이상이고 is_student가 "Y"가 아니면 "성인"을 출력한다.
- 그 외에는 "미성년자"를 출력한다.

- **A**: age = int(input()) is_student = input() if age >= 20 and is_student == "Y":     print('%s' % '성인 학생') elif age >= 20:     print('%s' % '성인') else:     print('%s' % '미성년자')
- **B**: age = int(input()) is_student = input() if age >= 20 or is_student == "Y":     print('%s' % '성인 학생') elif age >= 20:     print('%s' % '성인') else:     print('%s' % '미성년자')
- **C**: age = int(input()) is_student = input() if age >= 20:     print('%s' % '성인') elif age >= 20 and is_student == "Y":     print('%s' % '성인 학생') else:     print('%s' % '미성년자')
- **D**: age = int(input()) is_student = input() if age >= 20 and is_student == "Y":     print('%s' % '성인 학생') else:     print('%s' % '성인') print('%s' % '미성년자')

---

### Q2. MCQ 2. 조건의 순서

아래 프로그램에서 입력이 95일 때, 출력으로 알맞은 것을 고르세요.

```c
score = int(input())
if score >= 70:
    print('%s' % 'C')
elif score >= 80:
    print('%s' % 'B')
elif score >= 90:
    print('%s' % 'A')
else:
    print('%s' % 'D')
```

- **A**: A
- **B**: B
- **C**: C
- **D**: D

---

### Q3. MCQ 3. if와 elif의 차이

아래 프로그램에서 입력이 6일 때, 출력으로 알맞은 것을 고르세요.

```c
n = int(input())
if n % 2 == 0:
    print('%s' % 'Even')
if n % 3 == 0:
    print('%s' % 'Three')
else:
    print('%s' % 'Other')
```

- **A**: Even
- **B**: Three
- **C**: Even Three
- **D**: Even Other

---

### Q4. MCQ 4. and / or 섞어서 쓰기

아래 프로그램에서 "OK"가 출력되는 n만 모아 둔 것을 고르세요.

```c
n = int(input())
if (n % 2 == 0 and n > 0) or n == 1:
    print('%s' % 'OK')
else:
    print('%s' % 'NG')
```

- **A**: 1, 2
- **B**: 1, 2, -2
- **C**: -2, 0
- **D**: 0, 1

---

### Q5. MCQ 5. 중첩 if의 동작

아래 프로그램에서 입력이 75일 때, 출력으로 알맞은 것을 고르세요.

```c
score = int(input())
if score >= 60:
    if score >= 90:
        print('%s' % 'A')
    else:
        print('%s' % 'B')
else:
    print('%s' % 'F')
```

- **A**: A
- **B**: B
- **C**: F
- **D**: 아무 것도 출력되지 않는다.

---

### Q6. Trace 1. 복합 조건 통과 판정

key, hp, ticket 조합에 따라 GO/STOP이 결정됩니다. 조건 결과를 표에 채우세요.

입력 케이스 예시:
- case1: key=1, hp=20, ticket=1
- case2: key=1, hp=40, ticket=0
- case3: key=0, hp=80, ticket=1

```c
key, hp, ticket = map(int, input().split())
if key == 1 and (hp >= 30 or ticket == 1):
    print('%s' % 'GO')
else:
    print('%s' % 'STOP')
```

---

### Q7. Short 1. 여러 조건 분기

아래 프로그램에서 입력이 6일 때, 출력되는 한 줄을 그대로 쓰세요.
(따옴표는 쓰지 마시오)

```c
n = int(input())
if n < 0:
    print('%s' % 'minus')
elif n == 0:
    print('%s' % 'zero')
elif n % 2 == 0:
    print('%s' % 'plus-even')
else:
    print('%s' % 'plus-odd')
```

---

### Q8. Short 2. 조건을 만족하는 값 찾기

다음 조건식이 참(true)이 되도록 n의 값을 하나만 쓰세요.
(여러 개 중 아무거나 하나 맞으면 정답입니다.)

```c
n % 2 == 0 and 10 <= n <= 20
```

---

### Q9. Code 1. 두 자리 양수이면서 짝수

정수 n이 "두 자리 양수(10 이상 99 이하)"이고, 동시에 짝수일 때만 "YES"를 출력하려고 합니다.
if 뒤 괄호 안에 들어갈 조건식을 한 줄로 작성하세요.

```c
n = int(input())
if  # 여기에 조건식을 작성하세요:
    print('%s' % 'YES')
else:
    print('%s' % 'NO')
```

---

### Q10. Code 2. 학점 B 구간 조건식

아래는 학점을 A, B, C로 나누는 코드의 일부입니다.
- 90 이상이면 A
- 80 이상 90 미만이면 B
- 나머지는 C

elif 줄의 조건식을 완성하세요.

```c
score = int(input())
if score >= 90:
    print('%s' % 'A')
elif  # 여기에 조건식을 작성하세요:
    print('%s' % 'B')
else:
    print('%s' % 'C')
```

---
