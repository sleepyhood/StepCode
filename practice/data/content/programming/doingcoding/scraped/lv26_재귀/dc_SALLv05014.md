---
id: dc_SALLv05014
legacy_id: dc_SALLv05004
title: "14. [재귀함수 - 14] 숫자 만들기"
platform: "doingcoding"
is_scraped: true
time_limit: "1s"
memory_limit: "256MB"
tags: [doingcoding, scraped]
source_url: "http://edu.doingcoding.com/problem/SALLv05004"
---

# [SALLv05014번] 13. [재귀함수 - 14] 숫자 만들기

## 1. 문제 설명
숫자 $N$과 집합 $Q$의 원소 개수 $K$, 그리고 $Q$의 원소들이 주어집니다.

$N$보다 작거나 같은 자연수 중 $Q$의 원소들로만(중복 가능) 구성된 가장 큰 수를 출력하는 프로그램을 작성하세요. 집합 $Q$는 1부터 9 사이의 자연수로만 이루어져 있습니다.

예를 들어, $N=657$이고 $Q=\{1, 5, 7\}$일 때, 1, 5, 7로 만들 수 있는 657 이하의 가장 큰 숫자는 577입니다.

---

## 2. 입출력 설명

* **입력:**
첫째 줄에 $N$과 $K$가 공백으로 구분되어 입력됩니다. ($10 \le N \le 100,000,000$, $1 \le K \le 3$)
둘째 줄에 집합 $Q$의 원소 $K$개가 입력됩니다.

* **출력:**
$N$보다 작거나 같은 자연수 중 $Q$의 원소로만 구성된 가장 큰 수를 출력합니다.

---

## 3. 예시

### 예시 입력 1
```text
42 2
1 9
```

### 예시 출력 1
```text
19
```

### 예시 입력 2
```text
7449 2
6 7
```

### 예시 출력 2
```text
6777
```

---

## 4. 힌트
재귀를 통해 가능한 모든 조합을 탐색하며 $N$ 이하의 최대값을 찾아보세요. 이 문제는 백트래킹(탐색)의 기초 원리를 익히기에 좋습니다.

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (C)
```c
#include <stdio.h>

int N, K;
int Q[5];
int max_val = -1;

void solve(int current) {
    if (current > N) return;
    if (current > max_val) max_val = current;
    
    // N이 1억까지이므로, 현재 값이 1억을 넘지 않을 때만 다음 숫자를 붙임
    if (current > 10000000) return;

    for (int i = 0; i < K; i++) {
        solve(current * 10 + Q[i]);
    }
}

int main() {
    scanf("%d %d", &N, &K);
    for (int i = 0; i < K; i++) {
        scanf("%d", &Q[i]);
    }
    for (int i = 0; i < K; i++) {
        solve(Q[i]);
    }
    printf("%d", max_val);
    return 0;
}
```
<!-- ANSWER_END -->
