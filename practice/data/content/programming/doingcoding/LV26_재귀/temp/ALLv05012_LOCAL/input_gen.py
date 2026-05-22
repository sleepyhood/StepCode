import sys
import random
import string

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print("a")
elif case_num == 2:
    print("z" * 100)
elif case_num == 3:
    print("HelloWorld")
else:
    length = random.randint(1, 100)
    res = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    print(res)
