#include <stdio.h>

struct Person {
    char name[30];
    int age;
};

int main() {
    struct Person p1, p2;
    if (scanf("%s %d %s %d", p1.name, &p1.age, p2.name, &p2.age) == 4) {
        if (p1.age <= p2.age) {
            printf("이름: %s, 나이: %d\n", p1.name, p1.age);
            printf("이름: %s, 나이: %d\n", p2.name, p2.age);
        } else {
            printf("이름: %s, 나이: %d\n", p2.name, p2.age);
            printf("이름: %s, 나이: %d\n", p1.name, p1.age);
        }
    }
    return 0;
}
