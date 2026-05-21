// SP101v0614 | [숙제 4] 도형 넓이 계산기
// 입력: 도형 문자(T/t=삼각형, R/r=사각형), 가로, 세로 (공백으로 구분)
// 출력:
//   T/t: (가로 × 세로) / 2  (정수 출력, 소수점 버림)
//   R/r: 가로 × 세로
//   가로 또는 세로가 0 이하: "잘못된 길이입니다"
//   그 외 문자: "잘못된 도형"
// 핵심: char switch + 내부 if 중첩 (18번 계산기와 동일 패턴)
// 논리 흐름:
//   1) switch로 도형 문자를 먼저 판별
//   2) 유효한 도형 안에서 if로 길이의 0 이하 여부를 검사
//   3) 도형이 틀린 경우는 default → "잘못된 도형"
//      (길이가 동시에 잘못됐더라도 도형 판별이 먼저임)
// 검증:
//   T 4 5  → (4*5)/2 = 10 ✓
//   r 3 6  → 3*6 = 18 ✓
//   T 0 5  → 0 이하 → 잘못된 길이입니다 ✓
//   Q 4 5  → default → 잘못된 도형 ✓
//   Q 0 5  → default → 잘못된 도형 (도형이 먼저 처리됨) ✓
#include <stdio.h>

int main(void) {
    char shape;
    int w, h;
    scanf(" %c %d %d", &shape, &w, &h);

    switch (shape) {
        case 'T':
        case 't':
            if (w <= 0 || h <= 0) {
                printf("잘못된 길이입니다\n");
            } else {
                printf("%d\n", (w * h) / 2);
            }
            break;
        case 'R':
        case 'r':
            if (w <= 0 || h <= 0) {
                printf("잘못된 길이입니다\n");
            } else {
                printf("%d\n", w * h);
            }
            break;
        default:
            printf("잘못된 도형\n");
            break;
    }

    return 0;
}
