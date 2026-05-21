import sys

# SP101v0613 | 등급 판정기
# 입력 도메인: 단일 문자 (A/a, B/b, C/c 및 그 외)
# 케이스 수: 15 (정상 6 + 잘못된 학점 9)

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print('A')  # 예시 1
elif case_num == 2:
    print('b')  # 예시 2
elif case_num == 3:
    print('Z')  # 예시 3
elif case_num == 4:
    print('a')
elif case_num == 5:
    print('B')
elif case_num == 6:
    print('C')
elif case_num == 7:
    print('c')
elif case_num == 8:
    print('d')
elif case_num == 9:
    print('D')
elif case_num == 10:
    print('F')
elif case_num == 11:
    print('f')
elif case_num == 12:
    print('1')
elif case_num == 13:
    print('!')
elif case_num == 14:
    print(' ')
elif case_num == 15:
    print('x')
