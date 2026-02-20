# Python Contest Week 11 Problem Set

## 주차 주제
- 비트연산/진수, 2차원 배열, 탐색

## 실전 문제 묶음
- 아래 문항은 출처 원문에서 주차 목표에 맞게 선별한 실제 문제이다.

### PY_1회차
- 문항: 8, 17, 21, 24

#### 문제 8
8. 다음 중 아래 코드의 빈 칸에 넣었을 때 출력 결과가 다
른 값을 고르시오. [고]
```python
print([빈 칸])
```
⓵ 9 * 8
⓶ 37 ^ 109
⓷ 9 << 3
⓸ (2 ^ 3) * (3 ^ 2)
⓹ (36 if 7*3 else 21)*2

---

#### 문제 17
17. 다음 코드의 실행 결과로 올바른 것을 고르시오. [초중고]
```python
def f(v):
    if v > 0: return v
    else: return -v
a = [[10, 2], [0, 5]]
t = [[0, 0], [0, 0]]
n = 8
for m in range(n):
    for i in range(2):
        for j in range(2):
            for k in range(2):
                t[i][j] += a[i][k] * a[k][j]
p = f(t[0][0] * t[0][1] - t[1][0] * t[1][1]) % 5
print(p)
```
⓵ 0
⓶ 1
⓷ 2
⓸ 3
⓹ 4

---

#### 문제 21
21. 다음 코드의 실행 결과로 올바른 것을 고르시오. [초고]

```python
n, m, cnt = 6, 6, 0
a = ["....@@",
"@@...@",
".@.@@.",
"@@.@.@",
"@@..@@",
"......"]
for i in range(n):
    for j in range(1, m):
        if a[i][j-1] != a[i][j]:
            cnt += 1

for i in range(n-1):
    if i % 2 == 0:
    for j in range(1, m):
            if a[i][j] != a[i+1][j-1]:
                cnt += 1
    else:
        for j in range(m):
            if a[i][j] != a[i+1][j]:
                cnt += 1

for i in range(n-1):
    if i % 2 == 0:
    for j in range(m):
            if a[i][j] != a[i+1][j]:
                cnt += 1
    else:
        for j in range(m-1):
            if a[i][j] != a[i+1][j+1]:
                cnt += 1
print(cnt % 5)
```
⓵ 0 
⓶ 1 
⓷ 2
⓸ 3 
⓹ 4

---

#### 문제 24
24. 다음 코드의 실행 결과로 올바른 값을 작성하시오. [중고]
```python
a = [7, 890, 1, 234, 5678, 901, 23, 45, 6]
cnt = 0
for i in a:
    b = (i & 1) | (i & 2)
    if b > 0: cnt += 1
print(cnt)
```

---

### PY_2회차
- 문항: 13, 16, 17, 18, 21

#### 문제 13
13. 다음 프로그램의 실행 결과에서 제일 오른쪽에 연속으로 나타나는 0 의 개수는 몇 개 인지 고르시오. [초, 중, 고]
```python
a = 1
for i in range(1, 11):
    a *= i
print('%o' % a)
```
⓵ 1개
⓶ 2개
⓷ 3개
⓸ 4개
⓹ 5개

---

#### 문제 16
16. 다음 프로그램의 빈 칸에 값을 넣었을 때 실행 결과가 1 인 것을 고르시오. [초, 중, 고]
```python   
a = [ ]
b = 0
for i in range(len(a)):
    b ^= a[i]
print(b)
```
⓵ 0, 1, 2, 3, 4
⓶ 1, 2, 3, 4, 6
⓷ 1, 3, 1, 3, 1
⓸ 0, 0, 0, 1, 1
⓹ 10, -10, 10, -10, 10

---

#### 문제 17
17. 다음 프로그램의 실행 결과가 <보기>와 같을 때, 빈 칸
에 들어갈 코드로 올바른 것을 고르시오. [초, 중, 고]
```python
a = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
for i in range(3):
    for j in range(3):
        print(빈칸, end=' ')
    print()
```
```text
<보기>
6 3 0
7 4 1
8 5 2
```
⓵ a[2-i][j]
⓶ a[i][2-j]
⓷ a[j][2-i]
⓸ a[i][j]
⓹ a[2-j][i]

