#include <stdio.h>

struct Item {
    char name[30];
    int price;
};

int main() {
    struct Item i1, i2;
    if (scanf("%s %d %s %d", i1.name, &i1.price, i2.name, &i2.price) == 4) {
        int avg = (i1.price + i2.price) / 2;
        printf("%d\n", avg);
    }
    return 0;
}
