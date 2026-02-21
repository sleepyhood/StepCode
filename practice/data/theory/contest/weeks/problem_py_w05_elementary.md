# Python Contest Week 05 Elementary Problem Set

## 범위
- 2중/3중 반복 기초
- 배열 탐색(최댓값)
- 누적 계산

## 문제 1
연계 개념: 개념 1) 이중합 분해 (`Σi Σj`)
다음 프로그램의 실행 결과는 무엇인가?
```python
a = [13, 8, 7, 11]
b = [2, 15, 3, 12]
c = 0
for i in a:
    for j in b:
        if i + j > c:
            c = i + j
print(c)
```
⓵ 15
⓶ 23
⓷ 25
⓸ 26
⓹ 28

## 문제 2
연계 개념: 개념 2) 3중 반복에서 항 분리 계산
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a, b, c = [], [], []
d = 0
for i in range(3):
    a.append(i + 2)
    b.append(i * 4)
    c.append(i * i)
for i in range(3):
    for j in range(3):
        for k in range(3):
            d += a[i] + b[j] * c[k]
print(d)
```
⓵ 234
⓶ 261
⓷ 297
⓸ 1089
⓹ 1116

## 문제 3
연계 개념: 개념 1) 이중합 분해 (`Σi Σj`)
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
cnt = 0
for i in range(1, 4):
    for j in range(2):
        cnt += i + j
print(cnt)
```
⓵ 9
⓶ 12
⓷ 15
⓸ 18
⓹ 21

## 문제 4
연계 개념: 개념 1) 이중합 분해 (`Σi Σj`)
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = [2, 4, 6]
b = [1, 3, 5]
m = 0
for i in a:
    for j in b:
        if i * j > m:
            m = i * j
print(m)
```
⓵ 18
⓶ 24
⓷ 27
⓸ 30
⓹ 36

## 문제 5
연계 개념: 개념 1) 이중합 분해 (`Σi Σj`)
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
s = 0
for i in range(3):
    for j in range(3):
        s += i * j
print(s)
```
⓵ 6
⓶ 9
⓷ 12
⓸ 15
⓹ 18
