import sys
import random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print("1 1")
elif case_num == 2:
    print("15 45")
elif case_num == 3:
    print("15 15")
else:
    n = random.randint(1, 15)
    # S must be between n (all 1s) and 3*n (all 3s)
    s = random.randint(n, 3 * n)
    print(f"{n} {s}")
