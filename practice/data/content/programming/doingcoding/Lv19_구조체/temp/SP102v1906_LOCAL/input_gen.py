import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('1\nA 1')
elif case_num == 2:
    print('3\nYuna 3\nAnna 2\nDora 1')
elif case_num == 15:
    n = 50
    names = [f'Z{i:02d}' for i in range(n, 0, -1)]
    lines = [f'{names[i-1]} {i % 4 + 1}' for i in range(n, 0, -1)]
    print(f'{n}\n' + '\n'.join(lines))
else:
    n = random.randint(3, 20)
    names = ['Yuna', 'Anna', 'Dora', 'Bella', 'Carl', 'Zack', 'Evan', 'Fiona']
    lines = [f'{names[i % len(names)]}{i} {random.randint(1, 4)}' for i in range(n)]
    print(f'{n}\n' + '\n'.join(lines))
