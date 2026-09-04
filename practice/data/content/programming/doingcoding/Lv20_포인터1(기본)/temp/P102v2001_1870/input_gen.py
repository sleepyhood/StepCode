import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case == 1:
    print("0 0")
elif case == 2:
    print("10 5")
elif case == 3:
    print("7 -3")
elif case == 15:
    print("-1000 1000")
else:
    print(f"{random.randint(-1000, 1000)} {random.randint(-1000, 1000)}")
