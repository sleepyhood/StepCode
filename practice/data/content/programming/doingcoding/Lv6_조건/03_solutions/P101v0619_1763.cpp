// P101v0619 | 19. [조건-switch case default] 성적표
// 입력: 0~100 사이의 정수 (점수)
// 출력: 90 이상→A, 80~89→B, 70~79→C, 그 외→F
// 핵심: 점수/10 몫으로 분기
//   100점: 100/10 = 10 → case 10과 case 9를 함께 묶어 A 처리
//   90~99점: 몫 9 → A
//   80~89점: 몫 8 → B
//   70~79점: 몫 7 → C
//   0~69점: 몫 0~6 → F (default)
#include <stdio.h>

int main(void) {
    int score;
    scanf("%d", &score);

    switch (score / 10) {
        case 10:  // 100점 예외 처리: 100/10=10
        case 9:
            printf("A\n");
            break;
        case 8:
            printf("B\n");
            break;
        case 7:
            printf("C\n");
            break;
        default:
            printf("F\n");
            break;
    }

    return 0;
}
