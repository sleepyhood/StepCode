# Python 경시대회 W10 모듈(datetime/re/collections)

## 메타
- week: W10
- slug: module_datetime_re_collections
- audience: common, elementary, middle, high

## 학습 목표
- 표준 라이브러리 모듈의 역할을 기능 기준으로 구분합니다.
- `os` 모듈 함수 존재 여부를 이름/용도로 판별합니다.
- `re.fullmatch`의 전체 문자열 매칭 규칙을 정확히 적용합니다.
- `datetime.strftime` 형식 코드 의미를 예시와 함께 해석합니다.
- `collections` 특수 컨테이너와 내장 컨테이너 대응 관계를 설명합니다.

## 대상 난이도
- 공통: 초등, 중등, 고등
- 분기: ELEMENTARY, MIDDLE, HIGH

## 공통 이론 (COMMON)
<!-- audience:common -->
### 개념 1) 모듈-용도 매핑 규칙
- 개념 정의: 모듈 이름과 대표 기능을 연결해 맞는 짝/틀린 짝을 판별하는 개념입니다.
- 핵심 내용:
  - 모듈은 핵심 책임(운영체제, 정규식, 날짜/시간, 컨테이너 확장 등)으로 구분합니다.
  - 함수 이름 하나보다 모듈 전체 역할을 기준으로 판단해야 합니다.
  - 기능 키워드를 모듈명과 1:1로 연결하면 선택지 제거가 쉬워집니다.
- 오답 포인트: 함수 하나만 보고 모듈 전체 용도를 판단하면 오답이 됩니다.

| 모듈 | 대표 용도 | 자주 쓰는 예 |
| --- | --- | --- |
| `os` | 운영체제/파일 경로/프로세스 | `listdir`, `getcwd`, `getpid` |
| `re` | 정규식 검색/검증 | `search`, `fullmatch`, `sub` |
| `datetime` | 날짜/시간 표현/포맷 | `datetime.now()`, `strftime` |
| `collections` | 고급 컨테이너 | `Counter`, `deque`, `defaultdict` |
| `pickle` | 직렬화/역직렬화 | `dumps`, `loads` |

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
- 개념 정의: `os` 모듈에 실제 정의된 함수인지 이름과 철자로 판별하는 개념입니다.
- 핵심 내용:
  - 존재 여부는 `hasattr(os, name)` 또는 공식 문서로 검증합니다.
  - 함수명 철자 오탈자 하나로 결과가 완전히 달라집니다.
  - 이름이 비슷해도 모듈 함수가 아닐 수 있습니다.
- 오답 포인트: 유사 철자(`getpid`/`seekid`) 혼동으로 잘못 판단하기 쉽습니다.

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
- 개념 정의: 정규식이 문자열 전체와 일치할 때만 매칭되는 `fullmatch` 규칙을 해석하는 개념입니다.
- 핵심 내용:
  - `fullmatch`는 전체 문자열 일치를 요구합니다.
  - `search`는 부분 일치도 허용하므로 결과가 다를 수 있습니다.
  - 같은 패턴이라도 함수 선택에 따라 판정이 달라집니다.
- 오답 포인트: `search` 기준으로 해석하면 `fullmatch` 결과를 반대로 고를 수 있습니다.

| 함수 | 매칭 범위 | `"dog"` + 패턴 `"o[gh]"` | 대표 용도 |
| --- | --- | --- | --- |
| `re.search` | 문자열 일부 | 매치됨 (`"og"`) | 포함 여부 검사 |
| `re.match` | 문자열 시작 부분 | 매치 안 됨 | 접두 패턴 검사 |
| `re.fullmatch` | 문자열 전체 | 매치 안 됨 | 입력 형식 검증 |

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
- 개념 정의: `strftime` 포맷 코드를 실제 날짜/시간 문자열로 매핑해 해석하는 개념입니다.
- 핵심 내용:
  - `%Y`, `%B`, `%M`, `%a`, `%Z`, `%p`는 서로 다른 항목(연도/월/분/요일/시간대/오전오후)을 나타냅니다.
  - 코드 하나만 바뀌어도 출력 의미가 달라집니다.
  - naive datetime에서는 `%Z`가 빈 문자열일 수 있습니다.
- 오답 포인트: `%Z`와 `%p`처럼 의미가 다른 코드를 혼동하면 오답이 됩니다.

