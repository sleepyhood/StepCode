#include <stdio.h>

void print_bar(int depth) {
    for (int i = 0; i < depth; i++) printf("____");
}

void open_doll(int depth, int n) {
    // 재귀 호출 전: 인형을 열기
    print_bar(depth);
    printf("인형을 열었다.\n");

    if (depth == n - 1) {
        // 기저 조건: 마지막 인형 안의 사탕 발견
        print_bar(depth + 1);
        printf("사탕을 발견했다!\n");
    } else {
        // 재귀 호출 (한 단계 더 깊이)
        open_doll(depth + 1, n);
    }

    // 재귀 호출 후: 인형을 닫기
    print_bar(depth);
    printf("인형을 닫았다.\n");
}

int main() {
    int n;
    scanf("%d", &n);
    open_doll(0, n);
    return 0;
}