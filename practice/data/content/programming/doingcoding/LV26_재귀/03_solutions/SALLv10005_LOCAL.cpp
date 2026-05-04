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