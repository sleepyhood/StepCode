#include <stdio.h>

int main() {
    int arr[5];
    for (int i = 0; i < 5; i++) {
        if (scanf("%d", &arr[i]) != 1) return 0;
    }
    int K;
    if (scanf("%d", &K) != 1) return 0;
    for (int *p = arr; p < arr + 5; p++) {
        if (*p % 2 == 0) {
            *p *= K;
        }
    }
    for (int i = 0; i < 5; i++) {
        printf("%d\n", arr[i]);
    }
    return 0;
}
