import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

random.seed(1804 + case_num)

words_sample = [
    "apple", "banana", "cat", "dog", "elephant", "fox", "grape", "house",
    "ice", "jungle", "korea", "lemon", "monkey", "nut", "orange", "piano",
    "queen", "rabbit", "sun", "tiger", "umbrella", "violet", "water", "xylophone",
    "yellow", "zebra"
]

if case_num == 1:
    # 예시 1: 완전 역순
    print("cherry banana apple")
elif case_num == 2:
    # 예시 2: 일부 정렬
    print("apple dog cat")
elif case_num == 3:
    # 예시 3: 3단어 모두 일치 (ALL_SAME)
    print("code code code")
elif case_num == 4:
    # 1글자 단어 3개 역순
    print("c b a")
elif case_num == 5:
    # 1글자 단어 3개 일치 (ALL_SAME)
    print("z z z")
elif case_num == 6:
    # 2단어 일치 + 1단어 상이
    print("banana apple banana")
elif case_num == 7:
    # 접두사 관계 3단어
    print("application apple app")
elif case_num == 8:
    # 이미 정렬된 상태
    print("ant bear cat")
elif case_num == 9:
    # 앞 두 단어 일치
    print("apple apple cat")
elif case_num == 10:
    # 뒤 두 단어 일치
    print("dog banana banana")
elif case_num == 15:
    # 30자 최대 경계값
    w1 = "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    w2 = "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"
    w3 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    print(f"{w1} {w2} {w3}")
else:
    mode = case_num % 4
    if mode == 0:
        # ALL_SAME 랜덤
        w = random.choice(words_sample)
        print(f"{w} {w} {w}")
    elif mode == 1:
        # 3개 서로 다른 랜덤 단어 (임의 순서)
        w1, w2, w3 = random.sample(words_sample, 3)
        print(f"{w1} {w2} {w3}")
    elif mode == 2:
        # 2개 동일, 1개 다른 단어
        w1, w2 = random.sample(words_sample, 2)
        print(f"{w1} {w2} {w1}")
    else:
        # 역순 정렬 랜덤 단어
        triplet = sorted(random.sample(words_sample, 3), reverse=True)
        print(f"{triplet[0]} {triplet[1]} {triplet[2]}")
