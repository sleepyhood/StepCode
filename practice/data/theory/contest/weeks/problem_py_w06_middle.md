# Python Contest Week 06 Middle Problem Set

## 범위
- 문자열 비교/탐색
- 문자열 메서드
- 부분문자열 처리

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
다음 설명에 맞는 함수 이름을 순서대로 올바르게 나열한 것을 고르시오.
1) 리스트 뒤에 값을 1개 추가
2) 문자열이 특정 접미사로 종료되는지 확인
3) 문자열 왼쪽에 특정 길이만큼 0을 추가
4) 딕셔너리에서 특정 키의 값을 꺼내며 제거

⓵ append, endswith, zfill, pop
⓶ append, startswith, zfill, pop
⓷ extend, endswith, zfill, remove
⓸ append, endswith, ljust, pop
⓹ insert, endswith, zfill, pop

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
⓵ abcd
⓶ abcde
⓷ bcde
⓸ abcdef
⓹ aabcde

## 문제 5
연계 개념: 개념 3) 중첩 반복 문자열 비교 카운트
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
s = "banana"
print(s.count("an"), s.find("na"), s.rfind("na"))
```
⓵ 2 1 3
⓶ 2 2 4
⓷ 3 2 4
⓸ 2 3 5
⓹ 3 1 3
