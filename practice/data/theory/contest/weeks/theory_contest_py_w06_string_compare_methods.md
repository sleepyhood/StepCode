# Python 경시대회 W06 문자열 비교/메서드

## 메타
- week: W06
- slug: string_compare_methods
- audience: common, elementary, middle, high

## 학습 목표
- 문자열 비교에서 인덱스와 기준 문자 갱신 흐름을 안정적으로 추적합니다.
- 부분문자열 탐색에서 한 칸 이동과 점프 이동을 구분해 누적값을 계산합니다.
- 문자열/리스트/딕셔너리 메서드의 역할을 맥락에 맞게 분류해 선택합니다.
- 함수 내부 갱신에서 전역 변수와 슬라이싱 치환의 동작 범위를 설명합니다.

## 대상 난이도
- 공통: 초등, 중등, 고등
- 분기: ELEMENTARY, MIDDLE, HIGH

## 공통 이론 (COMMON)
<!-- audience:common -->
### 개념 1) 인접 문자 비교와 연속 구간 카운트
- 개념 정의: 문자열을 순회하며 기준 문자와 현재 문자를 비교해 연속 길이를 갱신하는 개념입니다.
- 핵심 내용:
  - 연속 판단은 `현재 문자 == 기준 문자`일 때만 유지됩니다.
  - 문자가 바뀌면 기준 문자를 현재 문자로 교체해야 합니다.
  - 연속 카운트와 최대값 갱신은 별도 단계로 분리하면 안정적입니다.
- 오답 포인트: 기준 문자 갱신 위치가 잘못되면 연속 판정이 무너집니다.

![연속 문자 카운트 상태기계](./data/theory/images/contest_w06_run_count_state_machine.svg)

예시 (기본):
```python
s = "baallooon"
c = s[0]
cnt = 0
mx = 0
for i in range(1, len(s)):
    if s[i] == c:
        cnt += 1
    else:
        c = s[i]
    if cnt > mx:
        mx = cnt
print(mx)
```
```io
input:
(없음)
output:
2
```

예시 (변형):
```python
s = "aabbbcccc"
c = s[0]
cnt = 0
mx = 0
for i in range(1, len(s)):
    if s[i] == c and c in "aeiou":
        cnt += 1
    else:
        c = s[i]
    if cnt > mx:
        mx = cnt
print(mx)
```
```io
input:
(없음)
output:
1
```

예시 (함정):
```python
s = "aabb"
c = s[0]
cnt = 0
mx = 0
for i in range(1, len(s)):
    if s[i] == c:
        cnt += 1
    c = s[i]
    if cnt > mx:
        mx = cnt
print(mx)
```
```io
input:
(없음)
output:
0
```

### 개념 2) 부분문자열 스캔과 인덱스 점프
- 개념 정의: 부분문자열 매칭에서 성공 시 점프, 실패 시 1칸 이동으로 인덱스를 제어하는 개념입니다.
- 핵심 내용:
  - 완전 매칭이면 `i += len(t)`로 점프해 비중첩 탐색을 수행합니다.
  - 매칭 실패면 `i += 1`로 다음 시작점만 확인합니다.
  - 시작 인덱스 이동 규칙이 카운트 결과를 결정합니다.
- 오답 포인트: 실패 시에도 점프 이동을 적용하면 후보 위치를 놓칩니다.

![부분문자열 탐색 인덱스 이동도](./data/theory/images/contest_w06_substring_index_shift.svg)

예시 (기본):
```python
s = "abcabcx"
t = "abc"
i = 0
cnt = 0
while i <= len(s) - len(t):
    ok = True
    for j in range(len(t)):
        if s[i + j] != t[j]:
            ok = False
            break
    if ok:
        cnt += 1
        i += len(t)
    else:
        i += 1
print(cnt)
```
```io
input:
(없음)
output:
2
```

예시 (변형):
```python
s = "aaaaa"
t = "aa"
i = 0
cnt = 0
while i <= len(s) - len(t):
    ok = True
    for j in range(len(t)):
        if s[i + j] != t[j]:
            ok = False
            break
    if ok:
        cnt += 1
        i += len(t)
    else:
        i += 1
print(cnt)
```
```io
input:
(없음)
output:
2
```

