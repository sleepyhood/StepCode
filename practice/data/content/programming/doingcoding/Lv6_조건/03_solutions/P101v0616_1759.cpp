// P101v0616 | 16. [조건-switch char] 알파벳 신호등
// 입력: 알파벳 문자 하나 (R/r, G/g, Y/y 또는 그 외)
// 출력: R/r→정지, G/g→진행, Y/y→주의, 그 외→잘못된 신호
// 핵심: char 타입 switch + 대소문자 case 묶기
#include <stdio.h>

int main(void) {
    char c;
    scanf(" %c", &c);  // 앞 공백으로 개행 문자 스킵

    switch (c) {
        case 'R':
        case 'r':
            printf("정지\n");
            break;
        case 'G':
        case 'g':
            printf("진행\n");
            break;
        case 'Y':
        case 'y':
            printf("주의\n");
            break;
        default:
            printf("잘못된 신호\n");
            break;
    }

    return 0;
}
