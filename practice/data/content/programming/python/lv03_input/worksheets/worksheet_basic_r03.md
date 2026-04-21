---
id: "py_lv03_input_basic_r03"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_input"
title: "Python 입력 기초 3회차"
round: 3
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python 입력 기초 3회차

### Q1. Trace 1. 세 정수 합

한 줄에서 정수 3개를 읽어 합을 계산해요.
요구사항:
- a, b, c를 정수로 변환해요.
- a + b + c를 output에 적어요.
- a, b, c, output을 표에 채워요.

예시 표:
| a | b | c | output |
| --- | --- | --- | --- |
| 3 | 5 | 1 | 0 |

```c
a, b, c = map(int, input().split())
print(a + b + c)
```

---

### Q2. Code 1. 세 정수 입력 한 줄

한 줄에서 정수 3개를 읽는 코드입니다.
주석 위치에 들어갈 입력 한 줄만 작성하세요.

```c
# TODO: 한 줄 입력에서 정수 3개를 읽어 a, b, c에 저장하세요.
print('%d' % (a + b + c))
```

---

### Q3. Short 1. split() 이후 자료형

아래 코드에서 `a, b, c`의 자료형을 쓰세요.
정답은 `str` 또는 `int` 중 하나입니다.

```c
a, b, c = input().split()
```

---

### Q4. Code 2. 식 계산 출력

a, b, c가 정수로 저장되어 있습니다.
주석 위치에 `(a + b) * c`를 서식문자로 출력하는 한 줄을 작성하세요.

```c
a, b = map(int, input().split())
c = int(input())
# TODO: (a + b) * c 결과를 한 줄로 출력하세요.
```

---

### Q5. Reverse 1. 세 번째 입력 찾기

a, b와 출력값(a + b + c)이 주어집니다.
빠진 c를 구해 숫자만 작성하세요.

```c
a, b, c = map(int, input().split())
print(a + b + c)
```

---

### Q6. Short 3. 정수 평균

정수 3개의 평균을 //로 계산해요.
요구사항:
- 합을 구한 뒤 평균을 계산해요.
- 결과만 한 줄로 출력해요.

```c
a, b, c = map(int, input().split())
print((a + b + c) // 3)
```

---
