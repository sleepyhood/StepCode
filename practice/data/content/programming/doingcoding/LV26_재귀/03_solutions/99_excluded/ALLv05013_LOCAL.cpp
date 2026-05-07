#include <stdio.h>

void to_octal(int n) {
    // 기저 조건: 8보다 작으면 바로 출력
    if (n < 8) {
        printf("%d", n);
        return;
    }
    // 재귀 호출로 앞자리 먼저 처리
    to_octal(n / 8);
    // 현재 자리(나머지) 출력
    printf("%d", n % 8);
}

int main() {
    int n;
    scanf("%d", &n);
    to_octal(n);
    printf("\n");
    return 0;
}