import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('1\nA 10')
elif case_num == 2:
    print('3\nAnna 24\nBen 30\nCara 28')
elif case_num == 15:
    n = 50
    lines = [f'User{i} {i+10}' for i in range(n)]
    print(f'{n}\n' + '\n'.join(lines))
else:
    n = random.randint(3, 20)
    names = ['Amy', 'Bob', 'Chris', 'Dan', 'Eve', 'Fay', 'Gil', 'Hal', 'Ian', 'Jan', 'Kim', 'Lou']
    lines = [f'{names[i % len(names)]}{i} {random.randint(10, 60)}' for i in range(n)]
    print(f'{n}\n' + '\n'.join(lines))
