#include <stdio.h>

int main() {
    const char *str = "HelloPointer";
    int N;
    if (scanf("%d", &N) == 1) {
        printf("%s\n", str + N);
    }
    return 0;
}
