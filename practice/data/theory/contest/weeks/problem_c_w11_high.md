# C Contest Week 11 High Problem Set

## 범위
- Week 11 core source pool mapping
- 분반: 고등
- W11 개념 1~3 적용

## 문제 1
연계 개념: 개념 1) 행/열 인덱스와 경계
다음 코드의 실행 결과로 올바른 것을 고르시오.

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

## 문제 2
연계 개념: 개념 1) 행/열 인덱스와 경계, 개념 2) 인접 방향 벡터, 개념 3) 방문 체크와 중복 탐색 방지
다음 코드의 실행 결과를 작성하시오.

<입력>
```text
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

## 문제 3
연계 개념: 개념 1) 행/열 인덱스와 경계, 개념 2) 인접 방향 벡터, 개념 3) 방문 체크와 중복 탐색 방지
다음 코드의 실행 결과로 올바른 것을 고르시오.

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

## 문제 4
연계 개념: 개념 1) 행/열 인덱스와 경계
다음 코드의 실행 결과를 작성하시오.

<입력>
```text
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

## 문제 5
연계 개념: 개념 1) 행/열 인덱스와 경계
다음 코드의 실행 결과로 올바른 것을 고르시오.

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
