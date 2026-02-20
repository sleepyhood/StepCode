# Python Contest Week 02 Elementary Problem Set

## 범위
- for, range 반복 횟수
- 누적합/카운트
- 중첩 반복 기본

## 문제 1
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
p = 5
for i in range(3, 35, 2):
    p += 2
print(p)
```
⓵ 35
⓶ 36
⓷ 37
⓸ 38
⓹ 39

## 문제 2
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

## 문제 3
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

## 문제 4
다음 중 `range(100, 2024, 150)`의 반복 횟수로 올바른 것을 고르시오.
⓵ 11회
⓶ 12회
⓷ 13회
⓸ 14회
⓹ 15회

## 문제 5
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = 0
for i in range(100, 551, 150):
    a += i
print(a)
```
⓵ 850
⓶ 1000
⓷ 1150
⓸ 1300
⓹ 1450
