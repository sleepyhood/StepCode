# Python Contest Week 07 Middle Problem Set

## 범위
- 함수 스코프
- global/지역변수 구분
- 재귀 호출 횟수

## 문제 1
연계 개념: 개념 1) 함수 선언/전역 선언 키워드
다음 중 함수의 정의 시 사용하는 키워드와 함수 내에서 전역변수임을 선언하는 키워드로 올바른 것을 고르시오.
⓵ func, global
⓶ func, local
⓷ func, static
⓸ def, global
⓹ def, static

## 문제 2
연계 개념: 개념 3) 재귀 호출 횟수 누적(`a += 1`)
다음 코드의 실행 결과로 올바른 것을 고르시오.
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

f(9)
print(a)
```
⓵ 18
⓶ 19
⓷ 20
⓸ 21
⓹ 22

## 문제 3
연계 개념: 개념 2) 지역/전역 스코프 충돌 추적
다음 코드 실행 시 가장 타당한 결과를 고르시오.
```python
p = 10

def g():
    p = p + 1

g()
print(p)
```
⓵ 11
⓶ 10
⓷ 1
⓸ 0
⓹ 오류 발생

## 문제 4
연계 개념: 개념 2) 지역/전역 스코프 충돌 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
t = 2

def f():
    global t
    t += 3

f()
print(t)
```
⓵ 2
⓶ 3
⓷ 4
⓸ 5
⓹ 오류

## 문제 5
연계 개념: 개념 2) 지역/전역 스코프 충돌 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
def outer(x):
    y = 2
    def inner(z):
        return x + y + z
    return inner(3)

print(outer(4))
```
⓵ 7
⓶ 8
⓷ 9
⓸ 10
⓹ 11
