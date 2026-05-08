#include <stdio.h>

#define MAX_N 16

char grid[MAX_N][MAX_N + 1]; // +1 for null terminator
int N;

// (rs, cs): 현재 영역의 시작 행/열, size: 현재 영역의 크기
void draw(int rs, int cs, int size) {
    // 기저 조건: 1×1 영역은 더 이상 선을 그을 수 없음
    if (size == 1) return;

    int mid_r = rs + size / 2;
    int mid_c = cs + size / 2;

    // 중앙 행 전체를 '+' 로 채우기
    for (int c = cs; c < cs + size; c++) {
        grid[mid_r][c] = '+';
    }
    // 중앙 열 전체를 '+' 로 채우기
    for (int r = rs; r < rs + size; r++) {
        grid[r][mid_c] = '+';
    }

    int sub = size / 2; // 서브 영역 크기 (N=3이면 sub=1, N=7이면 sub=3)

    // 4개 서브 영역에 재귀 호출
    draw(rs,           cs,           sub); // 좌상
    draw(rs,           mid_c + 1,   sub); // 우상
    draw(mid_r + 1,   cs,           sub); // 좌하
    draw(mid_r + 1,   mid_c + 1,   sub); // 우하
}

int main() {
    int k;
    scanf("%d", &k);

    // N = 2^k - 1
    N = (1 << k) - 1;

    // 격자 초기화 ('.' 로 채우기)
    for (int r = 0; r < N; r++) {
        for (int c = 0; c < N; c++) {
            grid[r][c] = '.';
        }
        grid[r][N] = '\0'; // 문자열 종료
    }

    draw(0, 0, N);

    // 출력
    for (int r = 0; r < N; r++) {
        printf("%s\n", grid[r]);
    }

    return 0;
}