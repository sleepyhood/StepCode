import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case == 1:
    print("2\n10 20\n5 1")
elif case == 2:
    print("5\n10 50 30 20 40\n100 1")
elif case == 3:
    print("4\n15 8 23 12\n50 0")
elif case == 15:
    n = 20
    vals = random.sample(range(-1000, 1000), n)
    k = vals.index(max(vals))
    print(f"{n}\n" + " ".join(map(str, vals)) + f"\n-50 {k}")
else:
    n = (case % 15) + 3
    vals = random.sample(range(-500, 500), n)
    x = random.randint(-100, 100)
    k = random.randint(0, n - 1)
    print(f"{n}\n" + " ".join(map(str, vals)) + f"\n{x} {k}")
