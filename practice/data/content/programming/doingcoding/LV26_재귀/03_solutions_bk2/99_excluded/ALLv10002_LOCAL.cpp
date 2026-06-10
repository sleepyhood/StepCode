#include <stdio.h>

void print_tree(int depth) {
    // 기저 조건: 깊이가 0이면 출력할 것이 없음
    if (depth == 0) return;

    print_tree(depth - 1);          // [전] 왼쪽 서브트리 출력
    printf("%c", 'A' + depth - 1); // [중] 현재 깊이의 알파벳 출력
    print_tree(depth - 1);          // [후] 오른쪽 서브트리 출력 (왼쪽과 동일)
}

int main() {
    int n;
    scanf("%d", &n);
    print_tree(n);
    printf("\n");
    return 0;
}