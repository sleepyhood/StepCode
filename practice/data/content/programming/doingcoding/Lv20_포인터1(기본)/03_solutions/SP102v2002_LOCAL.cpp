#include <stdio.h>

int main() {
    int N;
    if (scanf("%d", &N) != 1) return 0;
    int arr[25];
    for (int i = 0; i < N; i++) {
        scanf("%d", &arr[i]);
    }
    for (int *p = arr + N - 1; p >= arr; p--) {
        printf("%d%c", *p, (p == arr ? '\n' : ' '));
    }
    return 0;
}
