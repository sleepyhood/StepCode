---
id: "SP102v1804"
db_id: LOCAL
legacy_id: null
title: "04. [문자열2(함수)] 웹 URL 쿼리 스트링 파서"
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

# 04. [문자열2(함수)] 웹 URL 쿼리 스트링 파서

## 1. 문제 설명
웹 서버의 수신 로그 데이터에는 URL 주소 뒤에 파라미터가 덧붙여진 쿼리 스트링(Query String) 문자열이 입력됩니다.

주어지는 URL 문자열에는 반드시 `age=` 파라미터와 `score=` 파라미터가 포함되어 있습니다.

예: `http://site.com/page?age=25&score=100`

이 URL 문자열에서 문자열 탐색 및 파싱 함수를 활용하여 다음을 수행하세요.
1. `age=` 뒤에 오는 숫자 문자열을 찾아 정수 `age`로 변환합니다.
2. `score=` 뒤에 오는 숫자 문자열을 찾아 정수 `score`로 변환합니다.

추출한 두 정수에 대해 첫째 줄에는 **두 수의 합(`age + score`)**, 둘째 줄에는 **두 수의 곱(`age * score`)**을 출력하는 프로그램을 작성하세요.

---

## 2. 입출력 설명

* **입력:**
첫째 줄에 `age=` 와 `score=` 파라미터가 포함된 URL 문자열이 한 줄로 입력됩니다. (문자열 길이는 20자 이상 100자 이하, age와 score 수치는 1 이상 1,000 이하의 정수)

* **출력:**
첫째 줄에 추출된 두 정수의 합을 출력합니다.
둘째 줄에 추출된 두 정수의 곱을 출력합니다.

---

## 3. 예시
### 예시 입력 1
```text
http://site.com/page?age=25&score=100
```

### 예시 출력 1
```text
125
2500
```

### 예시 입력 2
```text
http://site.com/page?age=15&score=200
```

### 예시 출력 2
```text
215
3000
```

---

## 4. 힌트
### 💡 힌트 (개념 조합)
- 이 문제는 **특정 파라미터 위치 탐색 함수(`strstr` / `strchr`)**와 **문자열-수치 변환 함수(`atoi`)**를 조합하여 실무 데이터를 파싱하는 문제입니다.
- C언어 구동 방식:
  - `char *p1 = strstr(url, "age=");` 로 `age=` 의 시작 포인터를 찾은 뒤, `"age="` 의 길이(4자)만큼 뒤로 이동한 `p1 + 4` 포인터를 `atoi(p1 + 4)`에 전달하여 정수 `age`를 추출합니다.
  - 동일하게 `char *p2 = strstr(url, "score=");` 로 위치를 찾고 `atoi(p2 + 6)`을 호출하여 정수 `score`를 추출합니다.
- Python에서는 `url.split("age=")[1].split("&")[0]` 등으로 분할 후 `int()` 변환하고, Java에서도 `split()` 또는 `indexOf()`로 구현할 수 있습니다.
