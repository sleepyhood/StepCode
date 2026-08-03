---
id: "SP102v1802"
db_id: LOCAL
legacy_id: null
title: "02. [문자열2(함수)] 사전순 극단 단어 추적기"
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

# 02. [문자열2(함수)] 사전순 극단 단어 추적기

## 1. 문제 설명
영단어 학습 프로그램에서 사용자가 입력하는 여러 단어들 중 사전순으로 가장 앞에 나오는 단어와 가장 뒤에 나오는 단어를 자동으로 추적하고자 합니다.

첫째 줄에 입력받을 단어의 개수 N이 주어집니다.

이후 N개의 줄에 걸쳐 단어가 한 줄에 하나씩 주어집니다. 

단어를 하나씩 입력받을 때마다 사전순 비교를 수행하여 다음을 갱신합니다.
- 사전순으로 가장 앞서는 단어(`min_word`)를 지속적으로 추적하고 갱신합니다.
- 사전순으로 가장 뒤에 오는 단어(`max_word`)를 지속적으로 추적하고 갱신합니다.

모든 단어 입력이 끝난 후, 첫째 줄에 **사전순으로 가장 앞서는 단어 `min_word`**, 둘째 줄에 **사전순으로 가장 뒤에 오는 단어 `max_word`**를 출력하는 프로그램을 작성하세요.

---

## 2. 입출력 설명

* **입력:**
첫째 줄에 단어의 개수 N이 주어집니다. (1 이상 20 이하의 정수)
둘째 줄부터 N개의 줄에 걸쳐 단어가 한 줄에 하나씩 주어집니다. (각 단어는 영문 소문자 1자 이상 30자 이하)

* **출력:**
첫째 줄에 사전순으로 가장 앞서는 단어 `min_word`를 출력합니다.
둘째 줄에 사전순으로 가장 뒤에 오는 단어 `max_word`를 출력합니다.

---

## 3. 예시
### 예시 입력 1
```text
4
banana
apple
dog
cat
```

### 예시 출력 1
```text
apple
dog
```

### 예시 입력 2
```text
3
korea
japan
china
```

### 예시 출력 2
```text
china
korea
```

---

## 4. 힌트
### 💡 힌트 (개념 조합)
- 이 문제는 반복문 내에서 **사전순 비교 함수(`strcmp`)**와 **문자열 대입/복사 함수(`strcpy`)**를 조합하여 최소/최대 단어를 추적하는 문제입니다.
- C언어 구동 방식:
  - 첫 번째 단어를 입력받았을 때는 `strcpy(min_word, word)`와 `strcpy(max_word, word)`로 두 변수를 초기화합니다.
  - 이후 단어들을 받으면서 `strcmp(word, min_word) < 0` 이면 `strcpy(min_word, word)`를 실행합니다.
  - 마찬가지로 `strcmp(word, max_word) > 0` 이면 `strcpy(max_word, word)`를 실행하여 최댓값을 갱신합니다.
- Python에서는 `word < min_word`, Java에서는 `word.compareTo(min_word) < 0` 조건식으로 쉽게 비교하여 갱신할 수 있습니다.
