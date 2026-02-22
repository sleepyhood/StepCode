# C Contest Week 08 Problem Set

## 주차 주제
- 재귀 기본(종료조건/복귀)

## 실전 문제 묶음
- 아래 문항은 출처 원문에서 주차 목표에 맞게 선별한 실제 문제이다.

### C_2023_1회
- 문항: 9, 12, 13, 16

#### 문제 9
9. 다음 코드의 실행 결과로 올바른 것을 고르시오 [중고]
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

#재귀함수

---

#### 문제 12
12. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초중]
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

---

#### 문제 13
13. 다음 코드의 실행 결과로 올바른 것을 고르시오 [중고]
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

---

#### 문제 16
16. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초]
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

---

### C_2024_2회
- 문항: 7, 8, 12

#### 문제 7
7. 다음 프로그램의 실행 결과는 무엇인가? [고]
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

---

#### 문제 8
8. 다음 프로그램의 실행 결과는 무엇인가? [초]
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

---

#### 문제 12
12. 다음 프로그램의 빈 칸에 값을 넣었을 때 가장 큰 값을 가지는 코드를 고르시오. [초, 중]
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

---

### C_2024_3회
- 문항: 8, 9, 11

#### 문제 8
8. 다음 프로그램의 실행 결과는 무엇인가? [초, 중]
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

---

#### 문제 9
9. 다음 프로그램의 실행 결과는 무엇인가? [초]
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

---

#### 문제 11
11. 다음 프로그램의 실행 결과는 무엇인가? [초, 중, 고]
```c
#include<stdio.h>
int f(int n) {
    if(n == 0) return 1;
    if(n == 1) return 5;
    if(n == 2) return 9;
    int a = 0;
    if(n % 5 == 0 || n % 5 == 3) a = 4;
    else if(n % 5 == 4) a = 6;
    else a = 5;
    return f(n-1) + a;
}
int main()
{
    printf("%d", f(7));
    return 0;
}
```
① 15  ② 24  ③ 33  ④ 43  ⑤ 53

---
