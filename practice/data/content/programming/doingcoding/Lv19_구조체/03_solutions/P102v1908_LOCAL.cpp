#include <stdio.h>

struct Student {
    char name[30];
    int score;
};

int main() {
    int n, k, x, m;
    struct Student arr[105];
    if (scanf("%d", &n) == 1) {
        for (int i = 0; i < n; i++) {
            scanf("%s %d", arr[i].name, &arr[i].score);
        }
        if (scanf("%d %d", &k, &x) == 2) {
            if (k >= 0 && k < n) {
                arr[k].score += x; // in-place update
            }
        }
        if (scanf("%d", &m) == 1) {
            if (m >= 0 && m < n) {
                printf("이름: %s, 점수: %d\n", arr[m].name, arr[m].score);
            }
        }
    }
    return 0;
}
