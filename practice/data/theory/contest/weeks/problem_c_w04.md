# C Contest Week 04 Problem Set

## 주차 주제
- 반복문 기초(for/while), 흐름 제어

## 실전 문제 묶음
- 아래 문항은 출처 원문에서 주차 목표에 맞게 선별한 실제 문제이다.

### C_2024_2회
- 문항: 1, 3, 6, 17

#### 문제 1
1. 다음 프로그램의 실행 결과는 무엇인가? [초, 중]
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

#### 문제 3
3. 다음 프로그램의 실행 결과는 무엇인가? [고]
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

#### 문제 6
6. 다음 프로그램의 실행 결과는 무엇인가? [중, 고]
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

#### 문제 17
17. 다음 프로그램의 실행 결과는 무엇인가? [초, 중]
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

### C_2024_3회
- 문항: 1, 3, 16

#### 문제 1
1. 다음 프로그램의 실행 결과는 무엇인가? [고]
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

#### 문제 3
3. 다음 프로그램의 실행 결과는 무엇인가? [초, 중]
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

#### 문제 16
16. 다음 프로그램의 실행 결과는 무엇인가? [초, 중]
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
