# Python Contest Week 12 Problem Set

## 주차 주제
- 종합 모의 + 해설 + 피드백

## 실전 문제 묶음
- 아래 문항은 출처 원문에서 주차 목표에 맞게 선별한 실제 문제이다.

### PY_1회차
- 문항: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25

#### 문제 1
1. 다음은 파이썬 모듈에 대한 설명이다. 올바르지 않게 짝지어 진 것을 고르시오. [중고]
⓵ datetime – 날짜를 다루기 위한 모듈
⓶ math – 수학과 관련된 함수가 포함된 모듈
⓷ os – 환경변수나 디렉터리 등을 제어하는 모듈
⓸ pickle – 특정 디렉터리에 있는 파일 이름을 모두 알아야 할 때 사용하는 모듈
⓹ traceback – 프로그램 실행 중 발생한 오류를 추적하는 모듈

---

#### 문제 2
2. 다음 중 os 모듈에 정의되어 있지 않은 함수를 고르시오. [초]
⓵ getid
⓶ setregid
⓷ read
⓸ chdir
⓹ seekid

---

#### 문제 3
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

---

#### 문제 4
4. 다음 코드의 실행 결과로 올바른 것을 고르시오. (단, 띄어쓰기는 _로 표시한다.) [초중]
```python
print("A{:-7d}30{:6s}A".format(2023, "KITPA"))
```
⓵ A___2023KITPA_A
⓶ A2023___30_KITPAA
⓷ A2023___30KITPA_A
⓸ A___2023_KITPA_A
⓹ A___202330KITPAA

---

#### 문제 5
5. 다음 중 함수의 정의 시 사용하는 키워드와 함수 내에서 전역변수 임을 선언하는 키워드로 올바른 것을 고르시오. [초중고]

⓵ func, global
⓶ func, local
⓷ func, static
⓸ def, global
⓹ def, static

---

#### 문제 6
6. 다음 중 a 변수에 87.362가 저장되어있다고 할 때,
87.4를 출력하는 올바른 코드를 고르시오. [초고]

⓵ print(round(a, -1))
⓶ print(round(a))
⓷ print(round(a, 1))
⓸ print(round(a, 2))
⓹ print(round(a, 3))

---

#### 문제 7
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

---

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

#### 문제 9
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

---

#### 문제 10
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

---

#### 문제 11
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

---

#### 문제 12
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

---

#### 문제 13
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

---

#### 문제 14
14. 다음 중 리스트의 중간에 특정 위치에 요소를 하나 삽입
할 때 사용하는 함수로 올바른 것을 고르시오. [초중]
⓵ append
⓶ insert
⓷ pop
⓸ extend
⓹ remove

---

#### 문제 15
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

---

#### 문제 16
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

#### 문제 18
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

---

#### 문제 19
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

---

#### 문제 20
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
                break
        i += 1
        if not u:
            i += p
            r -= p - 1
    else:
        i += 1
print(r)
```

---

#### 문제 23
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

#### 문제 25
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

---

### PY_2회차
- 문항: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21

#### 문제 1
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

---

#### 문제 2
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

---

#### 문제 3
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

---

#### 문제 4
4. collections 모듈은 파이썬의 범용 내장 컨테이너에 대한 대안을 제공하는 특수 컨테이너가 구현되어 있는 모듈입니다. 이 모듈의 컬렉션들이 구현하고 있는 파이썬 내장 컨테이너가 아닌 것을 고르시오. [초, 중, 고]
⓵ list
⓶ dict
⓷ set
⓸ str
⓹ tuple

---

#### 문제 5
5. 다음 프로그램의 실행 결과에서 None 을 출력하지 않는 줄은 몇 번 줄인가? [초, 중, 고]
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

---

#### 문제 6
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

---

#### 문제 7
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

---

#### 문제 8
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

---

#### 문제 9
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
⓸ 181
⓹ 237

---

#### 문제 10
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

---

#### 문제 11
11. datetime 의 strftime 함수는 날짜 데이터를 형식을 통해 출력할 수 있도록 도와주는 함수입니다. 다음 중 형식과 그 예시가 올바르게 짝지어지지 않은 것을 고르시오. [초, 중, 고]
⓵ `%a`- Mon
⓶ `%B`- February
⓷ `%M`- 03
⓸ `%Z`- AM
⓹ `%Y`- 2024

---

#### 문제 12
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

---

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

#### 문제 14
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

---

#### 문제 15
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
⓶ 1, 2, 3, 4, 5
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

#### 문제 19
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

---

#### 문제 20
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
- 문항: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16

#### 문제 1
1. 다음 프로그램의 실행 결과는 무엇인가? [초,중,고]
```python
a = 0
for i in range(1, 30, 2):
    for j in range(2, 20, 3):
        a += 1
