import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case == 1:
    print("0 0\n1")
elif case == 2:
    print("10 20\n1")
elif case == 3:
    print("100 500\n2")
elif case == 15:
    print("-1000 1000\n1")
else:
    op = 1 if case % 2 == 0 else 2
    print(f"{random.randint(-1000, 1000)} {random.randint(-1000, 1000)}\n{op}")
