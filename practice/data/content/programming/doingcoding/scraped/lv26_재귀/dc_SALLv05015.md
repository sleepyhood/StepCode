---
id: dc_SALLv05015
legacy_id: 
title: "15. [재귀함수 - 15] 재귀의 함정 (피보나치 카운트)"
platform: "doingcoding"
is_scraped: false
time_limit: "1s"
memory_limit: "256MB"
tags: [doingcoding, recursion, practice]
---

# [SALLv05015번] 14. 재귀의 함정 (피보나치 카운트)

## 1. 문제 설명
수업 시간에 배운 대로, 재귀 함수는 자기 자신을 호출하며 문제를 해결합니다. 하지만 어떤 재귀 함수는 똑같은 연산을 수없이 반복하여 매우 느려지기도 합니다. 이를 **"재귀의 함정"**이라고 부릅니다.

대표적인 예가 바로 피보나치 수열($F_n = F_{n-1} + F_{n-2}$)입니다.

입력으로 정수 $N$이 주어졌을 때, 아래의 `fibo` 함수를 사용하여 $F_N$의 값과, **함수가 총 몇 번 호출되었는지**를 구하는 프로그램을 작성하세요.

```c
int fibo(int n) {
    // 여기에 호출 횟수를 카운트하는 로직이 들어가야 합니다.
    if (n <= 1) return n;
    return fibo(n - 1) + fibo(n - 2);
}
```

---

## 2. 입출력 설명

* **입력:**
정수 $N$이 주어집니다. ($1 \le N \le 25$)

* **출력:**
첫째 줄에 피보나치 수 $F_N$의 값을 출력합니다.
둘째 줄에 `fibo` 함수가 호출된 총 횟수를 출력합니다.

---

## 3. 예시

### 예시 입력 1
```text
5
```

### 예시 출력 1
```text
5
15
```
*(설명: F(5)=5이며, 호출 횟수는 F(5):1 + F(4):1 + F(3):2 + F(2):3 + F(1):5 + F(0):3 ... 등등 총 15번입니다.)*

---

## 4. 힌트
수업 시간에 배운 `cnt` 전역 변수를 활용하세요. $N$이 커질수록 호출 횟수가 기하급수적으로 늘어나는 것을 확인할 수 있습니다. $N=25$일 때 호출 횟수가 얼마나 커지는지 직접 확인해 보세요!

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (C)
```c
#include <stdio.h>

int cnt = 0; // 전역 변수

int fibo(int n) {
    cnt++; // 호출될 때마다 1 증가
    if (n <= 1) return n;
    return fibo(n - 1) + fibo(n - 2);
}

int main() {
    int n;
    scanf("%d", &n);
    int result = fibo(n);
    printf("%d\n%d", result, cnt);
    return 0;
}
```
<!-- ANSWER_END -->
