---
id: dc_ALLv05008
legacy_id: dc_P301v2609
title: "09. [재귀함수 - 9] 삼각형 출력하기"
platform: "doingcoding"
is_scraped: true
time_limit: "1s"
memory_limit: "256MB"
tags: [doingcoding, scraped]
source_url: "http://edu.doingcoding.com/problem/P301v2609"
---

# [ALLv05008번] 09. [재귀함수 - 9] 삼각형 출력하기

## 1. 문제 설명
n이 입력되면 다음과 같은 삼각형을 출력하시오.

예)

n이 5이면

\*

\*\*

\*\*\*

\*\*\*\*

\*\*\*\*\*

# **절대로 반복문을 돌리지 말고<u>재귀함수로만</u>푸세요.**

---

## 2. 입출력 설명

* **입력:**
길이 n이 입력된다.(n은 1이상 150이하)

* **출력:**
삼각형을 출력한다.

---

## 3. 예시

### 예시 입력 1
```text
3
```

### 예시 출력 1
```text
*
**
***
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
