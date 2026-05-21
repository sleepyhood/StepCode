import sys

# P101v0617 | 달력 문제
# 입력 도메인: 정수 하나 (1~12 유효, 그 외는 잘못된 입력)
# 케이스 수: 15 (정상 12개월 + 잘못된 입력 3개)

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print(3)    # 예시 1
elif case_num == 2:
    print(2)    # 예시 2
elif case_num == 3:
    print(13)   # 예시 3
elif case_num == 4:
    print(1)
elif case_num == 5:
    print(4)
elif case_num == 6:
    print(5)
elif case_num == 7:
    print(6)
elif case_num == 8:
    print(7)
elif case_num == 9:
    print(8)
elif case_num == 10:
    print(9)
elif case_num == 11:
    print(10)
elif case_num == 12:
    print(11)
elif case_num == 13:
    print(12)
elif case_num == 14:
    print(0)
elif case_num == 15:
    print(-5)
