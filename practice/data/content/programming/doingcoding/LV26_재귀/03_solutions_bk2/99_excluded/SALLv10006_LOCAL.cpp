#include <stdio.h>

int cnt = 0; // 전역 변수

int fibo(int n) {
    cnt++; // 호출될 때마다 1 증가
    if (n <= 1) return n;
    return fibo(n - 1) + fibo(n - 2);
}

int main() {
    int n;
    scanf("%d", &n);
    int result = fibo(n);
    printf("%d\n%d", result, cnt);
    return 0;
}