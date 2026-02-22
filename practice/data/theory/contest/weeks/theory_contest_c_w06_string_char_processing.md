# C 경시대회 W06 - 문자열/문자 처리

## 메타
- week: W06
- slug: string_char_processing
- audience: common, elementary, middle, high

## 학습 목표
- `problem_c_w06.md`와 `problem_c_w06_map.md`를 개념 1~3으로 분해해 푸는 것이 목표입니다.
- 문자열 문제에서 길이/문자코드/순회 규칙을 분리해 추적하는 습관을 만드는 것이 목표입니다.

## 문항-개념 빠른 연결
- 개념 1) 널 문자와 `strlen`: 문자열 길이 판단, `\0`/이스케이프 문자 해석 문항
- 개념 2) 문자 분류와 ASCII 이동: 대소문자 변환, 문자 비교, 빈도 차이 계산 문항
- 개념 3) 문자열 순회/치환: 연속 문자 압축, 함수 역할 판별, 문자열 스캔 로직 문항

## 공통 이론 (COMMON)
<!-- audience:common -->
### 개념 1) 널 문자와 `strlen`
- 개념 정의: C 문자열의 종료 문자(`\0`) 기준으로 길이를 판정하는 개념입니다.
- 판별 규칙: `strlen`은 첫 `\0` 전까지 문자 개수만 센다.
- 판별 규칙: `"...\0..."` 리터럴은 `\0` 뒤 내용이 길이 계산에서 제외된다.
- 판별 규칙: `\n`은 개행 문자 1개로 길이에 포함된다.
- 추적 절차: 문자열 리터럴을 문자 단위로 분해 -> 첫 `\0` 위치 확인 -> 길이 계산 순서로 푼다.
- 오답 포인트: `\0`을 화면 출력 기호처럼 취급하거나 `\n`을 길이 0으로 보면 틀립니다.

| 표기 | 길이 계산 반영 | 확인 포인트 |
| --- | --- | --- |
| 일반 문자(`A`, `b`, `7`) | 1글자 포함 | 문자 1개로 센다 |
| `\n` | 1글자 포함 | 개행도 문자다 |
| `\0` | 종료 지점, 이후 미포함 | 첫 `\0`에서 `strlen` 종료 |
| `"ABC\0XYZ"` | 3 | `XYZ`는 길이 계산 제외 |

![널 문자 경계와 strlen 길이 계산 다이어그램](./data/theory/images/contest_w06_strlen_null_boundary.svg)

예시 (기본):
```c
#include <stdio.h>
#include <string.h>
int main(void) {
    printf("%d", (int)strlen("HELLO"));
    return 0;
}
```
```io
input:
(없음)
output:
5
```

예시 (변형):
```c
#include <stdio.h>
#include <string.h>
int main(void) {
    int a = (int)strlen("ABC\0XYZ");
    int b = (int)strlen("ABC\n");
    printf("%d %d", a, b);
    return 0;
}
```
```io
input:
(없음)
output:
3 4
```

예시 (함정):
```text
"KITPA\0"의 strlen은 5이고, "KITPA\n"의 strlen은 6이다.
```

### 개념 2) 문자 분류와 ASCII 이동
- 개념 정의: 문자 코드를 이용해 대소문자 변환, 문자 비교, 빈도 차이를 계산하는 개념입니다.
- 판별 규칙: 영문 대문자와 소문자 차이는 32(`'a' - 'A'`)다.
- 판별 규칙: 문자 비교(`>`/`<`)는 ASCII 코드 크기 비교다.
- 판별 규칙: 알파벳 빈도 배열은 `cnt[ch - 'a']`처럼 인덱싱한다.
- 추적 절차: 문자 코드 기준 확정 -> 조건 통과 여부 기록 -> 누적 변수 갱신 순으로 푼다.
- 오답 포인트: 문자 자체를 숫자와 섞어 직관적으로 비교하면 누적 결과가 어긋납니다.

| 작업 유형 | 핵심 규칙 | 계산 루틴 |
| --- | --- | --- |
| 대문자 -> 소문자 | `ch += 32` (A~Z 범위) | 범위 확인 후 변환 |
| 소문자 -> 대문자 | `ch -= 32` (a~z 범위) | 범위 확인 후 변환 |
| 문자 비교 | ASCII 코드값 비교 | 조건 참/거짓을 먼저 기록 |
| 빈도 인덱싱 | `idx = ch - 'a'` | `0~25` 범위인지 검산 |

![문자 분류와 ASCII 이동 규칙 다이어그램](./data/theory/images/contest_w06_ascii_classify_shift.svg)

예시 (기본):
```c
#include <stdio.h>
int main(void) {
    char s[] = "AbC";
    for (int i = 0; s[i]; i++) if (s[i] <= 'Z') s[i] += 32;
    printf("%s", s);
    return 0;
}
```
```io
input:
(없음)
output:
abc
```

예시 (변형):
```c
#include <stdio.h>
int main(void) {
    char a[] = "banana";
    int c = 0;
    for (int i = 0; i < 6; i++)
        for (int j = 0; j < 6; j++)
            if (a[i] != a[j]) c++;
    printf("%d", c);
    return 0;
}
```
```io
input:
(없음)
output:
20
```

예시 (함정):
```text
문자 빈도 차이 배열에서 첫 불일치 인덱스가 곧 알파벳 위치다.
예: 인덱스 5 -> 'f'
```

