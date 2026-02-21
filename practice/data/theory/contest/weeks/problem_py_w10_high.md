# Python Contest Week 10 High Problem Set

## 범위
- 모듈 혼합 해석
- regex 패턴 판별
- datetime 포맷 코드

## 문제 1
연계 개념: 개념 1) 모듈-용도 매핑 규칙
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
from datetime import datetime
d = datetime(2024, 2, 1, 9, 3)
print(d.strftime('%a %B %M %Y'))
```
(단, 로케일은 영어 약어 기준)
⓵ Thu February 03 2024
⓶ Feb Thursday 03 2024
⓷ Thu February 09 2024
⓸ Thu Feb 03 24
⓹ Thursday February 03 2024

## 문제 2
연계 개념: 개념 2) `os` 함수 존재 여부 판별
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
import re
pattern = re.compile('o[gh]')
vals = ['o', 'oh', 'dog', 'doggie', 'ogre']
print([v for v in vals if pattern.fullmatch(v)])
```
⓵ []
⓶ ['o']
⓷ ['oh']
⓸ ['o', 'oh']
⓹ ['og', 'oh']

## 문제 3
연계 개념: 개념 3) `re.fullmatch` 전체 매칭
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
from collections import deque
q = deque([1, 2, 3])
q.appendleft(0)
q.pop()
print(list(q))
```
⓵ [0, 1, 2]
⓶ [1, 2, 3]
⓷ [0, 1, 2, 3]
⓸ [0, 2, 3]
⓹ [1, 2]

## 문제 4
연계 개념: 개념 3) `re.fullmatch` 전체 매칭
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
from collections import Counter
c = Counter('banana')
print(c['a'], c.most_common(1)[0][0])
```
⓵ 2 b
⓶ 3 a
⓷ 3 n
⓸ 2 a
⓹ 1 b

## 문제 5
연계 개념: 개념 1) 모듈-용도 매핑 규칙
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
import os
print(hasattr(os, 'chdir'), hasattr(os, 'seekid'))
```
⓵ True True
⓶ True False
⓷ False True
⓸ False False
⓹ 오류
