import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

random.seed(1803 + case_num)

words_sample = [
    "apple", "banana", "cat", "dog", "elephant", "fox", "grape", "house",
    "ice", "jungle", "korea", "lemon", "monkey", "nut", "orange", "piano",
    "queen", "rabbit", "sun", "tiger", "umbrella", "violet", "water", "xylophone",
    "yellow", "zebra", "superman", "developer", "structure", "algorithm",
    "network", "database", "security", "framework", "optimization", "intelligence"
]

if case_num == 1:
    # 예시 1
    print("code 2")
    print("superman")
    print("apple")
elif case_num == 2:
    # 예시 2 (20자 트렁케이션)
    print("code 3")
    print("programming")
    print("python")
    print("javascript")
elif case_num == 3:
    # 예시 3 (N=0 경계값)
    print("stepcode 0")
elif case_num == 4:
    # 1글자 단어 누적
    print("a 5")
    for ch in ["b", "c", "d", "e", "f"]:
        print(ch)
elif case_num == 5:
    # 매번 lenS < lenW (앞 3글자씩만 결합)
    print("hi 4")
    print("elephant")
    print("crocodile")
    print("alligator")
    print("kangaroo")
elif case_num == 6:
    # 정확히 20자에 도달하는 케이스
    # step (4) + code (4) -> 8 + javascript (10) -> 18 + go (2) -> 20
    print("step 3")
    print("code")
    print("javascript")
    print("go")
elif case_num == 7:
    # 시작부터 20자 단어
    w20 = "abcdefghijklmnopqrst"
    print(f"{w20} 2")
    print("hello")
    print("world")
elif case_num == 8:
    # N=1 전체 결합
    print("programming 1")
    print("c")
elif case_num == 9:
    # N=1 3글자 결합
    print("c 1")
    print("programming")
elif case_num == 10:
    # N=10 최대 단어 개수
    print("start 10")
    for w in random.sample(words_sample, 10):
        print(w)
elif case_num == 15:
    # 20자 초기 단어 + 최대 N=10
    w20 = "zzzzzzzzzzzzzzzzzzzz"
    print(f"{w20} 10")
    for _ in range(10):
        print(random.choice(words_sample))
else:
    init_word = random.choice(words_sample)[:random.randint(1, 15)]
    n = random.randint(1, 8)
    print(f"{init_word} {n}")
    for _ in range(n):
        print(random.choice(words_sample))
