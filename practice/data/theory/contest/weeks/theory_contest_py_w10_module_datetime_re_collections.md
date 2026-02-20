# Python 경시대회 W10 모듈(datetime/re/collections)

## 메타
- week: W10
- slug: module_datetime_re_collections
- audience: common, elementary, middle, high

## 학습 목표
- 표준 라이브러리 모듈의 역할을 기능 기준으로 구분하는 것이 목표입니다.
- `os` 모듈 함수 존재 여부를 이름/용도로 판별하는 것이 목표입니다.
- `re.fullmatch`의 전체 문자열 매칭 규칙을 정확히 적용하는 것이 목표입니다.
- `datetime.strftime` 형식 코드의 의미를 예시와 함께 해석하는 것이 목표입니다.
- `collections`가 제공하는 특수 컨테이너와 내장 컨테이너 대응 관계를 설명하는 것이 목표입니다.

## 대상 난이도
- 공통: 초등, 중등, 고등
- 분기: ELEMENTARY, MIDDLE, HIGH

## 공통 이론 (COMMON)
<!-- audience:common -->
### 핵심 개념 요약
- 주제: datetime, re, collections
- 운영: 개념 20분 + 예측형 25분 + 구현형 15분

### 개념 1) 모듈-용도 매핑 규칙
- 개념 정의: 모듈 이름과 대표 기능을 연결해 맞는 짝/틀린 짝을 고르는 유형입니다.
- 판별 규칙: 모듈의 핵심 책임을 1문장으로 고정해 판단한다.
- 추적 절차: 모듈명 확인 -> 대표 기능 키워드 대입 -> 보기 문장과 일치 여부 판정 순으로 풀이합니다.
- 오답 포인트: 함수 이름 하나만 보고 모듈 전체 용도를 오해하면 오답이 됩니다.

![모듈-기능 매핑 맵](./data/theory/images/contest_w10_module_function_map.svg)

예시 (기본):
```python
import datetime, math, os, pickle, traceback

print(hasattr(datetime, "date"))
print(hasattr(math, "sqrt"))
print(hasattr(os, "listdir"))
```
```io
input:
(없음)
output:
True
True
True
```

예시 (변형):
```python
import pickle

data = {"a": 1}
b = pickle.dumps(data)
print(type(b).__name__)
```
```io
input:
(없음)
output:
bytes
```

예시 (함정):
```python
import os
print(os.listdir("." ) is not None)
```
```io
input:
(없음)
output:
True
```

### 개념 2) `os` 함수 존재 여부 판별
- 개념 정의: `os` 모듈에 실제로 정의된 함수인지 이름을 보고 판별하는 유형입니다.
- 판별 규칙: 존재 여부는 문서/자동완성 또는 `hasattr(os, name)`로 확인한다.
- 추적 절차: 함수 이름 정확히 읽기 -> 철자 오탈자 점검 -> `os` 네임스페이스에 존재하는지 검증 순으로 판단합니다.
- 오답 포인트: 비슷한 철자(`getpid` vs `seekid`)를 혼동하면 오답이 됩니다.

예시 (기본):
```python
import os
print(hasattr(os, "getpid"))
print(hasattr(os, "chdir"))
print(hasattr(os, "seekid"))
```
```io
input:
(없음)
output:
True
True
False
```

예시 (변형):
```python
import os
print(callable(getattr(os, "read", None)))
```
```io
input:
(없음)
output:
True
```

예시 (함정):
```python
import os
name = "setgrid"  # setregid 오타
print(hasattr(os, name))
```
```io
input:
(없음)
output:
False
```

### 개념 3) `re.fullmatch` 전체 매칭
- 개념 정의: 정규식이 문자열 전체와 일치할 때만 매치 객체를 반환하는 유형입니다.
- 판별 규칙: `fullmatch`는 부분 일치가 아니라 전체 일치를 요구한다.
- 추적 절차: 패턴 해석 -> 대상 문자열 전체 비교 -> 매치/None 판정 -> 줄 번호 매핑 순으로 풀이합니다.
- 오답 포인트: `search`처럼 부분 매칭으로 해석하면 결과를 반대로 고르게 됩니다.

