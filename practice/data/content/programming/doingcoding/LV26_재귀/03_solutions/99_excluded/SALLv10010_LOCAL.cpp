#include <stdio.h>

int target_n, target_s;
int count = 0;

void solve(int dice_count, int current_sum) {
    // 모든 주사위를 다 던졌을 때
    if (dice_count == target_n) {
        if (current_sum == target_s) {
            count++;
        }
        return;
    }

    // 가지치기: 현재 합이 이미 목표를 초과했거나, 남은 주사위로 최소/최대 합을 만들어도 범위를 벗어나는 경우
    if (current_sum > target_s) return;
    if (current_sum + (target_n - dice_count) * 6 < target_s) return;

    for (int i = 1; i <= 6; i++) {
        solve(dice_count + 1, current_sum + i);
    }
}

int main() {
    scanf("%d %d", &target_n, &target_s);
    solve(0, 0);
    printf("%d", count);
    return 0;
}