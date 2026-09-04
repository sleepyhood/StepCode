import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case == 1:
    print("1 3 5 7 9\n10")
elif case == 2:
    print("1 2 3 4 5\n10")
elif case == 3:
    print("6 8 10 12 14\n2")
elif case == 15:
    print("-100 -50 0 50 100\n-2")
else:
    vals = [random.randint(-100, 100) for _ in range(5)]
    k = random.randint(-10, 10)
    print(" ".join(map(str, vals)) + "\n" + str(k))
