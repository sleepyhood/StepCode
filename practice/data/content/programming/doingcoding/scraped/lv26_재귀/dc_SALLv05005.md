---
id: dc_SALLv05005
legacy_id: 
title: "05. [재귀함수 - 5] 가중치 피보나치 수열"
platform: "doingcoding"
is_scraped: false
time_limit: "1s"
memory_limit: "256MB"
tags: [doingcoding, recursion, practice]
---

# [SALLv05005번] 05. 가중치 피보나치 수열

## 1. 문제 설명
피보나치 수열의 원형을 조금 변형한 **가중치 피보나치 수열**을 구현해 봅시다. 

이 수열의 정의는 다음과 같습니다.
* $F(0) = 0$
* $F(1) = 1$
* $F(n) = 2 \times F(n-1) + F(n-2)$ (단, $n \ge 2$)

정수 $n$이 입력될 때, 해당 수열의 $n$번째 값을 구하는 프로그램을 재귀 함수로 작성하세요.

---

## 2. 입출력 설명

* **입력:**
정수 $n$이 입력됩니다. ($0 \le n \le 15$)

* **출력:**
$n$번째 가중치 피보나치 수를 출력합니다.

---

## 3. 예시

### 예시 입력 1
```text
3
```

### 예시 출력 1
```text
5
```
*(설명: F(0)=0, F(1)=1, F(2)=2*1 + 0 = 2, F(3)=2*2 + 1 = 5)*

---

## 4. 힌트
수업에서 배운 포비나치 수열이나 트리보나치 수열처럼, 점화식의 계수(곱해지는 수)만 잘 조절하면 됩니다.

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (C)
```c
#include <stdio.h>

long long f(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    return 2 * f(n - 1) + f(n - 2);
}

int main() {
    int n;
    scanf("%d", &n);
    printf("%lld", f(n));
    return 0;
}
```
<!-- ANSWER_END -->
