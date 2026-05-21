// P101v0612 | 12. [조건-switch case] switch case 배우기
// 입력: 1, 2, 3 중 하나의 정수
// 출력: 하나, 둘, 셋
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);

    switch (n) {
        case 1:
            printf("하나\n");
            break;
        case 2:
            printf("둘\n");
            break;
        case 3:
            printf("셋\n");
            break;
    }

    return 0;
}
