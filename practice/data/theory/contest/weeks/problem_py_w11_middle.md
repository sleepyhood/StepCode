# Python Contest Week 11 Middle Problem Set

## 범위
- 비트/XOR
- 2차원 배열 회전
- DFS/BFS 결과 추적

## 문제 1
다음 프로그램의 실행 결과가 1이 되는 빈 칸을 고르시오.
```python
a = [빈칸]
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

## 문제 2
다음 프로그램의 실행 결과가 보기와 같을 때, 빈 칸에 들어갈 코드로 올바른 것을 고르시오.
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

## 문제 3
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
다음 프로그램의 실행 결과는 무엇인가?
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

## 문제 5
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = 1
for i in range(1, 11):
    a *= i
print('%o' % a)
```
⓵ 15657400
⓶ 15767400
⓷ 15657440
⓸ 15657404
⓹ 15657411
