import sys

# P101v0616 | 알파벳 신호등
# 입력 도메인: 단일 문자 (R/r, G/g, Y/y 및 그 외)
# 케이스 수: 15 (정상 6개 + 잘못된 신호 9개)
# 주의: 출력 후 자동 개행(\n) 포함

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print('R')
elif case_num == 2:
    print('g')  # 예시 2
elif case_num == 3:
    print('B')  # 예시 3
elif case_num == 4:
    print('r')
elif case_num == 5:
    print('G')
elif case_num == 6:
    print('Y')
elif case_num == 7:
    print('y')
elif case_num == 8:
    print('Z')
elif case_num == 9:
    print('a')
elif case_num == 10:
    print('1')
elif case_num == 11:
    print('!')
elif case_num == 12:
    print('x')
elif case_num == 13:
    print('P')
elif case_num == 14:
    print('?')
elif case_num == 15:
    print(' ')
