#include <stdio.h>
#include <string.h>

struct Student {
    char name[30];
    int age;
};

struct Student createStudent(const char* name, int age) {
    struct Student s;
    strcpy(s.name, name);
    s.age = age;
    return s;
}

int main() {
    char name[30];
    int age;
    if (scanf("%s %d", name, &age) == 2) {
        struct Student s = createStudent(name, age);
        printf("이름: %s, 나이: %d\n", s.name, s.age);
    }
    return 0;
}
