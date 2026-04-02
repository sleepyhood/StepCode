---
id: "py_lv03_input_basic_r01"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_input"
title: "Python 입력 기초 1회차"
round: 1
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python 입력 기초 1회차

### Q1. Trace 1. 한 줄 두 정수

한 줄 입력에서 값 두 개를 읽어 정수로 바꿔요.
요구사항:
- input1, input2에는 입력 토큰 그대로 적어요.
- a, b에는 정수 변환 결과를 적어요.
- a + b를 계산해 output에 적어요.

예시 표:
| input1 | input2 | a | b | output |
| --- | --- | --- | --- | --- |
| 3 | 5 | 3 | 5 | 0 |

```c
a, b = map(int, input().split())
print(a + b)
```

---

### Q2. Code 1. 두 정수 입력 받기

한 줄에서 정수 2개를 읽는 코드입니다.
주석 위치에 들어갈 입력 한 줄만 작성하세요.

```c
# TODO: 한 줄 입력에서 정수 2개를 읽어 a, b에 저장하세요.
print('%d' % (a + b))
```

---

### Q3. Short 1. 출력 순서 바꾸기

두 값을 입력받아 순서를 바꿔 출력하세요.
출력은 공백으로 구분된 한 줄입니다.

```c
a, b = input().split()
print(b, a)
```

---

### Q4. Code 2. 서식문자 합 출력

a와 b가 이미 정수로 저장되어 있습니다.
주석 위치에 들어갈 출력 한 줄만 작성하세요.
출력 형식은 `a + b = result` 입니다.

```c
a, b = map(int, input().split())
# TODO: 서식문자로 "a + b = result"를 출력하세요.
```

---

### Q5. Short 2. 두 줄 곱셈 결과

두 줄 입력을 차례로 읽어 곱을 계산해요.
요구사항:
- line1 값을 a에 저장해요.
- line2 값을 b에 저장해요.
- a * b의 결과만 출력해요.

```c
a = int(input())
b = int(input())
print(a * b)
```

---
