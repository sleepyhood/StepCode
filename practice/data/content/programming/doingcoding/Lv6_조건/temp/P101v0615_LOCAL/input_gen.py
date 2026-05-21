import sys

# P101v0615 | 평일/주말 구분기 (정수형 case 묶기)
# 입력 도메인: 1~7이면 유효 요일, 그 외는 잘못된 입력
# 케이스 수: 15 (유효 요일 7개 + default 처리 8개)

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print(1)        # → 평일 (월)
elif case_num == 2:
    print(3)        # → 평일 (수)  (예시 입력 1)
elif case_num == 3:
    print(5)        # → 평일 (금)
elif case_num == 4:
    print(6)        # → 주말 (토)
elif case_num == 5:
    print(7)        # → 주말 (일)  (예시 입력 2)
elif case_num == 6:
    print(2)        # → 평일 (화)
elif case_num == 7:
    print(4)        # → 평일 (목)
elif case_num == 8:
    print(9)        # → 잘못된 입력  (예시 입력 3)
elif case_num == 9:
    print(0)        # → 잘못된 입력
elif case_num == 10:
    print(-1)       # → 잘못된 입력
elif case_num == 11:
    print(8)        # → 잘못된 입력
elif case_num == 12:
    print(10)       # → 잘못된 입력
elif case_num == 13:
    print(100)      # → 잘못된 입력
elif case_num == 14:
    print(-7)       # → 잘못된 입력
elif case_num == 15:
    print(50)       # → 잘못된 입력
