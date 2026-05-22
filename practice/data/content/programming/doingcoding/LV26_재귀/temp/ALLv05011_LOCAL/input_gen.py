import sys
import random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print("0 2")
elif case_num == 2:
    print("10000 9")
elif case_num == 3:
    print("10000 2")
else:
    n = random.randint(0, 10000)
    k = random.randint(2, 9)
    print(f"{n} {k}")
