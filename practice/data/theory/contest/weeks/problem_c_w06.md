# C Contest Week 06 Problem Set

## 주차 주제
- 문자열/문자 처리

## 실전 문제 묶음
- 아래 문항은 출처 원문에서 주차 목표에 맞게 선별한 실제 문제이다.

### C_2023_1회
- 문항: 14, 19, 21

#### 문제 14
14. 다음은 string.h 헤더 파일에 정의된 함수에 대한 설명이다. 올바르지 않은 설명을 고르시오 [초고]
⓵ strcpy – 문자열을 문자열에 복사한다 (destination, source)  
⓶ strcmp – 두 문자열을 비교한다  
⓷ strchr – 문자열에서 처음으로 특정 문자와 일치하는 문자의 주소를 반환한다  
⓸ strstr – 문자열1에서 문자열2를 검색하여 가장 먼저 나타나는 곳의 위치를 반환한다  
⓹ strcat – 문자열을 특정 문자들로 분리한다

---

#### 문제 19
19. 아래 코드의 입력이 다음과 같을 때 실행 결과로 올바른 것을 고르시오 [초중]
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

---

#### 문제 21
21. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초중]
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

---

### C_2024_2회
- 문항: 10, 15, 20

#### 문제 10
10. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]
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

---

#### 문제 15
15. 다음 프로그램의 실행 결과는 무엇인가? [초, 중, 고]
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

---

#### 문제 20
20. 다음 프로그램의 실행 결과는 무엇인가? [초]
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

---

### C_2024_3회
- 문항: 12, 18

#### 문제 12
12. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]
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

---

#### 문제 18
18. 다음 프로그램에 아래 값을 입력했을 때의 출력 결과는 무엇인가? [중, 고]
<입력>
```
kitpaa afogai
```

```c
#include <stdio.h>
#include <string.h>

int cnt[26];
char str1[101], str2[101];

int main()
{
    int i;
    scanf("%s %s", str1, str2);
    for (i = 0; str1[i] != '\0'; i++)
        cnt[str1[i] - 'a'] += 1;
    for (i = 0; str2[i] != '\0'; i++)
        cnt[str2[i] - 'a'] -= 1;
    for (i = 0; i < 26; i++) {
        if (cnt[i]) {
            printf("%s %d", str1, i);
            break;
        }
    }
    if (i == 26)
        printf("%s %d", str2, i);
    return 0;
}
```

---
