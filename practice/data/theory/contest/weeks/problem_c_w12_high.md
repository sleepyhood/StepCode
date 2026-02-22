# C Contest Week 12 High Problem Set

## 범위
- Week 12 core source pool mapping
- 분반: 고등
- W12 개념 1~3 적용

## 문제 1
연계 개념: 개념 1) 복합 조건 분해, 개념 2) 추적표 기반 검산
다음 코드의 실행 결과로 올바른 것을 고르시오.

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

## 문제 2
연계 개념: 개념 1) 복합 조건 분해, 개념 2) 추적표 기반 검산, 개념 3) 시간 안배와 선택 전략
다음 코드의 실행 결과를 작성하시오.

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

## 문제 3
연계 개념: 개념 1) 복합 조건 분해, 개념 2) 추적표 기반 검산
다음 코드의 실행 결과로 올바른 것을 고르시오.

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

## 문제 4
연계 개념: 개념 1) 복합 조건 분해, 개념 2) 추적표 기반 검산, 개념 3) 시간 안배와 선택 전략
다음 코드의 실행 결과를 작성하시오.

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

## 문제 5
연계 개념: 개념 1) 복합 조건 분해, 개념 2) 추적표 기반 검산
다음 코드의 실행 결과로 올바른 것을 고르시오.

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
