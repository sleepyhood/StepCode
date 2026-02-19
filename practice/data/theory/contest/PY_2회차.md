# 2024 청소년 IT 경시대회 Python 문제지 (Markdown)


## 문제 1

1. 다음 프로그램의 실행 결과는 무엇인가? [고]
```python
a = 0
for i in range(100, 2024, 150):
    a += i
print(a)
```
⓵ 11500
⓶ 12000
⓷ 12500
⓸ 13000
⓹ 13500



## 문제 2

2. 다음 프로그램의 실행 결과는 무엇인가? [초]
```python
b = 0
for i in [1, 2, 3, 4, 5, 6, 7]:
    if i % 2 == 1:
        b += i
    if i % 3 == 1:
        b -= i
print(b)
```
⓵ -9
⓶ -4
⓷ 0
⓸ 4
⓹ 9

## 문제 3
3. 다음 프로그램의 실행 결과는 무엇인가? [초, 중, 고]
```python
a = 0
i = 0
while True:
    if i > 10:
        break
    i += 2
    a += 3
print(a)
```
⓵ 6
⓶ 9
⓷ 12
⓸ 15
⓹ 18


## 문제 4
4. collections 모듈은 파이썬의 범용 내장 컨테이너에 대한 대안을 제공하는 특수 컨테이너가 구현되어 있는 모듈입니다. 이 모듈의 컬렉션들이 구현하고 있는 파이썬 내장 컨테이너가 아닌 것을 고르시오. [초, 중, 고]
⓵ list
⓶ dict
⓷ set
⓸ str
⓹ tuple


## 문제 5

5. 다음 프로그램의 실행 결과에서 None 을 출력하지 않는
줄은 몇 번 줄인가? [초, 중, 고]
```python
import re
pattern = re.compile('o[gh]')
print(pattern.fullmatch('o'))
print(pattern.fullmatch('oh'))
print(pattern.fullmatch('dog'))
print(pattern.fullmatch('doggie'))
print(pattern.fullmatch('ogre'))
```

⓵ 1번 줄
⓶ 2번 줄
⓷ 3번 줄
⓸ 4번 줄
⓹ 5번 줄


## 문제 6
6. 다음 프로그램의 실행 결과는 무엇인가? [초, 중, 고]
```python
x = 12
y = 15
print(x+y if x>y else x*y)
```
⓵ 3
⓶ 12
⓷ 15
⓸ 27
⓹ 180

## 문제 7
7. 다음 프로그램의 실행 결과는 무엇인가? [초, 중]
```python
def f(a, b):
    if a == 1:
        return 1
    return b * f(a-1, b)

print(f(4, 6))
```
⓵ 216
⓶ 256
⓷ 1024
⓸ 1296
⓹ 4096

## 문제 8

8. 다음 프로그램에서 3 번재 줄에 출력되는 값은 무엇인가? [초]
```python
def f(a, b):
    if a == b:
        print(a)
        return
    c = (a + b) // 2
    f(a, c)
    f(c+1, b)

f(0, 7)
```
⓵ 1
⓶ 2
⓷ 3
⓸ 4
⓹ 5



## 문제 9

9. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]
```python
def f(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 8
    return f(n-1) + f(n-3)
print(f(10))
```
⓵ 51
⓶ 76
⓷ 110
⓸ 161
⓹ 237


## 문제 10
10. 다음 프로그램의 실행 결과는 무엇인가? [초]
```python
a = "apple"
b = 0
for i in range(5):
    for j in range(i):
        if a[i] != a[j]:
            b += 1
print(b)
```
⓵ 6
⓶ 7
⓷ 8
⓸ 9
⓹ 10

## 문제 11

11. datetime 의 strftime 함수는 날짜 데이터를 형식을 통해 출력할 수 있도록 도와주는 함수입니다. 다음 중 형식과 그 예시가 올바르게 짝지어지지 않은 것을 고르시오. [초, 중, 고]
⓵ `%a`- Mon
⓶ `%B`- February
⓷ `%M`- 03
⓸ `%Z`- AM
⓹ `%Y`- 2024

## 문제 12

12. 다음 프로그램의 빈 칸에 값을 넣었을 때 가장 큰 값을 가지는 코드를 고르시오. [고]
```python
def f(a):
    if a <= 0:
        return 0
    return (a % 7) * f(a // 7) + a % 7
print(f(빈칸))
``` 
⓵ 14
⓶ 89
⓷ 168
⓸ 223
⓹ 512

## 문제 13
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

## 문제 14

14. 다음 프로그램의 빈 칸에 값을 넣었을 때 가장 큰 값을
출력하는 코드를 고르시오.  [초, 중, 고]
```python
a = 0
def f(x):
    global a
    a += 1
    if x == 1:
        return
    if x & 1 == 0:
        f(x // 2)
    else:
        f(x * 3 + 1)
f(빈칸)
print(a)
```
⓵ 3
⓶ 5
⓷ 7
⓸ 9
⓹ 11

## 문제 15

15. 다음 프로그램의 실행 결과는 무엇인가? [초]
```python
f = lambda x: x + 1
a = 4
print(f(a), f(a)*f(a+1))
```
⓵ 4 16
⓶ 4 20
⓷ 4 24
⓸ 5 25
⓹ 5 30

## 문제 16
16. 다음 프로그램의 빈 칸에 값을 넣었을 때 실행 결과가 1 인 것을 고르시오. [초, 중, 고]
```python   
a = [ ]
b = 0
for i in range(len(a)):
    b ^= a[i]
print(b)
```
⓵ 0, 1, 2, 3, 4
⓶ 1, 2, 3, 4, 5
⓷ 1, 3, 1, 3, 1
⓸ 0, 0, 0, 1, 1
⓹ 10, -10, 10, -10, 10

## 문제 17

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

## 문제 18

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

## 문제 19
19. 다음 프로그램의 실행 결과는 무엇인가? [고]
```python
for i in range(1, 10):
    for j in range(10):
        if i == j: continue
        for k in range(10):
            if k in (i, j): continue
            for l in range(10):
                if l in (i, j, k): continue
                if int(str(i)+str(j)+str(k)+str(l)) * l == int(f"{l}{k}{j}{i}"):
                    print(l)
```
⓵ 1
⓶ 3
⓷ 5
⓸ 7
⓹ 9

## 문제 20
20. 다음은 파이썬에서 사용되는 함수들입니다. 설명을 읽고 어떤 함수에 대한 설명인지 순서대로 작성하시오. [초, 중, 고]
```text
<보기>
append capitalize clear copy encode endswith extend
get insert isalpha items pop remove upper zfill
```
1) 리스트의 뒤에 값을 1 개 추가
2) 문자열이 특정 접미사로 종료되는지 확인
3) 문자열의 왼쪽에 특정 길이만큼의 0을 주가
4) 딕셔너리에서 특정 키를 가지는 키-값 쌍 제거


## 문제 21

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