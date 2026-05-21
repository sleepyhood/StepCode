import sys

# P101v0612 | switch case 배우기
# 입력 도메인: 1, 2, 3 (총 3개, 입력 제약 그대로)
# 케이스 수: 3

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print(1)
elif case_num == 2:
    print(2)
elif case_num == 3:
    print(3)
