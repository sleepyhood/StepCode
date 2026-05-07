#include <stdio.h>

int k;
int S[15];
int selected[6];

// count: 현재까지 선택한 숫자의 개수
// start_idx: 집합 S에서 다음에 선택할 수 있는 인덱스
void solve(int count, int start_idx) {
    if (count == 6) {
        for (int i = 0; i < 6; i++) {
            printf("%d%c", selected[i], (i == 5 ? '\n' : ' '));
        }
        return;
    }

    for (int i = start_idx; i < k; i++) {
        selected[count] = S[i];
        solve(count + 1, i + 1);
    }
}

int main() {
    bool first = true;
    while (scanf("%d", &k) == 1 && k != 0) {
        if (!first) printf("\n"); // 테스트 케이스 사이의 빈 줄
        
        for (int i = 0; i < k; i++) {
            scanf("%d", &S[i]);
        }
        
        solve(0, 0);
        first = false;
    }
    return 0;
}
