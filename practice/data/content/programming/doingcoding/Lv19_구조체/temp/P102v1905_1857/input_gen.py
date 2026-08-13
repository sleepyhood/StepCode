import sys, random
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if case_num == 1:
    print('A 1 B 00000')
elif case_num == 2:
    print('Frank 16 Seoul 04500')
elif case_num == 3:
    print('Grace 20 Busan 48900')
elif case_num == 15:
    print('Christopher 100 Incheon 21000')
else:
    cities = ['Daegu', 'Daejeon', 'Gwangju', 'Ulsan', 'Suwon']
    names = ['Liam', 'Maya', 'Nathan', 'Olivia', 'Paul']
    print(f"{names[case_num % len(names)]} {random.randint(1, 99)} {cities[case_num % len(cities)]} {random.randint(10000, 99999):05d}")
