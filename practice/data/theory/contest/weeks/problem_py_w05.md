# Python Contest Week 05 Problem Set

## 주차 주제
- 2중/3중 반복 + 배열 탐색

## 실전 문제 묶음
- 아래 문항은 출처 원문에서 주차 목표에 맞게 선별한 실제 문제이다.

### PY_1회차
- 문항: 12, 16

#### 문제 12
12. 다음 코드의 실행 결과로 올바른 것을 고르시오. [중고]
```python
a = []
b = []
s = 0
for i in range(6):
    a.append(i)
    b.append(a[i]*2-4)
for i in range(6):
    for j in range(6):
        s += a[i] * b[j]
print(s//2)
```
⓵ 30
⓶ 45
⓷ 60
⓸ 75
⓹ 90

---

#### 문제 16
16. 다음 코드의 실행 결과로 올바른 것을 고르시오. [초중고]
```python
a, b, c = [], [], []
d = 0
for i in range(3):
    a.append(i+2)
    b.append(i*4)
    c.append(i*i)
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

---

### PY_2회차
- 문항: 19

#### 문제 19
19. 다음 프로그램의 실행 결과는 무엇인가? [고]
```python
for i in range(1, 10):
    for j in range(10):
        if i == j: continue
        for k in range(10):
            if k in (i, j): continue
            for l in range(10):
                if l in (i, j, k): continue
                if int(str(i)+str(j)+str(k)+str(l)) * l == int(f"{l}{k}{j}{i}"):
                    print(l)
```
⓵ 1
⓶ 3
⓷ 5
⓸ 7
⓹ 9

---
### PY_3회차
- 문항: 11, 12, 13

#### 문제 11
11. 다음 프로그램의 실행 결과는 무엇인가? [초,중,고]
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

---

#### 문제 12
12. 다음 프로그램의 실행 결과는 무엇인가? [초]
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

---

#### 문제 13
13. 다음 프로그램의 실행 결과는 무엇인가? [초,중]
```python
a = 0
for i in range(1, 10):
    for j in range(10):
        for k in range(10):
            if i == k or j == k: continue
            if int(str(i)+str(j)) * k == int(f"{j}{i}"):
                print(k)
                a = 1
                break
        if a == 1: break
    if a == 1: break
```
⓵ 1
⓶ 3
⓷ 5
⓸ 7
⓹ 9

---


