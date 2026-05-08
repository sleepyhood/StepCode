#include <stdio.h>

int is_first = 1; // 첫 번째 숫자 앞에는 공백을 붙이지 않기 위한 플래그

void ruler(int depth) {
    if (depth == 0) return;

    ruler(depth - 1);

    // 첫 번째 출력이면 공백 없이, 이후엔 공백으로 구분
    if (is_first) {
        printf("%d", depth);
        is_first = 0;
    } else {
        printf(" %d", depth);
    }

    ruler(depth - 1);
}

int main() {
    int n;
    scanf("%d", &n);
    ruler(n);
    printf("\n");
    return 0;
}