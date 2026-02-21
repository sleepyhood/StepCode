# Python Contest Week 08 High Problem Set

## 범위
- 재귀 함수 설계
- 종료조건/방문체크
- 점화식 고난도 추적

## 문제 1
연계 개념: 개념 3) 다중 초기값 점화식 계산
다음 코드의 실행 결과로 올바른 값을 고르시오.
```python
def f(x, y, p, a):
    if x < 0 or y < 0:
        return 0
    if x >= 4 or y >= 4:
        return 0
    if a[x][y]:
        return 0
    if x == 3 and y == 3:
        return p + 1
    a[x][y] = 1
    k = 0
    for i in range(3):
        k += f(x + i // 2, y + i // 2, p, a)
    a[x][y] = 0
    return k

print(f(0, 0, 0, [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]))
```
⓵ 1
⓶ 2
⓷ 3
⓸ 4
⓹ 5

## 문제 2
연계 개념: 개념 3) 다중 초기값 점화식 계산
다음 프로그램의 실행 결과는 무엇인가?
```python
def f(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 8
    return f(n - 1) + f(n - 3)

print(f(10))
```
⓵ 51
⓶ 76
⓷ 110
⓸ 161
⓹ 237

## 문제 3
연계 개념: 개념 1) 종료조건 우선 확인
다음 프로그램의 빈칸에 값을 넣었을 때 가장 큰 값을 가지는 코드를 고르시오.
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

## 문제 4
연계 개념: 개념 3) 다중 초기값 점화식 계산
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
def f(m, n):
    if m == 0 or n == 0:
        return 1
    return f(m - 1, n) + f(m - 1, n - 1) + f(m, n - 1)

print(f(3, 3))
```
⓵ 31
⓶ 43
⓷ 55
⓸ 63
⓹ 75

## 문제 5
연계 개념: 개념 1) 종료조건 우선 확인
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
def f(a, b):
    if a == 1:
        return 1
    return b * f(a - 1, b)

print(f(5, 3))
```
⓵ 27
⓶ 54
⓷ 81
⓸ 243
⓹ 729
