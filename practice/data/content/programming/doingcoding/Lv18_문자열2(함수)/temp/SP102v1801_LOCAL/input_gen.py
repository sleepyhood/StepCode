import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

random.seed(1801 + case_num)

letters = "abcdefghijklmnopqrstuvwxyz"

if case_num == 1:
    print("a 1")
    print("apple")
elif case_num == 2:
    print("apple 3")
    print("element")
    print("tiger")
    print("rabbit")
elif case_num == 3:
    print("korea 3")
    print("banana")
    print("apple")
    print("element")
elif case_num == 15:
    words = []
    curr_char = 'a'
    S = "a" + "".join(random.choice(letters) for _ in range(18)) + curr_char
    for _ in range(10):
        next_char = random.choice(letters)
        word = curr_char + "".join(random.choice(letters) for _ in range(18)) + next_char
        words.append(word)
        curr_char = next_char
    print(f"{S} 10")
    for w in words:
        print(w)
else:
    N = random.randint(2, 9)
    S = "".join(random.choice(letters) for _ in range(random.randint(3, 10)))
    print(f"{S} {N}")
    curr = S
    for i in range(N):
        if random.random() < 0.7:
            first = curr[-1]
            word = first + "".join(random.choice(letters) for _ in range(random.randint(2, 10)))
            curr = curr + word
        else:
            word = "".join(random.choice(letters) for _ in range(random.randint(3, 10)))
        print(word)
