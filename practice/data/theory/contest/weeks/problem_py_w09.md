# Python Contest Week 09 Problem Set

## 주차 주제
- 람다, 정렬 key, 삼항 연산자

## 실전 문제 묶음
- 아래 문항은 출처 원문에서 주차 목표에 맞게 선별한 실제 문제이다.

### PY_1회차
- 문항: 18, 20, 23

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

### PY_2회차
- 문항: 6, 15

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
### PY_3회차
- 문항: 6

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


