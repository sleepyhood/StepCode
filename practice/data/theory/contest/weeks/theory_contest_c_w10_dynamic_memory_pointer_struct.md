# C 경시대회 W10 - 동적메모리/포인터/구조체

## 메타
- week: W10
- slug: dynamic_memory_pointer_struct
- audience: common, elementary, middle, high

## 학습 목표
- `problem_c_w10.md`와 `problem_c_w10_map.md`를 포인터/동적 메모리/구조체 관점으로 해석하는 것이 목표입니다.
- API 암기형 풀이가 아니라 메모리 상태 변화와 필드 갱신 흐름으로 검산하는 것이 목표입니다.

## 문항-개념 빠른 연결
- 개념 1) 포인터 역참조와 주소 전달: `int *link[]`, `link[c][i]`, DFS 인접리스트 접근
- 개념 2) 동적 메모리 생명주기: `malloc/calloc/realloc/free` 역할, 크기 재할당 시 상태 변화
- 개념 3) 구조체 필드 접근: `front/rear` 인덱스 갱신과 문자열 출력 범위 추적

## 공통 이론 (COMMON)
<!-- audience:common -->
### 개념 1) 포인터 역참조와 주소 전달
- 개념 정의: 포인터 배열과 역참조를 통해 실제 데이터에 접근하는 규칙을 추적하는 개념입니다.
- 판별 규칙: `link[c][i]`는 `*(link[c] + i)`와 동일한 접근이다.
- 판별 규칙: 주소를 전달하면 함수 내부에서 같은 메모리 영역을 직접 바꾼다.
- 추적 절차: 포인터가 가리키는 대상 확인 -> 인덱스 접근 해석 -> 읽기/쓰기 값 기록 순으로 푼다.
- 오답 포인트: "포인터 변수 값"과 "포인터가 가리키는 값"을 혼동하면 DFS/그래프 문항에서 오답이 납니다.

| 표현 | 의미 | 확인 포인트 |
| --- | --- | --- |
| `p` | 주소값 자체 | 어느 배열/변수를 가리키는지 확인 |
| `*p` | `p`가 가리키는 실제 값 | 읽기/쓰기 대상 값인지 확인 |
| `p[i]` | `*(p+i)` | 인덱스 기준 접근과 동일 |
| `link[c][i]` | `*(*(link+c)+i)` | 2단계 역참조 순서를 유지 |

![포인터 주소와 역참조 접근을 추적하는 흐름도](./data/theory/images/contest_w10_pointer_deref_flow.svg)

예시 (기본):
```c
#include <stdio.h>
int main(void){
    int a[3] = {10,20,30};
    int *p = a;
    printf("%d %d", p[0], *(p+2));
    return 0;
}
```
```io
input:
(없음)
output:
10 30
```

예시 (변형):
```c
#include <stdio.h>
void add_one(int *x){ *x += 1; }
int main(void){
    int v = 7;
    add_one(&v);
    printf("%d", v);
    return 0;
}
```
```io
input:
(없음)
output:
8
```

예시 (함정):
```text
int *p 와 *p 는 다르다.
p는 주소, *p는 그 주소의 실제 값이다.
```

### 개념 2) 동적 메모리 생명주기
- 개념 정의: 동적 할당 영역을 생성/초기화/확장/해제하는 흐름을 관리하는 개념입니다.
- 판별 규칙: `malloc`은 할당만, `calloc`은 할당+0초기화다.
- 판별 규칙: `realloc`은 크기를 바꾸며 기존 내용 일부를 유지할 수 있다.
- 판별 규칙: `free`는 해제 함수이며 할당 함수가 아니다.
- 추적 절차: 할당 시점 -> 사용 시점 -> 재할당 시점 -> 해제 시점 순으로 메모리 상태를 기록한다.
- 오답 포인트: API 이름만 외우고 역할을 섞으면 객관식과 추적형 모두 틀립니다.

