import sys
import random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print("1 1")
elif case_num == 2:
    print("8 48")
elif case_num == 3:
    print("8 8")
else:
    n = random.randint(1, 8)
    s_min = n         # all 1s
    s_max = min(6 * n, 48)
    s = random.randint(s_min, s_max)
    print(f"{n} {s}")
