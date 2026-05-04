#include <stdio.h>
#include <string.h>

char str[105];

void reversePrint(int i) {
    if (str[i] == '\0') return;
    reversePrint(i + 1);
    printf("%c", str[i]);
}

int main() {
    scanf("%s", str);
    reversePrint(0);
    return 0;
}