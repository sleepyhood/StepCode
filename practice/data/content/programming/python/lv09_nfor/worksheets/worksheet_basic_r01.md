---
id: "py_lv09_nfor_basic_r01"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_nfor"
title: "Python 중첩 for문 LV09 기초 1회차"
round: 1
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python 중첩 for문 LV09 기초 1회차

### Q1. MCQ 1. 출력 예시 보고 코드 고르기

다음 출력 결과와 **같이 출력**하는 Python 코드를 고르세요.
(문자열 반복(곱셈)은 사용하지 않는다.)

출력:
```
****
****
****
```

- **A**: for i in range(3):     for j in range(4):         print('*')     print()
- **B**: for i in range(3):     for j in range(4):         print('*', end='')     print()
- **C**: for i in range(4):     for j in range(3):         print('*', end='')     print()
- **D**: for i in range(3):     for j in range(4):         print('*', end='') print()

---

### Q2. MCQ 2. 높이 4 왼쪽 직각삼각형

다음 출력 결과와 **같이 출력**하는 Python 코드를 고르세요.
(문자열 반복(곱셈)은 사용하지 않는다.)

출력:
```
*
**
***
****
```

- **A**: for i in range(4):     for j in range(i):         print('*', end='')     print()
- **B**: for i in range(4):     for j in range(i + 1):         print('*', end='')     print()
- **C**: for i in range(1, 5):     for j in range(i + 1):         print('*', end='')     print()
- **D**: for i in range(4):     for j in range(i + 1):         print('*')     print()

---

### Q3. Short 1. 출력되는 별의 개수

아래 프로그램이 출력하는 별(*)의 총 개수를 한 줄에 숫자로 쓰시오.

```c
for i in range(2):
    for j in range(3):
        print('*', end='')
    print()
```

---

### Q4. Code 1. 4열을 반복하는 내부 for문

아래 코드는 다음 출력 결과를 만들려고 합니다.
주석 위치에 들어갈 **내부 for문 한 줄**을 작성하세요.

- 한 행에 별 4개를 출력해야 한다.
- 문자열 반복(곱셈)은 사용하지 않는다.

출력:
```
****
****
****
```

```c
for i in range(3):
    # TODO: 열(4번)을 반복하는 for문 한 줄을 작성하시오.
        print('*', end='')
    print()
```

---

### Q5. Code 2. 줄바꿈 없이 출력하기

아래 코드에서 주석 위치에 들어갈 **print 한 줄**을 작성하세요.

- 별(*)을 출력하되 줄바꿈을 하면 안 된다.

```c
for j in range(5):
    # TODO: 줄바꿈 없이 별(*)을 출력하시오.
print()
```

---

### Q6. Code 3. 한 행 출력 후 줄바꿈

아래 코드에서 주석 위치에 들어갈 **줄바꿈 한 줄**을 작성하세요.

- 내부 반복문이 끝난 뒤에 한 번만 줄바꿈한다.

```c
for i in range(2):
    for j in range(3):
        print('*', end='')
    # TODO: 여기에서 줄바꿈을 하시오.
```

---

### Q7. Code 4. 숫자를 한 줄에 이어서 출력

아래 코드는 1부터 5까지를 한 줄에 이어서 출력하려고 합니다.
주석 위치에 들어갈 **print 한 줄**을 작성하세요.

- 숫자는 서식문자(%)를 사용해 출력한다.

출력:
```
12345
```

```c
for j in range(1, 6):
    # TODO: 줄바꿈 없이 j를 출력하시오.
print()
```

---

### Q8. Code 5. n×n 별 정사각형(외부 for문)

정수 n을 입력받아 n×n 별 정사각형을 출력하려고 합니다.
주석 위치에 들어갈 **외부 for문 한 줄**을 작성하세요.

- 문자열 반복(곱셈)은 사용하지 않는다.

예: n=3일 때 출력
```
***
***
***
```

```c
n = int(input())
# TODO: n행을 반복하는 for문 한 줄을 작성하시오.
    for j in range(n):
        print('*', end='')
    print()
```

---

### Q9. Code 6. n×n 별 정사각형(내부 for문)

정수 n을 입력받아 n×n 별 정사각형을 출력하려고 합니다.
주석 위치에 들어갈 **내부 for문 한 줄**을 작성하세요.

- 문자열 반복(곱셈)은 사용하지 않는다.

예: n=3일 때 출력
```
***
***
***
```

```c
n = int(input())
for i in range(n):
    # TODO: n열을 반복하는 for문 한 줄을 작성하시오.
        print('*', end='')
    print()
```

---
