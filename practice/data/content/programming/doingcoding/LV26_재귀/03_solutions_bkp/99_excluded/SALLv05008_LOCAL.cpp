#include <stdio.h>

long long f(int n) {
    if (n <= 0) return 1;
    if (n % 3 == 0) return n + f(n - 1);
    else return n * f(n - 2);
}

int main() {
    int n;
    scanf("%d", &n);
    printf("%lld", f(n));
    return 0;
}