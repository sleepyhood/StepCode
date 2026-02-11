# 입력 핵심 이론

## 핵심 개념
- 입력은 사용자에게 값을 받아 변수에 저장하는 과정입니다.
- 받은 값은 보통 문자열이므로 필요하면 숫자로 변환해야 합니다.

## 기본 문법
{lang:python}
```python
n = int(input())
print(n + 1)
```

{lang:c}
```c
int n;
scanf("%d", &n);
printf("%d\n", n + 1);
```

{lang:java}
```java
Scanner sc = new Scanner(System.in);
int n = sc.nextInt();
System.out.println(n + 1);
```

```io
input:
7
output:
8
```

## 자주 틀리는 포인트
- Python에서 `int()` 변환 누락
- C에서 `&` 누락
- Java에서 입력 메서드 타입 불일치
