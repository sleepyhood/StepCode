# Python Contest Week 06 Problem Set

## 주차 주제
- 문자열 슬라이싱/비교/메서드

## 실전 문제 묶음
- 아래 문항은 출처 원문에서 주차 목표에 맞게 선별한 실제 문제이다.

### PY_1회차
- 문항: 19, 22

#### 문제 19
19. 아래 코드의 입력이 다음과 같을 때 실행 결과로 올바른
것을 고르시오. [초중고]

<다음>
5
programming
hoolly
clanguage
engineeriing
kitpa

```python
t = int(input())
mx = -1
b = ''
for i in range(t):
    cnt = 0
    a = input()
    c = a[0]
for j in range(1, len(a)):
    if c == a[j] and c in "aeiou":
        cnt += 1
    else:
        c = a[j]
    if mx < cnt:
        mx = cnt
        b = a
print(b)
```
⓵ programming
⓶ hoolly
⓷ clanguage
⓸ engineeriing
⓹ kitpa

---

#### 문제 22
22. 아래 프로그램에 <입력 1>과 <입력 2>를 입력했을 때 출력되는 값의 합을 작성하시오. [초중]

<입력 1>
savefromtheavalanche av
<입력 2>
thathathathhtat tha

```python
s, t = input().split()
r = len(s)
p = len(t)
i = 0
while i <= len(s)-p:
    j, u = 0, 0
    if s[i] == t[j]:
        for j in range(1, p):
            if s[i+j] != t[j]:
                u = 1
                i += 1
                break
        
        if not u:
            i += p
            r -= p - 1
    else:
        i += 1
print(r)
```

---

### PY_2회차
- 문항: 10, 20

#### 문제 10
10. 다음 프로그램의 실행 결과는 무엇인가? [초]
```python
a = "apple"
b = 0
for i in range(5):
    for j in range(i):
        if a[i] != a[j]:
            b += 1
print(b)
```
⓵ 6
⓶ 7
⓷ 8
⓸ 9
⓹ 10

---

#### 문제 20
20. 다음은 파이썬에서 사용되는 함수들입니다. 설명을 읽고 어떤 함수에 대한 설명인지 순서대로 작성하시오. [초, 중, 고]
```text
<보기>
append capitalize clear copy encode endswith extend
get insert isalpha items pop remove upper zfill
```
1) 리스트의 뒤에 값을 1 개 추가
2) 문자열이 특정 접미사로 종료되는지 확인
3) 문자열의 왼쪽에 특정 길이만큼의 0을 주가
4) 딕셔너리에서 특정 키를 가지는 키-값 쌍 제거

---
### PY_3회차
- 문항: 10, 15

#### 문제 10
10. 다음 프로그램의 실행 결과는 무엇인가? [초]
```python
a = "apple"
b = 0
for i in range(5):
    for j in range(i):
        if a[i] != a[j]:
            b += 1
print(b)
```
⓵ 6
⓶ 7
⓷ 8
⓸ 9
⓹ 10

---

#### 문제 15
15. 다음 프로그램의 실행 결과는 무엇인가? [초]
```python
def f():
    global a, b
    i = 0
    j = 0
    while i < len(a) - 1:
        if a[i] != a[i+1]:
        b = b[:j] + a[i] + b[j+1:]
        j += 1
    i += 1
a = "aaabbccccdefffff"
b = ""
f()
print(b)
```

---


