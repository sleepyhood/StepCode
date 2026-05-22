---
id: dc_ALLv05013
legacy_id: 
title: "13. [재귀함수 - 13] 8진수 변환 (진법 변환 심화)"
platform: "doingcoding"
is_scraped: false
time_limit: "1s"
memory_limit: "256MB"
tags: [doingcoding, recursion, tutorial]
---

# [ALLv05013번] 13. [재귀함수 - 13] 8진수 변환 (진법 변환 심화)

## 1. 문제 설명
이전 수업(`ALLv05011`)에서는 10진수를 **어떤 진수 $N$이든** 변환하는 범용 함수를 만들었습니다.

이번에는 그 원리를 특정 진수(8진수)에 집중해서 다시 한번 확실히 이해해 봅시다.

8진수 변환은 10진수를 8로 계속 나누어, **나머지를 역순으로 이어 붙이는** 과정입니다. 재귀 함수를 사용하면 이 '역순 출력'을 매우 자연스럽게 구현할 수 있습니다.

10진수 양의 정수 $N$이 주어졌을 때, 이를 8진수로 변환하여 출력하는 프로그램을 재귀 함수로 작성하세요.

---

## 2. 입출력 설명

* **입력:**
첫째 줄에 10진수 양의 정수 $N$이 주어집니다. ($1 \le N \le 1{,}000{,}000$)

* **출력:**
$N$을 8진수로 변환한 결과를 출력합니다.

---

## 3. 예시

### 예시 입력 1
```text
8
```

### 예시 출력 1
```text
10
```

### 예시 입력 2
```text
255
```

### 예시 출력 2
```text
377
```

---

## 4. 힌트
`ALLv05011`에서 만든 `convert(n, base)` 함수의 `base` 자리에 `8`을 넣으면 됩니다.

재귀 함수의 구조를 다시 한번 떠올려 보세요:
- **기저 조건**: `n`이 8보다 작으면 그대로 출력하고 종료
- **재귀 호출**: `convert(n / 8)`로 앞자리 먼저 출력
- **현재 자리**: `n % 8`을 출력

```
void convert(int n):
    if n < 8: print(n); return
    convert(n / 8)
    print(n % 8)
```

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (C)
```c
#include <stdio.h>

void to_octal(int n) {
    // 기저 조건: 8보다 작으면 바로 출력
    if (n < 8) {
        printf("%d", n);
        return;
    }
    // 재귀 호출로 앞자리 먼저 처리
    to_octal(n / 8);
    // 현재 자리(나머지) 출력
    printf("%d", n % 8);
}

int main() {
    int n;
    scanf("%d", &n);
    to_octal(n);
    printf("\n");
    return 0;
}
```
<!-- ANSWER_END -->