| 함수 | 역할 | 상태 변화 체크 |
| --- | --- | --- |
| `malloc(n)` | n바이트 할당 | 초기값 미정 상태 |
| `calloc(k,sz)` | `k*sz` 할당 + 0초기화 | 초기값 0 보장 |
| `realloc(p,n)` | 크기 재조정 | 주소 변경 가능성/기존 값 보존 범위 확인 |
| `free(p)` | 할당 메모리 해제 | 해제 후 재사용 금지 |

![동적 메모리 함수 역할과 생명주기 비교 도식](./data/theory/images/contest_w10_dynamic_memory_lifecycle.svg)

예시 (기본):
```c
#include <stdio.h>
#include <stdlib.h>
int main(void){
    int *p = (int*)calloc(4, sizeof(int));
    printf("%d %d", p[0], p[3]);
    free(p);
    return 0;
}
```
```io
input:
(없음)
output:
0 0
```

예시 (변형):
```c
#include <stdio.h>
#include <stdlib.h>
int main(void){
    int *p = (int*)malloc(sizeof(int)*2);
    p[0]=3; p[1]=5;
    p = (int*)realloc(p, sizeof(int)*3);
    p[2]=7;
    printf("%d", p[0]+p[1]+p[2]);
    free(p);
    return 0;
}
```
```io
input:
(없음)
output:
15
```

예시 (함정):
```text
calloc은 "할당 + 0 초기화"이고,
free는 "해제"라서 할당 함수 선택지에 포함되지 않는다.
```

