import sys
import random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

def gen_case(k):
    nums = sorted(random.sample(range(1, 50), k))
    return f"{k} " + " ".join(map(str, nums))

if case_num == 1:
    # minimum k=7
    print("7 1 2 3 4 5 6 7")
    print("0")
elif case_num == 2:
    # max k=12
    print(gen_case(12))
    print("0")
elif case_num == 15:
    # multiple test cases
    for _ in range(3):
        k = random.randint(7, 12)
        print(gen_case(k))
    print("0")
else:
    k = random.randint(7, 12)
    print(gen_case(k))
    print("0")
