---
id: dc_SALLv10008
legacy_id: 
title: "05. [재귀함수 - 5] 국가대표 선발 (조합 nCr)"
platform: "doingcoding"
is_scraped: false
time_limit: "1s"
memory_limit: "256MB"
tags: [doingcoding, recursion, backtracking]
---

# [SALLv10008번] 05. 국가대표 선발 (조합 nCr)

## 1. 문제 설명
어느 운동 종목의 국가대표팀 감독인 당신은 후보 선수 $N$명 중에서 국가대표로 활약할 선수 $K$명을 선발하려고 합니다. 각 선수에게는 $1$번부터 $N$번까지 번호가 매겨져 있습니다.

$N$명의 선수 중 $K$명을 선발할 수 있는 **모든 경우의 수**를 구하고, 각 경우에 선발된 선수의 번호를 오름차순으로 출력하는 프로그램을 작성하세요.

단, 각 경우(조합)는 사전순으로 출력해야 합니다.
예를 들어 $N=4, K=2$인 경우:
1. `1 2`
2. `1 3`
3. `1 4`
4. `2 3`
5. `2 4`
6. `3 4`
총 6가지입니다.

---

## 2. 입출력 설명

* **입력:**
전체 후보 선수의 수 $N$과 선발할 인원 $K$가 공백으로 구분되어 입력됩니다.
($1 \le K \le N \le 15$)

* **출력:**
첫째 줄에 가능한 모든 경우의 수를 출력합니다.
둘째 줄부터 각 줄에 선발된 선수들의 번호를 공백으로 구분하여 사전순으로 출력합니다.

---

## 3. 예시

### 예시 입력 1
```text
4 2
```

### 예시 출력 1
```text
6
1 2
1 3
1 4
2 3
2 4
3 4
```

---

## 4. 힌트
조합을 구할 때는 **"직전에 뽑은 선수보다 번호가 큰 선수만 다음에 뽑는다"**는 규칙을 재귀 함수에 매개변수로 전달하면 중복과 순서 문제를 동시에 해결할 수 있습니다.

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (C)
```c
#include <stdio.h>

int n, k;
int selected[20];
int total_count = 0;

// count_so_far: 현재까지 선발된 인원
// start_num: 다음에 선발할 수 있는 최소 선수 번호
void solve(int count_so_far, int start_num) {
    if (count_so_far == k) {
        for (int i = 0; i < k; i++) {
            printf("%d ", selected[i]);
        }
        printf("\n");
        return;
    }

    for (int i = start_num; i <= n; i++) {
        selected[count_so_far] = i;
        solve(count_so_far + 1, i + 1);
    }
}

// 개수만 먼저 세기 위한 함수 (또는 조합 공식을 사용해도 됨)
int combination_count(int n, int k) {
    if (k == 0 || k == n) return 1;
    return combination_count(n - 1, k - 1) + combination_count(n - 1, k);
}

int main() {
    scanf("%d %d", &n, &k);
    printf("%d\n", combination_count(n, k));
    solve(0, 1);
    return 0;
}
```
<!-- ANSWER_END -->
