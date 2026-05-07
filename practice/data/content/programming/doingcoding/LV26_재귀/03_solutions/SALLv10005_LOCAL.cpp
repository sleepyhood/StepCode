#include <stdio.h>

int n, m;
int maze[15][15];

int solve(int r, int c) {
    // 범위를 벗어나거나 장애물을 만난 경우
    if (r >= n || c >= m || maze[r][c] == 1) return 0;
    
    // 도착점에 도달한 경우
    if (r == n - 1 && c == m - 1) return 1;

    // 오른쪽으로 가는 경우 + 아래쪽으로 가는 경우
    return solve(r, c + 1) + solve(r + 1, c);
}

int main() {
    scanf("%d %d", &n, &m);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            scanf("%1d", &maze[i][j]);
        }
    }
    printf("%d", solve(0, 0));
    return 0;
}