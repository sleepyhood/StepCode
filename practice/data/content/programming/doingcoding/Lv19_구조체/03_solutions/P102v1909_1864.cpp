#include <stdio.h>
#include <string.h>

struct Student {
    char name[30];
    int age;
};

int main() {
    int n;
    struct Student arr[105];
    char target[30];
    if (scanf("%d", &n) == 1) {
        for (int i = 0; i < n; i++) {
            scanf("%s %d", arr[i].name, &arr[i].age);
        }
        if (scanf("%s", target) == 1) {
            for (int i = 0; i < n; i++) {
                if (strcmp(arr[i].name, target) == 0) {
                    printf("이름: %s, 나이: %d\n", arr[i].name, arr[i].age);
                    break;
                }
            }
        }
    }
    return 0;
}
