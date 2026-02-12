# 중첩 for 핵심 이론

## 1) 중첩 for가 하는 일

중첩 for는 for문 안에 또 for문을 넣어 "행과 열" 구조를 반복 처리하는 문법입니다.

- 바깥 루프(`i`)는 보통 행(줄) 단위를 담당합니다.
- 안쪽 루프(`j`)는 보통 열(한 줄 안의 칸) 단위를 담당합니다.
- 조건 단원 이후이므로, 결과만 보지 말고 `i/j` 변화 경로를 추적해야 합니다.

---

## 2) 실행 흐름

중첩 for는 아래 순서로 읽습니다.

1. 바깥 루프 `i` 1회 시작
2. 안쪽 루프 `j`를 처음부터 끝까지 실행
3. 안쪽 루프 종료 후 줄바꿈/후처리
4. 바깥 루프 다음 `i`로 이동

핵심은 "**`i`가 1번 바뀔 때마다 `j`는 처음부터 다시 돈다**"는 점입니다.

---

## 3) 가장 자주 쓰는 패턴

### 패턴 A: 좌표(i, j) 출력

{lang:python}
```python
for i in range(1, 4):
    for j in range(1, 4):
        print("%d %d" % (i, j))
```

{lang:c}
```c
for (int i = 1; i <= 3; i++) {
    for (int j = 1; j <= 3; j++) {
        printf("%d %d\n", i, j);
    }
}
```

{lang:java}
```java
for (int i = 1; i <= 3; i++) {
    for (int j = 1; j <= 3; j++) {
        System.out.printf("%d %d\n", i, j);
    }
}
```

```tracegrid
title: Trace 1. 좌표 출력 흐름
lang: python,c,java
columns: 순서, i, j, 출력
rows:
1 | 1 | 1 | 1 1
2 | 1 | 2 | 1 2
3 | 1 | 3 | 1 3
4 | 2 | 1 | 2 1
5 | 2 | 2 | 2 2
6 | 2 | 3 | 2 3
7 | 3 | 1 | 3 1
8 | 3 | 2 | 3 2
9 | 3 | 3 | 3 3
```

### 패턴 B: 별 삼각형(기본 형태)

{lang:python}
```python
for i in range(1, 4):
    for j in range(1, i + 1):
        print("*", end="")
    print()
```

{lang:c}
```c
for (int i = 1; i <= 3; i++) {
    for (int j = 1; j <= i; j++) {
        printf("*");
    }
    printf("\n");
}
```

{lang:java}
```java
for (int i = 1; i <= 3; i++) {
    for (int j = 1; j <= i; j++) {
        System.out.print("*");
    }
    System.out.println();
}
```

```io
input:
(없음)
output:
*
**
***
```

### 패턴 C: 숫자 삼각형(핵심)

{lang:python}
```python
for i in range(1, 4):
    for j in range(1, i + 1):
        print("%d" % j, end=" ")
    print()
```

{lang:c}
```c
for (int i = 1; i <= 3; i++) {
    for (int j = 1; j <= i; j++) {
        printf("%d ", j);
    }
    printf("\n");
}
```

{lang:java}
```java
for (int i = 1; i <= 3; i++) {
    for (int j = 1; j <= i; j++) {
        System.out.printf("%d ", j);
    }
    System.out.println();
}
```

```io
input:
(없음)
output:
1
1 2
1 2 3
```

아래 표는 **각 출력 직후 상태**를 기록한 것입니다.

```tracegrid
title: Trace 2. 숫자 삼각형 출력 경로
lang: python,c,java
columns: 순서, i, j, 출력 숫자
rows:
1 | 1 | 1 | 1
2 | 2 | 1 | 1
3 | 2 | 2 | 2
4 | 3 | 1 | 1
5 | 3 | 2 | 2
6 | 3 | 3 | 3
```

---

## 4) 분기/반복 추적 포인트 (nfor 단원 핵심)

nfor 단원에서는 "무엇을 출력하는가"보다 "`i/j`가 어떻게 변하는가"를 추적해야 합니다.

- `j`의 범위가 `1..i`인지, `1..n`인지 먼저 확인합니다.
- `j`를 출력하면 열 번호 패턴, `i`를 출력하면 행 번호 패턴이 됩니다.
- 숫자 삼각형은 `i/j` 값의 의미(행/열)를 설명하기 가장 좋습니다.

---

## 5) 자주 틀리는 포인트

1. 안쪽 루프 초기화 위치 실수
   `j`는 바깥 반복마다 다시 시작되어야 합니다.

2. 줄바꿈 위치 실수
   줄바꿈은 보통 안쪽 루프 밖(바깥 루프 안)입니다.

3. 경계값 실수
   `j <= i`와 `j < i`는 출력 개수가 달라집니다.

4. 출력 변수 혼동
   `i`를 찍어야 하는데 `j`를 찍거나, 그 반대를 자주 합니다.

---

## 5-1) 언어별 실전 팁

{lang:python} 같은 줄 출력은 `print(..., end="")` 또는 `end=" "`를 사용합니다.

{lang:c} 줄바꿈은 `printf("\n")` 위치로 제어합니다.

{lang:java} 같은 줄 출력은 `System.out.print/printf`, 줄바꿈은 `System.out.println()`을 사용합니다.

{lang:python,c,java} nfor 문제는 최종 모양만 보지 말고, `i/j` 쌍을 표로 먼저 적어 추적하면 안정적으로 풉니다.

---

## 6) 미니 체크 문제

### Q1

`for i=1..3`, `for j=1..i` 구조에서 총 출력 횟수는 몇 번인가요?  
정답: `6번`

### Q2

중첩 반복에서 `i`가 1번 증가할 때 `j`는 어떻게 되나요?  
정답: `처음 값부터 다시 시작합니다.`

### Q3 (언어별)

{lang:python} Python에서 같은 줄 출력 후 줄바꿈을 막을 때 주로 쓰는 옵션은 무엇인가요?  
정답: ``end=""`` 또는 ``end=" "``

{lang:c} C에서 줄바꿈 없이 출력할 때는 무엇을 넣지 않아야 하나요?  
정답: ``\n``

{lang:java} Java에서 같은 줄 출력에 주로 쓰는 메서드는 무엇인가요?  
정답: ``System.out.print`` 또는 ``System.out.printf``

---
## 7) 다음 학습

- 기본 문제: `py_lv09_nfor_b01`
- 심화 문제: `py_lv09_nfor_c01`
- 다음 개념: `array` (반복으로 여러 값을 저장/처리)


