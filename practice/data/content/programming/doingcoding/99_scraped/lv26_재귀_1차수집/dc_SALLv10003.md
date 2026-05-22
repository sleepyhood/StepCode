---
id: dc_SALLv10003
legacy_id: 
title: "03. [재귀함수 - 3] 재귀적 눈금 그리기"
platform: "doingcoding"
is_scraped: false
time_limit: "1s"
memory_limit: "256MB"
tags: [doingcoding, recursion, fractal]
---

# [SALLv10003번] 03. [재귀함수 - 3] 재귀적 눈금 그리기

## 1. 문제 설명

수업에서 알파벳 트리 구조를 배웠습니다.

> **깊이 N의 결과 = 깊이 (N-1)의 결과 + 현재 값 + 깊이 (N-1)의 결과**

이번에는 이 구조를 알파벳이 아닌 **숫자**에 적용해 봅시다.

눈금을 그릴 때 다음과 같은 규칙을 사용합니다.

```
깊이 1:      1
깊이 2:    1 2 1
깊이 3:  1 2 1 3 1 2 1
깊이 4: 1 2 1 3 1 2 1 4 1 2 1 3 1 2 1
```

$N$이 주어지면 깊이 $N$의 눈금 수열을 공백으로 구분하여 한 줄에 출력하세요.

---

## 2. 입출력 설명

* **입력:**
깊이를 나타내는 정수 $N$이 입력됩니다. ($1 \le N \le 16$)

* **출력:**
깊이 $N$의 눈금 수열을 공백으로 구분하여 한 줄에 출력합니다.

---

## 3. 예시

### 예시 입력 1
```text
1
```

### 예시 출력 1
```text
1
```

### 예시 입력 2
```text
2
```

### 예시 출력 2
```text
1 2 1
```

### 예시 입력 3
```text
3
```

### 예시 출력 3
```text
1 2 1 3 1 2 1
```

---

## 4. 힌트

* 수업(`ALLv10003`)의 알파벳 트리 코드에서 알파벳 출력 부분만 숫자로 바꾸면 됩니다.
* 공백 처리: `printf(" %d", depth)` 방식으로 출력하면 맨 앞에 공백이 생깁니다. 대신 가장 첫 번째 숫자를 따로 처리하거나, 전역 변수 `first`를 이용하여 깔끔하게 출력할 수 있습니다.

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 핵심 아이디어
수업(`ALLv10003`)의 `print_tree` 구조와 **동일**합니다.
다른 점은 알파벳 대신 정수 `depth`를 출력한다는 것뿐입니다.

### 모범 코드 (C)
```c
#include <stdio.h>

int is_first = 1; // 첫 번째 숫자 앞에는 공백을 붙이지 않기 위한 플래그

void ruler(int depth) {
    if (depth == 0) return;

    ruler(depth - 1);

    // 첫 번째 출력이면 공백 없이, 이후엔 공백으로 구분
    if (is_first) {
        printf("%d", depth);
        is_first = 0;
    } else {
        printf(" %d", depth);
    }

    ruler(depth - 1);
}

int main() {
    int n;
    scanf("%d", &n);
    ruler(n);
    printf("\n");
    return 0;
}
```

### 실행 추적 (N=2)
```
ruler(2)
  ruler(1)
    ruler(0) → 반환
    출력: "1"    ← is_first=0 이 됨
    ruler(0) → 반환
  출력: " 2"
  ruler(1)
    ruler(0) → 반환
    출력: " 1"
    ruler(0) → 반환
결과: 1 2 1
```
<!-- ANSWER_END -->
