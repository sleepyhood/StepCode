---
id: "SP102v1803"
db_id: LOCAL
legacy_id: null
title: "03. [문자열2(함수)] 스팸 메일 필터링 및 서식 리포트"
platform: "doingcoding"
level: "Low"
tags:
  - "SLv18 문자열2(함수)"
authors:
  - "root"
supported_languages:
  - "C"
  - "C++"
  - "Java"
  - "Python3"
time_limit: "1s"
memory_limit: "256MB"
accepted_user_count: 0
has_hint: "true"
archived_at: "2026-08-03"
---

# 03. [문자열2(함수)] 스팸 메일 필터링 및 서식 리포트

## 1. 문제 설명
사내 전자메일 시스템에서는 수신된 메일 제목들을 검사하여 스팸 메일을 필터링하고 이를 보관함 서식 보고서 문자열 버퍼 `report`에 작성하려고 합니다.

첫째 줄에 검사할 메일 제목의 개수 N이 주어집니다.

이후 N개의 줄에 걸쳐 메일 제목이 한 줄에 하나씩 주어집니다.

메일 제목을 검사할 때 다음 규칙을 적용합니다.
1. 메일 제목 내에 스팸 키워드인 `"AD"` 또는 `"LOAN"`이 포함되어 있는지 탐색합니다.
2. 두 키워드 중 하나라도 포함되어 있다면, 스팸 번호 `spam_cnt`를 1 증가시키고 임시 서식 변수에 `"[SPAM #spam_cnt] 메일제목"` 서식 형태로 저장합니다.
3. 생성된 서식 문자열을 보고서 버퍼 `report`에 줄바꿈(`"\n"`)을 포함하여 결합합니다.
4. 만약 N개의 메일 중 스팸 메일이 단 하나도 없다면, 보고서 버퍼 `report`에 `"CLEAN"`을 저장합니다.

보고서 완성이 끝난 후, 첫째 줄에 **최종 작성된 보고서 버퍼 `report`**, 둘째 줄에 **보고서 버퍼 `report`의 전체 문자열 길이**를 출력하는 프로그램을 작성하세요.

---

## 2. 입출력 설명

* **입력:**
첫째 줄에 메일 제목의 개수 N이 주어집니다. (1 이상 10 이하의 정수)
둘째 줄부터 N개의 줄에 걸쳐 메일 제목이 한 줄에 하나씩 주어집니다. (각 메일 제목은 영문 및 공백 포함 1자 이상 50자 이하)

* **출력:**
첫째 줄에 생성된 스팸 필터링 보고서 버퍼 `report`를 출력합니다.
둘째 줄에 보고서 버퍼 `report`의 전체 길이를 정수로 출력합니다.

---

## 3. 예시
### 예시 입력 1
```text
3
[AD] Special Offer Sale
Weekly Work Log Report
Fast Unsecured LOAN Offer
```

### 예시 출력 1
```text
[SPAM #1] [AD] Special Offer Sale
[SPAM #2] Fast Unsecured LOAN Offer
70
```

### 예시 입력 2
```text
2
Hello Weekly Team Report
Tomorrow Meeting Schedule
```

### 예시 출력 2
```text
CLEAN
5
```

---

## 4. 힌트
- **핵심 아이디어**: 제목 내 특정 키워드 탐색, 정수 번호가 포함된 서식 생성, 보고서 버퍼 결합을 순차적으로 수행하는 문제입니다.
- **생각해볼 점**: 
  1. 메일 제목 안에 특정 단어("AD", "LOAN")가 포함되어 있는지 부분 문자열 탐색 함수(또는 포함 여부 연산자)로 어떻게 확인할까요?
  2. 번호가 포함된 양식(`[SPAM #n] ...`)을 화면 출력이 아닌 '문자열 변수'에 서식화하여 작성한 뒤 최종 버퍼에 결합해 보세요.
