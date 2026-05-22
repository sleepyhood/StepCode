import sys
import random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print("1 1")
elif case_num == 2:
    print("10000 10000")
elif case_num == 3:
    print("1 10000")
elif case_num == 4:
    print("3 7")
else:
    n = random.randint(1, 10000)
    m = random.randint(1, 10000)
    print(f"{n} {m}")
