import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
random.seed(461300 + case_num)

if case_num == 1:
    print("1\n1 1") # 최소 사각형
elif case_num == 2:
    print("1\n5 8") # 예제 1
elif case_num == 3:
    print("2\n10") # 예제 2
elif case_num == 4:
    print("2\n1") # 최소 원
elif case_num == 15:
    print("1\n1000 1000") # 최대 사각형
else:
    t = 1 if case_num % 2 == 0 else 2
    if t == 1:
        w = random.randint(1, 500)
        h = random.randint(1, 500)
        print(f"1\n{w} {h}")
    else:
        r = random.randint(1, 500)
        print(f"2\n{r}")
