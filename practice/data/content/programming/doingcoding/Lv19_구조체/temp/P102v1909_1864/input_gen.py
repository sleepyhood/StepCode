import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('1\nA 10\nA')
elif case_num == 2:
    print('3\nAmy 18\nBen 22\nCara 20\nBen')
elif case_num == 3:
    print('3\nAmy 18\nBen 22\nCara 20\nNotFound')
elif case_num == 15:
    n = 50
    lines = [f'User{i} {20 + (i % 10)}' for i in range(n)]
    print(f'{n}\n' + '\n'.join(lines) + '\nUser49')
else:
    n = random.randint(4, 20)
    names = ['Amy', 'Ben', 'Cara', 'Dan', 'Eve', 'Fay', 'Gil', 'Hal']
    lines = [f'{names[i % len(names)]}{i}' for i in range(n)]
    lines_str = [f'{lines[i]} {random.randint(18, 30)}' for i in range(n)]
    target = lines[random.randint(0, n - 1)] if case_num % 2 == 0 else 'Unknown'
    print(f'{n}\n' + '\n'.join(lines_str) + f'\n{target}')
