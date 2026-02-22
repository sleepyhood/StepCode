# C Contest Week 10 Problem Set

## 주차 주제
- 동적 메모리/포인터/구조체

## 실전 문제 묶음
- 아래 문항은 주차 목표에 맞게 선별한 실제 문제이다.

### C_2024_2회
- 문항: 11

#### 문제 11
11. stdlib.h 헤더 파일에 정의 되어 있는 함수 중 동적 메모리 할당을 하며 배열을 0으로 초기화 하는 함수를 고르시오. [초, 중, 고]
① atoi  
② calloc  
③ free  
④ malloc  
⑤ realloc

---

### C_2023_1회
- 문항: 23, 24

#### 문제 23
23. 아래 프로그램에 <입력 1>과 <입력 2>를 입력했을 때 출력되는 문자열을 한 줄에 공백으로 구분하여 작성하시오.
예를 들어 <입력 1>의 출력 결과가 ABC, <입력2>의 출력 결과가 DEF라면, "ABC DEF" 를 답안에 작성하시오. [초중고] 

<입력 1>
```text
7
D B C A C D P
```

<입력 2>
```text
11
P R O G R A M M I N G
```

```c
#include<stdio.h>
typedef struct datastructure {
    int front;
    int rear;
    char q[101];
} DS;
int n;
char v;
DS d;

void f(char k) {
    d.front = d.rear = 50;
    d.q[50] = k;
}
void g(char k) {
    d.q[--(d.front)] = k;
}
void h(char k) {
    d.q[++(d.rear)] = k;
}
int main()
{
    scanf("%d", &n);
    scanf(" %c", &v);
    f(v);

    for(int i=0; i<n-1; i++) {
        scanf(" %c", &v);
        if(v <= d.q[d.front]) g(v);
        else                  h(v);
    }
    for(int i=d.front; i<=d.rear; i++) {
        printf("%c", d.q[i]);
    }
    return 0;
}
```

---

#### 문제 24
24. 아래 프로그램에 <입력>을 입력했을 때 출력되는 값을 작성하시오 [초중고]
<입력>
```text
8
4 6
8 1
4 1
2 3
4 7
5 6
1 3
```

```c
#include<stdio.h>
int n;
int *link[10];
int size[10], check[10], ans;

void search(int c, int p) {
    int count = 0;
    check[c] = 1;
    for(int i=0; i<size[c]; i++) {
        if(!check[ link[c][i] ]) {
            search(link[c][i], p+1);
            count++;
        }
    }
    if(count == 0) ans += p;
}

int main()
{
    scanf("%d", &n);

    for(int i=1; i<=n; i++) {
        link[i] = (int*)malloc(sizeof(int));
        link[i][0] = 0;
    }

    int p, q;
    for(int i=0; i<n-1; i++) {
        scanf("%d %d", &p, &q);

        link[p] = realloc(link[p], sizeof(int)*(size[p] + 1));
        link[p][size[p]] = q;
        size[p]++;

        link[q] = realloc(link[q], sizeof(int)*(size[q] + 1));
        link[q][size[q]] = p;
        size[q]++;
    }

    search(1, 0);
    printf("%d", ans);
    return 0;
}
```

---
