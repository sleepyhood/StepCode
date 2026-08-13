#include <stdio.h>

struct Book {
    char title[50];
    int pages;
};

struct Book getThickerBook(struct Book b1, struct Book b2) {
    if (b1.pages >= b2.pages) {
        return b1;
    }
    return b2;
}

int main() {
    struct Book b1, b2;
    if (scanf("%s %d %s %d", b1.title, &b1.pages, b2.title, &b2.pages) == 4) {
        struct Book thicker = getThickerBook(b1, b2);
        printf("%s\n", thicker.title);
    }
    return 0;
}
