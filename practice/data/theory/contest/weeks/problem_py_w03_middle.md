# Python Contest Week 03 Middle Problem Set

## 범위
- while 종료조건
- 유클리드 호제법
- 반복 제곱(mod)

## 문제 1
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = 88
b = 132
while b > 0:
    c = a % b
    a = b
    b = c
print(a)
```
⓵ 11
⓶ 22
⓷ 44
⓸ 66
⓹ 88

## 문제 2
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
n, m, k, a = 3, 10, 15, 1
while k > 0:
    if k % 2 == 1:
        a *= n
        a %= m
    n = (n * n) % m
    k //= 2
print(a)
```
⓵ 1
⓶ 3
⓷ 5
⓸ 7
⓹ 9

## 문제 3
다음 코드의 실행 결과로 올바른 것을 고르시오.
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
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
x = 0
i = 1
while i <= 15:
    if i % 3 == 0:
        x += i
    i += 2
print(x)
```
⓵ 21
⓶ 27
⓷ 30
⓸ 33
⓹ 36

## 문제 5
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = 84
b = 198
while b > 0:
    c = a % b
    a = b
    b = c
print(a)
```
⓵ 3
⓶ 6
⓷ 9
⓸ 12
⓹ 14
