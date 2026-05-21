// SP101v0613 | [숙제 3] 등급 판정기
// 입력: 알파벳 문자 하나 (A/a, B/b, C/c 또는 그 외)
// 출력: A/a→우수, B/b→보통, C/c→노력요함, 그 외→잘못된 학점
// 핵심: char 타입 switch + 대소문자 묶기 복습 (16번 알파벳 신호등과 동일 구조)
#include <stdio.h>

int main(void) {
    char c;
    scanf(" %c", &c);  // 앞 공백으로 개행 문자 스킵

    switch (c) {
        case 'A':
        case 'a':
            printf("우수\n");
            break;
        case 'B':
        case 'b':
            printf("보통\n");
            break;
        case 'C':
        case 'c':
            printf("노력요함\n");
            break;
        default:
            printf("잘못된 학점\n");
            break;
    }

    return 0;
}
