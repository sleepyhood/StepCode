#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(void) {
    char url[200];

    if (scanf("%s", url) != 1) return 0;

    char *p_age = strstr(url, "age=");
    char *p_score = strstr(url, "score=");

    if (p_age != NULL && p_score != NULL) {
        int age = atoi(p_age + 4);
        int score = atoi(p_score + 6);

        printf("%d\n", age + score);
        printf("%d\n", age * score);
    }

    return 0;
}
