---
id: "SP101v0611"
db_id: "LOCAL"
legacy_id: null
title: "11. [조건-switch case default] 음료수 자판기"
platform: "doingcoding"
level: "Low"
tags:
  - "SLv6 조건"
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

# 11. [조건-switch case default] 음료수 자판기

## 1. 문제 설명
자판기에서 메뉴 번호를 입력받아 해당 음료의 이름을 출력하는 프로그램을 작성하세요.

자판기의 메뉴 구성은 다음과 같습니다.
- 1번: 콜라
- 2번: 사이다
- 3번: 환타

위 메뉴에 없는 번호가 입력되면 `준비중인 음료입니다`를 출력합니다.

---

## 2. 입출력 설명

* **입력:**
정수 하나가 입력됩니다.

* **출력:**
해당 번호의 음료 이름 또는 `준비중인 음료입니다`를 출력합니다.

---

## 3. 예시
### 예시 입력 1
```text
1
```

### 예시 출력 1
```text
콜라
```

### 예시 입력 2
```text
4
```

### 예시 출력 2
```text
준비중인 음료입니다
```

---

## 4. 힌트
### 💡 힌트
수업 시간에 배운 **14번 문제(식당 키오스크)**와 완전히 똑같은 구조를 가집니다. `default`를 활용하여 예외 처리를 완성해보세요.
---
