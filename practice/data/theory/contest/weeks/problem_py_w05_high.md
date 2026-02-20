# Python Contest Week 05 High Problem Set

## 범위
- 다중 반복 심화
- 숫자 조합 탐색
- 배열 결합 누적

## 문제 1
다음 프로그램의 실행 결과는 무엇인가?
```python
for i in range(1, 10):
    for j in range(10):
        if i == j:
            continue
        for k in range(10):
            if k in (i, j):
                continue
            for l in range(10):
                if l in (i, j, k):
                    continue
                if int(str(i) + str(j) + str(k) + str(l)) * l == int(f"{l}{k}{j}{i}"):
                    print(l)
```
⓵ 1
⓶ 3
⓷ 5
⓸ 7
⓹ 9

## 문제 2
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = []
b = []
s = 0
for i in range(5):
    a.append(i + 1)
    b.append(2 * i - 3)
for i in range(5):
    for j in range(5):
        s += a[i] * b[j]
print(s)
```
⓵ 45
⓶ 60
⓷ 70
⓸ 75
⓹ 90

## 문제 3
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a, b, c = [], [], []
d = 0
for i in range(4):
    a.append(i + 1)
    b.append(i * 2)
    c.append(i)
for i in range(4):
    for j in range(4):
        for k in range(4):
            d += a[i] + b[j] * c[k]
print(d)
```
⓵ 384
⓶ 416
⓷ 448
⓸ 480
⓹ 512

## 문제 4
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
x = 0
for i in range(1, 10):
    for j in range(1, 10):
        if i == j:
            continue
        for k in range(1, 10):
            if k in (i, j):
                continue
            if i + j == k:
                x += 1
print(x)
```
⓵ 24
⓶ 28
⓷ 32
⓸ 36
⓹ 40

## 문제 5
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
a = 0
for i in range(1, 10):
    for j in range(10):
        if int(str(i) + str(j)) * 9 == int(f"{j}{i}"):
            a += 1
print(a)
```
⓵ 0
⓶ 1
⓷ 2
⓸ 3
⓹ 4
