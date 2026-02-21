# Python Contest Week 05 Middle Problem Set

## 범위
- 2중/3중 반복 추적
- 배열 누적합/최댓값
- 조건 break 탐색

## 문제 1
연계 개념: 개념 1) 이중합 분해 (`Σi Σj`)
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = []
b = []
s = 0
for i in range(6):
    a.append(i)
    b.append(a[i] * 2 - 4)
for i in range(6):
    for j in range(6):
        s += a[i] * b[j]
print(s // 2)
```
⓵ 30
⓶ 45
⓷ 60
⓸ 75
⓹ 90

## 문제 2
연계 개념: 개념 2) 3중 반복에서 항 분리 계산
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a, b, c = [], [], []
d = 0
for i in range(3):
    a.append(i + 1)
    b.append(i * 2)
    c.append(i * (i + 1))
for i in range(3):
    for j in range(3):
        for k in range(3):
            if k % 2 == 0:
                d += a[i] + b[j] + c[k]
            else:
                d -= a[i] + b[j] + c[k]
print(d)
```
⓵ 36
⓶ 48
⓷ 60
⓸ 72
⓹ 84

## 문제 3
연계 개념: 개념 3) 배열 탐색 최댓값 갱신 패턴
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = 0
for i in range(1, 10):
    for j in range(10):
        for k in range(10):
            if i == k or j == k:
                continue
            if int(str(i) + str(j)) * k == int(f"{j}{i}"):
                print(k)
                a = 1
                break
        if a == 1:
            break
    if a == 1:
        break
```
⓵ 1
⓶ 3
⓷ 5
⓸ 7
⓹ 9

## 문제 4
연계 개념: 개념 1) 이중합 분해 (`Σi Σj`)
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = [2, 5, 8]
b = [1, 4, 7]
c = 0
for i in range(3):
    for j in range(3):
        c += a[i] - b[j]
print(c)
```
⓵ 6
⓶ 9
⓷ 12
⓸ 15
⓹ 18

## 문제 5
연계 개념: 개념 2) 3중 반복에서 항 분리 계산
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
d = 0
for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 3):
            d += i + j + k
print(d)
```
⓵ 81
⓶ 90
⓷ 96
⓸ 99
⓹ 108
