# 청소년 IT경시대회 C언어 문제 개념별 정리 (문제 원문 포함)

각 문제는 대표 개념 1개에만 배치했습니다.

---

# 컴파일/전처리/표준 라이브러리

[출처: 2023년 제1회]

## 1. 고급 프로그래밍 언어를 실행 프로그램으로 만들기 위해 저급 프로그래밍 언어로 바꾸는데 사용하는 프로그램은 무엇인가 [초중고]  
⓵ 가상 머신  
⓶ 인터프리터  
⓷ 컴파일러  
⓸ 바이트코드  
⓹ C 언어  
#컴파일러

---

[출처: 2023년 제1회]

## 2. 다음은 C 언어의 표준 라이브러리와 그 헤더에 대한 설명이다. 올바르지 않게 짝지어진 것을 고르시오 [중고]  
⓵ stdio.h – C 언어에 입출력 기능을 제공한다  
⓶ time.h – 시간과 날짜 관련 함수를 제공한다  
⓷ assert.h – 논리 오류 및 디버깅 중의 오류 형 등을 제공한다  
⓸ stdarg.h – 다양한 예외 처리 들을 제어한다  
⓹ stddef.h – 일반적으로 사용되는 포인터, 변수, 형을 선언한다  
#헤더파일

---

[출처: 2024년 제3회]

## 5. stdio.h 헤더 파일에 정의 되어 있는 함수 중 형식이 있는 입출력을 수행하지 않는 함수를 고르시오. [초, 중]
① scanf  ② fputs  ③ vprintf  ④ printf  ⑤ sprintf

---

# 자료형/상수/진법

[출처: 2023년 제1회]

## 3. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초중고] 

```c
#include<stdio.h>
int main()
{
    short s = 32767;
    s = s + 1;
    printf("%d", s);
    return 0;
}
```

⓵ -32768  
⓶ -1  
⓷ 1  
⓸ 32768  
⓹ 오류가 발생한다  
#자료형 #오버플로우

---

[출처: 2023년 제1회]

## 4. 다음 코드의 실행 결과로 올바른 것을 고르시오 [중고] 

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
#진법 #8진법 #16진법

---

[출처: 2024년 제2회]

## 5. 다음 프로그램의 실행 결과는 무엇인가? [초, 중, 고]

```c
#include <stdio.h>
#include <limits.h>

int main()
{
    printf("%d\n", SHRT_MAX);
    return 0;
}
```

① 127  
② 255  
③ 32767  
④ 65535  
⑤ 2147483647

---

# 입출력/서식 지정

[출처: 2023년 제1회]

## 5. 다음 중 다른 값이 출력되는 출력문을 고르시오 [초고]  
⓵ printf("%lf", 3.14);  
⓶ printf("%7.6lf", 3.14);  
⓷ printf("%-8.6lf", 3.14);  
⓸ printf("%6.4lf00", 3.14);  
⓹ printf("%-10.3lf000", 3.14);  

#서식지정자 #서식지정자심화

---

# 사칙연산

[출처: 2023년 제1회]

## 7. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초중고] 

```c
#include<stdio.h>
int main()
{
    int a = (25 / 4) * 3;
    int b = (a * a) / a;
    printf("%d %d", a+b, a-b);
}
```

⓵ 36 0  
⓶ 35 1  
⓷ 35 0  
⓸ 34 1  
⓹ 37 0  


---

# 비트연산
[출처: 2024년 제3회]

## 14. 다음 프로그램의 빈 칸에 값을 넣었을 때 실행 결과가 1인 것을 고르시오. [초, 중, 고]

```c
#include <stdio.h>
int main()
{
    int a[5] = {빈 칸};
    int b = 0;
    for(int i=0 ; i<5 ; i++) {
        b ^= a[i];
    }
    printf("%d\n", b);
    return 0;
}
```
① 0, 1, 2, 3, 4  
② 1, 2, 3, 4, 4  
③ 1, 3, 1, 3, 1  
④ 0, 0, 0, 1, 1  
⑤ 10, -10, 10, -10, 10

