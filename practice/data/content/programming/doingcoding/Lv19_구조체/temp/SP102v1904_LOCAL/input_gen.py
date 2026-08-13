import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('1\nA 10\n10')
elif case_num == 2:
    print('3\nAmy 15\nBen 19\nCara 17\n17')
elif case_num == 15:
    n = 50
    lines = [f'Student{i} {i+10}' for i in range(n)]
    print(f'{n}\n' + '\n'.join(lines) + '\n5')
else:
    n = random.randint(3, 20)
    names = ['Amy', 'Ben', 'Cara', 'Dan', 'Eve', 'Fay']
    lines = [f'{names[i % len(names)]}{i} {random.randint(10, 25)}' for i in range(n)]
    cut = random.randint(15, 20)
    print(f'{n}\n' + '\n'.join(lines) + f'\n{cut}')
