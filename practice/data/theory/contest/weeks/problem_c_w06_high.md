# C Contest Week 06 High Problem Set

## 범위
- Week 06 core source pool mapping
- 분반: 고등
- W06 개념 1~3 적용

## 문제 1
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

## 문제 2
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

## 문제 3
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

## 문제 4
연계 개념: 개념 2) 문자 분류와 ASCII 이동, 개념 3) 문자열 순회/치환
다음 코드의 출력 결과를 작성하시오.

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

## 문제 5
연계 개념: 개념 3) 문자열 순회/치환
다음 중 문자열 함수 설명으로 올바르지 않은 것을 고르시오.

⓵ strcpy – 문자열을 문자열에 복사한다 (destination, source)  
⓶ strcmp – 두 문자열을 비교한다  
⓷ strchr – 문자열에서 처음으로 특정 문자와 일치하는 문자의 주소를 반환한다  
⓸ strstr – 문자열1에서 문자열2를 검색하여 가장 먼저 나타나는 곳의 위치를 반환한다  
⓹ strcat – 문자열을 특정 문자들로 분리한다
