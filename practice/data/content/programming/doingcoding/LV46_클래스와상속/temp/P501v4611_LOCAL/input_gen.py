import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
random.seed(461100 + case_num)

animals = ["Dog", "Cat", "Duck"]

if case_num == 1:
    print("Dog\n1")
elif case_num == 2:
    print("Dog\n3")  # 예제 1
elif case_num == 3:
    print("Cat\n2")  # 예제 2
elif case_num == 4:
    print("Duck\n1") # 예제 3
elif case_num == 15:
    print("Duck\n100") # 최대 경계값
else:
    animal = random.choice(animals)
    n = random.randint(1, 50)
    print(f"{animal}\n{n}")
