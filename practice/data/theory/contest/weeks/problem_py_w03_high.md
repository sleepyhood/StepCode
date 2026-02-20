# Python Contest Week 03 High Problem Set

## 범위
- while 추적 심화
- 종료조건/continue/break 혼합
- mod 반복 제곱

## 문제 1
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

## 문제 2
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
n, m, k, a = 7, 13, 11, 1
while k > 0:
    if k % 2 == 1:
        a *= n
        a %= m
    n = (n * n) % m
    k //= 2
print(a)
```
⓵ 1
⓶ 2
⓷ 3
⓸ 5
⓹ 7

## 문제 3
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
i = 0
s = 0
while i < 12:
    i += 1
    if i % 2 == 0:
        continue
    s += i
    if s > 15:
        break
print(i, s)
```
⓵ `5 9`
⓶ `6 9`
⓷ `7 16`
⓸ `8 16`
⓹ `9 25`

## 문제 4
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = 252
b = 105
while b > 0:
    c = a % b
    a = b
    b = c
print(a)
```
⓵ 14
⓶ 21
⓷ 28
⓸ 35
⓹ 42

## 문제 5
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
cnt = 0
n = 100
while n > 0:
    n //= 3
    cnt += 1
print(cnt)
```
⓵ 3
⓶ 4
⓷ 5
⓸ 6
⓹ 7
