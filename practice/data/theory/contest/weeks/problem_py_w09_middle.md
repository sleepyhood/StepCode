# Python Contest Week 09 Middle Problem Set

## 범위
- lambda + eval 추적
- 삼항 연산자
- key 정렬/튜플 정렬

## 문제 1
실행 결과로 올바른 것을 고르시오.
```python
f = lambda x: eval((str(x).replace("q", "4") + "*" + (str(x).replace("q", "4"))))
print(f("q"), f("q+1"), f("q+q"))
```
⓵ 16 25 64
⓶ 16 16 16
⓷ 16 9 24
⓸ 16 25 24
⓹ 오류가 발생한다.

## 문제 2
다음 프로그램의 실행 결과는 무엇인가?
```python
x = 12
y = 15
print(x + y if x > y else x * y)
```
⓵ 3
⓶ 12
⓷ 15
⓸ 27
⓹ 180

## 문제 3
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
arr = ["aa", "b", "cccc", "ddd"]
arr.sort(key=lambda s: (len(s), s))
print(arr)
```
⓵ ['b', 'aa', 'ddd', 'cccc']
⓶ ['aa', 'b', 'ddd', 'cccc']
⓷ ['b', 'aa', 'cccc', 'ddd']
⓸ ['aa', 'b', 'cccc', 'ddd']
⓹ ['b', 'ddd', 'aa', 'cccc']

## 문제 4
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
f = lambda a, b: a if a > b else b
g = lambda a, b: a + b
print(f(3, 7), g(f(2, 5), 4))
```
⓵ 3 6
⓶ 7 9
⓷ 7 8
⓸ 5 9
⓹ 7 7

## 문제 5
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
pts = [(3, 2), (1, 9), (3, 1), (2, 5)]
pts.sort(key=lambda p: (p[0], -p[1]))
print(pts[0], pts[-1])
```
⓵ (1, 9) (3, 1)
⓶ (1, 9) (3, 2)
⓷ (2, 5) (3, 1)
⓸ (3, 2) (1, 9)
⓹ (3, 1) (3, 2)
