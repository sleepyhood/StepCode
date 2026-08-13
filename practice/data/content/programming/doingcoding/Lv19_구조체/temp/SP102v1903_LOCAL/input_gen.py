import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('A 100\nB 100')
elif case_num == 2:
    print('ItemA 5000\nItemB 3000')
elif case_num == 3:
    print('Cheap 10\nExpensive 99990')
elif case_num == 15:
    print('MaxVal 1000000\nMinVal 0')
else:
    print(f"ItemAlpha{case_num} {random.randint(1000, 50000)}\nItemBeta{case_num} {random.randint(1000, 50000)}")
