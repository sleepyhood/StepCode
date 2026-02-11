# 2차원 배열 핵심 이론

## 핵심 개념
- 2차원 배열은 행(row)과 열(column)로 값을 저장합니다.
- 중첩 반복문으로 순회합니다.

## 기본 문법
{lang:python}
```python
a = [[1, 2], [3, 4]]
print(a[1][0])
```

{lang:c}
```c
int a[2][2] = {{1,2},{3,4}};
printf("%d\n", a[1][0]);
```

{lang:java}
```java
int[][] a = {{1,2},{3,4}};
System.out.println(a[1][0]);
```

```io
input:
(없음)
output:
3
```

```tracegrid
title: 2x2 순회 순서
lang: python,c,java
columns: 순서, r, c, 값
rows:
1 | 0 | 0 | 1
2 | 0 | 1 | 2
3 | 1 | 0 | 3
4 | 1 | 1 | 4
```

## 자주 틀리는 포인트
- 행/열 길이 혼동
- 루프 범위 실수
- 전치/회전 인덱스 계산 실수
