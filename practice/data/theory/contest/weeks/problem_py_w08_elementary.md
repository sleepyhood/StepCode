# Python Contest Week 08 Elementary Problem Set

## 범위
- 재귀 호출 기초
- 종료조건
- 분할 재귀 출력 순서

## 문제 1
다음 프로그램의 실행 결과는 무엇인가?
```python
def f(a, b):
    if a == 1:
        return 1
    return b * f(a - 1, b)

print(f(4, 6))
```
⓵ 216
⓶ 256
⓷ 1024
⓸ 1296
⓹ 4096

## 문제 2
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

## 문제 3
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
def g(n):
    if n == 0:
        return 0
    return n + g(n - 1)

print(g(5))
```
⓵ 10
⓶ 12
⓷ 15
⓸ 18
⓹ 21

## 문제 4
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
def f(n):
    if n <= 1:
        return 1
    return n * f(n - 1)

print(f(5))
```
⓵ 24
⓶ 60
⓷ 120
⓸ 240
⓹ 720

## 문제 5
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
def h(n):
    if n <= 1:
        return n
    return h(n - 1) + h(n - 2)

print(h(6))
```
⓵ 5
⓶ 8
⓷ 10
⓸ 13
⓹ 21
