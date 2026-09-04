import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case == 1:
    print("1\n42")
elif case == 2:
    print("5\n10 20 30 40 50")
elif case == 3:
    print("3\n7 14 21")
elif case == 15:
    n = 20
    vals = [random.randint(-1000, 1000) for _ in range(n)]
    print(f"{n}\n" + " ".join(map(str, vals)))
else:
    n = (case % 18) + 2
    vals = [random.randint(-1000, 1000) for _ in range(n)]
    print(f"{n}\n" + " ".join(map(str, vals)))
