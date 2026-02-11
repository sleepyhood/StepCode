# while문 핵심 이론

## 핵심 개념
- 반복 횟수가 명확하지 않을 때 while을 사용합니다.
- 조건이 참인 동안 반복합니다.
- 반복문 안에서 상태(변수)가 반드시 변해야 종료됩니다.

## 기본 문법
{lang:python}
```python
i = 1
while i <= 3:
    print(i)
    i += 1
```

{lang:c}
```c
int i = 1;
while (i <= 3) {
    printf("%d\n", i);
    i++;
}
```

{lang:java}
```java
int i = 1;
while (i <= 3) {
    System.out.println(i);
    i++;
}
```

```io
input:
(없음)
output:
1
2
3
```

## 자주 틀리는 포인트
- 증감 누락으로 무한 루프
- 조건 경계값(`<=`, `<`) 실수
- 입력 갱신 위치 실수(센티넬 패턴)
