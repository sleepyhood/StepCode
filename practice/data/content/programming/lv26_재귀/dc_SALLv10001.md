---
id: dc_SALLv10001
title: "01. [재귀함수 - 1] N과 M - 1"
platform: "doingcoding"
is_scraped: true
time_limit: "1s"
memory_limit: "512MB"
tags: [doingcoding, scraped]
source_url: "http://edu.doingcoding.com/problem/SALLv10001"
---

# [SALLv10001번] 01. [재귀함수 - 1] N과 M - 1

## 1. 문제 설명
자연수 N과 M이 주어졌을 때, 아래 조건을 만족하는 길이가 M인 수열을 모두 구하는 프로그램을 작성하시오.

* 1부터 N까지 자연수 중에서 중복 없이 M개를 고른 수열
* 고른 수열은 오름차순이어야 한다.

---

## 2. 입출력 설명

* **입력:**
첫째 줄에 자연수 N과 M이 주어진다. (1 ≤ M ≤ N ≤ 8)

* **출력:**
한 줄에 하나씩 문제의 조건을 만족하는 수열을 출력한다. 중복되는 수열을 여러 번 출력하면 안되며, 각 수열은 공백으로 구분해서 출력해야 한다.

수열은 사전 순으로 증가하는 순서로 출력해야 한다.

---

## 3. 예시

### 예시 입력 1
```text
3 1
```

### 예시 출력 1
```text
1
2
3
```

### 예시 입력 2
```text
4 2
```

### 예시 출력 2
```text
1 2
1 3
1 4
2 3
2 4
3 4
```

### 예시 입력 3
```text
4 4
```

### 예시 출력 3
```text
1 2 3 4
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
