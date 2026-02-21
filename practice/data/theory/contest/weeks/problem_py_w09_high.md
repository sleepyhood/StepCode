# Python Contest Week 09 High Problem Set

## 범위
- lambda/eval 추적 심화
- sort key 다중 기준
- 삼항/누적 결합

## 문제 1
연계 개념: 개념 1) 삼항 연산자 평가 순서
아래 코드의 입력이 다음과 같을 때 실행 결과로 올바른 것을 고르시오.

<입력>
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
    for i in range(n - 1, -1, -1):
        m = F(m, k[i])
    p = G(p, (m * s + 999) // 1000)
print(p)
```
⓵ -34
⓶ 0
⓷ 34
⓸ 35
⓹ 96

## 문제 2
연계 개념: 개념 2) 람다 함수 값 추적
아래 프로그램에 <입력>을 입력했을 때 출력되는 값을 고르시오.

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
p.sort(key=lambda a: (a.x, a.y))

for i in range(1, n + 1):
    tmp = 1000
    if p[i - 1].y == p[i].y:
        tmp = p[i].x - p[i - 1].x
    if p[i].y == p[i + 1].y:
        tmp = min(tmp, p[i + 1].x - p[i].x)
    s += 0 if tmp == 1000 else tmp
print(s)
```
⓵ 0
⓶ 1
⓷ 2
⓸ 3
⓹ 4

## 문제 3
연계 개념: 개념 1) 삼항 연산자 평가 순서
실행 결과로 올바른 것을 고르시오.
```python
f = lambda x: eval((str(x).replace("q", "4") + "*" + (str(x).replace("q", "4"))))
print(f("q"), f("q+1"), f("q+q"))
```
⓵ 16 25 64
⓶ 16 16 16
⓷ 16 9 24
⓸ 16 25 24
⓹ 오류가 발생한다.

## 문제 4
연계 개념: 개념 2) 람다 함수 값 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
data = [(2, 9), (2, 1), (1, 7), (3, 0)]
data.sort(key=lambda t: (t[0], -t[1]))
print(data)
```
⓵ [(1, 7), (2, 9), (2, 1), (3, 0)]
⓶ [(3, 0), (2, 9), (2, 1), (1, 7)]
⓷ [(1, 7), (2, 1), (2, 9), (3, 0)]
⓸ [(2, 9), (2, 1), (1, 7), (3, 0)]
⓹ [(1, 7), (3, 0), (2, 9), (2, 1)]

## 문제 5
연계 개념: 개념 1) 삼항 연산자 평가 순서
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
x = [3, 10, 5, 2]
f = lambda a, b: a if a > b else b
m = 0
for v in x:
    m = f(m, v)
print(m, m if m % 2 == 0 else -m)
```
⓵ 10 -10
⓶ 10 10
⓷ 5 -5
⓸ 3 -3
⓹ 2 2
