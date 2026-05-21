// P101v0618 | 18. [조건-switch case default] 계산기 만들기
// 입력: 정수1 연산자 정수2 (공백으로 구분, 한 줄)
// 출력:
//   올바른 연산 → 결과 정수 출력
//   0으로 나눌 경우 → "잘못된 연산입니다"
//   정의되지 않은 연산자 → "잘못된 연산자입니다"
// 핵심: char 연산자 switch + case 내부 if 중첩
#include <stdio.h>

int main(void) {
    int a, b;
    char op;
    scanf("%d %c %d", &a, &op, &b);

    switch (op) {
        case '+':
            printf("%d\n", a + b);
            break;
        case '-':
            printf("%d\n", a - b);
            break;
        case '*':
            printf("%d\n", a * b);
            break;
        case '/':
            if (b == 0) {
                printf("잘못된 연산입니다\n");
            } else {
                printf("%d\n", a / b);
            }
            break;
        default:
            printf("잘못된 연산자입니다\n");
            break;
    }

    return 0;
}
