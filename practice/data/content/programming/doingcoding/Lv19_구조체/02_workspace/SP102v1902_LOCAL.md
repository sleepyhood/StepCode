---
id: "SP102v1902"
db_id: LOCAL
legacy_id: null
title: "02. [구조체-함수] 더 두꺼운 책 찾기 함수"
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

# 02. [구조체-함수] 더 두꺼운 책 찾기 함수

## 1. 문제 설명
두 권의 책 정보(제목, 페이지 수)를 구조체 변수에 각각 입력받습니다.

두 책 구조체를 매개변수로 전달받아 페이지 수를 비교한 뒤, **더 두꺼운(페이지 수가 많은) 책의 구조체를 반환하는 함수**를 작성하세요.

페이지 수가 같다면 첫 번째 책을 반환하고, 메인 로직에서는 반환받은 책의 제목을 출력합니다.

---

## 2. 입출력 설명

* **입력:**
첫 번째 줄에 첫 번째 책의 제목과 페이지 수가 공백으로 주어집니다.
두 번째 줄에 두 번째 책의 제목과 페이지 수가 공백으로 주어집니다.

* **출력:**
더 두꺼운 책의 제목을 한 줄에 출력합니다.

---

## 3. 예시
### 예시 입력 1
```text
BookA 320
BookB 150
```

### 예시 출력 1
```text
BookA
```

---

## 4. 힌트
- `Book getThickerBook(Book b1, Book b2)` 형태의 함수를 구현하세요.
- 함수 내부에서 `b1.pages >= b2.pages`를 판단하여 더 인수가 큰 책 구조체를 반환합니다.
---
