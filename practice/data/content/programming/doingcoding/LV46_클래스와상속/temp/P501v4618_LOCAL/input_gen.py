import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
random.seed(461800 + case_num)

if case_num == 1:
    print("0 3 0") # 0원
elif case_num == 2:
    print("50000 1 12000") # 예제 1
elif case_num == 3:
    print("80000 2 15") # 예제 2
elif case_num == 4:
    print("30000 1 50000") # 예제 3 (초과 할인 -> 0원)
elif case_num == 5:
    print("25000 3 0") # 예제 4 (할인 없음)
elif case_num == 6:
    print("100000 2 100") # 100% 할인
elif case_num == 7:
    print("100000 2 0") # 0% 정률
elif case_num == 15:
    print("1000000 1 500000") # 최대 금액
else:
    price = random.randint(10000, 300000)
    t = random.choice([1, 2, 3])
    if t == 1:
        param = random.randint(1000, price + 5000)
    elif t == 2:
        param = random.randint(1, 50)
    else:
        param = 0
    print(f"{price} {t} {param}")
