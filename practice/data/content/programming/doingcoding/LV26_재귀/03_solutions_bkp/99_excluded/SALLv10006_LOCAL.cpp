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