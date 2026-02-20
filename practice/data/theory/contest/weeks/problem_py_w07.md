# Python Contest Week 07 Problem Set

## 주차 주제
- 함수, 스코프, 전역/지역

## 실전 문제 묶음
- 아래 문항은 출처 원문에서 주차 목표에 맞게 선별한 실제 문제이다.

### PY_1회차
- 문항: 5

#### 문제 5
5. 다음 중 함수의 정의 시 사용하는 키워드와 함수 내에서 전역변수 임을 선언하는 키워드로 올바른 것을 고르시오. [초중고]

⓵ func, global
⓶ func, local
⓷ func, static
⓸ def, global
⓹ def, static

---

### PY_2회차
- 문항: 14

#### 문제 14
14. 다음 프로그램의 빈 칸에 값을 넣었을 때 가장 큰 값을
출력하는 코드를 고르시오.  [초, 중, 고]
```python
a = 0
def f(x):
    global a
    a += 1
    if x == 1:
        return
    if x & 1 == 0:
        f(x // 2)
    else:
        f(x * 3 + 1)
f(빈칸)
print(a)
```
⓵ 3
⓶ 5
⓷ 7
⓸ 9
⓹ 11

---

