---
id: "py_lv10_array_basic_r01"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_array"
title: "Python 배열 Lv10 기초 1회차"
round: 1
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python 배열 Lv10 기초 1회차

### Q1. Trace 1. 인덱스-값-출력 추적

코드를 실행해 표를 채우세요. 각 반복이 끝난 직후의 i, lst[i], output을 적으세요.

표 예:
| i | lst[i] | output |
| --- | --- | --- |
| 0 | 10 | 10 |

```c
lst = [10, 20, 30, 40]
for i in range(len(lst)):
    print('%d' % lst[i])
```

---

### Q2. Code 1. 입력을 리스트로 저장

정수 n을 입력받은 뒤, 다음 줄의 정수들을 리스트 lst로 저장하는 한 줄을 작성하세요.

```c
n = int(input())
# TODO: 다음 줄의 정수들을 lst에 저장하세요.
```

---

### Q3. Short 1. 마지막 인덱스

리스트 길이가 n일 때 마지막 인덱스 값을 쓰세요.

```c
n = 8
```

---

### Q4. Code 2. 마지막 3개 역순 출력

lst의 마지막 3개 원소를 역순으로 출력하는 한 줄을 작성하세요.

```c
lst = list(map(int, input().split()))
n = len(lst)
# TODO: 마지막 3개를 역순으로 출력하세요.
```

---

### Q5. Short 2. 짝수 인덱스 합

코드의 실행 결과를 쓰세요.

```c
lst = [5, 1, 4, 2, 7]
s = 0
for i in range(0, len(lst), 2):
    s += lst[i]
print('%d' % s)
```

---

### Q6. Code 3. 마지막 원소 출력

리스트의 마지막 원소를 출력하는 한 줄을 작성하세요.

```c
lst = [4, 8, 15, 16, 23, 42]
n = len(lst)
# TODO: 마지막 원소 출력
```

---

### Q7. 보충 1. 마지막 값 추론

보충 문제입니다. 출력이 42가 되도록 x 값을 채우세요.

```c
lst = [4, 8, 15, 16, 23, x]
print(lst[-1])
```

---

### Q8. Code 4. range 범위 수정

배열 인덱스 오류가 나지 않도록 BUG 한 줄을 수정하세요.

```c
lst = [3, 6, 9, 12]
# BUG
for i in range(len(lst) + 1):
    print('%d' % lst[i])
```

---

### Q9. MCQ 1. 경계값 선택

리스트의 모든 원소를 정확히 한 번씩 출력하려면 `range( ??? )`에 무엇이 들어가야 하는지 고르세요.

```c
for i in range( ??? ):
    print(lst[i])
```

- **A**: len(lst) + 1
- **B**: len(lst)
- **C**: len(lst) - 1
- **D**: 1, len(lst)

---
