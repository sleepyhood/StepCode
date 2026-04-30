---
id: dc_SALLv10006
legacy_id: 
title: "03. [재귀함수 - 3] 숫자 카드 조합 (목표 합 만들기)"
platform: "doingcoding"
is_scraped: false
time_limit: "1s"
memory_limit: "256MB"
tags: [doingcoding, recursion, backtracking]
---

# [SALLv10006번] 03. 숫자 카드 조합 (목표 합 만들기)

## 1. 문제 설명
여러분에게는 `1`, `2`, `3` 이라는 숫자가 적힌 카드가 무수히 많이 있습니다. 이 카드들 중 **정확히 $N$장**을 골라서, 그 합이 **정확히 $S$**가 되는 서로 다른 조합의 개수를 구하는 프로그램을 작성하세요.

단, 조합을 구성하는 숫자의 구성이 같으면 같은 경우로 취급합니다.
(예를 들어, `1, 1, 3`과 `1, 3, 1`은 같은 조합입니다.)

---

## 2. 입출력 설명

* **입력:**
골라야 하는 카드의 장수 $N$과 목표 합 $S$가 공백으로 구분되어 입력됩니다.
($1 \le N \le 15$, $1 \le S \le 45$)

* **출력:**
합이 $S$가 되는 서로 다른 조합의 개수를 출력합니다.

---

## 3. 예시

### 예시 입력 1
```text
3 5
```

### 예시 출력 1
```text
2
```
*(설명: {1, 1, 3}, {1, 2, 2} 두 가지 조합이 가능합니다.)*

---

## 4. 힌트
중복된 조합을 피하기 위해서는 재귀 호출 시 **"현재 고른 숫자보다 크거나 같은 숫자만 다음에 고르도록"** 범위를 제한하면 됩니다.

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (C)
```c
#include <stdio.h>

int target_n, target_s;
int count = 0;

// count_so_far: 현재까지 고른 카드 장수
// sum_so_far: 현재까지 고른 카드의 합
// start_num: 중복 조합을 피하기 위해 다음에 고를 수 있는 최소 숫자
void solve(int count_so_far, int sum_so_far, int start_num) {
    // 정확히 N장을 골랐을 때
    if (count_so_far == target_n) {
        if (sum_so_far == target_s) {
            count++;
        }
        return;
    }

    // 현재 합이 이미 목표치를 넘었거나, 남은 장수를 3으로 채워도 모자란 경우 등 
    // 가지치기를 할 수 있지만, N=15 정도는 단순 탐색으로도 충분합니다.
    if (sum_so_far > target_s) return;

    for (int i = start_num; i <= 3; i++) {
        solve(count_so_far + 1, sum_so_far + i, i);
    }
}

int main() {
    scanf("%d %d", &target_n, &target_s);
    solve(0, 0, 1);
    printf("%d", count);
    return 0;
}
```
<!-- ANSWER_END -->