---

# 조건문/삼항연산자

[출처: 2023년 제1회]

## 6. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초] 

```c
#include<stdio.h>
int main()
{
    int x = 12;
    int y = 15;
    printf("%d", x>y?(x+y):(x*y));
    return 0;
}
```

⓵ 3  
⓶ 12  
⓷ 15  
⓸ 27  
⓹ 180  


---

[출처: 2023년 제1회]

## 8. 어떤 해가 윤년인지 판단하는 기준은 연도 값이 4로 나누어 떨어지면 윤년이지만 100으로 나누어 떨어지면 윤년이 아니다. 그러나 400으로 나누어 떨어지면 윤년이다.  
주어진 연도가 윤년이면 1, 아니면 0을 반환하는 함수를 만든다고 할 때 빈 칸에 들어갈 코드로 알맞은 것을 고르시오 [초중고] 

```c
int leapYear(int y) {
    if([빈 칸]) return 0;  // 빈 칸
    else return 1;
}
```

⓵ (y % 4 == 0 && y % 100 != 0) && y % 400 == 0  
⓶ (y % 4 == 0 && y % 100 != 0) || y % 400 == 0  
⓷ (y % 4 != 0 && y % 100 == 0) || y % 400 != 0  
⓸ (y % 4 != 0 || y % 100 == 0) || y % 400 != 0  
⓹ (y % 4 != 0 || y % 100 == 0) && y % 400 != 0  


---

[출처: 2023년 제1회]

## 15. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초중고] 

```c
#include<stdio.h>
int	main()
{
	int	a[144];
	int	n = 144;
	for (int i = 0; i < n; i++) {
		if (i % 5 == 1 || i % 5 == 2) a[i] = 1;
		else if (i % 5 == 4) a[i] = 2;
		else a[i] = 3;
	}
	int	b = a[0], m = 1;
	for (int i = 1; i < n; i++) {
		if (m == 0) {
			b = a[i];
			m = 1;
		}
		else {
			if (b % 2 == 0) {
				b += a[i];
				m--;
			}
			else {
				b -= a[i];
			}
		}
	}
	printf("%d", b);
	return	0;
}
```

⓵ 1  
⓶ 2  
⓷ 3  
⓸ 4  
⓹ 5

---

[출처: 2023년 제1회]

## 18. 산악회 소속 준용이는 이번에 전국에 있는 산을 바이크를 타며 투어를 하려고 한다. 준용이는 N개의 체크 포인트를 지정하였고, i번째 체크포인트는 H_i의 높이를 가진다.  
준용이는 전체 체크포인트 중에 “정점”이 총 몇 개인지 알고 싶어 한다. “정점”이란 첫 번째와 N번째 체크포인트를 제외하고 전과 후의 체크포인트보다 높은 높이를 가진 체크포인트를 말한다. 준용이를 도와 총 몇 개의 “정점”이 있는지 구해봅시다.

첫 번째 줄에 전체 체크포인트의 수 N (1 <= N <= 100)이 주어집니다.  
두 번째 줄에 전체 체크포인트의 높이 H_i (1 <= H_i <= 10,000)가 공백으로 구분되어 주어집니다.

다음은 몇 개의 “정점”이 있는지 출력하는 프로그램의 일부입니다. 빈 칸에 들어갈 코드로 알맞은 것을 고르시오 [초중고]

```c
#include<stdio.h>
int main()
{
    int n, cnt = 0;
    int a[101];
    scanf("%d", &n);
    for(int i=0; i<n; i++) {
        scanf("%d", &a[i]);
    }
    for([빈 칸 a ]) {      // 빈 칸
        if([빈 칸 b ]) {   // 빈 칸
            cnt++;
        }
    }
    printf("%d", cnt);
    return 0;
}
```

