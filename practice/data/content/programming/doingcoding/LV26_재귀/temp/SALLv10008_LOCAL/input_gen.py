import sys
import random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print("1 1")
elif case_num == 2:
    print("15 15")
elif case_num == 3:
    print("15 1")
else:
    n = random.randint(1, 15)
    k = random.randint(1, n)
    print(f"{n} {k}")
