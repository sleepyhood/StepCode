# 2024 청소년 IT 경시대회 Python 문제지 (Markdown)


## 문제 1

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

## 문제 4
4. collections 모듈은 파이썬의 범용 내장 컨테이너에 대한 대안을 제공하는 특수 컨테이너가 구현되어 있는 모듈입니다. 이 모듈의 컬렉션들이 구현하고 있는 파이썬 내장 컨테이너가 아닌 것을 고르시오. [초, 중, 고]
⓵ list
⓶ dict
⓷ set
⓸ str
⓹ tuple


## 문제 5

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

## 문제 12

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

## 문제 13
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

## 문제 14

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

## 문제 15

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

## 문제 16
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
