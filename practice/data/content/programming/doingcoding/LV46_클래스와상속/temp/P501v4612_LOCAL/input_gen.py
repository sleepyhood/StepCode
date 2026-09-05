import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
random.seed(461200 + case_num)

if case_num == 1:
    print("0 0 0") # 최소 경계값
elif case_num == 2:
    print("10 3 5") # 예제 1
elif case_num == 3:
    print("0 10 25") # 예제 2
elif case_num == 15:
    print("10000 1000 10000") # 최대 경계값
else:
    s = random.randint(0, 5000)
    k = random.randint(0, 500)
    v = random.randint(0, 5000)
    print(f"{s} {k} {v}")
