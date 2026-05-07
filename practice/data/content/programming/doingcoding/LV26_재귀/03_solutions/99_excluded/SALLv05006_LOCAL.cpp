#include <stdio.h>

long long f(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    return 2 * f(n - 1) + f(n - 2);
}

int main() {
    int n;
    scanf("%d", &n);
    printf("%lld", f(n));
    return 0;
}