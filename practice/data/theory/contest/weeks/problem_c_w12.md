# C Contest Week 12 Problem Set

## 주차 주제
- 종합 모의 + 해설 + 피드백

## 실전 문제 묶음
- 아래 문항은 주차 목표에 맞게 선별한 실제 문제이다.

### C_2023_1회
- 문항: 20, 25

#### 문제 20
20. 아래 코드의 입력이 다음과 같을 때 실행 결과로 올바른 것을 고르시오 [중고]
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

#### 문제 25
25. 아래 프로그램에 <입력1>과 <입력2>를 입력했을 때 출력되는 값의 합을 작성하시오 [중고]
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

## 주차 메모
- 12주차는 `C_2023_1회` 20, 25번을 기반으로 하고, 1~11주 핵심 문항 재구성 세트를 함께 운영한다.

