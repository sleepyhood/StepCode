import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('A 1')
elif case_num == 2:
    print('Ethan 14')
elif case_num == 3:
    print('David 25')
elif case_num == 15:
    print('Maximilian 99')
else:
    names = ['Oliver', 'Sophia', 'Lucas', 'Ava', 'Mason', 'Isabella', 'Logan']
    print(f"{names[case_num % len(names)]} {random.randint(1, 99)}")
