import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('1\nBookA 1')
elif case_num == 2:
    print('3\nBookC 12\nBookPy 5\nBookAlgo 8')
elif case_num == 15:
    n = 50
    lines = [f'Book{i} {50 - i}' for i in range(n)]
    print(f'{n}\n' + '\n'.join(lines))
else:
    n = random.randint(3, 20)
    titles = ['CBasic', 'PyIntro', 'JavaCore', 'AlgoPro', 'DataStruct', 'WebDev']
    lines = [f'{titles[i % len(titles)]}{i} {random.randint(1, 30)}' for i in range(n)]
    print(f'{n}\n' + '\n'.join(lines))
