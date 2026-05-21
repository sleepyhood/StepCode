// P101v0615 | 15. [조건-switch break] 평일/주말 구분기
// 입력: 정수 하나 (요일 번호)
// 출력: 1~5→평일, 6~7→주말, 그 외→잘못된 입력
// 핵심: case 묶기(fall-through 활용) + default
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);

    switch (n) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
            printf("평일\n");
            break;
        case 6:
        case 7:
            printf("주말\n");
            break;
        default:
            printf("잘못된 입력\n");
            break;
    }

    return 0;
}
