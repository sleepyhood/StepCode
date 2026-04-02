---
id: "py_lv09_nfor_basic_r03"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_nfor"
title: "Python 중첩 for문 LV09 기초 3회차"
round: 3
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python 중첩 for문 LV09 기초 3회차

### Q1. MCQ 1. 오른쪽 정렬 삼각형

다음 출력 결과와 **같이 출력**하는 Python 코드를 고르세요.
(공백도 반복문으로 출력한다, 문자열 반복(곱셈) 금지)

예: N=4일 때 출력
```
   *
  **
 ***
****
```

- **A**: n = int(input()) for i in range(n):     for j in range(n - i):         print(' ', end='')     for j in range(i + 1):         print('*', end='')     print()
- **B**: n = int(input()) for i in range(n):     for j in range(n - i - 1):         print(' ', end='')     for j in range(i + 1):         print('*', end='')     print()
- **C**: n = int(input()) for i in range(n):     for j in range(n - i - 1):         print('*', end='')     for j in range(i + 1):         print(' ', end='')     print()
- **D**: n = int(input()) for i in range(n):     for j in range(n - i - 1):         print(' ', end='')     for j in range(i):         print('*', end='')     print()

---

### Q2. MCQ 2. 가운데 정렬 피라미드

다음 출력 결과와 **같이 출력**하는 Python 코드를 고르세요.
(공백/별 모두 반복문으로 출력한다, 문자열 반복(곱셈) 금지)

예: N=3일 때 출력
```
  *
 ***
*****
```

- **A**: n = int(input()) for i in range(n):     for j in range(n - i - 1):         print(' ', end='')     for j in range(2 * i + 1):         print('*', end='')     print()
- **B**: n = int(input()) for i in range(n):     for j in range(n - i):         print(' ', end='')     for j in range(2 * i + 1):         print('*', end='')     print()
- **C**: n = int(input()) for i in range(n):     for j in range(n - i - 1):         print(' ', end='')     for j in range(2 * i - 1):         print('*', end='')     print()
- **D**: n = int(input()) for i in range(n):     for j in range(n - i - 1):         print('*', end='')     for j in range(2 * i + 1):         print(' ', end='')     print()

---

### Q3. Short 1. 공백과 별 개수

높이 N=5인 가운데 정렬 피라미드에서 i=2(0부터 시작)번째 줄에 출력되는
공백 개수와 별 개수를 순서대로 공백으로 구분해 쓰시오.
(예: 2 3)

```c
N = 5
# i = 2일 때: 공백 N-i-1개, 별 2*i+1개
```

---

### Q4. Code 1. 공백 반복(for문)

오른쪽 정렬 삼각형에서 i번째 줄의 공백을 출력하는 for문 한 줄을 작성하세요.

- 공백 개수는 n - i - 1개이다.

예: N=4일 때 출력
```
   *
  **
 ***
****
```

```c
n = int(input())
for i in range(n):
    # TODO: 공백(n - i - 1개)을 출력하는 for문 한 줄을 작성하시오.
        print(' ', end='')
    for j in range(i + 1):
        print('*', end='')
    print()
```

---

### Q5. Code 2. 별 반복(for문)

오른쪽 정렬 삼각형에서 i번째 줄의 별을 출력하는 for문 한 줄을 작성하세요.

- 별 개수는 i + 1개이다.

예: N=4일 때 출력
```
   *
  **
 ***
****
```

```c
n = int(input())
for i in range(n):
    for j in range(n - i - 1):
        print(' ', end='')
    # TODO: 별(i + 1개)을 출력하는 for문 한 줄을 작성하시오.
        print('*', end='')
    print()
```

---

### Q6. Code 3. 공백 출력(print)

가운데 정렬 피라미드를 출력하려고 합니다.
주석 위치에 들어갈 **공백 출력 print 한 줄**을 작성하세요.

```c
for j in range(3):
    # TODO: 공백 한 칸을 줄바꿈 없이 출력하시오.
```

---

### Q7. Code 4. 별 출력(print)

가운데 정렬 피라미드를 출력하려고 합니다.
주석 위치에 들어갈 **별 출력 print 한 줄**을 작성하세요.

```c
for j in range(5):
    # TODO: 별(*) 한 개를 줄바꿈 없이 출력하시오.
```

---

### Q8. Code 5. 피라미드 별 반복(for문)

가운데 정렬 피라미드에서 i번째 줄의 별 개수는 2*i+1개입니다.
주석 위치에 들어갈 **별 출력 for문 한 줄**을 작성하세요.

예: N=3일 때 출력
```
  *
 ***
*****
```

```c
n = int(input())
for i in range(n):
    for j in range(n - i - 1):
        print(' ', end='')
    # TODO: 별(2*i+1개)을 출력하는 for문 한 줄을 작성하시오.
        print('*', end='')
    print()
```

---

### Q9. Code 6. 오른쪽 정렬 숫자 삼각형(출력)

정수 N을 입력받아 오른쪽 정렬 숫자 삼각형을 출력합니다.
i번째 줄(1부터 시작): 공백 N-i개, 숫자 i를 i번 출력합니다.
주석 위치에 들어갈 **print 한 줄**을 작성하세요.

- 숫자는 서식문자(%)를 사용한다.
- 공백은 이미 출력되어 있다고 가정한다.

예: N=3일 때 출력
```
  1
 22
333
```

```c
n = int(input())
for i in range(1, n + 1):
    for j in range(n - i):
        print(' ', end='')
    for j in range(i):
        # TODO: i를 줄바꿈 없이 출력하시오.
    print()
```

---
