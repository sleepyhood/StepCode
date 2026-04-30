---
id: dc_SALLv05008
legacy_id: 
title: "08. [재귀함수 - 8] 계단식 재귀 함수"
platform: "doingcoding"
is_scraped: false
time_limit: "1s"
memory_limit: "256MB"
tags: [doingcoding, recursion, practice]
---

# [SALLv05008번] 07. 계단식 재귀 함수

## 1. 문제 설명
다음과 같은 규칙을 가진 재귀 함수 $f(n)$을 작성하고, 입력받은 $n$에 대한 결과값을 출력하세요.

* $n \le 0$ 이면, $f(n) = 1$
* $n$이 3의 배수이면, $f(n) = n + f(n-1)$
* $n$이 3의 배수가 아니면, $f(n) = n \times f(n-2)$

이 문제는 매개변수의 값에 따라 서로 다른 길을 선택하는 '조건부 재귀'를 연습하기 위한 문제입니다.

---

## 2. 입출력 설명

* **입력:**
정수 $n$이 입력됩니다. ($0 \le n \le 15$)

* **출력:**
$f(n)$의 결과값을 출력합니다.

---

## 3. 예시

### 예시 입력 1
```text
5
```

### 예시 출력 1
```text
60
```
*(설명: f(5) = 5 * f(3) = 5 * (3 + f(2)) = 5 * (3 + (2 * f(0))) = 5 * (3 + 2) = 25... 아차, 예시를 다시 계산합니다.)*
* f(5) = 5 * f(3) (3의 배수 아님)
* f(3) = 3 + f(2) (3의 배수)
* f(2) = 2 * f(0) (3의 배수 아님)
* f(0) = 1 (기저 조건)
* 계산: 5 * (3 + (2 * 1)) = 5 * 5 = 25.

### 예시 출력 1 (수정)
```text
25
```

---

## 4. 힌트
`if`와 `else if`를 사용하여 문제에 주어진 3가지 조건을 정확히 나누어 구현해 보세요.

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (C)
```c
#include <stdio.h>

long long f(int n) {
    if (n <= 0) return 1;
    if (n % 3 == 0) return n + f(n - 1);
    else return n * f(n - 2);
}

int main() {
    int n;
    scanf("%d", &n);
    printf("%lld", f(n));
    return 0;
}
```
<!-- ANSWER_END -->
