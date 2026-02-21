# Python Contest Week 08 Middle Problem Set

## 범위
- 재귀 점화식 계산
- 출력 순서 추적
- 초기값/종료조건 분석

## 문제 1
연계 개념: 개념 3) 다중 초기값 점화식 계산
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
def f(m, n):
    if m == 0 or n == 0:
        return 1
    return f(m - 1, n) + f(m - 1, n - 1) + f(m, n - 1)

print(f(2, 5))
```
⓵ 25
⓶ 41
⓷ 61
⓸ 85
⓹ 231

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
연계 개념: 개념 2) 분할 재귀와 출력 순서
다음 프로그램에서 3번째 줄에 출력되는 값은 무엇인가?
```python
def f(a, b):
    if a == b:
        print(a)
        return
    c = (a + b) // 2
    f(a, c)
    f(c + 1, b)

f(0, 7)
```
⓵ 1
⓶ 2
⓷ 3
⓸ 4
⓹ 5

## 문제 4
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

## 문제 5
연계 개념: 개념 1) 종료조건 우선 확인
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
def p(a, b):
    if b == 0:
        return a
    return p(b, a % b)

print(p(132, 88))
```
⓵ 11
⓶ 22
⓷ 44
⓸ 66
⓹ 88
