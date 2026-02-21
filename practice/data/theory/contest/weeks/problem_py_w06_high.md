# Python Contest Week 06 High Problem Set

## 범위
- 문자열 비교/메서드 심화
- 부분문자열 비중복 처리
- 문자열 변형 결과 추적

## 문제 1
연계 개념: 개념 1) 인접 문자 비교와 연속 구간 카운트
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
words = ["programming", "hoolly", "clanguage", "engineeriing", "kitpa"]
mx = -1
b = ''
for a in words:
    cnt = 0
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

## 문제 2
연계 개념: 개념 2) 부분문자열 스캔과 인덱스 점프
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
def g(s, t):
    r = len(s)
    p = len(t)
    i = 0
    while i <= len(s) - p:
        u = 0
        if s[i] == t[0]:
            for j in range(1, p):
                if s[i + j] != t[j]:
                    u = 1
                    i += 1
                    break
            if not u:
                i += p
                r -= p - 1
        else:
            i += 1
    return r

print(g("savefromtheavalanche", "av") + g("thathathathhtat", "tha"))
```
⓵ 24
⓶ 25
⓷ 26
⓸ 27
⓹ 28

## 문제 3
연계 개념: 개념 3) 중첩 반복 문자열 비교 카운트
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
s = "mississippi"
print(s.replace("ss", "S", 1), s[1:8:2], s.count("si"))
```
⓵ miSissippi issi 2
⓶ miSissippi ispi 2
⓷ miSissippi issi 3
⓸ missiSippi issi 2
⓹ mississippi issi 2

## 문제 4
연계 개념: 개념 3) 중첩 반복 문자열 비교 카운트
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
d = {"a": 1, "b": 2, "c": 3}
x = d.pop("b")
print(x, len(d), "b" in d)
```
⓵ 1 3 False
⓶ 2 2 False
⓷ 2 3 False
⓸ 3 2 True
⓹ 2 2 True

## 문제 5
연계 개념: 개념 2) 부분문자열 스캔과 인덱스 점프
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
s = "thathathathhtat"
t = "tha"
r = len(s)
p = len(t)
i = 0
while i <= len(s) - p:
    u = 0
    if s[i] == t[0]:
        for j in range(1, p):
            if s[i + j] != t[j]:
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
⓵ 7
⓶ 8
⓷ 9
⓸ 10
⓹ 11
