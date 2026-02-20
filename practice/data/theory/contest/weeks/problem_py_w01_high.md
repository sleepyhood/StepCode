# Python Contest Week 01 High Problem Set

## 범위
- 연산/대입/나머지 + 조건식 혼합
- 포맷 해석
- 스코프 오류 판별
- 반올림/조건식 복합 추적

## 문제 1
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
s = -20
s += 7
s %= 6
ans = ""
if s:
    ans += "T"
if []:
    ans += "F"
print(s, ans)
```
⓵ `-1 T`
⓶ `5 T`
⓷ `1 T`
⓸ `1 TF`
⓹ `5 TF`

## 문제 2
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
print("A{:6d}B{:5s}C".format(81, "K"))
```
⓵ `A    81BK    C`
⓶ `A   81BK    C`
⓷ `A    81B    KC`
⓸ `A81    BK    C`
⓹ `A   81B   KC`

## 문제 3
다음 코드 실행 시 가장 타당한 결과를 고르시오.
```python
p = 10

def g():
    p = p + 1

g()
print(p)
```
⓵ 11
⓶ 10
⓷ 1
⓸ 0
⓹ 오류 발생

## 문제 4
다음 중 출력이 `88.0`이 되는 코드를 고르시오. (`a = 87.6`)
⓵ `print(round(a))`
⓶ `print(round(a, 1))`
⓷ `print(round(a, -1))`
⓸ `print(round(a, 2))`
⓹ `print(round(a, -2))`

## 문제 5
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
x = "False"
y = 0
z = None
k = ""
cnt = 0
for v in [x, y, z, k, 3]:
    if v:
        cnt += 1
print(cnt)
```
⓵ 1
⓶ 2
⓷ 3
⓸ 4
⓹ 5
