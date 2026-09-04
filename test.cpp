#include <stdio.h>
#include <string.h>

int main(void) {
    char A[100];
    char B[100];
    char temp[100];

    if (scanf("%s %s", A, B) != 2) return 0;

    int cmp = strcmp(A, B);
    if (cmp > 0) {
        strcpy(temp, A);
        strcpy(A, B);
        strcpy(B, temp);
    } else if (cmp == 0) {
        strcat(A, "-EQUAL");
    }

    printf("%s\n", A);
    printf("%s\n", B);

    return 0;
}
