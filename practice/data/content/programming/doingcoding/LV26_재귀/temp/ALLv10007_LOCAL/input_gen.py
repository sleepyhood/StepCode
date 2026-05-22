import sys
import random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print(1)
elif case_num == 15:
    print(30)
elif case_num <= 10:
    print(case_num * 3)
else:
    print(random.randint(1, 30))