---

#### 문제 18
18. 다음 프로그램의 실행 결과는 무엇인가? [초, 중, 고]
```python 
def f(v):
    if v > 0: return v
    else: return -v

a = [[10, 2], [0, 5]]
t = [[0, 0], [0, 0]]
n = 8
for m in range(n):
    for i in range(2):
        for j in range(2):
            for k in range(2):
                t[i][j] += a[i][k] * a[k][j]
p = f(t[0][0] * t[0][1] - t[1][0] * t[1][1]) % 5
print(p)
```
⓵ 0
⓶ 1
⓷ 2
⓸ 3
⓹ 4

---

#### 문제 21
21. 다음 프로그램의 입력이 아래와 같을 때 실행 결과는 무엇인가? [고]

```text
<입력>
5 100 3
1 1 1 0 0
1 0 1 0 0
0 0 1 1 1
1 1 0 0 0
0 1 1 0 1
```
```python
mapp = [[]]
f = 0
dy = [-1, 0, 1, 0]
dx = [0, -1, 0, 1]
def func2(y, x):
    if 1 <= y <= n and 1 <= x <= n:
        return 1
    else:
        return 0

def func(y, x):
    global mapp, dy, dx
    global f
    mapp[y][x] = f
    qy = [0 for _ in range(200)]
    qx = [0 for _ in range(200)]
    qs, qe = 0, 0

    qy[qe] = y
    qx[qe] = x
    qe += 1

    while qs != qe:
        qsy = qy[qs]
        qsx = qx[qs]
        qs += 1
        for i in range(4):
            nxy = qsy + dy[i]
            nxx = qsx + dx[i]
            if func2(nxy, nxx) == 1 and mapp[nxy][nxx] == -1:
                mapp[nxy][nxx] = f
                qy[qe] = nxy
                qx[qe] = nxx
                qe += 1

n, m, k = map(int, input().split())
for i in range(1, n+1):
    row = [0] + list(map(int, input().split()))
    mapp.append(row)
    for j in range(1, n+1):
        if mapp[i][j] == 0:
            mapp[i][j] = -1
        else:
            mapp[i][j] = 0

for i in range(1, n+1):
    for j in range(1, n+1):
        if mapp[i][j] == -1:
            f += 1
            func(i, j)

fs = [0 for _ in range(110)]

for i in range(1, n+1):
    for j in range(1, n+1):
        if mapp[i][j] > 0:
            fs[mapp[i][j]] += 1

for i in range(1, f+1):
    m -= (fs[i] + k - 1) // k

if m >= 0 and f > 0:
    print(m)
else:
    print(-1)
```

---
### PY_3회차
- 문항: 14, 16

#### 문제 14
14. 다음 프로그램의 실행 결과는 무엇인가? [중,고]
```python
a = ["000100", "101101", "111111", "110100", "111011", "001110"]
b = 0
def f(p, q, r):
    global b
    if p < 0 or q < 0 or p >= 6 or q >= 6:
        return
    if a[p][q] == '0':
        return
    b += r
    
    a[p] = a[p][:q] + '0' + a[p][q+1:]
    f(p-1, q, r+1)
    f(p+1, q, r+1)
    f(p, q-1, r+1)
    f(p, q+1, r+1)

for i in range(6):
    for j in range(6):
        if ord(a[i][j]) == 49:
            f(i, j, 1)
print(b)
```
⓵ 141
⓶ 153
⓷ 162
⓸ 177
⓹ 185

---

#### 문제 16
16. 다음 프로그램의 실행 결과는 무엇인가? [고]
```text
<입력>
1 2
1 3
```

```python   
def f(mapp, x, y, number, dep, answer):
    if dep == 2:
    answer.add(number)
    return
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in dirs:
    nxtx, nxty = x + dx, y + dy
    if 0 <= nxtx < 2 and 0 <= nxty < 2:
    f(mapp, nxtx, nxty, number +
    mapp[nxtx][nxty], dep + 1, answer)

mapp = [input().split() for _ in range(2)]
answer = set()

for i in range(2):
    for j in range(2):
        f(mapp, i, j, mapp[i][j], 0, answer)
print(len(answer))
```

---