![search vs fullmatch 매칭 범위 비교](./data/theory/images/contest_w10_search_vs_fullmatch.svg)

예시 (기본):
```python
import re
p = re.compile("o[gh]")
print(p.fullmatch("oh") is not None)
print(p.fullmatch("dog") is not None)
```
```io
input:
(없음)
output:
True
False
```

예시 (변형):
```python
import re
p = re.compile("ab[0-9]")
print(p.fullmatch("ab3") is not None)
print(p.fullmatch("zab3") is not None)
```
```io
input:
(없음)
output:
True
False
```

예시 (함정):
```python
import re
p = re.compile("o[gh]")
print(p.search("dog") is not None)
print(p.fullmatch("dog") is not None)
```
```io
input:
(없음)
output:
True
False
```

### 개념 4) `datetime.strftime` 포맷 코드
- 개념 정의: 날짜/시간 객체를 포맷 문자열 코드로 변환해 출력하는 유형입니다.
- 판별 규칙: `%Y` 연도, `%B` 월 이름, `%M` 분, `%a` 요일 축약, `%Z` 시간대, `%p` AM/PM이다.
- 추적 절차: 포맷 코드 분해 -> 각 코드 의미 대입 -> 예시 문자열과 일치 여부 판정 순으로 풀이합니다.
- 오답 포인트: `%Z`와 `%p`를 혼동하면 오답이 됩니다.

예시 (기본):
```python
from datetime import datetime

dt = datetime(2024, 2, 5, 13, 3)
print(dt.strftime("%Y"))
print(dt.strftime("%B"))
print(dt.strftime("%M"))
```
```io
input:
(없음)
output:
2024
February
03
```

예시 (변형):
```python
from datetime import datetime

dt = datetime(2024, 2, 5, 13, 3)
print(dt.strftime("%p"))
```
```io
input:
(없음)
output:
PM
```

예시 (함정):
```python
from datetime import datetime

dt = datetime(2024, 2, 5, 13, 3)
print(dt.strftime("%Z") == "PM")
```
```io
input:
(없음)
output:
False
```

### 개념 5) `collections`와 내장 컨테이너 대응
- 개념 정의: `collections`가 제공하는 특수 컨테이너가 어떤 내장 컨테이너 계열 확장인지 판별하는 유형입니다.
- 판별 규칙: 대표 대응은 `deque/list`, `defaultdict/dict`, `namedtuple/tuple`, `Counter/dict`다.
- 추적 절차: 컬렉션 이름 확인 -> 기반 컨테이너 계열 매핑 -> 보기와 일치 여부 판정 순으로 풀이합니다.
- 오답 포인트: 문자열(`str`)을 `collections` 대체 컨테이너로 착각하면 오답이 됩니다.

예시 (기본):
```python
from collections import deque, defaultdict, namedtuple

dq = deque([1, 2])
d = defaultdict(int)
Pt = namedtuple("Pt", ["x", "y"])
print(type(dq).__name__, type(d).__name__, type(Pt(1, 2)).__name__)
```
```io
input:
(없음)
output:
deque defaultdict Pt
```

예시 (변형):
```python
from collections import Counter

c = Counter("banana")
print(c["a"], c["b"])
```
```io
input:
(없음)
output:
3 1
```

예시 (함정):
```python
from collections import deque

s = "abc"
dq = deque(s)
print(type(s).__name__)
print(type(dq).__name__)
```
```io
input:
(없음)
output:
str
deque
```

### 공통 미니 체크
1. `pickle`의 핵심 용도를 한 줄로 쓰시오.
2. `os` 함수 존재 여부를 빠르게 확인하는 방법을 쓰시오.
3. `fullmatch`와 `search`의 차이를 쓰시오.
4. `%Z`와 `%p`가 나타내는 값을 각각 쓰시오.
5. `collections`에서 tuple 계열 확장 타입 1개를 쓰시오.

