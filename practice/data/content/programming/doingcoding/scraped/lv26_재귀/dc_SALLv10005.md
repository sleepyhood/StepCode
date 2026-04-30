---
id: dc_SALLv10005
legacy_id: 
title: "02. [재귀함수 - 2] 암호 해독 (연속된 1 없는 이진수)"
platform: "doingcoding"
is_scraped: false
time_limit: "1s"
memory_limit: "256MB"
tags: [doingcoding, recursion, backtracking]
---

# [SALLv10005번] 02. 암호 해독 (연속된 1 없는 이진수)

## 1. 문제 설명
어떤 국가의 일급 비밀 암호는 0과 1로 이루어진 이진수입니다. 하지만 이 암호에는 아주 특별한 제약 조건이 하나 있습니다.

**"암호 내에서 1이 두 번 연속으로 나타나면 안 된다."**

예를 들어 $N=3$일 때:
* `000`, `001`, `010`, `100`, `101` 은 가능한 암호입니다.
* `011`, `110`, `111` 은 1이 연속해서 나오므로 불가능한 암호입니다.

암호의 길이 $N$이 주어졌을 때, 위 조건을 만족하는 가능한 암호의 **총 개수**를 구하는 프로그램을 재귀 함수로 작성하세요.

---

## 2. 입출력 설명

* **입력:**
암호의 길이 정수 $N$이 입력됩니다. ($1 \le N \le 25$)

* **출력:**
조건을 만족하는 암호의 총 개수를 출력합니다.

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

---

## 4. 힌트
재귀 함수에 '현재 자릿수'와 '직전 자릿수 값'을 매개변수로 넘겨보세요. 만약 직전 값이 1이었다면 현재 자릿수에는 0만 올 수 있습니다.

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (C)
```c
#include <stdio.h>

long long count = 0;
int target_n;

// pos: 현재 자릿수 (0~n-1), last: 직전 자리에 놓인 숫자 (0 or 1)
void solve(int pos, int last) {
    if (pos == target_n) {
        count++;
        return;
    }

    // 현재 자리에 0을 놓는 경우 (언제나 가능)
    solve(pos + 1, 0);

    // 현재 자리에 1을 놓는 경우 (직전 자리가 1이 아닐 때만 가능)
    if (last == 0) {
        solve(pos + 1, 1);
    }
}

int main() {
    scanf("%d", &target_n);
    // 첫 자리는 직전 값이 없으므로 last=0으로 취급하여 0과 1 모두 올 수 있게 함
    // 또는 첫 자리에 0을 놓는 경우와 1을 놓는 경우를 직접 호출
    solve(1, 0); // 첫 자리에 0
    solve(1, 1); // 첫 자리에 1
    printf("%lld", count);
    return 0;
}
```
<!-- ANSWER_END -->
