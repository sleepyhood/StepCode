---
id: "SP102v1903"
db_id: LOCAL
legacy_id: null
title: "03. [구조체-연산] 상품 데이터 평균 가격 계산기"
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

# 03. [구조체-연산] 상품 데이터 평균 가격 계산기

## 1. 문제 설명
두 상품의 정보(상품명, 가격)를 구조체 변수에 각각 입력받아 저장한 뒤, 두 상품의 **평균 가격**을 계산하여 정수로 출력하는 프로그램을 작성하세요.

---

## 2. 입출력 설명

* **입력:**
첫 번째 줄에 첫 번째 상품명과 가격이 공백으로 주어집니다.
두 번째 줄에 두 번째 상품명과 가격이 공백으로 주어집니다.

* **출력:**
두 상품 가격의 정수 평균을 한 줄에 출력합니다. (소수점 이하 버림)

---

## 3. 예시
### 예시 입력 1
```text
ItemA 5000
ItemB 3000
```

### 예시 출력 1
```text
4000
```

---

## 4. 힌트
- 두 상품 구조체의 가격 멤버 `item1.price`와 `item2.price`를 더한 후 2로 나누어 출력합니다.
---
