# Python Contest Week 02 High Problem Set

## 범위
- for/range 누적합 심화
- 중첩 반복 식 계산
- 조건 결합 카운트

## 문제 1
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = 0
for i in range(100, 2024, 150):
    a += i
print(a)
```
⓵ 11500
⓶ 12000
⓷ 12500
⓸ 13000
⓹ 13500

## 문제 2
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = 0
for i in range(1, 30, 2):
    for j in range(2, 20, 3):
        a += i + j
print(a)
```
⓵ 1980
⓶ 2040
⓷ 2130
⓸ 2205
⓹ 2310

## 문제 3
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
b = 0
for i in [1, 2, 3, 4, 5, 6, 7]:
    if i % 2 == 1:
        b += i
    if i % 3 == 1:
        b -= 2 * i
print(b)
```
⓵ -10
⓶ -8
⓷ -6
⓸ -4
⓹ -2

## 문제 4
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
p = 5
for i in range(3, 35, 2):
    if i % 4 == 3:
        p += 1
    else:
        p += 2
print(p)
```
⓵ 25
⓶ 27
⓷ 28
⓸ 29
⓹ 31

## 문제 5
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
cnt = 0
for i in range(1, 30, 2):
    for j in range(2, 20, 3):
        if (i + j) % 2 == 0:
            cnt += 1
print(cnt)
```
⓵ 30
⓶ 36
⓷ 40
⓸ 45
⓹ 50
