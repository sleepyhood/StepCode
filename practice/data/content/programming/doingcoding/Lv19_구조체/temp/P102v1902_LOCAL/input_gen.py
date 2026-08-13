import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('A 1\n10')
elif case_num == 2:
    print('Alice 15\n20')
elif case_num == 3:
    print('Bob 30\n50')
elif case_num == 15:
    print('Zoe 100\n1')
else:
    names = ['David', 'Emma', 'Frank', 'Grace', 'Henry', 'Irene', 'Jack']
    print(f"{names[case_num % len(names)]} {random.randint(10, 80)}\n{random.randint(10, 80)}")
