---
id: "py_lv03_input_basic_r02"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_input"
title: "Python 입력 기초 2회차"
round: 2
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python 입력 기초 2회차

### Q1. Trace 1. 여러 공백 입력

입력 줄에 공백이 여러 개 있어요.
요구사항:
- split()으로 토큰을 나눠요.
- input1, input2에는 토큰 그대로 적어요.
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

### Q2. Short 1. 이름과 나이 출력

한 줄에서 이름과 나이를 읽어요.
요구사항:
- age를 정수로 변환해요.
- 출력 형식은 name:age예요.
- 결과 한 줄만 작성해요.

```c
name, age = input().split()
age = int(age)
print('%s:%d' % (name, age))
```

---

### Q3. Code 1. 두 번째 줄 입력 파싱

첫 줄은 이미 읽었습니다.
주석 위치에 둘째 줄 정수 두 개를 읽는 코드 한 줄을 작성하세요.

```c
a, b = map(int, input().split())
# TODO: 둘째 줄에서 정수 두 개를 읽어 c, d에 저장하세요.
print(a, b, c, d)
```

---

### Q4. Code 2. 네 값 서식문자 출력

a, b, c, d가 정수로 저장되어 있습니다.
주석 위치에 네 값을 공백으로 출력하는 한 줄을 작성하세요.

```c
a, b = map(int, input().split())
c, d = map(int, input().split())
# TODO: 서식문자로 a b c d를 한 줄 출력하세요.
```

---

### Q5. Short 2. 두 줄 입력 한 줄 출력

두 줄 입력을 한 줄로 정리해 출력해요.
요구사항:
- 1줄째 두 정수, 2줄째 두 정수를 읽어요.
- 네 값을 한 줄에 순서대로 출력해요.

```c
a, b = map(int, input().split())
c, d = map(int, input().split())
print(a, b, c, d)
```

---
