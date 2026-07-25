#include <cstdio>
#include <cstring>

int main()
{
    char data1[110] = {0,};
    char data2[110] = {0,};

    if (scanf("%s %s", data1, data2) == 2) {
        if (strcmp(data1, data2) < 0) {
            printf("%s\n", data1);
        } else {
            printf("%s\n", data2);
        }
    }

    return 0;
}
