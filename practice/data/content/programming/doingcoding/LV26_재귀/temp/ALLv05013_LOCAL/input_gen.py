import sys
import random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print(1)
elif case_num == 2:
    print(1000000)
elif case_num == 3:
    print(8)
else:
    print(random.randint(1, 1000000))
