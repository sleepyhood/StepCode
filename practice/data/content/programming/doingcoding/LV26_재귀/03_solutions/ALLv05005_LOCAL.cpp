#include <stdio.h>

void toBase(int n, int k) {
    if (n == 0) return;
    toBase(n / k, k);
    printf("%d", n % k);
}

int main() {
    int n, k;
    scanf("%d %d", &n, &k);
    if (n == 0) printf("0");
    else toBase(n, k);
    return 0;
}