# Python Contest Week 06 Elementary Problem Set

## 범위
- 문자열 비교
- 문자열 슬라이싱
- 문자열 메서드

## 문제 1
연계 개념: 개념 1) 인접 문자 비교와 연속 구간 카운트
다음 프로그램의 실행 결과는 무엇인가?
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

## 문제 2
연계 개념: 개념 3) 중첩 반복 문자열 비교 카운트
다음 중 문자열이 특정 접미사로 끝나는지 확인하는 메서드는 무엇인가?
⓵ append
⓶ endswith
⓷ split
⓸ replace
⓹ remove

## 문제 3
연계 개념: 개념 2) 부분문자열 스캔과 인덱스 점프
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
s = "savefromtheavalanche"
t = "av"
r = len(s)
p = len(t)
i = 0
while i <= len(s) - p:
    j, u = 0, 0
    if s[i] == t[j]:
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
⓵ 16
⓶ 17
⓷ 18
⓸ 19
⓹ 20

## 문제 4
연계 개념: 개념 1) 인접 문자 비교와 연속 구간 카운트
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
def f():
    global a, b
    i = 0
    j = 0
    while i < len(a) - 1:
        if a[i] != a[i + 1]:
            b = b[:j] + a[i] + b[j+1:]
            j += 1
        i += 1
a = "aaabbccccdefffff"
b = ""
f()
print(b)
```
⓵ abc
⓶ abcd
⓷ abcde
⓸ abccde
⓹ aabbccddee

## 문제 5
연계 개념: 개념 1) 인접 문자 비교와 연속 구간 카운트
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
s = "programming"
print(s[2:8:2])
```
⓵ prg
⓶ oag
⓷ orm
⓸ rmi
⓹ pgm
