// P101v0613 | 13. [조건-switch break] switch case break 배우기
// 입력: 1~3 사이의 정수
// 출력: fall-through 현상 관찰 (break 없음)
//   입력 1 → "1입니다\n2입니다\n3입니다"
//   입력 2 → "2입니다\n3입니다"
//   입력 3 → "3입니다"
// 핵심: 모든 case에 break 없음 → 아래 case가 연쇄 실행됨
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);

    switch (n) {
        case 1:
            printf("1입니다\n");
        case 2:
            printf("2입니다\n");
        case 3:
            printf("3입니다\n");
    }

    return 0;
}
