# C Contest Week 07 Elementary Problem Set

## 범위
- Week 07 core source pool mapping
- 분반: 초등
- W07 개념 1~3 적용

## 문제 1
연계 개념: 개념 1) `#define` 치환 규칙, 개념 2) 매크로 괄호와 부작용
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include<stdio.h>
#define S(X) X*X
int main()
{
    int q = 4;
    printf("%d %d %d", S(q), S(q+1), S(q+q));
    return 0;
}
``` 
⓵ 16 25 64  
⓶ 16 16 16  
⓷ 16 9 24  
⓸ 16 25 24  
⓹ 오류가 발생한다

## 문제 2
연계 개념: 개념 1) `#define` 치환 규칙, 개념 2) 매크로 괄호와 부작용
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>
#define f(x) x*x

int main()
{
    int a = 4;
    printf("%d %d\n", f(a), f(a+1));
    return 0;
}
```

① 16 8  
② 16 9  
③ 16 25  
④ 25 25  
⑤ 25 36

## 문제 3
연계 개념: 개념 1) `#define` 치환 규칙, 개념 2) 매크로 괄호와 부작용
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>
#define f(x) x+1
int main()
{
    int a = 5;
    printf("%d %d\n", f(a), f(a)*f(a));
    return 0;
}
```
① 5 10  ② 6 10  ③ 6 11  ④ 6 25  ⑤ 51 5151

## 문제 4
연계 개념: 개념 1) `#define` 치환 규칙, 개념 2) 매크로 괄호와 부작용
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include<stdio.h>
#define S(X) X*X
int main()
{
    int q = 4;
    printf("%d %d %d", S(q), S(q+1), S(q+q));
    return 0;
}
``` 
⓵ 16 25 64  
⓶ 16 16 16  
⓷ 16 9 24  
⓸ 16 25 24  
⓹ 오류가 발생한다

## 문제 5
연계 개념: 개념 1) `#define` 치환 규칙, 개념 2) 매크로 괄호와 부작용
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>
#define f(x) x*x

int main()
{
    int a = 4;
    printf("%d %d\n", f(a), f(a+1));
    return 0;
}
```

① 16 8  
② 16 9  
③ 16 25  
④ 25 25  
⑤ 25 36
