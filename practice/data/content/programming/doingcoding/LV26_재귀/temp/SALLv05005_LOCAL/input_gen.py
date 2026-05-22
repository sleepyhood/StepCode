import sys
import random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num <= 10:
    print(case_num) # Case 0-10
elif case_num == 15:
    print(20)
else:
    print(random.randint(0, 20))
