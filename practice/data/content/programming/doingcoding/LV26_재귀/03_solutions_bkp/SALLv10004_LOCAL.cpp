#include <stdio.h>

#define MAX_N 8

int grid[MAX_N][MAX_N];
int num = 1; // 다음에 기록할 번호

// (rs, cs): 현재 영역의 시작 행/열, size: 현재 영역의 크기
void assign(int rs, int cs, int size) {
    // 기저 조건: 1×1 칸이면 현재 번호를 기록하고 종료
    if (size == 1) {
        grid[rs][cs] = num++;
        return;
    }

    int half = size / 2;

    assign(rs,          cs,           half); // 좌상
    assign(rs,          cs + half,    half); // 우상
    assign(rs + half,   cs,           half); // 좌하
    assign(rs + half,   cs + half,    half); // 우하
}

int main() {
    int k;
    scanf("%d", &k);

    int N = 1 << k; // N = 2^k

    assign(0, 0, N);

    // 출력
    for (int r = 0; r < N; r++) {
        for (int c = 0; c < N; c++) {
            if (c > 0) printf(" ");
            printf("%d", grid[r][c]);
        }
        printf("\n");
    }

    return 0;
}