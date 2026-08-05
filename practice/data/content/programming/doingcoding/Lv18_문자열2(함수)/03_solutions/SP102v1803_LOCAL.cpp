#include <stdio.h>
#include <string.h>

int main(void) {
    int N;
    char title[100];
    char temp[200];
    char report[2000] = "";
    int spam_cnt = 0;

    if (scanf("%d", &N) != 1) return 0;
    while (getchar() != '\n'); // consume newline after N

    for (int i = 0; i < N; i++) {
        if (fgets(title, sizeof(title), stdin) == NULL) break;
        int len = (int)strlen(title);
        if (len > 0 && title[len - 1] == '\n') {
            title[len - 1] = '\0';
        }

        if (strstr(title, "AD") != NULL || strstr(title, "LOAN") != NULL) {
            spam_cnt++;
            sprintf(temp, "[SPAM #%d] %s\n", spam_cnt, title);
            strcat(report, temp);
        }
    }

    if (spam_cnt == 0) {
        strcpy(report, "CLEAN");
        printf("%s\n", report);
    } else {
        printf("%s", report);
    }

    printf("%d\n", (int)strlen(report));

    return 0;
}
