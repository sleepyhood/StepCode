import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('1\nA 15')
elif case_num == 2:
    print('3\nAmy 18\nBen 22\nCara 20')
elif case_num == 3:
    print('3\nTom 25\nJerry 30\nSpike 21')
elif case_num == 15:
    n = 50
    lines = [f'Person{i} {15 + (i % 15)}' for i in range(n)]
    print(f'{n}\n' + '\n'.join(lines))
else:
    n = random.randint(4, 25)
    names = ['Amy', 'Ben', 'Cara', 'Dan', 'Eve', 'Fay', 'Gil', 'Hal', 'Ian']
    lines = [f'{names[i % len(names)]}{i} {random.randint(15, 30)}' for i in range(n)]
    print(f'{n}\n' + '\n'.join(lines))
