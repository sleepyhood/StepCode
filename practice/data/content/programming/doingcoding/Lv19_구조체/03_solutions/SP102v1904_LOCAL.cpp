#include <stdio.h>

struct Student {
    char name[30];
    int age;
};

int main() {
    int n, cut;
    struct Student arr[105];
    if (scanf("%d", &n) == 1) {
        for (int i = 0; i < n; i++) {
            scanf("%s %d", arr[i].name, &arr[i].age);
        }
        if (scanf("%d", &cut) == 1) {
            for (int i = 0; i < n; i++) {
                if (arr[i].age >= cut) {
                    printf("이름: %s, 나이: %d\n", arr[i].name, arr[i].age);
                }
            }
        }
    }
    return 0;
}
