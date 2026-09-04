#include <stdio.h>

int main() {
    int num, K;
    if (scanf("%d %d", &num, &K) == 2) {
        int *p = &num;
        *p += K;
        printf("num의 값: %d\n", num);
        printf("포인터 p가 가리키는 값: %d\n", *p);
    }
    return 0;
}
