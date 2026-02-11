# 중첩 for 핵심 이론

## 핵심 개념
- for문 안에 for문을 넣어 2차원 구조를 처리합니다.
- 바깥 루프는 행, 안쪽 루프는 열 역할로 생각하면 쉽습니다.

## 기본 문법
{lang:python}
```python
for i in range(1, 4):
    for j in range(1, 4):
        print(i, j)
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
        System.out.println(i + " " + j);
    }
}
```

```tracegrid
title: 중첩 반복 흐름 (i, j)
lang: python,c,java
columns: 반복, i, j
rows:
1 | 1 | 1
2 | 1 | 2
3 | 1 | 3
4 | 2 | 1
5 | 2 | 2
6 | 2 | 3
```

## 자주 틀리는 포인트
- 안쪽 루프 초기화 위치
- 줄바꿈 위치
- 반복 횟수 계산 실수
