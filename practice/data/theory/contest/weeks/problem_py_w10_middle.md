# Python Contest Week 10 Middle Problem Set

## 범위
- collections/re/datetime 핵심
- 모듈 용도 판별
- 포맷 코드 해석

## 문제 1
다음 중 `collections` 모듈의 특수 컨테이너가 직접 대체 대상으로 두지 않는 내장 타입을 고르시오.
⓵ list
⓶ dict
⓷ set
⓸ str
⓹ tuple

## 문제 2
다음 프로그램의 실행 결과에서 None을 출력하지 않는 줄은 몇 번 줄인가?
```python
import re
pattern = re.compile('o[gh]')
print(pattern.fullmatch('o'))
print(pattern.fullmatch('oh'))
print(pattern.fullmatch('dog'))
print(pattern.fullmatch('doggie'))
print(pattern.fullmatch('ogre'))
```
⓵ 1번 줄
⓶ 2번 줄
⓷ 3번 줄
⓸ 4번 줄
⓹ 5번 줄

## 문제 3
datetime의 strftime 함수에 대한 설명으로 올바르지 않게 짝지어진 것을 고르시오.
⓵ `%a`- Mon
⓶ `%B`- February
⓷ `%M`- 03
⓸ `%Z`- AM
⓹ `%Y`- 2024

## 문제 4
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
from collections import defaultdict
d = defaultdict(int)
d['a'] += 2
d['b'] += 1
print(d['a'] + d['c'])
```
⓵ 0
⓶ 1
⓷ 2
⓸ 3
⓹ 오류

## 문제 5
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
import re
p = re.compile('ab+c')
print(bool(p.fullmatch('abbbc')), bool(p.fullmatch('ac')))
```
⓵ True True
⓶ True False
⓷ False True
⓸ False False
⓹ 오류
