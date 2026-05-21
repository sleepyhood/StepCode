// SP101v0612 | [숙제 2] 계절 구분기
// 입력: 월을 나타내는 정수 (1~12)
// 출력: 3~5월→봄, 6~8월→여름, 9~11월→가을, 12/1/2월→겨울, 그 외→잘못된 입력
// 핵심: 정수형 case 묶기 복습 (15번 평일/주말과 동일 구조)
// 주의: case 순서는 1, 2, 3~5, 6~8, 9~11, 12 순으로 작성하되
//       12, 1, 2를 겨울로 묶어야 하므로 case 12를 가장 먼저 배치하고
//       fall-through로 case 1, 2까지 연결하거나, 개별 case로 나열
#include <stdio.h>

int main(void) {
    int m;
    scanf("%d", &m);

    switch (m) {
        case 3:
        case 4:
        case 5:
            printf("봄\n");
            break;
        case 6:
        case 7:
        case 8:
            printf("여름\n");
            break;
        case 9:
        case 10:
        case 11:
            printf("가을\n");
            break;
        case 12:
        case 1:
        case 2:
            printf("겨울\n");
            break;
        default:
            printf("잘못된 입력\n");
            break;
    }

    return 0;
}
