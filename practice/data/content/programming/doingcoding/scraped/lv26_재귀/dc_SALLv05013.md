---
id: dc_SALLv05013
legacy_id: dc_SALLv05001
title: "13. [재귀함수 - 13] 9진수 변환"
platform: "doingcoding"
is_scraped: true
time_limit: "2s"
memory_limit: "512MB"
tags: [doingcoding, scraped]
source_url: "http://edu.doingcoding.com/problem/SALLv05001"
---

# [SALLv05013번] 12. [재귀함수 - 13] 9진수 변환

## 1. 문제 설명
10진수 정수를 입력받아 9진수로 변환하여 출력하는 프로그램을 작성하세요.

---

## 2. 입출력 설명

* **입력:**
첫째 줄에 10진수 정수 $T$가 주어진다. ($1 \le T \le 10,000$)

* **출력:**
$T$를 9진수로 변환한 결과를 출력한다.

---

## 3. 예시

### 예시 입력 1
```text
100
```

### 예시 출력 1
```text
121
```

---

## 4. 힌트
수업(ALLv05010)에서 배운 진법 변환의 원리를 9진수에 적용해 보세요. 숫자를 9로 나눈 나머지와 몫을 이용하면 됩니다.

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (C)
```c
#include <stdio.h>

void toBase9(int n) {
    if (n == 0) return;
    toBase9(n / 9);
    printf("%d", n % 9);
}

int main() {
    int n;
    scanf("%d", &n);
    if (n == 0) printf("0");
    else toBase9(n);
    return 0;
}
```
<!-- ANSWER_END -->