예시 (함정):
```python
s = "ababab"
t = "ab"
i = 0
cnt = 0
while i <= len(s) - len(t):
    if s[i] == t[0]:
        cnt += 1
        i += 1
    else:
        i += 1
print(cnt)
```
```io
input:
(없음)
output:
3
```

### 개념 3) 중첩 반복 문자열 비교 카운트
- 개념 정의: 문자열 인덱스 쌍을 만들고 조건 비교 횟수를 누적하는 중첩 반복 카운트 개념입니다.
- 핵심 내용:
  - `range(i)`는 항상 `j < i` 쌍만 비교합니다.
  - 비교 조건(`!=`, `==`)에 따라 누적 방향이 달라집니다.
  - 반복 범위가 1칸만 바뀌어도 전체 카운트가 크게 달라질 수 있습니다.
- 오답 포인트: `range(i+1)`로 자기 자신 비교를 포함하면 결과가 달라집니다.

예시 (기본):
```python
a = "apple"
b = 0
for i in range(len(a)):
    for j in range(i):
        if a[i] != a[j]:
            b += 1
print(b)
```
```io
input:
(없음)
output:
9
```

예시 (변형):
```python
a = "abca"
b = 0
for i in range(len(a)):
    for j in range(i):
        if a[i] != a[j]:
            b += 1
print(b)
```
```io
input:
(없음)
output:
4
```

예시 (함정):
```python
a = "abca"
b = 0
for i in range(len(a)):
    for j in range(i + 1):
        if a[i] != a[j]:
            b += 1
print(b)
```
```io
input:
(없음)
output:
4
```

### 개념 4) 메서드 분류와 목적 매칭
- 개념 정의: 자료형별 메서드를 요구 동작에 맞게 매칭해 선택하는 개념입니다.
- 핵심 내용:
  - 메서드는 자료형마다 동작과 반환값이 다릅니다.
  - 먼저 자료형을 고정하고, 동작(추가/삭제/탐색/치환)을 대응해야 합니다.
  - 반환값과 원본 변경 여부(부작용)를 함께 확인해야 합니다.
- 오답 포인트: `remove`와 `pop`처럼 유사 메서드를 혼동하면 오답이 발생합니다.

| 메서드 | 대상 자료형 | 핵심 기능 | 반환값 | 예시 |
| --- | --- | --- | --- | --- |
| `find(sub)` | `str` | 부분 문자열 첫 위치 | 인덱스 / `-1` | `"code".find("de") -> 2` |
| `count(sub)` | `str` | 부분 문자열 개수 | 정수 | `"banana".count("a") -> 3` |
| `replace(a,b)` | `str` | 치환된 새 문자열 생성 | 새 문자열 | `"a-b".replace("-",":")` |
| `split(sep)` | `str` | 문자열 분리 | 리스트 | `"a,b".split(",") -> ["a","b"]` |
| `strip()` | `str` | 양끝 공백 제거 | 새 문자열 | `"  hi ".strip() -> "hi"` |
| `append(x)` | `list` | 끝에 추가 | `None` | `arr.append(3)` |
| `pop(k)` | `dict`/`list` | 삭제 + 값 반환 | 삭제된 값 | `d.pop("a")`, `arr.pop()` |

예시 (기본):
```python
arr = [1, 2]
arr.append(3)
print(arr)
```
```io
input:
(없음)
output:
[1, 2, 3]
```

예시 (변형):
```python
s = "code"
print(s.endswith("de"))
print("42".zfill(5))
```
```io
input:
(없음)
output:
True
00042
```

예시 (함정):
```python
d = {"a": 10, "b": 20}
v = d.pop("a")
print(v)
print(d)
```
```io
input:
(없음)
output:
10
{'b': 20}
```

