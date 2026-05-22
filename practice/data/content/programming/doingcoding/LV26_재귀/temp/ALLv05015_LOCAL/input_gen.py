import sys
import random
import string

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

def gen_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

def gen_palindrome(length):
    half = gen_random_string(length // 2)
    if length % 2 == 0:
        return half + half[::-1]
    else:
        return half + random.choice(string.ascii_uppercase) + half[::-1]

if case_num == 1:
    # Small test cases
    print(3)
    print("AAA")
    print("ABC")
    print("ABA")
elif case_num == 2:
    # Max T and max length
    print(1000)
    for _ in range(1000):
        print(gen_random_string(1000))
elif case_num == 3:
    # Palindromes
    print(10)
    for i in range(1, 11):
        print(gen_palindrome(100))
else:
    t = random.randint(1, 100)
    print(t)
    for _ in range(t):
        if random.random() < 0.3:
            print(gen_palindrome(random.randint(1, 1000)))
        else:
            print(gen_random_string(random.randint(1, 1000)))
