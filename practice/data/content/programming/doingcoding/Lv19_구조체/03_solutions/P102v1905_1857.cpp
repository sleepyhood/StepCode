#include <stdio.h>

struct Address {
    char city[30];
    char zipcode[15];
};

struct Student {
    char name[30];
    int age;
    struct Address addr;
};

int main() {
    struct Student s;
    if (scanf("%s %d %s %s", s.name, &s.age, s.addr.city, s.addr.zipcode) == 4) {
        printf("이름: %s, 나이: %d, 도시: %s, 우편번호: %s\n", s.name, s.age, s.addr.city, s.addr.zipcode);
    }
    return 0;
}
