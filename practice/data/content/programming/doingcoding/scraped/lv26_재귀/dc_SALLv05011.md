---
id: dc_SALLv05011
legacy_id: dc_SALLv05002
title: "11. [재귀함수 - 11] 단어 나누기"
platform: "doingcoding"
is_scraped: true
time_limit: "2s"
memory_limit: "128MB"
tags: [doingcoding, scraped]
source_url: "http://edu.doingcoding.com/problem/SALLv05002"
---

# [SALLv05011번] 11. [재귀함수 - 11] 단어 나누기

## 1. 문제 설명
알파벳 소문자로 이루어진 단어를 가지고 아래와 같은 과정을 해 보려고 한다.

먼저 단어에서 임의의 두 부분을 골라서 단어를 쪼갠다. 즉, 주어진 단어를 세 개의 더 작은 단어로 나누는 것이다. 각각은 적어도 길이가 1 이상인 단어여야 한다. 이제 이렇게 나눈 세 개의 작은 단어들을 앞뒤를 뒤집고, 이를 다시 원래의 순서대로 합친다.

예를 들어,
* 단어 : arrested
* 세 단어로 나누기 : ar / rest / ed
* 각각 뒤집기 : ra / tser / de
* 합치기 : ratserde

단어가 주어지면, 이렇게 만들 수 있는 단어 중에서 사전순으로 가장 앞서는 단어를 출력하는 프로그램을 작성하시오.

---

## 2. 입출력 설명

* **입력:**
첫째 줄에 영어 소문자로 된 단어가 주어진다. 길이는 3 이상 50 이하이다.

* **출력:**
첫째 줄에 구하고자 하는 단어를 출력하면 된다.

---

## 3. 예시

### 예시 입력 1
```text
mobitel
```

### 예시 출력 1
```text
bometil
```

---

## 4. 힌트
단어를 세 부분으로 나누는 모든 경우를 재귀 또는 반복문을 통해 탐색해 보세요.

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (C)
```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char input[55];
char best[55];

void reverse(char *s, int start, int end) {
    while (start < end) {
        char temp = s[start];
        s[start] = s[end];
        s[end] = temp;
        start++;
        end--;
    }
}

int main() {
    scanf("%s", input);
    int len = strlen(input);
    strcpy(best, "{"); // 사전순으로 가장 뒤에 오는 문자

    for (int i = 1; i < len - 1; i++) {
        for (int j = i + 1; j < len; j++) {
            char current[55];
            strcpy(current, input);
            reverse(current, 0, i - 1);
            reverse(current, i, j - 1);
            reverse(current, j, len - 1);
            if (strcmp(current, best) < 0) {
                strcpy(best, current);
            }
        }
    }
    printf("%s", best);
    return 0;
}
```
<!-- ANSWER_END -->
