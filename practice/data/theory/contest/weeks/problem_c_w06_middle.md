# C Contest Week 06 Middle Problem Set

## 범위
- Week 06 core source pool mapping
- 분반: 중등
- W06 개념 1~3 적용

## 문제 1
연계 개념: 개념 2) 문자 분류와 ASCII 이동, 개념 3) 문자열 순회/치환
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include<stdio.h>
#include<string.h>
int	main()
{
	char s[50] = "QQqqQQwwWeeEeeERRrrrrqqtYYyyYUIOP";
	int	k = 4, chk[27] = { 0 }, b = 0;
	for (int i = 0; s[i] != 0; i++) {
		if (s[i] <= 'Z') s[i] += 32;
	}

	char a = s[0];
	int	c = 1;
	for (int i = 1; s[i] != 0; i++) {
		if (s[i] == a) {
			c++;
		}
		else {
			if (chk[a - 'a'] == 0) {
				if (c >= k)	b++;
				chk[a - 'a'] = 1;
				a = s[i];
				c = 1;
			}
			else {
				a = s[i];
				c = 1;
			}
		}
	}
	if (chk[a - 'a'] == 0 && c >= k) {
		b++;
	}
	printf("%d", b);
	return	0;
}

```

⓵ 3  
⓶ 4  
⓷ 5  
⓸ 6  
⓹ 7

## 문제 2
연계 개념: 개념 2) 문자 분류와 ASCII 이동
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>

int main()
{
    char a[6] = "banana";
    int b = 0;
    for(int i = 0; i < 5; i++){
        for(int j = 0; j < i; j++){
            if(a[i] > a[j]) b++;
        }
    }
    printf("%d", b);
    return 0;
}
```

① 1  
② 2  
③ 3  
④ 4  
⑤ 5

## 문제 3
연계 개념: 개념 1) 널 문자와 `strlen`
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>
#include <string.h>

int main()
{
    int a = (int)strlen("KITPA\0");
    int b = (int)strlen("KITPA\n");
    printf("%d %d\n", a, b);
    return 0;
}
```

① 5 5  
② 5 6  
③ 5 7  
④ 6 5  
⑤ 6 6

## 문제 4
연계 개념: 개념 3) 문자열 순회/치환
다음 코드의 실행 결과를 작성하시오.

```c
#include <stdio.h>

void f(char* str1, char* str2) {
    int i, j;
    for(i=0, j=0 ; str1[i] != 0 ; i++) {
        if(str1[i] != str1[i+1]) {
            str2[j] = str1[i];
            j++;
        }
    }
    str2[j] = 0;
}

int main()
{
    char a[20] = "aaabbccccdeffff", b[20];
    f(a, b);
    printf("%s\n", b);
    return 0;
}
```

## 문제 5
연계 개념: 개념 2) 문자 분류와 ASCII 이동, 개념 3) 문자열 순회/치환
다음 코드의 실행 결과로 올바른 것을 고르시오.

```c
#include <stdio.h>
int main()
{
    char a[7] = "banana";
    char b[7] = "papaya";
    int c = 0;
    for(int i=0 ; i<6 ; i++) {
        for(int j=0 ; j<6 ; j++) {
            if(a[i] != b[j]) c++;
        }
    }
    printf("%d", c);
    return 0;
}
```
① 12  ② 17  ③ 22  ④ 27  ⑤ 32  

---
