import sys

# SP101v0611 | 음료수 자판기
# 입력 도메인: 1~3 (정상), 그 외 (default)
# 케이스 수: 10 (정상 3 + default 7)

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print(1)    # 콜라 (예시 1)
elif case_num == 2:
    print(4)    # 예외 (예시 2)
elif case_num == 3:
    print(2)    # 사이다
elif case_num == 4:
    print(3)    # 환타
elif case_num == 5:
    print(0)
elif case_num == 6:
    print(5)
elif case_num == 7:
    print(-1)
elif case_num == 8:
    print(10)
elif case_num == 9:
    print(100)
elif case_num == 10:
    print(999)
