---
id: dc_SALLv10001
legacy_id: dc_SP301v2606
title: "01. [재귀함수 - 6] 정사면체 주사위"
platform: "doingcoding"
is_scraped: true
time_limit: "1s"
memory_limit: "256MB"
tags: [doingcoding, scraped]
source_url: "http://edu.doingcoding.com/problem/SP301v2606"
---

# [SALLv10001번] 01. [재귀함수 - 6] 정사면체 주사위

## 1. 문제 설명
정사면체 주사위는 주사위의 면이 4개 있는 주사위 입니다.

이 주사위를 n번 던져서 나온 숫자의 합 중, 제일 자주 나온 합이 몇번 나왔는지 계산하는 프로그램을 작성해주세요.

---

## 2. 입출력 설명

* **입력:**
첫 줄에 n이 입력됩니다. (1 <= n <= 10)

다음 줄에 주사위의 숫자 4개가 입력됩니다. (숫자는 1 이상 10 이하)

* **출력:**
주사위를 n번 던져서 나온 숫자의 합 중, 가장 자주 나온 합의 횟수를 출력해주세요.

---

## 3. 예시

### 예시 입력 1
```text
3
4 7 7 3
```

### 예시 출력 1
```text
12
```

### 예시 입력 2
```text
3
4 8 1 8
```

### 예시 출력 2
```text
12
```

### 예시 입력 3
```text
6
7 2 4 9
```

### 예시 출력 3
```text
400
```

---

## 4. 힌트
(힌트가 없습니다.)

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (Python)
**(백준 크롤러에서는 정답 코드를 긁어올 수 없으므로, 선생님께서 아래에 직접 보충해 주세요)**

```python
A, B = map(int, input().split())
print(A + B)
```
<!-- ANSWER_END -->
