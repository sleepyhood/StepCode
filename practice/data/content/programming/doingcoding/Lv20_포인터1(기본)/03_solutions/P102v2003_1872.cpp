#include <stdio.h>

int main() {
    int arr[3];
    if (scanf("%d %d %d", &arr[0], &arr[1], &arr[2]) == 3) {
        int *p = arr;
        for (int i = 0; i < 3; i++) {
            printf("arr[%d] = %d\n", i, *(p + i));
        }
    }
    return 0;
}
