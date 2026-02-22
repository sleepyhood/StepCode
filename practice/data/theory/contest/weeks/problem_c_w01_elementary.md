# C Contest Week 01 Elementary Problem Set

## 범위
- 컴파일러 기본 개념
- `limits.h`와 `SHRT_MAX`
- `short` 오버플로우
- 표준 헤더 매칭 기초

## 문제 1
연계 개념: 개념 1) 컴파일러/인터프리터/헤더 기능 판별
다음 중 C 소스 코드를 실행 가능한 형태로 변환하는 프로그램은 무엇인가?
⓵ 가상 머신
⓶ 인터프리터
⓷ 컴파일러
⓸ 바이트코드
⓹ 링커

## 문제 2
연계 개념: 개념 2) `limits.h`와 `SHRT_MAX` 해석
다음 중 `short` 자료형의 최댓값을 나타내는 상수는 무엇인가?
⓵ INT_MAX
⓶ CHAR_MAX
⓷ SHRT_MAX
⓸ LONG_MAX
⓹ DBL_MAX

## 문제 3
연계 개념: 개념 3) `short` 오버플로우와 정수 승격
다음 코드의 실행 결과로 올바른 것을 고르시오.
```c
#include <stdio.h>
int main() {
    short s = 32767;
    s = s + 1;
    printf("%d", s);
    return 0;
}
```
⓵ -32768
⓶ -1
⓷ 1
⓸ 32768
⓹ 오류

## 문제 4
연계 개념: 개념 2) `limits.h`와 `SHRT_MAX` 해석
다음 중 `SHRT_MAX`를 사용하기 위해 포함해야 하는 헤더는 무엇인가?
⓵ stdio.h
⓶ limits.h
⓷ string.h
⓸ stdlib.h
⓹ math.h

## 문제 5
연계 개념: 개념 1) 컴파일러/인터프리터/헤더 기능 판별
다음 중 헤더와 설명의 연결이 올바르지 않은 것을 고르시오.
⓵ stdio.h: 표준 입출력 함수 제공
⓶ time.h: 날짜/시간 관련 기능 제공
⓷ assert.h: 디버깅 검사용 매크로 제공
⓸ stdarg.h: 문자열 길이 계산 함수 제공
⓹ stddef.h: 공통 타입/매크로 제공


