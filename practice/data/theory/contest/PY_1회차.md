# 2023 청소년 IT 경시대회 Python 문제지 (Markdown)


## 문제 1

1. 다음은 파이썬 모듈에 대한 설명이다. 올바르지 않게 짝지어 진 것을 고르시오. [중고]
⓵ datetime – 날짜를 다루기 위한 모듈
⓶ math – 수학과 관련된 함수가 포함된 모듈
⓷ os – 환경변수나 디렉터리 등을 제어하는 모듈
⓸ pickle – 특정 디렉터리에 있는 파일 이름을 모두 알아야 할 때 사용하는 모듈
⓹ traceback – 프로그램 실행 중 발생한 오류를 추적하는 모듈

## 문제 2

2. 다음 중 os 모듈에 정의되어 있지 않은 함수를 고르시오. [초]
⓵ getpid
⓶ setregid
⓷ read
⓸ chdir
⓹ seekid

## 문제 3

3. 다음 코드의 실행 결과로 올바른 것을 고르시오. [초중고]
```python
s = -20
s += 1
s %= 5
print(s)
```
⓵ -1
⓶ 0
⓷ 1
⓸ 2
⓹ 오류가 발생한다.

## 문제 4

4. 다음 코드의 실행 결과로 올바른 것을 고르시오. (단, 띄어쓰기는 _로 표시한다.) [초중]
```python
print("A{:-7d}30{:6s}A".format(2023, "KITPA"))
```
⓵ A___2023KITPA_A
⓶ A2023___30_KITPAA
⓷ A2023___30KITPA_A
⓸ A___2023_KITPA_A
⓹ A___202330KITPAA

## 문제 5

5. 다음 중 함수의 정의 시 사용하는 키워드와 함수 내에서 전역변수 임을 선언하는 키워드로 올바른 것을 고르시오. [초중고]

⓵ func, global
⓶ func, local
⓷ func, static
⓸ def, global
⓹ def, static


## 문제 6

6. 다음 중 a 변수에 87.362가 저장되어있다고 할 때,
87.4를 출력하는 올바른 코드를 고르시오. [초고]

⓵ print(round(a, -1))
⓶ print(round(a))
⓷ print(round(a, 1))
⓸ print(round(a, 2))
⓹ print(round(a, 3))

## 문제 7

7. 다음 코드의 실행 결과로 올바른 것을 고르시오. [고]
```python
ans = ""
if "False":
    ans += "1"
if []:
    ans += "2"
if -10:
    ans += "3"
if 0:
    ans += "4"
if 3.14:
    ans += "5"
print(ans)
```

⓵ 1
⓶ 35
⓷ 125
⓸ 135
⓹ 1345

## 문제 8

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



## 문제 9

9. 다음 코드의 실행 결과로 올바른 것을 고르시오. [초]
```python
p = 5
for i in range(3, 35, 2):
    p += 2
print(p)
```
⓵ 35
⓶ 36
⓷ 37
⓸ 38
⓹ 39


## 문제 10

10. 다음 코드의 실행 결과로 올바른 것을 고르시오. [초중]
```python
a = 88
b = 132
while b > 0:
    c = a % b
    a = b
    b = c
print(a)
```
⓵ 11
⓶ 22
⓷ 44
⓸ 66
⓹ 88

## 문제 11

11. 다음 코드의 실행 결과로 올바른 것을 고르시오. [초중고]
```python
a = [6, 1, 5, 0, 2, 3, 4]
for i in range(5):
    b = i
    for j in range(1, 30):
    b = a[b]
    print(b, end=' ')
```
⓵ 3 1 4 5 6 
⓶ 6 2 3 4 1
⓷ 1 0 4 5 2 
⓸ 5 0 2 3 1
⓹ 4 2 1 5 3

## 문제 12

12. 다음 코드의 실행 결과로 올바른 것을 고르시오. [중고]
```python
a = []
b = []
s = 0
for i in range(6):
    a.append(i)
    b.append(a[i]*2-4)
for i in range(6):
    for j in range(6):
        s += a[i] * b[j]
print(s//2)
```
⓵ 30
⓶ 45
⓷ 60
⓸ 75
⓹ 90


## 문제 13

13. 다음 코드의 실행 결과로 올바른 것을 고르시오. [중고]
```python
n, m, k, a = 3, 10, 15, 1
while k > 0:
    if k % 2 == 1:
        a *= n
        a %= m
    n = (n * n) % m
    k //= 2
print(a)
```
⓵ 1
⓶ 3
⓷ 5
⓸ 7
⓹ 9

## 문제 14

14. 다음 중 리스트의 중간에 특정 위치에 요소를 하나 삽입
할 때 사용하는 함수로 올바른 것을 고르시오. [초중]
⓵ append
⓶ insert
⓷ pop
⓸ extend
⓹ remove


## 문제 15

