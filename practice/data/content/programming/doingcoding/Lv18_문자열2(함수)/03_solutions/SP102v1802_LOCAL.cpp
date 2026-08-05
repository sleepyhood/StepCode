#include <stdio.h>
#include <string.h>

int main(void) {
    int N;
    char min_word[50], max_word[50], word[50];

    if (scanf("%d", &N) != 1 || N <= 0) return 0;

    if (scanf("%s", word) != 1) return 0;
    strcpy(min_word, word);
    strcpy(max_word, word);

    for (int i = 1; i < N; i++) {
        if (scanf("%s", word) != 1) break;
        if (strcmp(word, min_word) < 0) {
            strcpy(min_word, word);
        }
        if (strcmp(word, max_word) > 0) {
            strcpy(max_word, word);
        }
    }

    printf("%s\n", min_word);
    printf("%s\n", max_word);

    return 0;
}
