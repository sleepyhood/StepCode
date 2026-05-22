import sys
import random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num <= 10:
    print(case_num)
elif case_num == 15:
    print(25)
else:
    print(random.randint(1, 25))