⓵ (a) int i=1; i<n-1; i++<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(b) a[i-1] < a[i] && a[i] > a[i+1]  
⓶ (a) int i=0; i<n;   i++<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(b) a[i-1] < a[i] && a[i] > a[i+1]  
⓷ (a) int i=0; i<n;   i++<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(b) a[i+1] < a[i] && a[i] > a[i-1]  
⓸ (a) int i=1; i<n-1; i++<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(b) a[i-1] < a[i] || a[i] > a[i+1]  
⓹ (a) int i=0; i<n;   i++<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(b) a[i-1] <= a[i] && a[i] >= a[i+1]

---

[출처: 2024년 제2회]

## 6. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]

```c
#include <stdio.h>

int main()
{
    int i, a = 0;
    for(i=2 ; i<62 ; i++) {
        if(i % 2 == 0 && i % 3 == 0 && i % 5 == 0) {
            a += i;
        }
    }
    printf("%d\n", a);
    return 0;
}
```

① 15  
② 30  
③ 45  
④ 60  
⑤ 90

---

[출처: 2024년 제2회]

## 16. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]

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

---

---

[출처: 2024년 제2회]

## 17. 다음 프로그램의 실행 결과는 무엇인가? [초, 중]

```c
#include <stdio.h>

int main()
{
    int flag = 0;
    for(int i=1 ; i<10 ; i++) {
        for(int j=0 ; j<10 ; j++) {
            for(int k=0 ; k<10 ; k++) {
                if(i == k || j == k) continue;
                if((i * 10 + j) * k == (j * 10 + i)) {
                    printf("%d\n", k);
                    flag = 1;
                    break;
                }
            }
            if(flag == 1) break;
        }
        if(flag == 1) break;
    }
    return 0;
}
```

① 1  
② 3  
③ 5  
④ 7  
⑤ 9

---

[출처: 2024년 제3회]

## 6. 다음 프로그램의 실행 결과는 무엇인가? [초]

```c
#include <stdio.h>
int main()
{
    int a = 0;
    for(int i=2 ; i<15 ; i++) {
        if(i % 2 == 0 || i % 3 == 0 && i % 5 == 0) {
            a++;
        }
    }
    printf("%d", a);
    return 0;
}
```
① 6  ② 7  ③ 14  ④ 15  ⑤ 16

---

[출처: 2024년 제3회]

## 7. 다음 프로그램의 실행 결과는 무엇인가? [초, 중, 고]

```c
#include<stdio.h>
int main()
{
    int x = 12;
    int y = 15;
    int z = 18;
    printf("%d", (x*y)>(y&z)?(x+y):(y+z));
    return 0;
}
```
① 0  ② 27  ③ 30  ④ 33  ⑤ 180

---



[출처: 2024년 제3회]

## 15. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]

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

---

# 반복문/흐름 제어

[출처: 2023년 제1회]

## 22. 아래 프로그램의 출력 결과에서 1번째 줄과 4번째 줄에 출력되는 숫자의 합을 작성하시오 [초] 

```c
#include<stdio.h>
int main()
{
    int a = 3, b = 7, k = 5;
    for(int i=a; i<=b; i++) {
        int d = (i-1) * i / 2 + 1;
        if(i <= k) {
            for(int j=d; j<=d+i-1; j++) {
                printf("%d ", j);
            }
        } else {
            for(int j=d; j<d+k; j++) {
                printf("%d ", j);
            }
        }
        printf("\n");
    }
}
```

---



[출처: 2024년 제2회]

## 1. 다음 프로그램의 실행 결과는 무엇인가? [초, 중]

```c
#include <stdio.h>

int main()
{
    int a = 0;
    for(int i=100 ; i<=2024 ; i+=100) {
        a += 2;
    }
    printf("%d\n", a);

    return 0;
}
```

① 36  
② 38  
③ 40  
④ 42  
⑤ 44

---

[출처: 2024년 제2회]

## 3. 다음 프로그램의 실행 결과는 무엇인가? [고]

