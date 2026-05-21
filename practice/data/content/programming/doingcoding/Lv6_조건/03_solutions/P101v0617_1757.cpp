// P101v0617 | 17. [조건-switch case] 달력 문제
// 입력: 월을 나타내는 정수 (1~12)
// 출력: 해당 월의 날짜 수, 1~12 외의 입력은 "잘못된 입력"
// 월별 날짜:
//   31일: 1, 3, 5, 7, 8, 10, 12월
//   28일: 2월 (윤년 무시)
//   30일: 4, 6, 9, 11월
// 핵심: 대규모 case 그룹핑 + default
#include <stdio.h>

int main(void) {
    int m;
    scanf("%d", &m);

    switch (m) {
        case 1:
        case 3:
        case 5:
        case 7:
        case 8:
        case 10:
        case 12:
            printf("31일\n");
            break;
        case 4:
        case 6:
        case 9:
        case 11:
            printf("30일\n");
            break;
        case 2:
            printf("28일\n");
            break;
        default:
            printf("잘못된 입력\n");
            break;
    }

    return 0;
}
