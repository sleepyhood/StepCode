---
id: "py_lv09_nfor_challenge_r01"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_nfor"
title: "Python 중첩 for문 LV09 챌린지 1회차"
round: 1
difficulty: "challenge"
status: "active"
audience: "common"
printDefault: true
---
# Python 중첩 for문 LV09 챌린지 1회차

### Q1. MCQ 1. 테두리만 별로 출력

다음 출력 결과와 **같이 출력**하는 Python 코드를 고르세요.
(공백도 반복문으로 출력한다, 문자열 반복(곱셈) 금지)

예: N=3, M=4일 때 출력
```
****
*  *
****
```

- **A**: n, m = map(int, input().split()) for i in range(n):     for j in range(m):         if i == 0 or i == n - 1 or j == 0 or j == m - 1:             print('*', end='')         else:             print(' ', end='')     print()
- **B**: n, m = map(int, input().split()) for i in range(n):     for j in range(m):         if i == 0 and i == n - 1 and j == 0 and j == m - 1:             print('*', end='')         else:             print(' ', end='')     print()
- **C**: n, m = map(int, input().split()) for i in range(n):     for j in range(m):         if i == 0 or i == n - 1 or j == 0 or j == m - 1:             print('*')         else:             print(' ')     print()
- **D**: n, m = map(int, input().split()) for i in range(m):     for j in range(n):         if i == 0 or i == n - 1 or j == 0 or j == m - 1:             print('*', end='')         else:             print(' ', end='')     print()

---

### Q2. MCQ 2. X 모양 출력

다음 출력 결과와 **같이 출력**하는 Python 코드를 고르세요.
(조건식은 i==j 또는 i+j==N-1 을 활용한다.)

예: N=5일 때 출력
```
*...*
.*.*.
..*..
.*.*.
*...*
```

- **A**: n = int(input()) for i in range(n):     for j in range(n):         if i == j and i + j == n - 1:             print('*', end='')         else:             print('.', end='')     print()
- **B**: n = int(input()) for i in range(n):     for j in range(n):         if i == j or i + j == n - 1:             print('*', end='')         else:             print('.', end='')     print()
- **C**: n = int(input()) for i in range(n):     for j in range(n):         if i == j or i + j == n - 1:             print('*')         else:             print('.')     print()
- **D**: n = int(input()) for i in range(n):     for j in range(n - 1):         if i == j or i + j == n - 1:             print('*', end='')         else:             print('.', end='')     print()

---

### Q3. Short 1. 테두리 별 개수

N=4, M=5일 때 테두리만 별(*)로 출력하는 사각형에서 출력되는 별의 총 개수를 쓰시오.

```c
N=4, M=5
(테두리만 '*', 내부는 공백)
```

---

### Q4. Code 1. 테두리 조건식

테두리만 별(*)을 출력하려고 합니다.
주석 위치에 들어갈 **if 조건식 한 줄**을 작성하세요.

- (i가 첫/마지막 행) 또는 (j가 첫/마지막 열) 이면 테두리이다.

예: N=3, M=4일 때 출력
```
****
*  *
****
```

```c
n, m = map(int, input().split())
for i in range(n):
    for j in range(m):
        # TODO: 테두리인지 판단하는 if 조건식을 작성하시오.
            print('*', end='')
        else:
            print(' ', end='')
    print()
```

---

### Q5. Code 2. 내부 출력(공백)

테두리 출력 코드에서 내부(테두리가 아닌 곳)는 공백을 출력해야 합니다.
주석 위치에 들어갈 **print 한 줄**을 작성하세요.

```c
if False:
    print('*', end='')
else:
    # TODO: 공백 한 칸을 줄바꿈 없이 출력하시오.
```

---

### Q6. Code 3. X 모양 조건식

N×N에서 X 모양을 출력하려고 합니다.
주석 위치에 들어갈 **if 조건식 한 줄**을 작성하세요.

- 두 대각선: i==j 또는 i+j==N-1

예: N=5일 때 출력
```
*...*
.*.*.
..*..
.*.*.
*...*
```

```c
n = int(input())
for i in range(n):
    for j in range(n):
        # TODO: X 모양 위치인지 판단하는 if 조건식을 작성하시오.
            print('*', end='')
        else:
            print('.', end='')
    print()
```

---

### Q7. Code 4. 1부터 증가하는 카운터 증가

아래 코드는 1부터 N×M까지 숫자를 차례대로 출력하려고 합니다.
주석 위치에 들어갈 **증가 한 줄**을 작성하세요.

예: N=2, M=3일 때 출력
```
1 2 3
4 5 6
```

```c
n, m = map(int, input().split())
cnt = 1
for i in range(n):
    for j in range(m):
        print('%d ' % cnt, end='')
        # TODO: cnt를 1 증가시키시오.
    print()
```

---

### Q8. Code 5. 체스판 패턴 조건식

정수 N을 입력받아 N×N 크기의 체스판 패턴을 출력합니다.
(i+j)가 짝수이면 1, 홀수이면 0을 출력합니다.
주석 위치에 들어갈 **if 조건식 한 줄**을 작성하세요.

예: N=4일 때 출력
```
1010
0101
1010
0101
```

```c
n = int(input())
for i in range(n):
    for j in range(n):
        # TODO: (i+j)가 짝수인지 판단하는 조건식을 작성하시오.
            print('1', end='')
        else:
            print('0', end='')
    print()
```

---

### Q9. Code 6. 곱셈표 한 칸 출력(서식문자 사용)

아래는 N×N 곱셈표를 출력하는 코드의 일부입니다.
주석 위치에 들어갈 **print 한 줄**을 작성하세요.

- (i+1)×(j+1) 값을 출력한다.
- 값 뒤에 공백 1개를 붙인다.

예: N=3일 때 출력
```
1 2 3
2 4 6
3 6 9
```

```c
n = int(input())
for i in range(n):
    for j in range(n):
        # TODO: (i+1)*(j+1) 값을 공백과 함께 출력하시오.
    print()
```

---
