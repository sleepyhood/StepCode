# Python Contest Week 11 High Problem Set

## 범위
- BFS 영역 탐색
- 비트/배열 결합
- 2차원 재귀 탐색

## 문제 1
연계 개념: 개념 3) 팩토리얼 8진수 끝자리 0 개수
다음 프로그램의 입력이 아래와 같을 때 실행 결과는 무엇인가?

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
⓵ 90
⓶ 92
⓷ 94
⓸ 96
⓹ -1

## 문제 2
연계 개념: 개념 3) 팩토리얼 8진수 끝자리 0 개수
다음 코드의 실행 결과로 올바른 값을 고르시오.
```python
def f(mapp, x, y, number, dep, answer):
    if dep == 2:
        answer.add(number)
        return
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in dirs:
        nxtx, nxty = x + dx, y + dy
        if 0 <= nxtx < 2 and 0 <= nxty < 2:
            f(mapp, nxtx, nxty, number + mapp[nxtx][nxty], dep + 1, answer)

mapp = [['1', '2'], ['1', '3']]
answer = set()
for i in range(2):
    for j in range(2):
        f(mapp, i, j, mapp[i][j], 0, answer)
print(len(answer))
```
⓵ 12
⓶ 13
⓷ 14
⓸ 15
⓹ 16

## 문제 3
연계 개념: 개념 2) XOR 누적과 소거 성질
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
def f(v):
    if v > 0:
        return v
    return -v

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

## 문제 4
연계 개념: 개념 1) 비트 연산과 값 판별
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = [7, 890, 1, 234, 5678, 901, 23, 45, 6]
cnt = 0
for i in a:
    b = (i & 1) | (i & 2)
    if b > 0:
        cnt += 1
print(cnt)
```
⓵ 6
⓶ 7
⓷ 8
⓸ 9
⓹ 10

## 문제 5
연계 개념: 개념 1) 비트 연산과 값 판별
다음 중 아래 코드의 빈 칸에 넣었을 때 출력 결과가 다른 값을 고르시오.
```python
print([빈 칸])
```
⓵ 9 * 8
⓶ 37 ^ 109
⓷ 9 << 3
⓸ (2 ^ 3) * (3 ^ 2)
⓹ (36 if 7*3 else 21) * 2
