import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
random.seed(461400 + case_num)

devices = ["TV", "AirConditioner", "Computer"]

if case_num == 1:
    print("1\nTV 1")
elif case_num == 2:
    print("3\nTV 3\nAirConditioner 2\nComputer 4") # 예제 1
elif case_num == 3:
    print("2\nComputer 8\nTV 5") # 예제 2
elif case_num == 15:
    lines = ["15"]
    for _ in range(15):
        lines.append(f"{random.choice(devices)} 100")
    print("\n".join(lines))
else:
    n = random.randint(2, 10)
    lines = [str(n)]
    for _ in range(n):
        d = random.choice(devices)
        h = random.randint(1, 24)
        lines.append(f"{d} {h}")
    print("\n".join(lines))
