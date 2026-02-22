# C Contest Week 08 Elementary Problem Set

## 범위
- Week 08 core source pool mapping
- 분반: 초등
- W08 개념 1~3 적용

## 문제 1
연계 개념: 개념 1) 기저 조건 설정, 개념 2) 호출-복귀 순서
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include<stdio.h>
void cnt(int n) {
    if(n > 0) cnt(n-1);
    printf("%d ", n);
}
int main()
{
    cnt(3);
}
```

⓵ 0 1 2 3  
⓶ 1 2 3  
⓷ 3 2 1  
⓸ 3 2 1 0  
⓹ 3 3 3  

## 문제 2
연계 개념: 개념 1) 기저 조건 설정, 개념 2) 호출-복귀 순서
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include<stdio.h>
int f(int a, int b) {
    if(a <= 0) return b;
    else return f(a-2, b*2) + b;
}
int main()
{
    printf("%d", f(10, 1));
    return 0;
}
```

⓵ 31  
⓶ 32  
⓷ 63  
⓸ 64  
⓹ 127

## 문제 3
연계 개념: 개념 1) 기저 조건 설정, 개념 2) 호출-복귀 순서
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include<stdio.h>
int f(int n) {
    if(n == 0) return 1;
    if(n == 1) return 4;
    if(n == 2) return 9;
    return f(n-1) + f(n-3);
}
int main()
{
    printf("%d", f(9));
    return 0;
}
```

⓵ 47  
⓶ 70  
⓷ 103  
⓸ 150  
⓹ 241

## 문제 4
연계 개념: 개념 1) 기저 조건 설정, 개념 2) 호출-복귀 순서
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include<stdio.h>
int	f(int v) {
	int	s = 0;
	if (v == 1)	return 1;
	return f(v / 2) + v;
}
int	main()
{
	printf("%d", f(16));
	return 0;
}
```

⓵ 15  
⓶ 30  
⓷ 31  
⓸ 62  
⓹ 63

## 문제 5
연계 개념: 개념 1) 기저 조건 설정, 개념 2) 호출-복귀 순서
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>

int f(int a, int b) {
    if(a == 1) return 1;
    else return b * f(a-1, b);
}

int main()
{
    printf("%d\n", f(5, 6));
    return 0;
}
```

① 216  
② 625  
③ 1296  
④ 3125  
⑤ 7776
