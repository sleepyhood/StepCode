#include <stdio.h>
#include <string.h>

int main(void) {
    char S[300];
    char word[50];
    int N;

    if (scanf("%s %d", S, &N) != 2) return 0;

    for (int i = 0; i < N; i++) {
        if (scanf("%s", word) != 1) break;
        int len = (int)strlen(S);
        if (len > 0 && S[len - 1] == word[0]) {
            strcat(S, word);
        } else {
            break;
        }
    }

    printf("%s\n", S);
    printf("%d\n", (int)strlen(S));

    return 0;
}
