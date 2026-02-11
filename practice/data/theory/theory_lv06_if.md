# 조건문 핵심 이론

## 핵심 개념
- 조건식이 참/거짓인지에 따라 실행 경로를 나눕니다.
- `if` / `else if(elif)` / `else`로 분기합니다.

## 기본 문법
{lang:python}
```python
score = 78
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C")
```

{lang:c}
```c
int score = 78;
if (score >= 90) printf("A\n");
else if (score >= 80) printf("B\n");
else printf("C\n");
```

{lang:java}
```java
int score = 78;
if (score >= 90) System.out.println("A");
else if (score >= 80) System.out.println("B");
else System.out.println("C");
```

```io
input:
78
output:
B
```

## 자주 틀리는 포인트
- 조건 순서(큰 범위부터 검사)
- 중첩 if에서 else가 붙는 위치
- 논리 연산자 우선순위
