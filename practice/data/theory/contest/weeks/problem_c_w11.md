# C Contest Week 11 Problem Set

## 주차 주제
- 2차원 배열/행렬/격자 탐색

## 실전 문제 묶음
- 아래 문항은 주차 목표에 맞게 선별한 실제 문제이다.

### C_2024_3회
- 문항: 17, 19

#### 문제 17
17. 다음 프로그램의 실행 결과는 무엇인가? [초, 중, 고]
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

#### 문제 19
19. 다음 프로그램에 아래 값을 입력했을 때의 출력 결과는 무엇인가? [초]
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

### C_2024_2회
- 문항: 19, 21

#### 문제 19
19. 다음 프로그램의 실행 결과는 무엇인가? [초]
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

#### 문제 21
21. 다음 프로그램의 입력이 아래와 같을 때 실행 결과는 무엇인가? [중, 고]
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

