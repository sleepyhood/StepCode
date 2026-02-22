# C Contest Week 07 Problem Set

## 주차 주제
- 전처리기 매크로

## 실전 문제 묶음
- 아래 문항은 출처 원문에서 주차 목표에 맞게 선별한 실제 문제이다.

### C_2023_1회
- 문항: 17

#### 문제 17
17. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초중고]
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

---

### C_2024_2회
- 문항: 13

#### 문제 13
13. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]
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

---

### C_2024_3회
- 문항: 13

#### 문제 13
13. 다음 프로그램의 실행 결과는 무엇인가? [초]
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

---
