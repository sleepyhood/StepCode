# C Contest Week 09 Problem Set

## 주차 주제
- 분할정복 출력/함수 반복 적용

## 실전 문제 묶음
- 아래 문항은 주차 목표에 맞게 선별한 실제 문제이다.

### C_2024_2회
- 문항: 9, 18

#### 문제 9
9. 다음 프로그램에서 4번째로 출력되는 수는 무엇인가? [중, 고]
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

#### 문제 18
18. 다음 프로그램의 실행 결과는 무엇인가? [고]
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

### C_2024_3회
- 문항: 10

#### 문제 10
10. 다음 프로그램에서 3번째로 출력되는 수는 무엇인가? [초]
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

