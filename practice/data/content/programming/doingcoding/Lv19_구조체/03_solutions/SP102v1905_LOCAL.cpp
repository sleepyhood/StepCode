#include <stdio.h>

struct Student {
    char name[30];
    int score;
};

int main() {
    int n;
    struct Student arr[105];
    if (scanf("%d", &n) == 1) {
        for (int i = 0; i < n; i++) {
            scanf("%s %d", arr[i].name, &arr[i].score);
        }
        int max_idx = 0;
        for (int i = 1; i < n; i++) {
            if (arr[i].score > arr[max_idx].score) {
                max_idx = i;
            }
        }
        printf("이름: %s, 점수: %d\n", arr[max_idx].name, arr[max_idx].score);
    }
    return 0;
}
