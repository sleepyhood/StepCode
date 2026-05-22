import sys
import random
import string

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print("a")
elif case_num == 2:
    print("apple")
elif case_num == 15:
    print("z" * 100)
else:
    length = random.randint(1, 100)
    print(''.join(random.choice(string.ascii_lowercase) for _ in range(length)))