### 개념 5) 전역 변수와 슬라이싱 치환
- 개념 정의: 함수 내부에서 전역 문자열을 슬라이싱 결합으로 갱신하는 동작 범위를 해석하는 개념입니다.
- 핵심 내용:
  - 문자열은 불변이므로 한 글자 치환도 새 문자열 재조합이 필요합니다.
  - 함수 내부에서 전역값을 바꿀 때는 `global` 선언이 필요합니다.
  - 슬라이싱 경계(`left/right`)를 정확히 잡아야 원하는 위치만 치환됩니다.
- 오답 포인트: 문자열을 리스트처럼 직접 대입하면 `TypeError`가 발생합니다.

예시 (기본):
```python
def f():
    global s
    s = s[:1] + "Z" + s[2:]

s = "abc"
f()
print(s)
```
```io
input:
(없음)
output:
aZc
```

예시 (변형):
```python
def g():
    global b, j, ch
    b = b[:j] + ch + b[j + 1:]

b = "_____"
j = 2
ch = "x"
g()
print(b)
```
```io
input:
(없음)
output:
__x__
```

예시 (함정):
```python
s = "abc"
try:
    s[1] = "Z"
except TypeError:
    print("TypeError")
```
```io
input:
(없음)
output:
TypeError
```

### 공통 미니 체크 (필수 제출)
> 제한 시간 5분. 정답만 쓰지 말고, 각 문항에 근거 한 줄을 함께 작성합니다.

문항:
1. 연속 구간 카운트에서 기준 문자를 갱신하는 정확한 시점을 쓰시오.
2. 부분문자열 매칭 실패 시 인덱스를 얼마나 이동해야 하는지 쓰시오.
3. `append`, `endswith`, `zfill`, `pop`의 자료형과 역할을 짝지으시오.
4. 문자열 한 글자 치환을 슬라이싱으로 표현하는 이유를 쓰시오.

답안 작성:
1. 정답: [ ] / 근거: [ ]
2. 정답: [ ] / 근거: [ ]
3. 정답: [ ] / 근거: [ ]
4. 정답: [ ] / 근거: [ ]
## 초등 트랙 (ELEMENTARY)
<!-- audience:elementary -->
### 초등 포인트
- 문자열 비교 카운트

### 초등 이론 보강
- 인덱스 표를 그리고 `i`, `j`가 가리키는 문자 쌍을 한 줄씩 기록합니다.
- 메서드 문제는 먼저 자료형(리스트/문자열/딕셔너리)을 표시하고 답을 고릅니다.

초등 규칙 카드:
1. 비교 전에 인덱스 범위를 먼저 확인한다.
2. 조건이 참일 때만 카운트를 증가시킨다.
3. 메서드 이름은 동작과 함께 암기한다.

### 초등 연계 실습 (핸즈온)
실습 목표:
- 핵심 규칙을 직접 계산/표기로 확인합니다.

실습 문제 코드:
```python
# W06 starter (초등): 문자열 인접 비교

def solve():
    s = "aabccc"
    cnt = 0
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            cnt += 1
    print(cnt)

if __name__ == "__main__":
    solve()
```

과제:
1. 문자열에서 서로 다른 문자 쌍의 개수를 손으로 계산하시오.
2. `append`, `endswith`, `zfill`을 각각 1회씩 사용하는 짧은 코드를 작성하시오.

체크포인트:
1. 과제별로 코드를 직접 실행해 결과를 확인했는가?
2. 정답과 함께 근거(판별 규칙/계산 과정)를 기록했는가?
3. 오답 가능 지점을 한 줄로 점검했는가?
### 초등 오답 패턴
- 인덱스 범위를 확인하지 않아 마지막 문자에서 비교가 어긋납니다.

## 중등 트랙 (MIDDLE)
<!-- audience:middle -->
### 중등 포인트
- 문자열+반복 혼합

### 중등 이론 보강
- 부분문자열 탐색에서 성공/실패 흐름을 분기도로 작성해 `i` 이동량을 분리합니다.
- 연속 구간 카운트에서 최대값 갱신 조건을 별도로 점검합니다.

중등 판별 루틴:
1. 반복 경계(`while` 종료 조건)를 확정한다.
2. 내부 비교 실패 시점과 탈출 경로를 표시한다.
3. 누적값(길이/횟수)을 각 분기마다 갱신한다.

