import sys

# P101v0614 | 식당 키오스크 (default 도입)
# 입력 도메인: 정수 하나 (1, 2, 3은 유효 메뉴, 그 외는 default)
# 케이스 수: 10 (유효 메뉴 3개 + default 처리 7개)

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print(1)        # → 비빔밥
elif case_num == 2:
    print(2)        # → 불고기  (예시 입력 1)
elif case_num == 3:
    print(3)        # → 냉면
elif case_num == 4:
    print(5)        # → 준비중인 메뉴입니다  (예시 입력 2)
elif case_num == 5:
    print(0)        # → 준비중인 메뉴입니다
elif case_num == 6:
    print(4)        # → 준비중인 메뉴입니다
elif case_num == 7:
    print(-1)       # → 준비중인 메뉴입니다
elif case_num == 8:
    print(10)       # → 준비중인 메뉴입니다
elif case_num == 9:
    print(100)      # → 준비중인 메뉴입니다
elif case_num == 10:
    print(999)      # → 준비중인 메뉴입니다
