#include <stdio.h>

int main() {
    int A, B, Op;
    if (scanf("%d %d", &A, &B) == 2 && scanf("%d", &Op) == 1) {
        int *pa = &A;
        int *pb = &B;
        int temp = *pa;
        *pa = *pb;
        *pb = temp;
        if (Op == 1) {
            printf("%d\n", A);
        } else {
            printf("%d\n", B);
        }
    }
    return 0;
}
