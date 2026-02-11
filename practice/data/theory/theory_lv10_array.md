# 배열 핵심 이론

## 핵심 개념
- 배열은 같은 타입의 값을 순서대로 저장합니다.
- 인덱스는 보통 0부터 시작합니다.

## 기본 문법
{lang:python}
```python
arr = [10, 20, 30]
print(arr[0])
```

{lang:c}
```c
int arr[3] = {10, 20, 30};
printf("%d\n", arr[0]);
```

{lang:java}
```java
int[] arr = {10, 20, 30};
System.out.println(arr[0]);
```

```io
input:
(없음)
output:
10
```

## 자주 틀리는 포인트
- 범위 밖 인덱스 접근
- 길이(length)와 마지막 인덱스 혼동
- 누적/탐색에서 초기값 실수
