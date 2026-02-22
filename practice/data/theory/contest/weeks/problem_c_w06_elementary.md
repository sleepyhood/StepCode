# C Contest Week 06 Elementary Problem Set

## 범위
- Week 06 core source pool mapping
- 분반: 초등
- W06 개념 1~3 적용

## 문제 1
연계 개념: 개념 3) 문자열 순회/치환
다음 중 문자열 함수 설명으로 올바르지 않은 것을 고르시오.

⓵ strcpy – 문자열을 문자열에 복사한다 (destination, source)  
⓶ strcmp – 두 문자열을 비교한다  
⓷ strchr – 문자열에서 처음으로 특정 문자와 일치하는 문자의 주소를 반환한다  
⓸ strstr – 문자열1에서 문자열2를 검색하여 가장 먼저 나타나는 곳의 위치를 반환한다  
⓹ strcat – 문자열을 특정 문자들로 분리한다

## 문제 2
연계 개념: 개념 1) 널 문자와 `strlen`, 개념 2) 문자 분류와 ASCII 이동
다음 코드의 실행 결과로 올바른 것을 고르시오.

<입력>
```text
clanguage python
```

```c
#include<stdio.h>
#include<string.h>
#define F(A,B) (A<B?A:B);
int main()
{
    char a[12], b[12];
    scanf("%s %s", a, b);

    int len_a = strlen(a);
    int len_b = strlen(b);
    int len_s = F(len_a, len_b);

    for(int i=0; i<len_s; i++) {
        if(i % 2 == 0) printf("%c", a[i]);
        else printf("%c", b[i]);
    }
}
```

⓵ pltnou  
⓶ cyahgn  
⓷ pltnoug  
⓸ cyahgnae  
⓹ clangu

## 문제 3
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

## 문제 4
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

## 문제 5
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
