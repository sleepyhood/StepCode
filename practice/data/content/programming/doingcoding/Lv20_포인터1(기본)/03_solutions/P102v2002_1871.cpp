#include <stdio.h>

int main() {
    int A, B;
    int target, V;
    if (scanf("%d %d", &A, &B) == 2 && scanf("%d %d", &target, &V) == 2) {
        int *p = NULL;
        if (target == 1) {
            p = &A;
        } else {
            p = &B;
        }
        *p = V;
        printf("%d %d\n", A, B);
    }
    return 0;
}
