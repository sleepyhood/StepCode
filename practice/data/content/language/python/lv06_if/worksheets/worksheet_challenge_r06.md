---
id: "py_lv06_if_challenge_r06"
contentType: "worksheet"
track: "language"
lang: "python"
categoryId: "py_if"
title: "Python 조건문 챌린지 2회차"
round: 6
difficulty: "challenge"
status: "active"
audience: "common"
printDefault: true
---
# Python 조건문 챌린지 2회차

### Q1. MCQ 1. 정책형 분기: 배송비 계산 (예외 우선)

다음 요구사항을 만족하는 코드를 고르세요.

입력: price(정수), is_remote("Y"/"N"), is_vip("Y"/"N")

출력: 배송비(정수)
- VIP(is_vip=="Y")는 항상 배송비 0
- VIP가 아니고, 도서산간(is_remote=="Y")이면 배송비 5000
- VIP가 아니고, 도서산간이 아니며(price>=50000)이면 배송비 0
- 그 외에는 배송비 3000

- **A**: price = int(input()) is_remote = input() is_vip = input()  if is_vip == "Y":     print('%d' % 0) elif is_remote == "Y":     print('%d' % 5000) elif price >= 50000:     print('%d' % 0) else:     print('%d' % 3000)
- **B**: price = int(input()) is_remote = input() is_vip = input()  if price >= 50000:     print('%d' % 0) elif is_remote == "Y":     print('%d' % 5000) elif is_vip == "Y":     print('%d' % 0) else:     print('%d' % 3000)
- **C**: price = int(input()) is_remote = input() is_vip = input()  if is_remote == "Y":     print('%d' % 5000) elif is_vip == "Y":     print('%d' % 0) elif price >= 50000:     print('%d' % 0) else:     print('%d' % 3000)
- **D**: price = int(input()) is_remote = input() is_vip = input()  if is_vip == "Y" or price >= 50000:     print('%d' % 0) elif is_remote == "Y":     print('%d' % 5000) else:     print('%d' % 3000)

---

### Q2. MCQ 2. 정책형 분기: 할인율 + 상한(최대 20%)

다음 요구사항을 만족하는 코드를 고르세요.

입력: grade("G"/"S"/"B"), coupon("Y"/"N"), first("Y"/"N")

출력: 최종 할인율(정수, %) 
- 등급 할인: G=15, S=10, B=5
- coupon이 Y면 +5
- first가 Y면 +5
- 최종 할인율은 최대 20%

- **A**: grade = input() coupon = input() first = input()  rate = 0 if grade == "G":     rate = 15 elif grade == "S":     rate = 10 else:     rate = 5  if coupon == "Y":     rate += 5 if first == "Y":     rate += 5  if rate > 20:     rate = 20 print('%d' % (rate))
- **B**: grade = input() coupon = input() first = input()  rate = 0 if grade == "G":     rate = 15 elif grade == "S":     rate = 10 else:     rate = 5  if rate > 20:     rate = 20 if coupon == "Y":     rate += 5 if first == "Y":     rate += 5  print('%d' % (rate))
- **C**: grade = input() coupon = input() first = input()  rate = 0 if grade == "G":     rate = 15 elif grade == "S":     rate = 10 elif grade == "B":     rate = 5  if coupon == "Y":     rate += 5 if first == "Y":     rate += 5  print('%d' % (rate))
- **D**: grade = input() coupon = input() first = input()  rate = 0 if grade == "G":     rate = 15 elif grade == "S":     rate = 10 else:     rate = 5  if coupon == "Y" or first == "Y":     rate += 5  if rate > 20:     rate = 20 print('%d' % (rate))

---

### Q3. MCQ 3. 버그를 잡는 테스트케이스

아래 코드는 배송비 정책을 구현하려고 했지만 버그가 있습니다.

(정답 기준 정책)
- VIP면 0
- VIP가 아니고 도서산간이면 5000
- VIP가 아니고 도서산간이 아니며 price>=50000이면 0
- 그 외 3000

다음 중 **이 코드의 버그를 확실히 드러내는 입력**을 고르세요.

```c
price = int(input())
is_remote = input()
is_vip = input()

if is_vip == "Y":
    print('%d' % 0)
elif price >= 50000:
    print('%d' % 0)
elif is_remote == "Y":
    print('%d' % 5000)
else:
    print('%d' % 3000)
```

