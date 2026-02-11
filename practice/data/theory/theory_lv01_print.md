# 출력 핵심 이론

## 핵심 개념
- 출력은 프로그램이 화면으로 값을 보여주는 동작입니다.
- 문자열/숫자/변수를 조합해 표현할 수 있습니다.
- 줄바꿈과 구분자 사용이 중요합니다.

## 기본 문법
{lang:python}
```python
name = "Kim"
age = 14
print(name, age)
```

{lang:c}
```c
char name[] = "Kim";
int age = 14;
printf("%s %d\n", name, age);
```

{lang:java}
```java
String name = "Kim";
int age = 14;
System.out.println(name + " " + age);
```

```io
input:
(없음)
output:
Kim 14
```

## 자주 틀리는 포인트
- 따옴표 누락
- 줄바꿈(`\n`) 위치 실수
- 형식 문자열과 값 개수 불일치(C)
