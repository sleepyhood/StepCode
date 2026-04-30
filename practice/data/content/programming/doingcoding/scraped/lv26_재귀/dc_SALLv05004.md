---
id: dc_SALLv05004
legacy_id: 
title: "04. [재귀함수 - 4] 트리보나치 수열 (Tribonacci)"
platform: "doingcoding"
is_scraped: false
time_limit: "1s"
memory_limit: "256MB"
tags: [doingcoding, recursion, practice]
---

# [SALLv05004번] 04. 트리보나치 수열 (Tribonacci)

## 1. 문제 설명
피보나치 수열이 앞의 두 항을 더하는 것이라면, **트리보나치(Tribonacci) 수열**은 앞의 세 항을 더하여 만드는 수열입니다.

수열의 시작이 다음과 같을 때, $n$번째 트리보나치 수를 구하는 프로그램을 재귀 함수로 작성해 보세요.

* $T(0) = 0$
* $T(1) = 0$
* $T(2) = 1$
* $T(n) = T(n-1) + T(n-2) + T(n-3)$ (단, $n \ge 3$)

---

## 2. 입출력 설명

* **입력:**
정수 $n$이 입력됩니다. ($0 \le n \le 20$)

* **출력:**
$n$번째 트리보나치 수를 출력합니다.

---

## 3. 예시

### 예시 입력 1
```text
5
```

### 예시 출력 1
```text
2
```


### 예시 입력 2
```text
4
```

### 예시 출력 2
```text
2
```

---

## 4. 힌트
수업에서 배운 피보나치 로직에서 재귀 호출을 하나 더 추가하면 됩니다. `return f(n-1) + f(n-2) + f(n-3);` 형태를 생각해 보세요.

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (C)
```c
#include <stdio.h>

int tribonacci(int n) {
    if (n == 0) return 0;
    if (n == 1) return 0;
    if (n == 2) return 1;
    return tribonacci(n - 1) + tribonacci(n - 2) + tribonacci(n - 3);
}

int main() {
    int n;
    scanf("%d", &n);
    printf("%d", tribonacci(n));
    return 0;
}
```
<!-- ANSWER_END -->
