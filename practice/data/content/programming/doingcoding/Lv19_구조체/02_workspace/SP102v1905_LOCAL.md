---
id: "SP102v1905"
db_id: LOCAL
legacy_id: null
title: "05. [구조체-배열] 가장 점수가 높은 학생 탐색"
platform: "doingcoding"
level: "Low"
tags:
  - "SLv19 구조체"
authors:
  - "root"
supported_languages:
  - "C"
  - "C++"
  - "Java"
  - "Python3"
time_limit: "1s"
memory_limit: "256MB"
accepted_user_count: 50
has_hint: "true"
archived_at: "2026-08-03"
---

# 05. [구조체-배열] 가장 점수가 높은 학생 탐색

## 1. 문제 설명
$N$명의 학생 정보(이름, 수학 점수)를 구조체 배열에 입력받아 저장합니다.

수학 점수가 **가장 높은 1등 학생**의 정보를 탐색하여 출력하는 프로그램을 작성하세요.
만약 최고 점수를 가진 학생이 여러 명이라면 **가장 먼저 입력된 학생**의 정보를 출력합니다.

---

## 2. 입출력 설명

* **입력:**
첫 번째 줄에 학생 수 $N$이 주어집니다. ($1 \le N \le 100$)
다음 $N$개 줄에 각 학생의 이름과 수학 점수가 공백으로 주어집니다.

* **출력:**
수학 점수가 가장 높은 학생의 정보를 `이름: [이름], 점수: [점수]` 형식으로 한 줄에 출력합니다.

---

## 3. 예시
### 예시 입력 1
```text
3
Amy 80
Ben 95
Cara 87
```

### 예시 출력 1
```text
이름: Ben, 점수: 95
```

---

## 4. 힌트
- 최댓값과 최고 점수 학생의 인덱스를 저장할 변수 `max_idx = 0`을 초기화하고 반복문을 순회하세요.
- `if (arr[i].score > arr[max_idx].score)` 조건 만족 시 `max_idx = i`로 갱신하면 동점자 시 첫 번째 학생이 유지됩니다.
---
