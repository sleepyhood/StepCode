# Python Contest Week 03 Elementary Problem Set

## 범위
- while 반복
- 종료조건과 break
- 반복 횟수/누적값 계산

## 문제 1
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = 0
i = 0
while True:
    if i > 10:
        break
    i += 2
    a += 3
print(a)
```
⓵ 6
⓶ 9
⓷ 12
⓸ 15
⓹ 18

## 문제 2
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

## 문제 3
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

## 문제 4
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
cnt = 0
i = 1
while i <= 9:
    cnt += 1
    i += 2
print(cnt)
```
⓵ 3
⓶ 4
⓷ 5
⓸ 6
⓹ 7

## 문제 5
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
s = 0
i = 2
while i < 12:
    s += i
    i += 3
print(s)
```
⓵ 20
⓶ 23
⓷ 25
⓸ 26
⓹ 29