print(a)
```
⓵ 30
⓶ 60
⓷ 90
⓸ 120
⓹ 150

---

#### 문제 2
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

---

#### 문제 3
3. 다음 프로그램의 실행 결과는 무엇인가? [초, 중, 고]
```python
a = 1
i = 1
while True:
    if i > 10:
        break
    i += 2
    a *= 3
print(a)
```
⓵ 9
⓶ 27
⓷ 81
⓸ 243
⓹ 729

---

#### 문제 4
4. collections 모듈은 파이썬의 범용 내장 컨테이너에 대한 대안을 제공하는 특수 컨테이너가 구현되어 있는 모듈입니다. 이 모듈의 컬렉션들이 구현하고 있는 파이썬 내장 컨테이너가 아닌 것을 고르시오. [초, 중, 고]
⓵ list
⓶ dict
⓷ set
⓸ str
⓹ tuple

---

#### 문제 5
5. 다음 프로그램의 실행 결과에서 None 을 출력하지 않는 줄은 몇 번 줄인가? [초, 중, 고]
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

---

#### 문제 6
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

---

#### 문제 7
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

---

#### 문제 8
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

---

#### 문제 9
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

---

#### 문제 10
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

---

#### 문제 11
11. 다음 프로그램의 실행 결과는 무엇인가? [초,중,고]
```python
a, b, c = [], [], []
d = 0
for i in range(3):
    a.append(i + 1)
    b.append(i * 2)
    c.append(i * (i + 1))
for i in range(3):
    for j in range(3):
        for k in range(3):
            if k % 2 == 0:
                d += a[i] + b[j] + c[k]
            else:
                d -= a[i] + b[j] + c[k]
print(d)
```

⓵ 36
⓶ 48
⓷ 60
⓸ 72
⓹ 84

---

#### 문제 12
12. 다음 프로그램의 실행 결과는 무엇인가? [초]
```python
a = [13, 8, 7, 11]
b = [2, 15, 3, 12]
c = 0
for i in a:
    for j in b:
        if i + j > c:
            c = i + j
print(c)
``` 
⓵ 15
⓶ 23
⓷ 25
⓸ 26
⓹ 28

---

#### 문제 13
13. 다음 프로그램의 실행 결과는 무엇인가? [초,중]
```python
a = 0
for i in range(1, 10):
    for j in range(10):
        for k in range(10):
            if i == k or j == k: continue
            if int(str(i)+str(j)) * k == int(f"{j}{i}"):
                print(k)
                a = 1
                break
        if a == 1: break
    if a == 1: break
```
⓵ 1
⓶ 3
⓷ 5
⓸ 7
⓹ 9

---

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

#### 문제 15
15. 다음 프로그램의 실행 결과는 무엇인가? [초]
```python
def f():
    global a, b
    i = 0
    j = 0
    while i < len(a) - 1:
        if a[i] != a[i+1]:
        b = b[:j] + a[i] + b[j+1:]
        j += 1
    i += 1
a = "aaabbccccdefffff"
b = ""
f()
print(b)
```

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


