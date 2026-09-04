#include <stdio.h>
#include <string.h>

int main(void) {
    char A[50], B[50], C[50], temp[50];
    char result[200] = "";

    if (scanf("%s %s %s", A, B, C) != 3) return 0;

    // 1. 3단어 사전순 정렬 (A <= B <= C)
    if (strcmp(A, B) > 0) {
        strcpy(temp, A);
        strcpy(A, B);
        strcpy(B, temp);
    }
    if (strcmp(B, C) > 0) {
        strcpy(temp, B);
        strcpy(B, C);
        strcpy(C, temp);
    }
    if (strcmp(A, B) > 0) {
        strcpy(temp, A);
        strcpy(A, B);
        strcpy(B, temp);
    }

    // 2. 색인 체인 결합
    strcpy(result, A);
    strcat(result, "-");
    strcat(result, B);
    strcat(result, "-");
    strcat(result, C);

    // 3. 3단어 모두 일치 시 태그 결합
    if (strcmp(A, B) == 0 && strcmp(B, C) == 0) {
        strcat(result, "(ALL_SAME)");
    }

    printf("%s\n", result);
    printf("%d\n", (int)strlen(result));

    return 0;
}