```c
#include <stdio.h>

int main()
{
    int a = 20, b = 30;
    while(a > 0) {
        a -= 6;
        b *= 3;
        b /= 2;
    }
    printf("%d\n", b);
    return 0;
}
```

① 100  
② 101  
③ 150  
④ 151  
⑤ 200  

---

---

[출처: 2024년 제2회]

## 10. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]

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

[출처: 2024년 제2회]

## 14. 다음 프로그램의 실행 결과는 무엇인가? [초, 중, 고]

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

---

[출처: 2024년 제3회]

## 1. 다음 프로그램의 실행 결과는 무엇인가? [고]


```c
#include <stdio.h>
int main()
{
    int sum = 0;
    for(int i=1 ; i<=10 ; i++) {
        if(i % 3 == 0) {
            sum += i;
        }
    }
    printf("%d", sum);
    return 0;
}
```

① 14  ② 16  ③ 18  ④ 20  ⑤ 22

---

[출처: 2024년 제3회]

## 3. 다음 프로그램의 실행 결과는 무엇인가? [초, 중]

```c
#include <stdio.h>
int main()
{
    int a = 20, b = 30;
    while(a > 0) {
        a -= 6;
        b += 3;
    }
    printf("%d\n", b);
    return 0;
}
```
① 30  ② 36  ③ 42  ④ 48  ⑤ 54  

---

---

[출처: 2024년 제3회]

## 12. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]

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

# 배열/인덱싱/브루트포스

[출처: 2023년 제1회]

## 10. 다음 코드의 실행 결과로 올바른 것을 고르시오 [고] 

```c
#include<stdio.h>
int	main()
{
	int	d[9] = { 90, 20, 30, 50, 40, 20, 40, 12 };
	int	s = d[0];
	int	n1 = d[0];
	int	n2 = d[0];

	for (int i = 1; i < 8; i++) {
		s += d[i];
		if (n1 > d[i])	n1 = d[i];
		if (n2 < d[i])	n2 = d[i];
	}

	printf("%d", (s - n1 - n2) / 6);
	return	0;
}
```

⓵ 30  
⓶ 32  
⓷ 33  
⓸ 35  
⓹ 37  

#배열 #반복문

---

[출처: 2023년 제1회]

## 11. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초중고] 

```c
#include<stdio.h>
int main()
{
    int a[5] = {3, 2, 0, 4, 1};
    for(int i=0; i<5; i++) {
        int b = i;
        for(int j=1; j<=2023; j++) {
            b = a[b];
        }
        printf("%d ", b);
    }
    return 0;
}
```

⓵ 4 0 3 1 2  
⓶ 1 3 4 2 0  
⓷ 2 4 1 0 3  
⓸ 3 2 0 4 1  
⓹ 0 1 2 3 4

---

[출처: 2024년 제2회]

## 2. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]

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

---


[출처: 2024년 제3회]

## 2. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]

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

---

# 문자열/문자 처리

[출처: 2023년 제1회]

## 14. 다음은 string.h 헤더 파일에 정의된 함수에 대한 설명이다. 올바르지 않은 설명을 고르시오 [초고]  
⓵ strcpy – 문자열을 문자열에 복사한다 (destination, source)  
⓶ strcmp – 두 문자열을 비교한다  
⓷ strchr – 문자열에서 처음으로 특정 문자와 일치하는 문자의 주소를 반환한다  
⓸ strstr – 문자열1에서 문자열2를 검색하여 가장 먼저 나타나는 곳의 위치를 반환한다  
⓹ strcat – 문자열을 특정 문자들로 분리한다

---

[출처: 2023년 제1회]

## 21. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초중] 

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

[출처: 2024년 제2회]

## 4. string.h 헤더 파일에 정의 되어 있는 strcpy 함수는 문자열을 복사하는 함수입니다. 이 함수의 원형으로 올바른 것을 고르시오. [고]

① char* strcpy(char*, const char*);  
② const char* strcpy(string, char*);  
③ char* strcpy(const char*, char*);  
④ const char* strcpy(char*, string);  
⑤ string strcpy(char*, char*);

