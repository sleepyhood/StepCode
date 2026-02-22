# C Contest Week 08 High Problem Set

## 범위
- Week 08 core source pool mapping
- 분반: 고등
- W08 개념 1~3 적용

## 문제 1
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

## 문제 2
연계 개념: 개념 1) 기저 조건 설정, 개념 2) 호출-복귀 순서
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>

int f(int a) {
    if(a <= 1) return 1;
    return f(a-1) * 2 + f(a-3) * 5;
}

int main()
{
    printf("%d\n", f(4));
}
```

① 42  
② 43  
③ 44  
④ 45  
⑤ 46  

---

## 문제 3
연계 개념: 개념 1) 기저 조건 설정, 개념 2) 호출-복귀 순서
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>

int f(int a) {
    if(a == 0) return 0;
    return f(a / 10) + a % 10;
}

int main()
{
    printf("%d\n", f(빈  칸));
}
```

① 14  
② 89  
③ 168  
④ 221  
⑤ 512  

---

## 문제 4
연계 개념: 개념 1) 기저 조건 설정, 개념 2) 호출-복귀 순서
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>
int f(int a, int b) {
    if(a == 1) return 1;
    if(a % 2 == 1) return b * f(a-1, b);
    else return b * f(a/2, b);
}
int main()
{
    printf("%d\n", f(11, 3));
    return 0;
}
```
① 9  ② 27  ③ 81  ④ 243  ⑤ 729  

---

## 문제 5
연계 개념: 개념 1) 기저 조건 설정, 개념 2) 호출-복귀 순서
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>
int f(int a) {
	if (a <= 1) return 1;
	return f(a - 1) + f(a - 4) * 2;
}
int main()
{
	printf("%d\n", f(6));
	return 0;
}
```
① 12  ② 13  ③ 14  ④ 15  ⑤ 16
