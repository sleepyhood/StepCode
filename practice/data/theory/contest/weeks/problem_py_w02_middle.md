# Python Contest Week 02 Middle Problem Set

## 범위
- for, range, 누적합
- 조건 누적
- 중첩 반복 추적

## 문제 1
연계 개념: 개념 1) `range` 반복 횟수 계산
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
연계 개념: 개념 3) 중첩 반복의 총 실행 횟수
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = 0
for i in range(1, 30, 2):
    for j in range(2, 20, 3):
        a += 1
print(a)
```
⓵ 30
⓶ 60
⓷ 90
⓸ 120
⓹ 150

## 문제 3
연계 개념: 개념 2) 누적합/카운트 분리 계산
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
b = 0
for i in [1, 2, 3, 4, 5, 6, 7]:
    if i % 2 == 1:
        b += i
    if i % 3 == 1:
        b -= i
print(b)
```
⓵ -9
⓶ -4
⓷ 0
⓸ 4
⓹ 9

## 문제 4
연계 개념: 개념 1) `range` 반복 횟수 계산
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
p = 1
for i in range(2, 20, 3):
    p += i
print(p)
```
⓵ 49
⓶ 52
⓷ 55
⓸ 58
⓹ 61

## 문제 5
연계 개념: 개념 3) 중첩 반복의 총 실행 횟수
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
cnt = 0
for i in range(1, 10, 2):
    for j in range(i, i + 3):
        cnt += 1
print(cnt)
```
⓵ 10
⓶ 12
⓷ 15
⓸ 18
⓹ 20
