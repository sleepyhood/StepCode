# 연산자 핵심 이론

## 핵심 개념
- 산술 연산자: `+ - * / %`
- 비교 연산자: `== != < <= > >=`
- 논리 연산자: and/or/not (또는 &&/||/!)

## 기본 문법
{lang:python}
```python
a, b = 7, 3
print(a + b)
print(a % b)
print(a > b)
```

{lang:c}
```c
int a = 7, b = 3;
printf("%d\n", a + b);
printf("%d\n", a % b);
printf("%d\n", a > b);
```

{lang:java}
```java
int a = 7, b = 3;
System.out.println(a + b);
System.out.println(a % b);
System.out.println(a > b);
```

```io
input:
(없음)
output:
10
1
true/1
```

## 자주 틀리는 포인트
- 정수 나눗셈 결과 착각
- `=`(대입)과 `==`(비교) 혼동
- 논리식 괄호 누락
