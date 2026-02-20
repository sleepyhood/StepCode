# Python 경시대회 W05 2중/3중 반복/배열 탐색

## 메타
- week: W05
- slug: nested_loop_array
- audience: common, elementary, middle, high

## 학습 목표
- 2중/3중 반복에서 총 연산량과 누적 구조를 분리해서 해석하는 것이 목표입니다.
- 배열/리스트 기반 탐색에서 최댓값 갱신 규칙을 안정적으로 적용하는 것이 목표입니다.
- `continue`, `break`, 플래그 변수로 중첩 루프를 제어하는 흐름을 설명할 수 있는 것이 목표입니다.

## 대상 난이도
- 공통: 초등, 중등, 고등
- 분기: ELEMENTARY, MIDDLE, HIGH

## 공통 이론 (COMMON)
<!-- audience:common -->
### 핵심 개념 요약
- 주제: 2중/3중 반복 + 배열 탐색
- 운영: 개념 20분 + 예측형 25분 + 구현형 15분

### 개념 1) 이중합 분해 (`Σi Σj`) 
- 한 줄 요약: 2중 반복에서 곱 형태 누적을 곱셈 구조로 축약하는 유형입니다.
- 암기 규칙: `Σi Σj (Ai*Bj)` 형태는 `(ΣAi) * (ΣBj)`로 분해 가능하다.
- 풀이 3단계: 각 배열 합 계산 -> 곱셈으로 이중합 계산 -> 후처리 연산 적용한다.
- 함정 포인트: 내부 루프를 모두 전개해 계산하다가 합산 실수가 자주 발생합니다.

![이중합 분해식 블록 다이어그램](./data/theory/images/contest_w05_double_sum_decomposition.svg)

**대표 예시**
```python
a = [1, 2, 3]
b = [4, 5]
s = 0
for i in range(len(a)):
    for j in range(len(b)):
        s += a[i] * b[j]
print(s)
```
```io
input:
(없음)
output:
54
```

**변형 예시**
```python
a = [0, 1, 2, 3]
b = [1, -1]
s = 0
for i in range(len(a)):
    for j in range(len(b)):
        s += a[i] * b[j]
print(s)
```
```io
input:
(없음)
output:
0
```

**함정 예시**
```python
a = [2, 4]
b = [3, 6]
s = 0
for i in range(2):
    for j in range(2):
        s += a[i] + b[j]
print(s)
```
```io
input:
(없음)
output:
30
```

### 개념 2) 3중 반복에서 항 분리 계산
- 한 줄 요약: 3중 반복 누적식에서 항을 분리해 반복 배수를 계산하는 유형입니다.
- 암기 규칙: `a[i] + b[j]*c[k]`는 `a`항과 `b*c`항을 분리해 반복 배수로 계산할 수 있다.
- 풀이 3단계: 각 차원 반복 횟수 계산 -> 항별 누적 배수 산출 -> 최종 합 결합한다.
- 함정 포인트: 모든 항이 같은 배수로 더해진다고 가정하면 오답이 됩니다.

**대표 예시**
```python
a = [1, 2]
b = [0, 3]
c = [1, 2]
t = 0
for i in range(2):
    for j in range(2):
        for k in range(2):
            t += a[i] + b[j] * c[k]
print(t)
```
```io
input:
(없음)
output:
36
```

**변형 예시**
```python
x = [2, 4, 6]
y = [1, 3]
z = [0, 5]
acc = 0
for i in range(3):
    for j in range(2):
        for k in range(2):
            acc += x[i] - y[j] + z[k]
print(acc)
```
```io
input:
(없음)
output:
60
```

**함정 예시**
```python
a = [1, 2]
b = [10, 20]
c = [0, 1]
s = 0
for i in range(2):
    for j in range(2):
        for k in range(2):
            if k == 0:
                s += a[i] + b[j]
            else:
                s -= a[i] + b[j]
print(s)
```
```io
input:
(없음)
output:
0
```

### 개념 3) 배열 탐색 최댓값 갱신 패턴
- 한 줄 요약: 다중 반복으로 후보 값을 비교하며 최대/최소를 갱신하는 유형입니다.
- 암기 규칙: `if candidate > best: best = candidate` 패턴은 초기값과 비교 방향이 핵심이다.
- 풀이 3단계: 초기값 설정 -> 후보 생성 -> 조건 비교 -> 갱신 여부 기록한다.
- 함정 포인트: 초기값을 너무 크게/작게 두면 갱신이 일어나지 않아 결과가 깨집니다.

**대표 예시**
```python
a = [8, 3, 10]
b = [1, 7]
best = 0
for x in a:
    for y in b:
        if x + y > best:
            best = x + y
print(best)
```
```io
input:
(없음)
output:
17
```

**변형 예시**
```python
a = [-3, -1, -7]
b = [2, 5]
best = -10**9
for x in a:
    for y in b:
        if x + y > best:
            best = x + y
print(best)
```
```io
input:
(없음)
output:
4
```

**함정 예시**
```python
a = [5, 1]
b = [2, 3]
best = 100
for x in a:
    for y in b:
        if x + y > best:
            best = x + y
print(best)
```
```io
input:
(없음)
output:
100
```

### 개념 4) 중첩 루프 제어 (`continue`/`break`/플래그)
- 한 줄 요약: 중첩 반복에서 특정 조건 만족 시 탐색을 건너뛰거나 조기 종료하는 유형입니다.
- 암기 규칙: `continue`는 현재 반복만 건너뛰고, `break`는 현재 루프 1단계만 종료한다.
- 풀이 3단계: 루프 깊이를 번호로 표시 -> `continue/break` 적용 범위를 기록 -> 플래그 전파 흐름 확인한다.
- 함정 포인트: `break`가 모든 루프를 한 번에 끝낸다고 오해하면 실행 순서가 뒤틀립니다.

