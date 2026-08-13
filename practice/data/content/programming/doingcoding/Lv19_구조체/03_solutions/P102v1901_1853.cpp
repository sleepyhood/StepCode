#include <stdio.h>

struct Student {
    char name[30];
    int age;
};

int main() {
    struct Student s;
    if (scanf("%s %d", s.name, &s.age) == 2) {
        printf("이름: %s, 나이: %d\n", s.name, s.age);
    }
    return 0;
}
