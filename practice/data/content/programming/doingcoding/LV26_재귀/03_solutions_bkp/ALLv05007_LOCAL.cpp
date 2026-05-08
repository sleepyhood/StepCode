#include <stdio.h>

int target_n;

// k: 현재까지 결정된 자릿수
// val: 현재까지 만들어진 숫자의 값
void solve(int k, int val) {
    // 목표 자릿수에 도달하면 출력하고 종료
    if (k == target_n) {
        printf("%d\n", val);
        return;
    }

    // 1을 붙이는 경우와 2를 붙이는 경우를 각각 호출
    solve(k + 1, val * 10 + 1);
    solve(k + 1, val * 10 + 2);
}

int main() {
    scanf("%d", &target_n);
    
    // 처음에 아무 숫자도 없는 상태(val=0)에서 시작
    solve(0, 0);
    
    return 0;
}