#include <stdio.h>
#include <string.h>

int main(void) {
    char S[100];
    char word[50];
    int N;

    if (scanf("%s %d", S, &N) != 2) return 0;

    for (int i = 0; i < N; i++) {
        if (scanf("%s", word) != 1) break;

        int lenS = (int)strlen(S);
        int lenW = (int)strlen(word);

        if (lenS >= lenW) {
            strcat(S, word);
        } else {
            strncat(S, word, 3);
        }

        if (strlen(S) > 20) {
            S[20] = '\0';
        }
    }

    printf("%s\n", S);
    printf("%d\n", (int)strlen(S));

    return 0;
}
