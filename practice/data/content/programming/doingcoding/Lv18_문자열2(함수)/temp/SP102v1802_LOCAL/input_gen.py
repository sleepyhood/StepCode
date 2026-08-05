import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

random.seed(1802 + case_num)

letters = "abcdefghijklmnopqrstuvwxyz"

if case_num == 1:
    print(1)
    print("hello")
elif case_num == 2:
    print(4)
    print("banana")
    print("apple")
    print("dog")
    print("cat")
elif case_num == 3:
    print(3)
    print("korea")
    print("japan")
    print("china")
elif case_num == 15:
    print(20)
    print("a" * 30)
    for _ in range(18):
        print("".join(random.choice(letters) for _ in range(30)))
    print("z" * 30)
else:
    N = random.randint(3, 18)
    print(N)
    for _ in range(N):
        w_len = random.randint(2, 25)
        print("".join(random.choice(letters) for _ in range(w_len)))
