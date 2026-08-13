import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('1\nA 50\n0 10\n0')
elif case_num == 2:
    print('3\nAmy 80\nBen 75\nCara 90\n1 10\n1')
elif case_num == 15:
    n = 50
    lines = [f'Student{i} {60 + (i % 40)}' for i in range(n)]
    print(f'{n}\n' + '\n'.join(lines) + f'\n49 10\n49')
else:
    n = random.randint(4, 20)
    names = ['Amy', 'Ben', 'Cara', 'Dan', 'Eve', 'Fay', 'Gil']
    lines = [f'{names[i % len(names)]}{i} {random.randint(50, 95)}' for i in range(n)]
    k = random.randint(0, n - 1)
    x = random.randint(1, 15)
    m = k if case_num % 2 == 0 else random.randint(0, n - 1)
    print(f'{n}\n' + '\n'.join(lines) + f'\n{k} {x}\n{m}')
