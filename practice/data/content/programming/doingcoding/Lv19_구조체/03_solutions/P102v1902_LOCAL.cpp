#include <stdio.h>

struct Student {
    char name[30];
    int age;
};

int main() {
    struct Student s1, s2;
    int new_age;
    if (scanf("%s %d", s1.name, &s1.age) == 2) {
        s2 = s1; // struct value copy
        if (scanf("%d", &new_age) == 1) {
            s1.age = new_age; // modify s1
        }
        printf("이름: %s, 나이: %d\n", s2.name, s2.age);
    }
    return 0;
}
