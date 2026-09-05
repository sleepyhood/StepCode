import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
random.seed(461700 + case_num)

if case_num == 1:
    print("0") # 경계값 최소 SAFE
elif case_num == 2:
    print("75") # 예제 1
elif case_num == 3:
    print("120") # 예제 2
elif case_num == 4:
    print("-5") # 예제 3
elif case_num == 5:
    print("100") # 경계값 최대 SAFE
elif case_num == 6:
    print("-1") # 경계값 직전 OUT_OF_RANGE
elif case_num == 7:
    print("101") # 경계값 직후 OUT_OF_RANGE
elif case_num == 15:
    print("-100") # 극단 음수
else:
    # 다양한 safe/unsafe 혼합
    if case_num % 2 == 0:
        print(str(random.randint(1, 99)))
    else:
        print(str(random.choice([random.randint(-50, -2), random.randint(102, 200)])))
