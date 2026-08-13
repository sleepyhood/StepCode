#include <stdio.h>
#include <string.h>

struct Student {
    char name[30];
    int grade;
};

int main() {
    int n;
    struct Student arr[105];
    if (scanf("%d", &n) == 1) {
        for (int i = 0; i < n; i++) {
            scanf("%s %d", arr[i].name, &arr[i].grade);
        }
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - 1 - i; j++) {
                if (strcmp(arr[j].name, arr[j + 1].name) > 0) {
                    struct Student temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
        for (int i = 0; i < n; i++) {
            printf("%s %d\n", arr[i].name, arr[i].grade);
        }
    }
    return 0;
}