### 중등 연계 실습 (핸즈온)
실습 목표:
- 판별 절차를 적용해 근거 중심으로 답안을 작성합니다.

실습 문제 코드:
```python
# W06 starter (중등): 부분문자열 스캔

def solve():
    s = "abcabcx"
    t = "abc"
    i = 0
    hit = 0
    while i <= len(s) - len(t):
        if s[i:i+len(t)] == t:
            hit += 1
            i += len(t)
        else:
            i += 1
    print(hit)

if __name__ == "__main__":
    solve()
```

과제:
1. 비중첩 매칭 방식과 한 칸 이동 방식의 결과 차이를 비교하시오.
2. 기준 문자 갱신 위치를 바꿨을 때 출력이 어떻게 달라지는지 설명하시오.

체크포인트:
1. 과제별로 코드를 직접 실행해 결과를 확인했는가?
2. 정답과 함께 근거(판별 규칙/계산 과정)를 기록했는가?
3. 오답 가능 지점을 한 줄로 점검했는가?
### 중등 오답 패턴
- 매칭 실패 분기에서도 점프 이동을 적용해 후보 위치를 누락합니다.

## 고등 트랙 (HIGH)
<!-- audience:high -->
### 고등 포인트
- 문자열+배열 동시 추적

### 고등 이론 보강
- 전역 변수 갱신 코드에서 들여쓰기와 루프 범위를 먼저 검증한 후 출력을 예측합니다.
- 슬라이싱 치환, 조기 종료, 분기 누적의 결합 동작을 단계별로 추적합니다.

고등 판별 프레임:
1. 함수 외부/내부 변수의 스코프를 분리한다.
2. 문자열 갱신 식의 좌/우 슬라이스 경계를 확인한다.
3. `break`/`continue` 적용 범위를 루프 깊이 기준으로 해석한다.

### 고등 연계 실습 (핸즈온)
실습 목표:
- 판별 근거를 먼저 세우고 결과를 검증합니다.

실습 문제 코드:
```python
# W06 starter (고등): 전역 문자열 치환

text = "_____"

def put(idx, ch):
    global text
    text = text[:idx] + ch + text[idx + 1:]

def solve():
    put(2, "x")
    put(4, "z")
    print(text)

if __name__ == "__main__":
    solve()
```

과제:
1. 인접 문자 경계만 추출하는 코드를 작성하고, 입력 2개로 결과를 검증하시오.
2. 전역 문자열을 여러 번 치환하는 함수에서 인덱스 이동 전략을 설계하시오.

체크포인트:
1. 과제별로 코드를 직접 실행해 결과를 확인했는가?
2. 정답과 함께 근거(판별 규칙/계산 과정)를 기록했는가?
3. 오답 가능 지점을 한 줄로 점검했는가?
### 고등 오답 패턴
- 코드 구조를 보지 않고 결과만 추측해 들여쓰기/스코프 오류를 놓칩니다.

## 적용 유형
- 문자열 인접 비교 기반 카운트
- 부분문자열 탐색과 인덱스 점프
- 중첩 반복 비교 카운트
- 문자열/리스트/딕셔너리 메서드 선택
- 전역 변수와 슬라이싱 결합 갱신

## {view:teacher} 과제
- 초등: 6문항
- 중등: 8문항
- 고등: 10~12문항

## {view:teacher} 평가
- 항목: 미니모의 2
- 오답코드: 인덱스, 종료조건, 분기누락, 메서드혼동, 스코프

평가 체크:
1. 인덱스 이동 규칙(1칸/점프)을 구분해 설명했는가
2. 연속 구간 카운트의 기준 문자 갱신 시점을 설명했는가
3. 메서드 선택 근거를 자료형 기준으로 제시했는가
4. 문자열 치환에서 불변성과 슬라이싱 결합을 설명했는가

## {view:teacher} 교사 메모
- 웹 렌더 규칙: COMMON + 선택 학년 섹션만 노출합니다.
- 수업 후 오답코드를 기준으로 다음 주차 보강 포인트를 기록합니다.
