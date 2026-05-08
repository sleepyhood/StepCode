#include <stdio.h>

int cut(int n, int m) {
    // 정사각형이 되면 1개로 종료
    if (n == m) return 1;

    int big = (n > m) ? n : m;
    int small = (n < m) ? n : m;

    // 이번 단계에서 잘라낼 수 있는 정사각형 수 + 나머지 직사각형 처리
    if (big % small == 0) return (big / small);
    return (big / small) + cut(small, big % small);
}

int main() {
    int n, m;
    scanf("%d %d", &n, &m);
    printf("%d", cut(n, m));
    return 0;
}