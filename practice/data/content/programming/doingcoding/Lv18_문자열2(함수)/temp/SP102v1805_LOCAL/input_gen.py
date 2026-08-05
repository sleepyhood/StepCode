import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

random.seed(1805 + case_num)

letters = "abcdefghijklmnopqrstuvwxyz"

if case_num == 1:
    print("a1")
elif case_num == 2:
    print("a3b2c4")
elif case_num == 3:
    print("x1y4z2")
elif case_num == 15:
    res = []
    for i in range(15):
        res.append(f"{letters[i % 26]}9")
    print("".join(res))
else:
    num_pairs = random.randint(2, 12)
    res = []
    for _ in range(num_pairs):
        ch = random.choice(letters)
        cnt = random.randint(1, 9)
        res.append(f"{ch}{cnt}")
    print("".join(res))
