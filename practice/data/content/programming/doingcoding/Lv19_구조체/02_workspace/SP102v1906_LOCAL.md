---
id: "SP102v1906"
db_id: LOCAL
legacy_id: null
title: "06. [구조체-정렬] 학생 이름 알파벳 순 정렬"
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

# 06. [구조체-정렬] 학생 이름 알파벳 순 정렬

## 1. 문제 설명
$N$명의 학생 정보(이름, 학년)를 구조체 배열에 입력받아 저장합니다.

학생들의 이름을 **알파벳 사전순(Lexicographical Order)** 으로 오름차순 정렬하여 출력하는 프로그램을 작성하세요.

정렬 시 문자열 멤버뿐만 아니라 학년 정보까지 포함된 **구조체 객체 전체를 스왑(Struct In-place Swap)** 해야 데이터 한 쌍이 깨지지 않습니다.

---

## 2. 입출력 설명

* **입력:**
첫 번째 줄에 학생 수 $N$이 주어집니다. ($1 \le N \le 100$)
다음 $N$개 줄에 각 학생의 이름과 학년이 공백으로 주어집니다.

* **출력:**
이름이 알파벳 사전순으로 빠른 순서대로 학생의 이름과 학년을 공백으로 구분하여 한 줄에 하나씩 출력합니다.

---

## 3. 예시
### 예시 입력 1
```text
3
Yuna 3
Anna 2
Dora 1
```

### 예시 출력 1
```text
Anna 2
Dora 1
Yuna 3
```

---

## 4. 힌트
- 두 문자열 멤버를 비교할 때 문자열 사전순 비교 함수/메서드를 사용하세요.
  - C: `strcmp(arr[i].name, arr[j].name) > 0`
  - C++ / Java / Python: 사전순 비교 메서드 활용
- 조건 만족 시 구조체 타입 임시 변수를 사용해 `temp = arr[i]; arr[i] = arr[j]; arr[j] = temp;`와 같이 객체 전체를 스왑합니다.
---
