---
id: dc_SALLv05010
legacy_id: dc_SP301v2604
title: "10. [재귀함수 - 10] 2진수 변환"
platform: "doingcoding"
is_scraped: true
time_limit: "1s"
memory_limit: "256MB"
tags: [doingcoding, scraped]
source_url: "http://edu.doingcoding.com/problem/SP301v2604"
---

# [SALLv05010번] 10. [재귀함수 - 10] 2진수 변환

## 1. 문제 설명
어떤 10진수 n이 주어지면 2진수로 변환해서 출력하시오.

예)
10 ----> 1010
0----> 0
1----> 1
2----> 10
1024---->10000000000

---

## 2. 입출력 설명

* **입력:**
10진수 정수 n이 입력된다. (n은 0이상 21억 이하)

* **출력:**
2진수로 변환해서 출력한다.

---

## 3. 예시

### 예시 입력 1
```text
7
```

### 예시 출력 1
```text
111
```

---

## 4. 힌트
수업(ALLv05010)에서 배운 진법 변환의 원리를 2진수에 적용해 보세요.

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (C)
```c
#include <stdio.h>

void toBinary(int n) {
    if (n == 0) return;
    toBinary(n / 2);
    printf("%d", n % 2);
}

int main() {
    int n;
    scanf("%d", &n);
    if (n == 0) printf("0");
    else toBinary(n);
    return 0;
}
```
<!-- ANSWER_END -->
