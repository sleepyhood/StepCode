#include <stdio.h>
#include <string.h>

int main(void) {
    char S[100];
    char restored[500] = "";

    if (scanf("%s", S) != 1) return 0;

    int len = (int)strlen(S);
    int pos = 0;

    for (int i = 0; i < len; i += 2) {
        char ch = S[i];
        int cnt = S[i + 1] - '0';
        for (int k = 0; k < cnt; k++) {
            restored[pos++] = ch;
        }
    }
    restored[pos] = '\0';

    printf("%s\n", restored);
    printf("%d\n", (int)strlen(restored));

    return 0;
}