| 제어문 | 즉시 영향 범위 | 바깥 루프 영향 | 대표 사용 목적 | 주의점 |
| --- | --- | --- | --- | --- |
| `continue` | 현재 루프의 "이번 회차"만 건너뜀 | 없음 | 특정 조건 스킵 | 아래 코드 미실행 |
| `break` | 현재 루프 1단계 종료 | 직접 영향 없음 | 조기 탈출 | 중첩일 때 한 단계만 종료 |
| `flag + break` | 현재 루프 종료 후 플래그 확인 | 있음(간접) | 다중 루프 탈출 | 플래그 검사 위치 필수 |

![continue/break 적용 범위 루프 깊이 트리](./data/theory/images/contest_w05_loop_control_depth_tree.svg)

**대표 예시**
```python
for i in range(3):
    for j in range(3):
        if j == 1:
            continue
        print(i, j)
```
```io
input:
(없음)
output:
0 0
0 2
1 0
1 2
2 0
2 2
```

**변형 예시**
```python
flag = 0
for i in range(1, 5):
    for j in range(1, 5):
        if i * j == 6:
            print(i, j)
            flag = 1
            break
    if flag:
        break
```
```io
input:
(없음)
output:
2 3
```

**함정 예시**
```python
for i in range(2):
    for j in range(3):
        if j == 1:
            break
        print(i, j)
    print("-")
```
```io
input:
(없음)
output:
0 0
-
1 0
-
```

### 공통 미니 체크
1. `Σi Σj (Ai*Bj)`를 빠르게 계산하는 변환식을 쓰시오.
2. 3중 반복 식에서 항 분리를 할 때 먼저 계산해야 하는 값 2가지는 무엇인가요?
3. 중첩 루프에서 `break`가 영향을 주는 범위를 어떻게 판단하나요?

## 초등 트랙 (ELEMENTARY)
<!-- audience:elementary -->
### 초등 포인트
- 2중 반복 카운트

### 초등 이론 보강
- 반복 횟수와 누적 변수를 표로 동시에 적는 연습을 합니다.
- 최댓값 갱신은 "초기값 -> 후보 비교 -> 갱신" 3단계로 고정합니다.

초등 규칙 카드:
1. 반복 1회마다 누적 변수 변화를 기록한다.
2. `best` 초기값은 문제 범위에 맞게 둔다.
3. `continue`는 현재 반복만 건너뛴다.

### 초등 연계 연습
1. 2중 반복에서 연산문이 총 몇 번 실행되는지 계산하시오.
2. 후보값 갱신 문제에서 초기값을 바꾸면 결과가 어떻게 달라지는지 설명하시오.

### 초등 오답 패턴
- 비교 연산은 맞게 쓰지만 초기값이 잘못되어 결과가 틀립니다.

## 중등 트랙 (MIDDLE)
<!-- audience:middle -->
### 중등 포인트
- 2중 반복 + 조건 결합

### 중등 이론 보강
- 조건별 집합을 나눠 부분합으로 계산한 뒤 결합합니다.
- `if` 두 개와 `if-else`의 실행 차이를 분리해서 해석합니다.

중등 판별 루틴:
1. 반복 범위를 확정한다.
2. 조건 통과 케이스를 분리한다.
3. 누적식을 항별로 계산해 결합한다.

### 중등 연계 연습
1. 조건이 포함된 3중 반복 코드를 항 분리 방식으로 풀이하시오.
2. `continue`가 있는 코드에서 실제 실행 줄만 추려 쓰시오.

### 중등 오답 패턴
- 조건 분기를 모두 같은 누적식으로 처리해 부호/배수가 틀립니다.

## 고등 트랙 (HIGH)
<!-- audience:high -->
### 고등 포인트
- 2중 반복 + 형변환 결합

### 고등 이론 보강
- 문자열 결합/정수 변환이 들어간 반복 탐색은 "생성 -> 필터 -> 검증" 순서로 해석합니다.
- 조기 종료(`break`)와 탐색 완전성의 균형을 판단하는 훈련이 필요합니다.

고등 판별 프레임:
1. 후보 생성 규칙을 정의한다.
2. 배제 조건(`continue`)을 먼저 적용한다.
3. 검증식 통과 시 종료 범위를 확인한다.

### 고등 연계 연습
1. 4중 반복 탐색에서 가지치기 조건을 2개 이상 설계하시오.
2. 플래그 변수를 사용하지 않고 조기 종료하는 방법을 제시하시오.

### 고등 오답 패턴
- 정답 후보는 찾았지만 종료 범위를 잘못 처리해 출력이 어긋납니다.

## 적용 유형
- 이중합/삼중합 계산
- 배열/리스트 최댓값 탐색
- 조건 분기 포함 중첩 반복 추적
- `continue`/`break` 조기 종료 해석

## {view:teacher} 과제
- 초등: 6문항
- 중등: 8문항
- 고등: 10~12문항

## {view:teacher} 평가
- 항목: 미니모의 1
- 오답코드: 인덱스, 종료조건, 방문처리, 형변환, 연산자 우선순위

평가 체크:
1. 항 분리/부분합으로 계산 근거를 제시했는가
2. 최댓값 갱신 규칙을 초기값부터 설명했는가
3. 조기 종료 범위를 루프 깊이 기준으로 설명했는가

## {view:teacher} 교사 메모
- 웹 렌더 규칙: COMMON + 선택 학년 섹션만 노출합니다.
- 수업 후 오답코드를 기준으로 다음 주차 보강 포인트를 기록합니다.

