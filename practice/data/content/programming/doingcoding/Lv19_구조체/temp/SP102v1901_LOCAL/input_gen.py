import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('A 1\nB 2')
elif case_num == 2:
    print('Alice 25\nBob 22')
elif case_num == 3:
    print('Same1 20\nSame2 20')
elif case_num == 15:
    print('Zoe 100\nAdam 1')
else:
    names1 = ['Alice', 'Clara', 'Emma', 'Grace', 'Ivy']
    names2 = ['Bob', 'David', 'Frank', 'Henry', 'Jack']
    print(f"{names1[case_num % len(names1)]} {random.randint(10, 50)}\n{names2[case_num % len(names2)]} {random.randint(10, 50)}")
