import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('A 10\nB 20')
elif case_num == 2:
    print('BookA 320\nBookB 150')
elif case_num == 3:
    print('BookEqual 200\nBookEqual2 200')
elif case_num == 15:
    print('Heavy 999\nLight 1')
else:
    print(f"BookX{case_num} {random.randint(100, 500)}\nBookY{case_num} {random.randint(100, 500)}")
