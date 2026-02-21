# Python Contest Week 01 Middle Problem Set

## 범위
- 연산/대입/나머지
- 출력 포맷 `.format()`
- 함수 스코프/`global`
- 반올림 자리수
- 조건식 판별

## 문제 1
연계 개념: 개념 1) 연산/대입/나머지
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = -14
a += 5
a %= 6
print(a)
```
⓵ -3
⓶ 1
⓷ 3
⓸ 5
⓹ 6

## 문제 2
연계 개념: 개념 2) 출력 포맷 `.format()`
다음 코드의 실행 결과로 올바른 것을 고르시오.
(`·`는 공백)
```python
print("X{:5d}Y{:4s}Z".format(27, "AB"))
```
⓵ `X···27YAB··Z`
⓶ `X··27Y··ABZ`
⓷ `X27···YAB··Z`
⓸ `X···27Y··ABZ`
⓹ `X··27YAB···Z`

## 문제 3
연계 개념: 개념 3) 함수 키워드/스코프
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

## 문제 4
연계 개념: 개념 5) 조건식 truthy/falsy 판별
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
ans = ""
if "":
    ans += "A"
if "NO":
    ans += "B"
if 0:
    ans += "C"
if [1]:
    ans += "D"
print(ans)
```
⓵ A
⓶ B
⓷ BD
⓸ ABC
⓹ ABCD

## 문제 5
연계 개념: 개념 4) 반올림 `round`
다음 중 결과가 70.0이 되는 코드를 고르시오. (`x = 74.9`)
⓵ `print(round(x))`
⓶ `print(round(x, 1))`
⓷ `print(round(x, -1))`
⓸ `print(round(x, 2))`
⓹ `print(round(x, -2))`
