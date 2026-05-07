#include <stdio.h>

void printStars(int count) {
    if (count <= 0) return;
    printf("*");
    printStars(count - 1);
}

void solve(int n) {
    if (n <= 0) return;
    printStars(n); // 현재 줄 출력
    printf("\n");
    solve(n - 1);  // 다음 줄(개수 감소) 호출
}

int main() {
    int n;
    scanf("%d", &n);
    solve(n);
    return 0;
}