---

[출처: 2024년 제2회]

## 15. 다음 프로그램의 실행 결과는 무엇인가? [초, 중, 고]

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

[출처: 2024년 제3회]

## 4. string.h 헤더 파일에 정의 되어 있는 strncmp 함수는 두 문자열을 특정 자리 수 만큼 비교하는 함수입니다. 이 함수의 원형으로 올바른 것을 고르시오. [초, 중, 고]
① int strncmp(const char*, const char*, size_t);  
② char* strncmp(const char*, const char*, size_t);  
③ void strncmp(const char*, const char*, size_t);  
④ int strncmp(const char*, const char*);  
⑤ char* strncmp(const char*, const char*);

---

[출처: 2024년 제3회]

## 18. 다음 프로그램에 아래 값을 입력했을 때의 출력 결과는 무엇인가? [중, 고]

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

# 전처리기 매크로

[출처: 2023년 제1회]

## 17. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초중고]
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

[출처: 2023년 제1회]

## 19. 아래 코드의 입력이 다음과 같을 때 실행 결과로 올바른 것을 고르시오 [초중] 

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

[출처: 2023년 제1회]

## 20. 아래 코드의 입력이 다음과 같을 때 실행 결과로 올바른 것을 고르시오 [중고] 

<다음>
```text
4
66
20
95
5
```

```c
#include<stdio.h>
#define K(A,B) (A>B?B:A)

int a[1300], ac;

void f() {
    a[0] = 2;
    ac = 1;
    for(int i=3; i<=111; i+=2) {
        int c = 0;
        for(int j=3; j*j<=i; j++) {
            if(i % j == 0) {
                c = 1;
                break;
            }
        }
        if(c == 1) continue;
        a[ac++] = i;
    }
}
int main()
{
    int t, p, v = 0;
    f();
    scanf("%d", &t);
    while(t--) {
        int n;
        scanf("%d", &n);
        for(int i=0; i<ac; i++) {
            if(a[i] == n) {
                v += 0;
                break;
            }
            if(a[i] < n && n < a[i+1]) {
                v += K(a[i+1]-n, n-a[i]);
            }
        }
    }
    printf("%d", v);
    return 0;
}
```



⓵ 1 
⓶ 2  
⓷ 3  
⓸ 4  
⓹ 5

---

[출처: 2024년 제2회]

## 13. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]

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

[출처: 2024년 제2회]

## 21. 다음 프로그램의 입력이 아래와 같을 때 실행 결과는 무엇인가? [중, 고]

<입력>
```
7 6
123151
315348
999181
994321
386357
617410
320987
```

```c
#include <stdio.h>

#define M(A, B) (A > B ? B : A)
#define N(A, B) (A ^ B == 0)
#define P(A, B) (A > B ? A : B)

int n, m;
int mapp[8][8];

int main(void) {
    int f = 1;
    scanf("%d %d", &n, &m);
    
    for(int i=0 ; i<n ; i++) {
        for(int j=0 ; j<m ; j++) {
            scanf("%1d", &mapp[i][j]);
        }
    }

    for(int k = M(n, m) ; k >= 2 ; k--) {
        for(int i=0 ; i<=n-k ; i++) {
            for(int j=0 ; j<=m-k ; j++) {
                if(N(N(mapp[i][j], mapp[i+k-1][j]),
                    N(mapp[i][j+k-1], mapp[i+k-1][j+k-1]))) {
                    f = P(f, k * k);
                }
            }
        }
    }

    printf("%d\n", f);
    return 0;
}
```

---

## 정답

| 문항 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| 정답 | 3 | 3 | 3 | 1 | 3 |

| 문항 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- |
| 정답 | 5 | 3 | 2 | 3 | 5 |

| 문항 | 11 | 12 | 13 | 14 | 15 |
| --- | --- | --- | --- | --- | --- |
| 정답 | 2 | 2 | 2 | 2 | 2 |

