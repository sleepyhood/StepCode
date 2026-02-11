# 자료형 변환 핵심 이론

## 핵심 개념
- 타입이 다르면 연산/출력 결과가 달라집니다.
- 명시적 변환(cast)으로 원하는 타입을 맞춥니다.

## 기본 문법
{lang:python}
```python
s = "12"
n = int(s)
print(n + 3)
```

{lang:c}
```c
int a = 7, b = 2;
double x = (double)a / b;
printf("%.1f\n", x);
```

{lang:java}
```java
String s = "12";
int n = Integer.parseInt(s);
System.out.println(n + 3);
```

```io
input:
(없음)
output:
15
```

## 자주 틀리는 포인트
- 문자열 덧셈 vs 숫자 덧셈
- 정수/실수 나눗셈 차이
- 변환 실패 예외 처리 누락