## 초등 트랙 (ELEMENTARY)
<!-- audience:elementary -->
### 초등 포인트
- 모듈 기초 용어/결과 예측

### 초등 이론 보강
- 모듈 이름과 대표 키워드를 1:1 카드로 먼저 암기합니다.
- `re.fullmatch`는 전체 일치만 허용한다는 규칙을 예시로 반복 확인합니다.

초등 규칙 카드:
1. 모듈명과 대표 기능을 함께 외운다.
2. 함수명은 철자를 먼저 점검한다.
3. 정규식은 전체 일치 여부를 먼저 본다.

### 초등 연계 연습
1. `os`, `math`, `pickle`의 대표 기능을 1개씩 쓰시오.
2. `o[gh]` 패턴에 대해 `oh`, `dog`의 `fullmatch` 결과를 쓰시오.

### 초등 오답 패턴
- 함수 이름 철자 확인 없이 익숙한 느낌으로 답을 고릅니다.

## 중등 트랙 (MIDDLE)
<!-- audience:middle -->
### 중등 포인트
- 정규식 기초 패턴 적용

### 중등 이론 보강
- `fullmatch`와 `search`를 같은 입력으로 비교해 차이를 고정합니다.
- `strftime` 코드표를 실제 출력과 연결해 암기 대신 해석 중심으로 훈련합니다.

중등 판별 루틴:
1. 문제의 함수가 `fullmatch`인지 확인한다.
2. 포맷 코드의 의미를 코드별로 분해한다.
3. 보기 문장을 기능 기준으로 재서술해 비교한다.

### 중등 연계 연습
1. 정규식 2개를 만들고 `search/fullmatch` 결과를 비교하시오.
2. `%Y-%m-%d %p %M` 포맷 결과를 예측하시오.

### 중등 오답 패턴
- 포맷 코드 한 글자를 바꿔도 같은 의미라고 가정합니다.

## 고등 트랙 (HIGH)
<!-- audience:high -->
### 고등 포인트
- 모듈 혼합 해석 문제

### 고등 이론 보강
- 모듈별 역할을 분리한 뒤 복합 코드에서 각 줄의 책임을 명시합니다.
- 컨테이너 계열 대응(list/dict/tuple)을 기준으로 보기 함정을 제거합니다.

고등 판별 프레임:
1. 모듈-기능 매핑을 먼저 고정한다.
2. API 이름/반환형을 확인한다.
3. 보기의 설명 문장을 기능 단위로 검증한다.

### 고등 연계 연습
1. `re`/`datetime`/`collections`를 동시에 사용하는 짧은 코드를 작성하시오.
2. 잘못된 모듈-설명 짝 3개를 만들고 올바르게 고치시오.

### 고등 오답 패턴
- 반환값 타입 확인 없이 기능 설명만 보고 정답을 추론합니다.

## 적용 유형
- 모듈-기능 매핑 판별
- `os` 함수 존재 여부 확인
- `re.fullmatch` 결과 예측
- `datetime.strftime` 코드 해석
- `collections` 컨테이너 대응 판별

## {view:teacher} 과제
- 초등: 6문항
- 중등: 8문항
- 고등: 10~12문항

## {view:teacher} 평가
- 항목: 오답 분류표 3
- 오답코드: 모듈용도혼동, 함수명오탈자, 전체매칭오해, 포맷코드혼동, 컨테이너매핑오류

평가 체크:
1. 모듈-기능 짝을 기능 키워드로 설명했는가
2. `os` 함수 존재 여부를 검증 근거와 함께 제시했는가
3. `fullmatch`와 `search` 차이를 예시로 설명했는가
4. `strftime` 코드 의미를 정확히 매핑했는가
5. `collections` 대응 컨테이너를 올바르게 분류했는가

## {view:teacher} 교사 메모
- 웹 렌더 규칙: COMMON + 선택 학년 섹션만 노출합니다.
- 수업 후 오답코드를 기준으로 다음 주차 보강 포인트를 기록합니다.
