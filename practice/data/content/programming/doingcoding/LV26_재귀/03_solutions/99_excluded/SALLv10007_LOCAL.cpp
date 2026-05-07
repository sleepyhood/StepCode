#include <stdio.h>

// tiling(n): 가로 길이가 n인 벽을 채우는 방법의 수
long long tiling(int n) {
    if (n == 1) return 1;
    if (n == 2) return 2;
    return tiling(n - 1) + tiling(n - 2);
}

int main() {
    int n;
    scanf("%d", &n);
    // n=30일 경우 재귀 호출 횟수가 많아질 수 있으나, 1초 내에 연산 가능합니다.
    // (더 큰 N에 대해서는 메모이제이션 또는 DP가 필요합니다.)
    printf("%lld", tiling(n));
    return 0;
}