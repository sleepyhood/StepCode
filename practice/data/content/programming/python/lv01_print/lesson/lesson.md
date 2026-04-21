---
id: "py_lv01_print"
contentType: "lesson"
track: "language"
lang: "python"
categoryId: "py_print"
title: "Python Lv1 출력"
status: "active"
order: 201
audience: "common"
recommendedSetId: "py_print_b1"
relatedSetIds: ["py_print_b1", "py_print_b2", "py_print_b3", "py_print_c1"]
prerequisites: []
nextConcepts: ["py_lv02_var"]
priority: 2
---
# 출력 핵심 이론

## 1) 출력 명령어가 하는 일

출력은 프로그램이 값을 화면에 보여주는 동작입니다.

- lv01에서는 **출력 명령어 자체**만 익힙니다.
- 이 단원에서는 변수와 입력을 사용하지 않습니다.
- 가장 먼저 큰따옴표 안 문자열을 그대로 출력하는 형태를 익힙니다.

---

## 2) 실행 흐름

출력 코드는 아래 순서로 읽습니다.

1. 출력 명령어 확인 (`print`, `printf`, `System.out.print/println/printf`)
2. 큰따옴표 안 내용 확인
3. 줄바꿈(`\n`) 포함 여부 확인
4. 화면에 실제로 보이는 결과 확인

핵심은 "**코드에 쓴 문자와 화면에 보이는 문자를 정확히 대응**"시키는 것입니다.

---

## 3) 가장 자주 쓰는 패턴

### 패턴 A: 큰따옴표 내부 문자열 바로 출력

{lang:python}
```python
print("Hello")
```

{lang:c}
```c
printf("Hello\n");
```

{lang:java}
```java
System.out.println("Hello");
```

```io
input:
(없음)
output:
Hello
```

### 패턴 B: 엔터 기호(`\n`) 출력

{lang:python}
```python
print("A")
print("B")
print("C")
```

{lang:c}
```c
printf("A\nB\nC\n");
```

{lang:java}
```java
System.out.print("A\nB\nC\n");
```

```io
input:
(없음)
output:
A
B
C
```

### 패턴 C: 특수문자 출력 (`"`, `'`, `\\`)

{lang:python}
```python
print("\"")
print("'")
print("\\")
```

{lang:c}
```c
printf("\"\\n");
printf("'\\n");
printf("\\\n");
```

{lang:java}
```java
System.out.println("\"");
System.out.println("'");
System.out.println("\\");
```

```io
input:
(없음)
output:
"
'
\
```

### 패턴 D: 서식문자 출력 (`%d`, `%lf`, `%.2lf`, `%c`, `%s`)

{lang:python}
```python
print("%d %.2f %c %s" % (7, 3.14159, 'A', "Hi"))
```

{lang:c}
```c
printf("%d %lf %.2lf %c %s\n", 7, 3.14159, 3.14159, 'A', "Hi");
```

{lang:java}
```java
System.out.printf("%d %f %.2f %c %s\n", 7, 3.14159, 3.14159, 'A', "Hi");
```

```io
input:
(없음)
output:
7 3.141590 3.14 A Hi
```

### 패턴 E: 서식문자 정렬 (`%2d`, `%8s`)

{lang:python}
```python
print("|%2d|" % 7)
print("|%8s|" % "cat")
```

{lang:c}
```c
printf("|%2d|\n", 7);
printf("|%8s|\n", "cat");
```

{lang:java}
```java
System.out.printf("|%2d|\n", 7);
System.out.printf("|%8s|\n", "cat");
```

```io
input:
(없음)
output:
| 7|
|     cat|
```

---

## 4) 출력 추적 포인트 (print 단원 핵심)

print 단원에서는 "문자 그대로 출력"과 "서식 적용 출력"을 구분해야 합니다.

- 문자열 직접 출력: 큰따옴표 안 내용이 그대로 나옵니다.
- 이스케이프 문자: `\n`, `\"`, `\\`처럼 특별한 의미를 가집니다.
- 서식문자 출력: `%d`, `%s` 등 자리에 값이 들어가며 모양이 바뀝니다.

---

## 5) 자주 틀리는 포인트

1. 따옴표 누락
   문자열은 큰따옴표로 감싸야 합니다.

2. 줄바꿈 위치 실수
   `\n` 위치 하나 차이로 출력 모양이 크게 달라집니다.

3. 특수문자 이스케이프 누락
   `"`, `\\`를 그냥 쓰면 문법 오류나 오출력이 납니다.

4. 서식문자와 값 개수/타입 불일치
   `%d`에 문자열을 넣거나, 개수가 맞지 않으면 오류가 납니다.

5. 정렬 폭 오해
   `%2d`, `%8s`는 출력 폭(칸 수)을 지정하는 형식입니다.

---

## 5-1) 언어별 실전 팁

{lang:python} 기본 출력은 `print("...")`를 사용하고, 서식은 `"%d" % 값` 형태를 사용합니다.

{lang:c} `printf`에서 `\n`과 서식문자(`%d`, `%lf`, `%.2lf`, `%c`, `%s`)를 정확히 맞춥니다.

{lang:java} `System.out.println`은 줄바꿈 포함, `System.out.printf`는 서식 출력에 사용합니다.

{lang:python,c,java} lv01에서는 변수/입력 없이 출력 명령어와 출력 모양 대응만 집중해서 연습합니다.

---

## 6) 미니 체크 문제

### Q1

출력 단원(lv01)에서 가장 먼저 익혀야 하는 것은 무엇인가요?  
정답: `큰따옴표 안 문자열을 출력 명령어로 그대로 출력하는 것`

### Q2

문자열 안에서 줄바꿈을 넣으려면 어떤 기호를 사용하나요?  
정답: ``\n``

### Q3 (언어별)

{lang:python} Python에서 `print("%8s" % "cat")`를 출력하면 앞쪽에 공백이 몇 칸 들어가나요?  
정답: `5칸`

{lang:c} C에서 폭 2칸 정수 정렬 출력에 사용하는 서식문자는 무엇인가요?  
정답: ``%2d``

{lang:java} Java에서 서식 정렬 출력에 사용하는 명령어는 무엇인가요?  
정답: ``System.out.printf(...)``

---
## 7) 다음 학습

- 기본 문제: `py_print_b1`
- 심화 문제: `py_print_c1`
- 다음 개념: `var` (출력할 값을 저장하는 방법)