- **A**: price=60000, is_remote=N, is_vip=N
- **B**: price=60000, is_remote=Y, is_vip=N
- **C**: price=40000, is_remote=N, is_vip=Y
- **D**: price=40000, is_remote=N, is_vip=N

---

### Q4. MCQ 4. 무료배송 조건식 고르기

다음 정책에서 배송비가 0이 되는 조건식으로 알맞은 것을 고르세요.

- VIP면 항상 0
- VIP가 아니면, 도서산간이 아니고(price>=50000)일 때만 0

변수: price(정수), is_remote("Y"/"N"), is_vip("Y"/"N")

- **A**: is_vip == "Y" or (is_remote == "N" and price >= 50000)
- **B**: (is_vip == "Y" or is_remote == "N") and price >= 50000
- **C**: is_vip == "Y" and (is_remote == "N" or price >= 50000)
- **D**: is_vip == "Y" or is_remote == "N" or price >= 50000

---

### Q5. MCQ 5. 케이스 누락 방지: 최소 테스트 3개

배송비 정책( VIP / 도서산간 / 5만원 이상 무료 / 그 외 )을 검증하려고 합니다.
아래 보기 중, **모든 분기(모든 출력)**를 최소한으로 확인할 수 있는 테스트 3개 묶음으로 가장 적절한 것은?

(각 테스트는 price, is_remote, is_vip 순서)

- **A**: (50000, N, N), (60000, N, N), (40000, N, N)
- **B**: (40000, N, Y), (60000, Y, N), (50000, N, N)
- **C**: (40000, Y, N), (60000, Y, N), (50000, N, N)
- **D**: (40000, N, Y), (40000, N, N), (40000, Y, N)

---

### Q6. Trace 1. 정책 우선순위 할인

spend, coupon, vip에 따라 할인율이 결정됩니다. 어떤 분기가 선택되는지 표에 채우세요.

입력 케이스 예시:
- case1: spend=120000, coupon=0, vip=1
- case2: spend=120000, coupon=1, vip=0
- case3: spend=90000, coupon=1, vip=0

```c
spend, coupon, vip = map(int, input().split())
if vip == 1:
    print('%d' % 30)
elif spend >= 100000 and coupon == 1:
    print('%d' % 20)
elif spend >= 100000:
    print('%d' % 10)
else:
    print('%d' % 0)
```

---

### Q7. Short 1. 경계값: VIP가 아니고 도서산간이 아닐 때 무료배송 최소 금액

정책이 다음과 같을 때,
- VIP가 아니고(is_vip="N")
- 도서산간이 아니며(is_remote="N")
무료배송(배송비 0)이 되기 위한 price의 최소값을 쓰세요.

---

### Q8. Short 2. 출력 예측: 예외 케이스(도서산간)

아래 정책(배송비 계산)에서 입력이
price=60000, is_remote=Y, is_vip=N 일 때 출력되는 배송비를 쓰세요.

---

### Q9. Code 1. 무료배송 조건식 한 줄

다음 정책에서 배송비가 0이 되는 조건식을 if 뒤에 한 줄로 작성하세요.

- VIP면 항상 0
- VIP가 아니면, 도서산간이 아니고(price>=50000)일 때만 0

변수: price, is_remote("Y"/"N"), is_vip("Y"/"N")

```c
if  # 여기에 조건식을 작성하세요:
    print('%d' % 0)
else:
    print('%d' % (1)  # (여기는 의미 없음))
```

---

### Q10. Code 2. 쿠폰 적용 가능 조건식 (등급/금액/예외)

쿠폰 사용 가능 조건은 다음과 같습니다.

- VIP(is_vip=="Y")면 언제나 쿠폰 사용 가능
- VIP가 아니면, price가 30000 이상이고 grade가 "G" 또는 "S"일 때만 쿠폰 사용 가능

변수: price(정수), grade("G"/"S"/"B"), is_vip("Y"/"N")
if 뒤의 조건식을 한 줄로 작성하세요.

```c
if  # 여기에 조건식을 작성하세요:
    print('%s' % 'COUPON')
else:
    print('%s' % 'NO')
```

---
