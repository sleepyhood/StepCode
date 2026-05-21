// SP101v0611 | [숙제 1] 음료수 자판기
// 입력: 정수 하나 (자판기 번호)
// 출력: 1→콜라, 2→사이다, 3→환타, 그 외→준비중인 음료입니다
// 핵심: default 예외 처리 복습 (14번 식당 키오스크와 동일 구조)
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);

    switch (n) {
        case 1:
            printf("콜라\n");
            break;
        case 2:
            printf("사이다\n");
            break;
        case 3:
            printf("환타\n");
            break;
        default:
            printf("준비중인 음료입니다\n");
            break;
    }

    return 0;
}
