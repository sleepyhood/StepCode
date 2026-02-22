# C Contest Week 04 High Problem Set

## 범위
- Week 04 core source pool mapping
- 분반: 고등
- W04 개념 1~3 적용

## 문제 1
연계 개념: 개념 1) for/while 종료 조건 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>
int main()
{
    int sum = 0;
    for(int i=1 ; i<=10 ; i++) {
        if(i % 3 == 0) {
            sum += i;
        }
    }
    printf("%d", sum);
    return 0;
}
```

① 14  ② 16  ③ 18  ④ 20  ⑤ 22

## 문제 2
연계 개념: 개념 1) for/while 종료 조건 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>
int main()
{
    int a = 20, b = 30;
    while(a > 0) {
        a -= 6;
        b += 3;
    }
    printf("%d\n", b);
    return 0;
}
```
① 30  ② 36  ③ 42  ④ 48  ⑤ 54  

## 문제 3
연계 개념: 개념 1) for/while 종료 조건 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>
int f(int a, int b) {
    return a - b * 3;
}
int main()
{
    int a = 3;
    for(int i=0 ; i<4 ; i++) {
        a = f(a, -i);
        a = f(a, i);
    }
    printf("%d\n", a);
    return 0;
}
```
① 0  ② 1  ③ 2  ④ 3  ⑤ 4  

## 문제 4
연계 개념: 개념 1) for/while 종료 조건 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>

int main()
{
    int a = 0;
    for(int i=100 ; i<=2024 ; i+=100) {
        a += 2;
    }
    printf("%d\n", a);

    return 0;
}
```

① 36  
② 38  
③ 40  
④ 42  
⑤ 44

## 문제 5
연계 개념: 개념 1) for/while 종료 조건 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>

int main()
{
    int a = 20, b = 30;
    while(a > 0) {
        a -= 6;
        b *= 3;
        b /= 2;
    }
    printf("%d\n", b);
    return 0;
}
```

① 100  
② 101  
③ 150  
④ 151  
⑤ 200  

