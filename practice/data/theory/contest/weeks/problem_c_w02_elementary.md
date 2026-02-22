# C Contest Week 02 Elementary Problem Set

## 범위
- Week 02 core source pool mapping
- 분반: 초등
- W02 개념 1~3 적용

## 문제 1
연계 개념: 개념 2) 진법 표기(`0`, `0x`)
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include<stdio.h>
int main()
{
    int a = 0x32;
    int b = 030;
    printf("%d", a+b);
    return 0;
}
```

⓵ 44  
⓶ 56  
⓷ 62  
⓸ 74  
⓹ 80

## 문제 2
연계 개념: 개념 1) `printf` 폭(width)과 정렬
다음 중 `3.14` 출력 서식으로 적절하지 않은 것을 고르시오.

⓵ printf("%lf", 3.14);  
⓶ printf("%7.6lf", 3.14);  
⓷ printf("%-8.6lf", 3.14);  
⓸ printf("%6.4lf00", 3.14);  
⓹ printf("%-10.3lf000", 3.14);

## 문제 3
연계 개념: 개념 2) 진법 표기(`0`, `0x`)
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include<stdio.h>
int main()
{
    int a = 0x32;
    int b = 030;
    printf("%d", a+b);
    return 0;
}
```

⓵ 44  
⓶ 56  
⓷ 62  
⓸ 74  
⓹ 80

## 문제 4
연계 개념: 개념 1) `printf` 폭(width)과 정렬
다음 중 `3.14` 출력 서식으로 적절하지 않은 것을 고르시오.

⓵ printf("%lf", 3.14);  
⓶ printf("%7.6lf", 3.14);  
⓷ printf("%-8.6lf", 3.14);  
⓸ printf("%6.4lf00", 3.14);  
⓹ printf("%-10.3lf000", 3.14);

## 문제 5
연계 개념: 개념 3) `scanf` 공백/개행 처리
다음 코드와 입력이 주어질 때 출력값으로 올바른 것을 고르시오.

```c
#include <stdio.h>
int main()
{
    int n;
    char ch;
    scanf("%d", &n);
    scanf("%c", &ch);
    printf("%d", ch);
    return 0;
}
```

입력
```
7
A
```

⓵ 55  
⓶ 65  
⓷ 10  
⓸ 32  
⓹ 입력 오류