| 코드 | 의미 | 예시 값 (`2024-02-05 13:03:07`) |
| --- | --- | --- |
| `%Y` | 4자리 연도 | `2024` |
| `%B` | 월 이름(영문 전체) | `February` |
| `%a` | 요일 축약(영문) | `Mon` |
| `%m` | 2자리 월 | `02` |
| `%d` | 2자리 일 | `05` |
| `%H` | 24시간 시 | `13` |
| `%M` | 분 | `03` |
| `%S` | 초 | `07` |
| `%Z` | 시간대 이름 | `''` (naive datetime이면 빈 문자열) |
| `%p` | AM/PM | `PM` |

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
- 개념 정의: `collections` 타입을 내장 컨테이너 계열과 대응시켜 해석하는 개념입니다.
- 핵심 내용:
  - `Counter`/`defaultdict`는 dict 계열, `deque`는 시퀀스 큐 계열, `namedtuple`은 tuple 확장입니다.
  - 타입명과 핵심 동작(빈도 집계, 양방향 큐, 기본값 생성)을 함께 매핑합니다.
  - 자료형 계열을 먼저 고정하면 보기 함정을 빠르게 제거할 수 있습니다.
- 오답 포인트: 문자열(`str`)이나 일반 리스트를 대체 타입으로 착각하면 오답이 됩니다.

| 타입 | 기반 계열 | 핵심 특징 | 대표 사용 |
| --- | --- | --- | --- |
| `Counter` | `dict` 확장 | 항목 빈도 자동 집계 | 문자/단어 개수 세기 |
| `deque` | 시퀀스 큐 | 양쪽 `append/pop` O(1) | BFS 큐 |
| `defaultdict` | `dict` 확장 | 없는 키 기본값 자동 생성 | 누적/그룹핑 |
| `namedtuple` | `tuple` 확장 | 필드명으로 접근 가능 | 좌표/레코드 |

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

### 공통 미니 체크 (필수 제출)
> 제한 시간 5분. 정답만 쓰지 말고, 각 문항에 근거 한 줄을 함께 작성합니다.

문항:
1. `pickle`의 핵심 용도를 한 줄로 쓰시오.
2. `os` 함수 존재 여부를 빠르게 확인하는 방법을 쓰시오.
3. `fullmatch`와 `search`의 차이를 쓰시오.
4. `%Z`와 `%p`가 나타내는 값을 각각 쓰시오.
5. `collections`에서 tuple 계열 확장 타입 1개를 쓰시오.

답안 작성:
1. 정답: [ ] / 근거: [ ]
2. 정답: [ ] / 근거: [ ]
3. 정답: [ ] / 근거: [ ]
4. 정답: [ ] / 근거: [ ]
5. 정답: [ ] / 근거: [ ]
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

### 초등 연계 실습 (핸즈온)
실습 목표:
- 핵심 규칙을 직접 계산/표기로 확인합니다.

실습 문제 코드:
```python
# W10 starter (초등): 모듈-기능 확인
import math
import os

def solve():
    print(hasattr(os, "getcwd"))
    print(math.sqrt(16))

if __name__ == "__main__":
    solve()
```

과제:
1. `os`, `math`, `pickle`의 대표 기능을 1개씩 쓰시오.
2. `o[gh]` 패턴에 대해 `oh`, `dog`의 `fullmatch` 결과를 쓰시오.

체크포인트:
1. 과제별로 코드를 직접 실행해 결과를 확인했는가?
2. 정답과 함께 근거(판별 규칙/계산 과정)를 기록했는가?
3. 오답 가능 지점을 한 줄로 점검했는가?
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

### 중등 연계 실습 (핸즈온)
실습 목표:
- 판별 절차를 적용해 근거 중심으로 답안을 작성합니다.

실습 문제 코드:
```python
# W10 starter (중등): re.fullmatch + datetime 포맷
import re
from datetime import datetime

def solve():
    print(bool(re.fullmatch(r"o[gh]", "oh")))
    now = datetime(2025, 1, 2, 15, 4)
    print(now.strftime("%Y-%m-%d %p %M"))

if __name__ == "__main__":
    solve()
```

과제:
1. 정규식 2개를 만들고 `search/fullmatch` 결과를 비교하시오.
2. `%Y-%m-%d %p %M` 포맷 결과를 예측하시오.

체크포인트:
1. 과제별로 코드를 직접 실행해 결과를 확인했는가?
2. 정답과 함께 근거(판별 규칙/계산 과정)를 기록했는가?
3. 오답 가능 지점을 한 줄로 점검했는가?
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

### 고등 연계 실습 (핸즈온)
실습 목표:
- 판별 근거를 먼저 세우고 결과를 검증합니다.

실습 문제 코드:
```python
# W10 starter (고등): collections 활용
from collections import Counter, deque

def solve():
    s = "abacaba"
    c = Counter(s)
    q = deque([1, 2, 3])
    q.appendleft(0)
    print(c["a"], list(q))

if __name__ == "__main__":
    solve()
```

과제:
1. `re`/`datetime`/`collections`를 동시에 사용하는 짧은 코드를 작성하시오.
2. 잘못된 모듈-설명 짝 3개를 만들고 올바르게 고치시오.

체크포인트:
1. 과제별로 코드를 직접 실행해 결과를 확인했는가?
2. 정답과 함께 근거(판별 규칙/계산 과정)를 기록했는가?
3. 오답 가능 지점을 한 줄로 점검했는가?
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