### 개념 3) 문자열 순회/치환
- 개념 정의: 문자열을 앞에서부터 순회하며 특정 규칙으로 치환/압축/판별하는 개념입니다.
- 판별 규칙: 순회 종료 조건은 `str[i] != '\0'`이다.
- 판별 규칙: 연속 중복 제거는 현재 문자와 다음 문자 비교(`str[i] != str[i+1]`)로 구현할 수 있다.
- 판별 규칙: `string.h` 함수 역할을 정확히 구분한다.
- 추적 절차: 입력 문자열 확인 -> 문자 단위 순회 -> 조건 만족 시 출력/저장 갱신 순으로 푼다.
- 오답 포인트: `strcat`을 분리 함수로 오해하는 등 함수 역할을 혼동하면 판별형에서 틀립니다.

| 함수/패턴 | 역할 | 실전 체크 |
| --- | --- | --- |
| `strcpy(dst, src)` | 문자열 복사 | 목적지 버퍼 크기 확인 |
| `strcmp(a, b)` | 사전식 비교 | 반환값 부호(음/0/양) 확인 |
| `strchr(s, ch)` | 문자 첫 위치 탐색 | 포인터 차이로 인덱스 계산 |
| 연속 문자 압축 | `s[i] != s[i+1]`일 때만 저장 | `i`와 `j` 인덱스 분리 기록 |

![문자열 순회와 치환 인덱스 분리 다이어그램](./data/theory/images/contest_w06_string_scan_replace.svg)

빠른 함수 구분:
- `strcpy`: 복사
- `strcmp`: 비교
- `strchr`: 특정 문자 첫 위치
- `strstr`: 부분 문자열 첫 위치
- `strcat`: 뒤에 이어 붙이기

예시 (기본):
```c
#include <stdio.h>
void compact(const char* s, char* t) {
    int i, j;
    for (i = 0, j = 0; s[i] != 0; i++) {
        if (s[i] != s[i+1]) t[j++] = s[i];
    }
    t[j] = 0;
}
int main(void) {
    char a[] = "aaabbccccdeffff", b[20];
    compact(a, b);
    printf("%s", b);
    return 0;
}
```
```io
input:
(없음)
output:
abcdef
```

예시 (변형):
```c
#include <stdio.h>
#include <string.h>
int main(void) {
    char s[] = "abcabc";
    printf("%d", (int)(strchr(s, 'b') - s));
    return 0;
}
```
```io
input:
(없음)
output:
1
```

예시 (함정):
```text
설명 판별: "strcat은 문자열을 분리한다" -> 틀림
(strcat은 문자열 결합 함수)
```

### 실전 풀이 루틴 (W06 공통)
1. 문자열 문제를 길이형/문자코드형/순회치환형으로 먼저 분류한다.
2. 길이형은 `\0` 위치를 먼저 표시하고 `strlen` 결과를 계산한다.
3. 문자코드형은 문자 비교를 숫자 비교로 환산해 누적한다.
4. 순회치환형은 인덱스 `i`와 결과 문자열 인덱스 `j`를 분리해 기록한다.
5. 최종 출력 타입(숫자/문자열)과 공백까지 검산한다.

### 공통 미니 체크 (필수 제출)
문항:
1. `strlen("AB\0CD")`의 결과를 쓰세요.
2. 대문자를 소문자로 바꿀 때 더하는 ASCII 차이를 쓰세요.
3. `strcat`과 `strtok`의 역할 차이를 한 줄로 쓰세요.

답안 작성:
1. 정답: [ ] / 근거: [ ]
2. 정답: [ ] / 근거: [ ]
3. 정답: [ ] / 근거: [ ]

## 초등 트랙 (ELEMENTARY)
<!-- audience:elementary -->
### 초등 포인트
- 함수 역할과 `strlen` 규칙을 빠르게 판별해 기본 점수를 확보합니다.

### 초등 연계 실습
실습 목표:
- 문자열 함수 설명의 참/거짓을 구분합니다.

실습 문제:
```c
#include <stdio.h>
#include <string.h>
int main(void) {
    char a[20] = "abc";
    strcat(a, "de");
    printf("%s", a);
    return 0;
}
```

체크포인트:
1. `strcat`이 결합 함수임을 설명했는가?
2. 결과 문자열 길이를 `strlen`으로 검산했는가?

## 중등 트랙 (MIDDLE)
<!-- audience:middle -->
### 중등 포인트
- 문자 비교 누적과 문자열 순회 치환을 같은 표에서 추적합니다.

### 중등 연계 실습
실습 목표:
- 이중 반복 비교에서 불일치 개수를 계산합니다.

실습 문제:
```c
#include <stdio.h>
int main(void) {
    char a[] = "abc";
    char b[] = "bcd";
    int c = 0;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            if (a[i] != b[j]) c++;
    printf("%d", c);
    return 0;
}
```

체크포인트:
1. 각 `(i,j)` 비교 결과를 표로 기록했는가?
2. `c` 증가 횟수를 합산해 검산했는가?

## 고등 트랙 (HIGH)
<!-- audience:high -->
### 고등 포인트
- 문자열 빈도 차이 배열을 사용해 첫 불일치 인덱스를 찾는 절차를 고정합니다.

### 고등 연계 실습
실습 목표:
- 두 문자열의 문자 빈도 차이를 인덱스로 추적합니다.

실습 문제:
```c
#include <stdio.h>
int cnt[26];
int main(void) {
    char s1[] = "kitpaa";
    char s2[] = "afogai";
    for (int i = 0; s1[i]; i++) cnt[s1[i]-'a']++;
    for (int i = 0; s2[i]; i++) cnt[s2[i]-'a']--;
    for (int i = 0; i < 26; i++) {
        if (cnt[i]) { printf("%d", i); break; }
    }
    return 0;
}
```

체크포인트:
1. 증가/감소 루프를 분리해 기록했는가?
2. 첫 불일치 인덱스가 무엇을 의미하는지 설명했는가?
