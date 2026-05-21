// P101v0614 | 14. [조건-switch default] 식당 키오스크
// 입력: 정수 하나 (메뉴 번호)
// 출력: 1→비빔밥, 2→불고기, 3→냉면, 그 외→준비중인 메뉴입니다
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);

    switch (n) {
        case 1:
            printf("비빔밥\n");
            break;
        case 2:
            printf("불고기\n");
            break;
        case 3:
            printf("냉면\n");
            break;
        default:
            printf("준비중인 메뉴입니다\n");
            break;
    }

    return 0;
}
