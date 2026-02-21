# Python Contest Week 07 High Problem Set

## 범위
- 함수/스코프 심화
- global과 지역 변수 충돌
- 재귀 호출 흐름

## 문제 1
연계 개념: 개념 3) 재귀 호출 횟수 누적(`a += 1`)
다음 프로그램의 빈 칸에 값을 넣었을 때 가장 큰 값을 출력하는 코드를 고르시오.
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

## 문제 2
연계 개념: 개념 2) 지역/전역 스코프 충돌 추적
다음 코드 실행 시 가장 타당한 결과를 고르시오.
```python
x = 5

def f():
    x += 1
    return x

print(f())
```
⓵ 6
⓶ 5
⓷ 1
⓸ None
⓹ 오류 발생

## 문제 3
연계 개념: 개념 2) 지역/전역 스코프 충돌 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
x = 5

def f():
    global x
    x += 1

f()
print(x)
```
⓵ 5
⓶ 6
⓷ 7
⓸ 8
⓹ 오류

## 문제 4
연계 개념: 개념 3) 재귀 호출 횟수 누적(`a += 1`)
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)

print(fact(5))
```
⓵ 24
⓶ 60
⓷ 120
⓸ 240
⓹ 720

## 문제 5
연계 개념: 개념 3) 재귀 호출 횟수 누적(`a += 1`)
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = 1

def f(x):
    global a
    if x == 0:
        return
    a *= 2
    f(x - 1)

f(4)
print(a)
```
⓵ 8
⓶ 12
⓷ 16
⓸ 24
⓹ 32
