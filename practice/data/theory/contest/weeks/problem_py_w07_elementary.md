# Python Contest Week 07 Elementary Problem Set

## 범위
- 함수 키워드
- global 기본
- 함수 호출 흐름

## 문제 1
다음 중 함수의 정의 시 사용하는 키워드와 함수 내에서 전역변수임을 선언하는 키워드로 올바른 것을 고르시오.
⓵ func, global
⓶ func, local
⓷ func, static
⓸ def, global
⓹ def, static

## 문제 2
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = 1

def f():
    global a
    a += 2

f()
print(a)
```
⓵ 1
⓶ 2
⓷ 3
⓸ 4
⓹ 오류

## 문제 3
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
def g(x):
    return x * 2

print(g(5))
```
⓵ 5
⓶ 7
⓷ 10
⓸ 12
⓹ 15

## 문제 4
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

## 문제 5
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
x = 10

def h():
    x = 3
    return x + 2

print(h(), x)
```
⓵ 3 10
⓶ 5 10
⓷ 5 3
⓸ 12 10
⓹ 오류
