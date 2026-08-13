import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('1\nA 100')
elif case_num == 2:
    print('3\nAmy 80\nBen 95\nCara 87')
elif case_num == 3:
    print('3\nTie1 90\nTie2 90\nOther 80')
elif case_num == 15:
    n = 50
    lines = [f'User{i} {i+10}' for i in range(n)]
    print(f'{n}\n' + '\n'.join(lines))
else:
    n = random.randint(3, 20)
    names = ['Amy', 'Ben', 'Cara', 'Dan', 'Eve', 'Fay', 'Gil']
    lines = [f'{names[i % len(names)]}{i} {random.randint(50, 100)}' for i in range(n)]
    print(f'{n}\n' + '\n'.join(lines))
