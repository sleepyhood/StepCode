# C Contest Week 09 High Problem Set

## 범위
- Week 09 core source pool mapping
- 분반: 고등
- W09 개념 1~3 적용

## 문제 1
연계 개념: 개념 2) 호출 순서(전위/중위/후위), 개념 3) 호출 트리 깊이 추정
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>

int f(int a, int b) {
    return b * 2 - a;
}

int main()
{
    int a = 1;
    for(int i=0 ; i<12 ; i++) {
        a = f(a, -i);
        a = f(a, i);
    }
    printf("%d\n", a);
    return 0;
}
```

① 256  
② 259  
③ 262  
④ 265  
⑤ 268

## 문제 2
연계 개념: 개념 1) 절반 분할 조건, 개념 2) 호출 순서(전위/중위/후위)
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>
void f(int a, int b) {
    if(a == b) {
        printf("%d ", a);
        return;
    }
    int c = a + (b - a) / 4;
    f(a, c);
    f(c+1, b);
}
int main()
{
    f(0, 15);
    return 0;
}
```
① 1  ② 2  ③ 3  ④ 4  ⑤ 5

## 문제 3
연계 개념: 개념 1) 절반 분할 조건, 개념 2) 호출 순서(전위/중위/후위)
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>

void f(int a, int b) {
    if(a == b) {
        printf("%d ", a);
        return;
    }
    int c = (a + b) / 2;
    f(a, c);
    f(c+1, b);
}

int main()
{
    f(0, 15);
    return 0;
}
```

① 1  
② 2  
③ 3  
④ 4  
⑤ 5

## 문제 4
연계 개념: 개념 2) 호출 순서(전위/중위/후위), 개념 3) 호출 트리 깊이 추정
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>

int f(int a, int b) {
    return b * 2 - a;
}

int main()
{
    int a = 1;
    for(int i=0 ; i<12 ; i++) {
        a = f(a, -i);
        a = f(a, i);
    }
    printf("%d\n", a);
    return 0;
}
```

① 256  
② 259  
③ 262  
④ 265  
⑤ 268

## 문제 5
연계 개념: 개념 1) 절반 분할 조건, 개념 2) 호출 순서(전위/중위/후위)
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>
void f(int a, int b) {
    if(a == b) {
        printf("%d ", a);
        return;
    }
    int c = a + (b - a) / 4;
    f(a, c);
    f(c+1, b);
}
int main()
{
    f(0, 15);
    return 0;
}
```
① 1  ② 2  ③ 3  ④ 4  ⑤ 5
