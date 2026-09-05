import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
random.seed(461500 + case_num)

animals = ["Duck", "Penguin", "Sparrow"]
actions = ["swim", "fly"]

if case_num == 1:
    print("Duck\nswim 1")
elif case_num == 2:
    print("Duck\nswim 50") # 예제 1
elif case_num == 3:
    print("Penguin\nfly 20") # 예제 2 (cannot fly)
elif case_num == 4:
    print("Duck\nfly 100") # 예제 3
elif case_num == 5:
    print("Sparrow\nswim 10") # cannot swim
elif case_num == 15:
    print("Duck\nfly 10000") # 최대 거리
else:
    animal = random.choice(animals)
    action = random.choice(actions)
    d = random.randint(10, 5000)
    print(f"{animal}\n{action} {d}")