15. 다음 코드의 실행 결과로 올바른 것을 고르시오. [초중]
```python
def f(m, n):
    if m == 0 or n == 0:
        return 1
    else:
        return f(m-1, n) + f(m-1, n-1) + f(m, n-1)
print(f(2, 5))
```
⓵ 25 
⓶ 41 
⓷ 61
⓸ 85 
⓹ 231

## 문제 16

16. 다음 코드의 실행 결과로 올바른 것을 고르시오. [초중고]
```python
a, b, c = [], [], []
d = 0
for i in range(3):
    a.append(i+2)
    b.append(i*4)
    c.append(i*i)
for i in range(3):
    for j in range(3):
        for k in range(3):
            d += a[i] + b[j] * c[k]
print(d)
```
⓵ 234
⓶ 261
⓷ 297
⓸ 1089
⓹ 1116

## 문제 17

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



## 문제 18

18. 실행 결과로 올바른 것을 고르시오. [초중고]
```python
f = lambda x: eval((str(x).replace("q","4")+"*"+(str(x).replace("q","4"))))
print(f("q"), f("q+1"), f("q+q"))
```
⓵ 16 25 64
⓶ 16 16 16
⓷ 16 9 24
⓸ 16 25 24
⓹ 오류가 발생한다.

## 문제 19

19. 아래 코드의 입력이 다음과 같을 때 실행 결과로 올바른
것을 고르시오. [초중고]

<다음>
5
programming
hoolly
clanguage
engineeriing
kitpa

```python
t = int(input())
mx = -1
b = ''
for i in range(t):
    cnt = 0
    a = input()
    c = a[0]
for j in range(1, len(a)):
    if c == a[j] and c in "aeiou":
        cnt += 1
    else:
        c = a[j]
    if mx < cnt:
        mx = cnt
        b = a
print(b)
```
⓵ programming
⓶ hoolly
⓷ clanguage
⓸ engineeriing
⓹ kitpa

## 문제 20


20. 아래 코드의 입력이 다음과 같을 때 실행 결과로 올바
른 것을 고르시오. [초고]

<다음>
3
2 5
300 350
3 7
1200 3500 200
5 10
200 300 250 800 200

```python
F = lambda A, B: A if A > B else B
G = lambda A, B: A + B
t = int(input())
p = 0
while t:
    t -= 1
    m = 0
    n, s = map(int, input().split())
    k = list(map(int, input().split()))
    for i in range(n-1, -1, -1):
        m = F(m, k[i])
    p = G(p, (m*s+999)//1000)
print(p)
```
⓵ -34 
⓶ 0 
⓷ 34 
⓸ 35 
⓹ 96

## 문제 21

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

#### 문제 22
22. 아래 프로그램에 <입력 1>과 <입력 2>를 입력했을 때 출력되는 값의 합을 작성하시오. [초중]

<입력 1>
savefromtheavalanche av
<입력 2>
thathathathhtat tha

```python
s, t = input().split()
r = len(s)
p = len(t)
i = 0
while i <= len(s)-p:
    j, u = 0, 0
    if s[i] == t[j]:
        for j in range(1, p):
            if s[i+j] != t[j]:
                u = 1
                i += 1
                break
        
        if not u:
            i += p
            r -= p - 1
    else:
        i += 1
print(r)
```

## 문제 23

23. 아래 프로그램에 <입력>를 입력했을 때 출력되는 값을
작성하시오. [초중고]

<입력>
7
3 10
5 2
10 3
9 5
8 3
2 6
4 4

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
n = int(input())
s = 0
p = [Point(0, 0)]
for i in range(n):
    a, b = map(int, input().split())
    p.append(Point(a, b))

p.append(Point(0, 0))
p.sort(key = lambda a: (a.x, a.y))

for i in range(1, n+1):
    tmp = 1000
    if p[i-1].y == p[i].y:
        tmp = p[i].x - p[i-1].x
    if p[i].y == p[i+1].y:
        tmp = min(tmp, p[i+1].x - p[i].x)
    s += 0 if tmp == 1000 else tmp
print(s)
```

## 문제 24

24. 다음 코드의 실행 결과로 올바른 값을 작성하시오. [중고]
```python
a = [7, 890, 1, 234, 5678, 901, 23, 45, 6]
cnt = 0
for i in a:
    b = (i & 1) | (i & 2)
    if b > 0: cnt += 1
print(cnt)
```

## 문제 25

25. 다음 코드의 실행 결과로 올바른 값을 작성하시오. [고]

```python
def f(x, y, p, a):
    if x < 0 or y < 0: return 0
    if x >= 4 or y >= 4: return 0
    if a[x][y]: return 0
    if x == 3 and y == 3:
        return p + 1
    a[x][y] = 1
    k = 0
    for i in range(3):
        k += f(x + i//2, y + i//2, p, a)
    a[x][y] = 0
    return k

print(f(0, 0, 0,[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]))
```