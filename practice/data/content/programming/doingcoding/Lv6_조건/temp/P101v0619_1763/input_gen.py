import sys

# P101v0619 | 성적표
# 입력 도메인: 0~100 정수
# 케이스 수: 15
# 예외/경계 케이스 명시적 포함 (100, 90, 89, 80, 79, 70, 69, 0)

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print(0)     # F (최소 경계)
elif case_num == 2:
    print(85)    # B (예시 1)
elif case_num == 3:
    print(63)    # F (예시 2)
elif case_num == 4:
    print(100)   # A (몫 10 경계)
elif case_num == 5:
    print(90)    # A (경계)
elif case_num == 6:
    print(89)    # B (경계)
elif case_num == 7:
    print(80)    # B (경계)
elif case_num == 8:
    print(79)    # C (경계)
elif case_num == 9:
    print(70)    # C (경계)
elif case_num == 10:
    print(69)    # F (경계)
elif case_num == 11:
    print(95)    # A
elif case_num == 12:
    print(75)    # C
elif case_num == 13:
    print(50)    # F
elif case_num == 14:
    print(99)    # A (경계)
elif case_num == 15:
    print(10)    # F
