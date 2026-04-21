---
id: "py_lv10_array_basic_r03"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_array"
title: "Python 배열 Lv10 기초 3회차"
round: 3
difficulty: "basic"
status: "active"
audience: "common"
printDefault: true
---
# Python 배열 Lv10 기초 3회차

### Q1. Trace 1. 탐색 상태 추적

코드를 실행하며 표를 채우세요. 각 반복에서 i, lst[i], idx 변화를 적으세요.

```c
lst = [4, 7, 2, 7]
target = 7
idx = -1
for i in range(len(lst)):
    if lst[i] == target:
        idx = i
        break
print(idx)
```

---

### Q2. Code 1. 첫 등장 찾기

target을 처음 찾았을 때 idx를 저장하고 즉시 종료하는 코드를 작성하세요.

```c
idx = -1
for i in range(len(lst)):
    # TODO: target을 찾으면 idx를 저장하고 종료
```

---

### Q3. Short 1. 첫 등장 인덱스

lst=[2,5,2,5]에서 값 5의 첫 등장 인덱스를 쓰세요.

```c
lst = [2, 5, 2, 5]
```

---

### Q4. Code 2. 역순 for 범위

인덱스를 n-1부터 0까지 감소시키는 for문 한 줄을 작성하세요.

```c
n = len(lst)
# TODO: i를 n-1부터 0까지 감소
```

---

### Q5. Code 3. 마지막 등장 인덱스 갱신

target을 찾을 때마다 last 인덱스를 갱신하는 한 줄을 작성하세요.

```c
last = -1
for i in range(len(lst)):
    # TODO: target이면 last 갱신
```

---

### Q6. Short 2. 등장 횟수 세기

lst=[2,5,2,5,5]에서 값 5의 등장 횟수를 쓰세요.

```c
lst = [2, 5, 2, 5, 5]
```

---

### Q7. Reverse 1. 마지막 등장 위치 추론

last 인덱스 출력이 4이고 lst=[2,5,2,5,5]입니다. target 값을 쓰세요.

```c
# last index of target is 4
```

---

### Q8. Code 4. 반복 범위 완성

i가 1부터 len(lst)-1까지 순회하도록 빈칸을 채우세요.

```c
mx = lst[0]
# TODO: 빈칸을 채워 전체 원소를 비교
for i in ____:
    if lst[i] > mx:
        mx = lst[i]
```

---

### Q9. MCQ 1. break 역할

선형 탐색에서 아래 위치에 `break`를 두는 이유로 가장 알맞은 것을 고르세요.

```c
if lst[i] == target:
    idx = i
    break
```

- **A**: 찾은 뒤에도 끝까지 계속 검사하려고
- **B**: 첫 등장 위치를 찾으면 즉시 종료하려고
- **C**: idx를 항상 -1로 유지하려고
- **D**: 반복 횟수를 1 늘리려고

---
