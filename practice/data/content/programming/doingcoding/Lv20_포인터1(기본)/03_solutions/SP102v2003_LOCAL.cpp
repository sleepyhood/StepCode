#include <stdio.h>

int main() {
    int N;
    if (scanf("%d", &N) != 1) return 0;
    int arr[25];
    for (int i = 0; i < N; i++) {
        scanf("%d", &arr[i]);
    }
    int X, K;
    if (scanf("%d %d", &X, &K) != 2) return 0;
    int *max_ptr = arr;
    for (int *p = arr + 1; p < arr + N; p++) {
        if (*p > *max_ptr) {
            max_ptr = p;
        }
    }
    *max_ptr += X;
    printf("%d\n", arr[K]);
    return 0;
}
