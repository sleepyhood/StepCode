import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('A 1')
elif case_num == 2:
    print('Brian 16')
elif case_num == 3:
    print('Charlie 22')
elif case_num == 15:
    print('Alexander 100')
else:
    names = ['Daniel', 'Emily', 'Finn', 'Hannah', 'Isaac', 'Julia', 'Kevin']
    print(f"{names[case_num % len(names)]} {random.randint(1, 99)}")
