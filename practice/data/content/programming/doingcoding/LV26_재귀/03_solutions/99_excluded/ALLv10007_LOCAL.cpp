#include <stdio.h>

int N;
int stack[35];

// current_sum: 현재까지 쌓인 정사각형 총합
// depth: 현재 열의 번호 (0부터 시작)
// last_height: 바로 왼쪽 열의 높이 (이보다 크면 안 됨)
void solve(int current_sum, int depth, int last_height) {
    if (current_sum == N) {
        // 모든 정사각형을 사용했으면 출력
        for (int i = 0; i < depth; i++) {
            printf("%d%c", stack[i], (i == depth - 1 ? '\n' : ' '));
        }
        return;
    }

    // 다음 열에 쌓을 수 있는 높이 i: 
    // 1. 최소 1개
    // 2. 최대 last_height (비오름차순 유지)
    // 3. 남은 정사각형 개수(N - current_sum)를 초과할 수 없음
    for (int i = last_height; i >= 1; i--) {
        if (current_sum + i <= N) {
            stack[depth] = i;
            solve(current_sum + i, depth + 1, i);
        }
    }
}

int main() {
    if (scanf("%d", &N) != 1) return 0;

    // 첫 번째 열은 최대 N까지 가능하므로 last_height를 N으로 시작
    solve(0, 0, N);

    return 0;
}
