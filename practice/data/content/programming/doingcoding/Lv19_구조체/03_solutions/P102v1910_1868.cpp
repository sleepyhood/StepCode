#include <stdio.h>

struct Book {
    char title[50];
    int count;
};

int main() {
    int n;
    struct Book arr[105];
    if (scanf("%d", &n) == 1) {
        for (int i = 0; i < n; i++) {
            scanf("%s %d", arr[i].title, &arr[i].count);
        }
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - 1 - i; j++) {
                if (arr[j].count > arr[j + 1].count) {
                    struct Book temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
        for (int i = 0; i < n; i++) {
            printf("%s %d\n", arr[i].title, arr[i].count);
        }
    }
    return 0;
}