| 문항 | 16 | 17 | 18 | 19 | 20 |
| --- | --- | --- | --- | --- | --- |
| 정답 | 4 | 1 | 4 | 4 | abcdef |

| 문항 | 21 |
| --- | --- |
| 정답 | 36 |

---

[출처: 2024년 제3회]

## 13. 다음 프로그램의 실행 결과는 무엇인가? [초]

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

# 재귀/분할정복

[출처: 2023년 제1회]

## 9. 다음 코드의 실행 결과로 올바른 것을 고르시오 [중고] 

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

[출처: 2023년 제1회]

## 12. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초중] 

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

[출처: 2023년 제1회]

## 13. 다음 코드의 실행 결과로 올바른 것을 고르시오 [중고] 

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

[출처: 2023년 제1회]

## 16. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초]

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

[출처: 2023년 제1회]

## 23. 아래 프로그램에 <입력 1>과 <입력 2>를 입력했을 때 출력되는 문자열을 한 줄에 공백으로 구분하여 작성하시오.  
예를 들어 <입력 1>의 출력 결과가 ABC, <입력2>의 출력 결과가 DEF라면, "ABC DEF" 를 답안에 작성하시오. [초중고] 

<입력 1>
```text
7
D B C A C D P
```

<입력 2>
```text
11
P R O G R A M M I N G
```

```c
#include<stdio.h>
typedef struct datastructure {
    int front;
    int rear;
    char q[101];
} DS;
int n;
char v;
DS d;

void f(char k) {
    d.front = d.rear = 50;
    d.q[50] = k;
}
void g(char k) {
    d.q[--(d.front)] = k;
}
void h(char k) {
    d.q[++(d.rear)] = k;
}
int main()
{
    scanf("%d", &n);
    scanf(" %c", &v);
    f(v);

    for(int i=0; i<n-1; i++) {
        scanf(" %c", &v);
        if(v <= d.q[d.front]) g(v);
        else                  h(v);
    }
    for(int i=d.front; i<=d.rear; i++) {
        printf("%c", d.q[i]);
    }
    return 0;
}
```
#typedef #구조체


[출처: 2024년 제2회]

## 7. 다음 프로그램의 실행 결과는 무엇인가? [고]

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

[출처: 2024년 제2회]

## 8. 다음 프로그램의 실행 결과는 무엇인가? [초]

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

[출처: 2024년 제2회]

## 9. 다음 프로그램에서 4번째로 출력되는 수는 무엇인가? [중, 고]

```c
#include <stdio.h>

void f(int a, int b) {
    if(a == b) {
        printf("%d ", a);
        return;
    }
    int c = (a + b) / 2;
    f(a, c);
    f(c+1, b);
}

int main()
{
    f(0, 15);
    return 0;
}
```

① 1  
② 2  
③ 3  
④ 4  
⑤ 5

---

[출처: 2024년 제2회]

## 12. 다음 프로그램의 빈 칸에 값을 넣었을 때 가장 큰 값을 가지는 코드를 고르시오. [초, 중]

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

[출처: 2024년 제2회]

## 18. 다음 프로그램의 실행 결과는 무엇인가? [고]

```c
#include <stdio.h>

int f(int a, int b) {
    return b * 2 - a;
}

int main()
{
    int a = 1;
    for(int i=0 ; i<12 ; i++) {
        a = f(a, -i);
        a = f(a, i);
    }
    printf("%d\n", a);
    return 0;
}
```

① 256  
② 259  
③ 262  
④ 265  
⑤ 268

---

[출처: 2024년 제2회]

## 20. 다음 프로그램의 실행 결과는 무엇인가? [초]

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

[출처: 2024년 제3회]

## 8. 다음 프로그램의 실행 결과는 무엇인가? [초, 중]

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

[출처: 2024년 제3회]

## 9. 다음 프로그램의 실행 결과는 무엇인가? [초]

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

[출처: 2024년 제3회]

## 10. 다음 프로그램에서 3번째로 출력되는 수는 무엇인가? [초]

