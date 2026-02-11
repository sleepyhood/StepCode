# 변수 핵심 이론

## 핵심 개념
- 변수는 값을 저장하는 이름입니다.
- 같은 변수에 새 값을 넣으면 이전 값은 덮어씁니다.
- 변수 이름은 의미 있게 짓는 것이 좋습니다.

## 기본 문법
{lang:python}
```python
x = 10
x = x + 3
print(x)
```

{lang:c}
```c
int x = 10;
x = x + 3;
printf("%d\n", x);
```

{lang:java}
```java
int x = 10;
x = x + 3;
System.out.println(x);
```

```io
input:
(없음)
output:
13
```

## 자주 틀리는 포인트
- 선언/초기화 순서 혼동(C/Java)
- 문자열과 숫자 타입 혼동
- 변수명 재사용으로 의미가 흐려지는 경우
