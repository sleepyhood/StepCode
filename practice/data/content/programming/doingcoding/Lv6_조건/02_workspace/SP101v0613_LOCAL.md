---
id: "SP101v0613"
db_id: "LOCAL"
legacy_id: null
title: "[숙제 3] 등급 판정기"
platform: "doingcoding"
level: "Low"
tags:
  - "Lv6 조건"
authors:
  - "LOCAL"
supported_languages:
  - "C"
  - "C++"
  - "Java"
  - "Python3"
time_limit: "1s"
memory_limit: "256MB"
accepted_user_count: 0
has_hint: "true"
archived_at: "2026-05-19"
---

# [숙제 3] 등급 판정기

## 1. 문제 설명
학생의 학점을 의미하는 알파벳을 입력받아, 해당하는 평가 결과를 출력하는 프로그램을 작성하세요.

대문자와 소문자를 모두 받아들입니다.

- `A` 또는 `a` → `우수`
- `B` 또는 `b` → `보통`
- `C` 또는 `c` → `노력요함`
- 그 외의 문자 → `잘못된 학점`

---

## 2. 입출력 설명

* **입력:**
알파벳 문자 하나가 입력됩니다.

* **출력:**
해당 학점의 평가 결과를 출력합니다.

---

## 3. 예시
### 예시 입력 1
```text
A
```

### 예시 출력 1
```text
우수
```

### 예시 입력 2
```text
b
```

### 예시 출력 2
```text
보통
```

### 예시 입력 3
```text
Z
```

### 예시 출력 3
```text
잘못된 학점
```

---

## 4. 힌트
### 💡 힌트
수업 시간에 배운 **16번 문제(알파벳 신호등)**와 동일한 로직입니다.
`char` 타입 문자를 `switch`에서 사용할 때, 대문자와 소문자를 연속으로 묶어서 처리해보세요!
---
