import sys

# SP101v0612 | 계절 구분기
# 입력 도메인: 1~12 (정상), 그 외 (default)
# 케이스 수: 15 (정상 12 + 예외 3)

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print(4)    # 예시 1 (봄)
elif case_num == 2:
    print(12)   # 예시 2 (겨울)
elif case_num == 3:
    print(13)   # 예시 3 (예외)
elif case_num == 4:
    print(1)
elif case_num == 5:
    print(2)
elif case_num == 6:
    print(3)
elif case_num == 7:
    print(5)
elif case_num == 8:
    print(6)
elif case_num == 9:
    print(7)
elif case_num == 10:
    print(8)
elif case_num == 11:
    print(9)
elif case_num == 12:
    print(10)
elif case_num == 13:
    print(11)
elif case_num == 14:
    print(0)
elif case_num == 15:
    print(-10)