```c
#include <stdio.h>
void f(int a, int b) {
    if(a == b) {
        printf("%d ", a);
        return;
    }
    int c = a + (b - a) / 4;
    f(a, c);
    f(c+1, b);
}
int main()
{
    f(0, 15);
    return 0;
}
```
① 1  ② 2  ③ 3  ④ 4  ⑤ 5

---

[출처: 2024년 제3회]

## 11. 다음 프로그램의 실행 결과는 무엇인가? [초, 중, 고]

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

[출처: 2024년 제3회]

## 16. 다음 프로그램의 실행 결과는 무엇인가? [초, 중]


```c
#include <stdio.h>
int f(int a, int b) {
    return a - b * 3;
}
int main()
{
    int a = 3;
    for(int i=0 ; i<4 ; i++) {
        a = f(a, -i);
        a = f(a, i);
    }
    printf("%d\n", a);
    return 0;
}
```
① 0  ② 1  ③ 2  ④ 3  ⑤ 4  

---

---

# 동적 메모리/포인터

[출처: 2024년 제2회]

## 11. stdlib.h 헤더 파일에 정의 되어 있는 함수 중 동적 메모리 할당을 하며 배열을 0으로 초기화 하는 함수를 고르시오. [초, 중, 고]

① atoi  
② calloc  
③ free  
④ malloc  
⑤ realloc

---

# 그래프/격자 탐색(DFS)

[출처: 2024년 제2회]

## 19. 다음 프로그램의 실행 결과는 무엇인가? [초]

```c
#include <stdio.h>

char a[5][5] = {"0010", "1111", "1100", "0111"};
int b;

void f(int p, int q, int r) {
    if(p < 0 || q < 0 || p >= 4 || q >= 4) return;
    if(a[p][q] == '0') return;
    b += r;

    a[p][q] = '0';
    f(p-1, q, r+1);
    f(p+1, q, r+1);
    f(p, q-1, r+1);
    f(p, q+1, r+1);
}

int main()
{
    for(int i=0 ; i<4 ; i++) {
        for(int j=0 ; j<4 ; j++) {
            if(a[i][j] == '1') {
                f(i, j, 1);
            }
        }
    }
    printf("%d\n", b);
    return 0;
}
```

① 8  
② 14  
③ 36  
④ 42  
⑤ 68

---

[출처: 2024년 제3회]

## 19. 다음 프로그램에 아래 값을 입력했을 때의 출력 결과는 무엇인가? [초]

<입력>
```
5 4
1 0 1 0 0
1 0 0 0 0
1 0 1 0 1
1 0 0 1 0
```

```c
#include <stdio.h>
int mapp[10][10], w, h;
int ans;
void f(int x, int y) {
    if(x < 1 || x > w || y < 1 || y > h) return;
    if(!mapp[x][y]) return;
    mapp[x][y] = 0;
    for(int i=-1 ; i<=1 ; i++) {
        for(int j=-1 ; j<=1 ; j++) {
            f(x+i, y+j);
        }
    }
}
int main()
{
    scanf("%d %d", &h, &w);
    for(int i=1 ; i<=w ; i++) {
        for(int j=1 ; j<=h ; j++) {
            scanf("%d", &mapp[i][j]);
        }
    }
    for(int i=1 ; i<=w ; i++) {
        for(int j=1 ; j<=h ; j++) {
            if(mapp[i][j]) {
                ans++;
                f(i, j);
            }
        }
    }
    printf("%d", ans);
}
```

---

## 정답 (C언어)
| 문항 | 정답 |
|---:|:---|
| 1 | 3 |
| 2 | 5 |
| 3 | 3 |
| 4 | 1 |
| 5 | 2 |
| 6 | 2 |
| 7 | 2 |
| 8 | 4 |
| 9 | 4 |
| 10 | 2 |
| 11 | 3 |
| 12 | 4 |
| 13 | 3 |
| 14 | 3 |
| 15 | 4 |
| 16 | 4 |
| 17 | 5 |
| 18 | kitpaa 5 |
| 19 | 3 |

