# C Contest Week 05 Elementary Problem Set

## 범위
- Week 05 core source pool mapping
- 분반: 초등
- W05 개념 1~3 적용

## 문제 1
연계 개념: 개념 2) 누적합/최댓값 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.

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

## 문제 2
연계 개념: 개념 1) 배열 인덱스 경계
다음 코드의 실행 결과로 올바른 것을 고르시오.

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

## 문제 3
연계 개념: 개념 2) 누적합/최댓값 추적
다음 코드의 실행 결과로 올바른 것을 고르시오.

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

## 문제 4
연계 개념: 개념 1) 배열 인덱스 경계

준용이는 전체 체크포인트 중에 “정점”이 총 몇 개인지 알고 싶어 한다. “정점”이란 첫 번째와 N번째 체크포인트를 제외하고 전과 후의 체크포인트보다 높은 높이를 가진 체크포인트를 말한다. 준용이를 도와 총 몇 개의 “정점”이 있는지 구해봅시다.

첫 번째 줄에 전체 체크포인트의 수 N (1 <= N <= 100)이 주어집니다.  
두 번째 줄에 전체 체크포인트의 높이 H_i (1 <= H_i <= 10,000)가 공백으로 구분되어 주어집니다.

다음은 몇 개의 “정점”이 있는지 출력하는 프로그램의 일부입니다. 빈 칸에 들어갈 코드로 알맞은 것을 고르시오.

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

## 문제 5
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
