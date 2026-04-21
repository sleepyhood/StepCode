---
id: "py_lv09_nfor_basic_r02"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_nfor"
title: "Python 중첩 for문 LV09 기초 2회차"
round: 2
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python 중첩 for문 LV09 기초 2회차

### Q1. MCQ 1. N행 M열 별 사각형(입력)

다음 출력 결과와 **같이 출력**하는 Python 코드를 고르세요.
(문자열 반복(곱셈)은 사용하지 않는다.)

예: N=2, M=3일 때 출력
```
***
***
```

- **A**: n, m = map(int, input().split()) for i in range(m):     for j in range(n):         print('*', end='')     print()
- **B**: n, m = map(int, input().split()) for i in range(n):     for j in range(m):         print('*', end='')     print()
- **C**: n, m = map(int, input().split()) for i in range(n):     for j in range(m):         print('*')     print()
- **D**: n, m = map(int, input().split()) for i in range(n):     for j in range(m):         print('*', end='')

---

### Q2. MCQ 2. 높이 N 삼각형(입력)

다음 출력 결과와 **같이 출력**하는 Python 코드를 고르세요.
(문자열 반복(곱셈)은 사용하지 않는다.)

예: N=4일 때 출력
```
*
**
***
****
```

- **A**: n = int(input()) for i in range(1, n):     for j in range(i):         print('*', end='')     print()
- **B**: n = int(input()) for i in range(1, n + 1):     for j in range(i):         print('*', end='')     print()
- **C**: n = int(input()) for i in range(n):     for j in range(i):         print('*', end='')     print()
- **D**: n = int(input()) for i in range(1, n + 1):     for j in range(i):         print('*')     print()

---

### Q3. Short 1. 별 개수(삼각형)

정수 N=4일 때, 아래 프로그램이 출력하는 별(*)의 총 개수를 쓰시오.

```c
n = 4
for i in range(1, n + 1):
    for j in range(i):
        print('*', end='')
    print()
```

---

### Q4. Code 1. N행을 반복하는 외부 for문

첫 줄에 N과 M을 입력받아 N행 M열 별 사각형을 출력합니다.
주석 위치에 들어갈 **외부 for문 한 줄**을 작성하세요.

예: N=2, M=3일 때 출력
```
***
***
```

```c
n, m = map(int, input().split())
# TODO: n행을 반복하는 for문 한 줄을 작성하시오.
    for j in range(m):
        print('*', end='')
    print()
```

---

### Q5. Code 2. M열을 반복하는 내부 for문

첫 줄에 N과 M을 입력받아 N행 M열 별 사각형을 출력합니다.
주석 위치에 들어갈 **내부 for문 한 줄**을 작성하세요.

예: N=2, M=3일 때 출력
```
***
***
```

```c
n, m = map(int, input().split())
for i in range(n):
    # TODO: m열을 반복하는 for문 한 줄을 작성하시오.
        print('*', end='')
    print()
```

---

### Q6. Code 3. i번째 줄에 i개 출력(내부 for문)

정수 N을 입력받아 왼쪽 직각삼각형을 출력합니다.
주석 위치에 들어갈 **내부 for문 한 줄**을 작성하세요.

- 1번째 줄: 1개, ..., N번째 줄: N개

예: N=3일 때 출력
```
*
**
***
```

```c
n = int(input())
for i in range(1, n + 1):
    # TODO: i번 반복하는 for문 한 줄을 작성하시오.
        print('*', end='')
    print()
```

---

### Q7. Code 4. 역삼각형(내부 for문)

정수 N을 입력받아 역삼각형을 출력합니다.
주석 위치에 들어갈 **내부 for문 한 줄**을 작성하세요.

- 1번째 줄: N개, 2번째 줄: N-1개, ..., N번째 줄: 1개

예: N=3일 때 출력
```
***
**
*
```

```c
n = int(input())
for i in range(n, 0, -1):
    # TODO: i번 반복하는 for문 한 줄을 작성하시오.
        print('*', end='')
    print()
```

---

### Q8. Code 5. 행 번호를 출력(서식문자 사용)

정수 N을 입력받아 N×N 숫자 사각형을 출력합니다.
i번째 행(1부터 시작)에는 숫자 i를 N번 출력합니다.
주석 위치에 들어갈 **print 한 줄**을 작성하세요.

- 숫자는 서식문자(%)를 사용한다.
- 숫자 사이에는 공백 1개를 둔다.

예: N=3일 때 출력
```
1 1 1
2 2 2
3 3 3
```

```c
n = int(input())
for i in range(1, n + 1):
    for j in range(n):
        # TODO: i를 공백과 함께 출력하시오.
    print()
```

---

### Q9. Code 6. 열 번호를 출력(서식문자 사용)

정수 N을 입력받아 N×N 숫자 사각형을 출력합니다.
각 행은 1 2 3 ... N 형태로 출력합니다.
주석 위치에 들어갈 **print 한 줄**을 작성하세요.

- 숫자는 서식문자(%)를 사용한다.
- 숫자 사이에는 공백 1개를 둔다.

예: N=3일 때 출력
```
1 2 3
1 2 3
1 2 3
```

```c
n = int(input())
for i in range(n):
    for j in range(1, n + 1):
        # TODO: j를 공백과 함께 출력하시오.
    print()
```

---