### 개념 3) 구조체 필드 접근
- 개념 정의: 구조체 멤버를 갱신하면서 자료구조 상태(`front`, `rear`, 배열 구간`)를 추적하는 개념입니다.
- 판별 규칙: `d.front`, `d.rear`는 현재 유효 구간의 양 끝 인덱스다.
- 판별 규칙: `--front`, `++rear` 같은 전위 갱신은 저장 전에 인덱스를 바꾼다.
- 판별 규칙: 출력 구간 `for(i=front; i<=rear; i++)`가 최종 문자열을 결정한다.
- 추적 절차: 초기 위치 설정 -> 입력마다 front/rear 변화 기록 -> 최종 구간 출력 순으로 푼다.
- 오답 포인트: front/rear 갱신 시점을 반대로 보면 문자열 순서가 뒤집힙니다.

| 연산 형태 | 인덱스 변화 시점 | 저장/출력 영향 |
| --- | --- | --- |
| `q[--front] = v` | 먼저 감소 후 저장 | 왼쪽 칸에 저장 |
| `q[front--] = v` | 저장 후 감소 | 현재 칸 저장 후 이동 |
| `q[++rear] = v` | 먼저 증가 후 저장 | 오른쪽 새 칸에 저장 |
| `for(i=front; i<=rear; i++)` | 갱신 완료 후 순회 | 최종 문자열 구간 결정 |

![구조체 front rear 갱신과 출력 구간 추적 도식](./data/theory/images/contest_w10_struct_front_rear_trace.svg)

예시 (기본):
```c
#include <stdio.h>
typedef struct { int front, rear; char q[20]; } DS;
int main(void){
    DS d; d.front=d.rear=10; d.q[10]='M';
    d.q[--d.front]='A';
    d.q[++d.rear]='Z';
    for(int i=d.front;i<=d.rear;i++) printf("%c", d.q[i]);
    return 0;
}
```
```io
input:
(없음)
output:
AMZ
```

예시 (변형):
```c
#include <stdio.h>
typedef struct { int f, r; char q[20]; } DS;
int main(void){
    DS d; d.f=d.r=5; d.q[5]='C';
    d.q[++d.r]='D';
    d.q[++d.r]='E';
    for(int i=d.f;i<=d.r;i++) printf("%c", d.q[i]);
    return 0;
}
```
```io
input:
(없음)
output:
CDE
```

예시 (함정):
```text
d.q[--front] 와 d.q[front--] 는 저장 위치가 다르다.
문항 코드의 전위/후위를 그대로 따라야 한다.
```

### 실전 풀이 루틴 (W10 공통)
1. 코드에서 포인터/구조체/할당 API를 먼저 표시한다.
2. 포인터가 가리키는 실제 데이터와 인덱스를 표로 추적한다.
3. `malloc/calloc/realloc/free`의 역할을 문제 조건과 대조한다.
4. 구조체 필드(`front/rear`) 갱신 시점을 한 줄씩 기록한다.
5. 마지막 출력 구간 또는 누적값을 계산해 정답을 검산한다.

### 공통 미니 체크 (필수 제출)
문항:
1. `malloc`과 `calloc`의 차이를 1문장으로 쓰세요.
2. `link[c][i]`가 의미하는 접근을 포인터 식으로 쓰세요.
3. `--front`와 `front--`의 차이를 쓰세요.

답안 작성:
1. 정답: [ ] / 근거: [ ]
2. 정답: [ ] / 근거: [ ]
3. 정답: [ ] / 근거: [ ]

## 초등 트랙 (ELEMENTARY)
<!-- audience:elementary -->
### 초등 포인트
- 동적 메모리 함수 역할 구분과 구조체 필드 추적을 확실히 합니다.

### 초등 연계 실습
실습 목표:
- `front/rear` 갱신으로 문자열 출력 순서를 계산합니다.

실습 문제:
```c
#include <stdio.h>
typedef struct { int front, rear; char q[20]; } DS;
int main(void){
    DS d; d.front=d.rear=3; d.q[3]='B';
    d.q[--d.front]='A'; d.q[++d.rear]='C';
    for(int i=d.front;i<=d.rear;i++) printf("%c", d.q[i]);
}
```

체크포인트:
1. 각 입력 처리 후 front/rear 값을 기록했는가?
2. 최종 출력 구간을 정확히 썼는가?

## 중등 트랙 (MIDDLE)
<!-- audience:middle -->
### 중등 포인트
- 인접리스트 포인터와 재할당 흐름을 함께 추적합니다.

### 중등 연계 실습
실습 목표:
- `realloc` 후 인덱스 저장값 변화를 점검합니다.

실습 문제:
```c
#include <stdio.h>
#include <stdlib.h>
int main(void){
    int *v = (int*)malloc(sizeof(int));
    v[0] = 4;
    v = (int*)realloc(v, sizeof(int)*3);
    v[1] = 6; v[2] = 8;
    printf("%d", v[0]+v[1]+v[2]);
    free(v);
}
```

체크포인트:
1. 재할당 전후 유효 인덱스를 구분했는가?
2. 저장/읽기 시점의 값을 기록했는가?

## 고등 트랙 (HIGH)
<!-- audience:high -->
### 고등 포인트
- 포인터 기반 그래프 순회에서 방문/리프 조건을 정확히 판별합니다.

### 고등 연계 실습
실습 목표:
- DFS 리프 깊이 합 계산을 포인터 인접리스트로 검산합니다.

실습 문제:
```c
#include <stdio.h>
#include <stdlib.h>
int *g[4], sz[4], vis[4], ans;
void dfs(int c,int d){
    int child=0; vis[c]=1;
    for(int i=0;i<sz[c];i++) if(!vis[g[c][i]]){ dfs(g[c][i], d+1); child++; }
    if(child==0) ans+=d;
}
int main(void){
    for(int i=1;i<=3;i++){ g[i]=(int*)malloc(sizeof(int)); }
    g[1]=(int*)realloc(g[1],sizeof(int)*2); g[1][0]=2; g[1][1]=3; sz[1]=2;
    g[2]=(int*)realloc(g[2],sizeof(int)*1); g[2][0]=1; sz[2]=1;
    g[3]=(int*)realloc(g[3],sizeof(int)*1); g[3][0]=1; sz[3]=1;
    dfs(1,0); printf("%d", ans);
}
```

체크포인트:
1. 리프 판정 조건을 정확히 적었는가?
2. 각 리프의 깊이 누적 과정을 검산했는가?
