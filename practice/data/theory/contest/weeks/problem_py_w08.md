# Python Contest Week 08 Problem Set

## 주차 주제
- 재귀 기본, 종료조건, 초기값

## 실전 문제 묶음
- 아래 문항은 출처 원문에서 주차 목표에 맞게 선별한 실제 문제이다.

### PY_1회차
- 문항: 15, 25

#### 문제 15
15. 다음 코드의 실행 결과로 올바른 것을 고르시오. [초중]
```python
def f(m, n):
    if m == 0 or n == 0:
        return 1
    else:
        return f(m-1, n) + f(m-1, n-1) + f(m, n-1)
print(f(2, 5))
```
⓵ 25 
⓶ 41 
⓷ 61
⓸ 85 
⓹ 231

---

#### 문제 25
25. 다음 코드의 실행 결과로 올바른 값을 작성하시오. [고]

```python
def f(x, y, p, a):
    if x < 0 or y < 0: return 0
    if x >= 4 or y >= 4: return 0
    if a[x][y]: return 0
    if x == 3 and y == 3:
        return p + 1
    a[x][y] = 1
    k = 0
    for i in range(3):
        k += f(x + i//2, y + i//2, p, a)
    a[x][y] = 0
    return k

print(f(0, 0, 0,[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]))
```

---

### PY_2회차
- 문항: 7, 8, 9, 12

#### 문제 7
7. 다음 프로그램의 실행 결과는 무엇인가? [초, 중]
```python
def f(a, b):
    if a == 1:
        return 1
    return b * f(a-1, b)
print(f(4, 6))
```
⓵ 216
⓶ 256
⓷ 1024
⓸ 1296
⓹ 4096

---

#### 문제 8
8. 다음 프로그램에서 3 번재 줄에 출력되는 값은 무엇인가? [초]
```python
def f(a, b):
    if a == b:
        print(a)
        return
    c = (a + b) // 2
    f(a, c)
    f(c+1, b)

f(0, 7)
```
⓵ 1
⓶ 2
⓷ 3
⓸ 4
⓹ 5

---

#### 문제 9
9. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]
```python
def f(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 8
    return f(n-1) + f(n-3)

print(f(10))
```
⓵ 51
⓶ 76
⓷ 110
⓸ 181
⓹ 237

---

#### 문제 12
12. 다음 프로그램의 빈 칸에 값을 넣었을 때 가장 큰 값을 가지는 코드를 고르시오. [고]
```python
def f(a):
    if a <= 0:
        return 0
    return (a % 7) * f(a // 7) + a % 7
print(f(빈칸))
``` 
⓵ 14
⓶ 89
⓷ 168
⓸ 223
⓹ 512

---
### PY_3회차
- 문항: 7, 8, 9

#### 문제 7
7. 다음 프로그램의 실행 결과는 무엇인가? [초, 중]
```python
def f(a, b):
    if a == 1:
        return 1
    return b * f(a-1, b)

print(f(4, 6))
```
⓵ 216
⓶ 256
⓷ 1024
⓸ 1296
⓹ 4096

---

#### 문제 8
8. 다음 프로그램에서 3 번재 줄에 출력되는 값은 무엇인가? [초]
```python
def f(a, b):
    if a == b:
        print(a)
        return
    c = (a + b) // 2
    f(a, c)
    f(c+1, b)

f(0, 7)
```
⓵ 1
⓶ 2
⓷ 3
⓸ 4
⓹ 5

---

#### 문제 9
9. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]
```python
def f(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 8
    return f(n-1) + f(n-3)
print(f(10))
```
⓵ 51
⓶ 76
⓷ 110
⓸ 161
⓹ 237

---


