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