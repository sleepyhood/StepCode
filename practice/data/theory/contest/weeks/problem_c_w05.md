# C Contest Week 05 Problem Set

## 주차 주제
- 배열/인덱싱/중첩 반복

## 실전 문제 묶음
- 아래 문항은 출처 원문에서 주차 목표에 맞게 선별한 실제 문제이다.

### C_2023_1회
- 문항: 10, 11, 15, 18

#### 문제 10
10. 다음 코드의 실행 결과로 올바른 것을 고르시오 [고]
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

#### 문제 11
11. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초중고]
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

#### 문제 15
15. 다음 코드의 실행 결과로 올바른 것을 고르시오 [초중고]
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

#### 문제 18
18. 산악회 소속 준용이는 이번에 전국에 있는 산을 바이크를 타며 투어를 하려고 한다. 준용이는 N개의 체크 포인트를 지정하였고, i번째 체크포인트는 H_i의 높이를 가진다.
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

### C_2024_2회
- 문항: 2, 14, 16

#### 문제 2
2. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]
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

#### 문제 14
14. 다음 프로그램의 실행 결과는 무엇인가? [초, 중, 고]
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

#### 문제 16
16. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]
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

### C_2024_3회
- 문항: 2, 15

#### 문제 2
2. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]
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

#### 문제 15
15. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]
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
