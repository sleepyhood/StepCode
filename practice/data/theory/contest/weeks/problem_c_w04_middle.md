# C Contest Week 04 Middle Problem Set

## 범위
- Week 04 core source pool mapping
- 분반: 중등
- W04 개념 1~3 적용

## 문제 1
연계 개념: 개념 1) for/while 종료 조건 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>

int main()
{
    int i, a = 0;
    for(i=2 ; i<62 ; i++) {
        if(i % 2 == 0 && i % 3 == 0 && i % 5 == 0) {
            a += i;
        }
    }
    printf("%d\n", a);
    return 0;
}
```

① 15  
② 30  
③ 45  
④ 60  
⑤ 90

## 문제 2
연계 개념: 개념 2) break/continue 영향 범위, 개념 3) 중첩 반복 총 실행 횟수
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>

int main()
{
    int flag = 0;
    for(int i=1 ; i<10 ; i++) {
        for(int j=0 ; j<10 ; j++) {
            for(int k=0 ; k<10 ; k++) {
                if(i == k || j == k) continue;
                if((i * 10 + j) * k == (j * 10 + i)) {
                    printf("%d\n", k);
                    flag = 1;
                    break;
                }
            }
            if(flag == 1) break;
        }
        if(flag == 1) break;
    }
    return 0;
}
```

① 1  
② 3  
③ 5  
④ 7  
⑤ 9

## 문제 3
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

## 문제 4
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

## 문제 5
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

