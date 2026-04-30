---
id: dc_SALLv05008
legacy_id: 
title: "08. [재귀함수 - 8] 역삼각형 출력하기"
platform: "doingcoding"
is_scraped: false
time_limit: "1s"
memory_limit: "256MB"
tags: [doingcoding, recursion, practice]
---

# [SALLv05008번] 08. 역삼각형 출력하기

## 1. 문제 설명
정수 $n$을 입력받아 다음과 같이 역삼각형 모양으로 별을 출력하는 프로그램을 재귀 함수로 작성하세요.

만약 $n=3$이라면:
```text
***
**
*
```

---

## 2. 입출력 설명

* **입력:**
정수 $n$이 입력됩니다. ($1 \le n \le 20$)

* **출력:**
$n$줄에 걸쳐 역삼각형 모양의 별을 출력합니다.

---

## 3. 예시

### 예시 입력 1
```text
3
```

### 예시 출력 1
```text
***
**
*
```

---

## 4. 힌트
재귀 함수 안에서 $n$개의 별을 출력한 뒤, `f(n-1)`을 호출해 보세요. 호출 순서(전위 호출)에 따라 삼각형의 방향이 결정됩니다.

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (C)
```c
#include <stdio.h>

void printStars(int count) {
    if (count <= 0) return;
    printf("*");
    printStars(count - 1);
}

void solve(int n) {
    if (n <= 0) return;
    printStars(n); // 현재 줄 출력
    printf("\n");
    solve(n - 1);  // 다음 줄(개수 감소) 호출
}

int main() {
    int n;
    scanf("%d", &n);
    solve(n);
    return 0;
}
```
<!-- ANSWER_END -->