---

# 그래프/트리/탐색(DFS) + 동적 메모리

[출처: 2023년 제1회]

## 24. 아래 프로그램에 <입력>을 입력했을 때 출력되는 값을 작성하시오 [초중고] 

<입력>
```text
8
4 6
8 1
4 1
2 3
4 7
5 6
1 3
```

```c
#include<stdio.h>
int n;
int *link[10];
int size[10], check[10], ans;

void search(int c, int p) {
    int count = 0;
    check[c] = 1;
    for(int i=0; i<size[c]; i++) {
        if(!check[ link[c][i] ]) {
            search(link[c][i], p+1);
            count++;
        }
    }
    if(count == 0) ans += p;
}

int main()
{
    scanf("%d", &n);

    for(int i=1; i<=n; i++) {
        link[i] = (int*)malloc(sizeof(int));
        link[i][0] = 0;
    }

    int p, q;
    for(int i=0; i<n-1; i++) {
        scanf("%d %d", &p, &q);

        link[p] = realloc(link[p], sizeof(int)*(size[p] + 1));
        link[p][size[p]] = q;
        size[p]++;

        link[q] = realloc(link[q], sizeof(int)*(size[q] + 1));
        link[q][size[q]] = p;
        size[q]++;
    }

    search(1, 0);
    printf("%d", ans);
    return 0;
}
```

---

# 이분 탐색/파라메트릭 서치

[출처: 2023년 제1회]

## 25. 아래 프로그램에 <입력1>과 <입력2>를 입력했을 때 출력되는 값의 합을 작성하시오 [중고] 

<입력 1> 
```text
8 3
3 4 5 6 7 8 9 10
```

<입력 2>
```text
12 4
10 20 30 40 30 40 20 30 40 50 10 20
```

```c
#include<stdio.h>
int main()
{
    int n, m, a[20];
    int s = 0;
    scanf("%d %d", &n, &m);
    for(int i=0; i<n; i++) {
        scanf("%d", &a[i]);
        s += a[i];
    }

    int l = 0, r = s;
    int ans = -1;
    while(l <= r) {
        int c = (l + r) / 2;
        int cnt = 1, t = 0, flg = 0;
        for(int i=0; i<n; i++) {
            if(t + a[i] <= c) {
                t += a[i];
            } else {
                if(a[i] <= c) {
                    t = a[i];
                    cnt++;
                } else {
                    flg = 1;
                    break;
                }
            }
        }
        if(flg || cnt > m) {
            l = c + 1;
        } else {
            r = c - 1;
            ans = c;
        }
    }
    printf("%d", ans);
    return 0;
}
```

---

## 정답
2023년 제1회 청소년 IT경시대회 기출문제 프로그래밍 언어(C언어) 언어 부문 정답

1 2 3 4 5  
3 4 1 4 5  

6 7 8 9 10  
5 1 2 1 3  

11 12 13 14 15  
2 3 3 5 3  

16 17 18 19 20  
3 3 1 2 4  

21 22  
2 105  

23 24  
ABDCCDP AGOPRRMMING 8  

25  
119

---

# 2차원 배열/행렬

[출처: 2024년 제3회]

## 17. 다음 프로그램의 실행 결과는 무엇인가? [초, 중, 고]


```c
#include <stdio.h>
int main()
{
    int a[3][3] = {{1, 2, 0}, {1, 0, 2}, {0, 1, 2}};
    int b[3][3] = {{1, -1, 2}, {0, 1, 1}, {2, 0, 1}};
    for(int i=0 ; i<3 ; i++) {
        for(int j=0 ; j<3 ; j++) {
            int c = 0;
            for(int k=0 ; k<3 ; k++) {
                c += a[i][k] * b[k][j];
            }
            printf("%d ", c);
        }
    }
    return 0;
}
```
① -1  ② 1  ③ 3  ④ 5  ⑤ 6

---
