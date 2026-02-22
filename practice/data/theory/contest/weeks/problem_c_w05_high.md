# C Contest Week 05 High Problem Set

## 범위
- Week 05 core source pool mapping
- 분반: 고등
- W05 개념 1~3 적용

## 문제 1
연계 개념: 개념 2) 누적합/최댓값 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>

int main()
{
    int a[] = {6, 7, 1, 3, 2, 10, 5, 8, 4, 9};
    int b = 0;
    for(int i=0 ; i<10 ; i++) {
        if(a[i] % 2 == 1) b += a[i];
        if(a[i] % 3 == 1) b -= a[i];
    }
    printf("%d\n", b);
    return 0;
}
```

① 1  
② 2  
③ 3  
④ 4  
⑤ 5

## 문제 2
연계 개념: 개념 3) 2차원 배열 순회
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include<stdio.h>

int main()
{
    int a[3], b[3], c[3];
    int d = 0;
    for(int i=0 ; i<3 ; i++) {
        a[i] = i + 2;
        b[i] = i * 4;
        c[i] = i * i;
    }
    for(int i=0 ; i<3 ; i++) {
        for(int j=0 ; j<3 ; j++) {
            for(int k=0 ; k<3 ; k++) {
                d += a[i] + b[j] * c[k];
            }
        }
    }

    printf("%d", d);
    return 0;
}
```

① 234  
② 261  
③ 297  
④ 1089  
⑤ 1116

## 문제 3
연계 개념: 개념 2) 누적합/최댓값 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>

int main()
{
    int a[4] = {13, 8, 7, 11};
    int b[4] = {2, 15, 3, 12};
    int c = 0;

    for(int i=0 ; i<4 ; i++) {
        for(int j=0 ; j<4 ; j++) {
            if(a[i] + b[j] <= 16 && a[i] + b[j] > c)
            {
                c = a[i] + b[j];
            }
        }
    }
    printf("%d\n", c);
    return 0;
}
```

① 8  
② 11  
③ 13  
④ 16  
⑤ 28  

## 문제 4
연계 개념: 개념 2) 누적합/최댓값 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>
int main()
{
    int a[] = {9, 10, 12, 3, 5, 1, 11, 6, 4, 2, 8, 7};
    int b = 0;
    for(int i=0 ; i<12 ; i++) {
        if(i % 2 == 1) b += a[i];
        if(i % 3 == 2) b -= a[i];
    }
    printf("%d", b);
    return 0;
}
```

① 1  ② 2  ③ 3  ④ 4  ⑤ 5

## 문제 5
연계 개념: 개념 2) 누적합/최댓값 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>
int main()
{
    int arr1[4] = {13, 8, 7, 11};
    int arr2[4] = {2, 15, 3, 12};
    int ans = 0;
    for(int i=0 ; i<4 ; i++) {
        for(int j=0 ; j<4 ; j++) {
            if((arr1[i] + arr2[j]) % 2 == 0 &&
               arr1[i] + arr2[j] > ans) {
                ans = arr1[i] + arr2[j];
            }
        }
    }
    printf("%d\n", ans);
    return 0;
}
```
① 8  ② 12  ③ 16  ④ 28  ⑤ 32
