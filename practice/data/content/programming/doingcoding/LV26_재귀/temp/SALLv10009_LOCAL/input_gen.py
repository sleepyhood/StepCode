import sys
import random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

def gen_maze(n, m):
    # Always keep (0,0) and (n-1,m-1) as 0
    grid = []
    for r in range(n):
        row = ""
        for c in range(m):
            if (r == 0 and c == 0) or (r == n-1 and c == m-1):
                row += "0"
            else:
                row += str(random.randint(0, 1))
        grid.append(row)
    return grid

if case_num == 1:
    print("1 1")
    print("0")
elif case_num == 2:
    print("10 10")
    grid = gen_maze(10, 10)
    for row in grid:
        print(row)
elif case_num == 3:
    # all zeros 5x5
    print("5 5")
    for _ in range(5):
        print("0" * 5)
else:
    n = random.randint(1, 10)
    m = random.randint(1, 10)
    print(f"{n} {m}")
    grid = gen_maze(n, m)
    for row in grid:
        print(row)
