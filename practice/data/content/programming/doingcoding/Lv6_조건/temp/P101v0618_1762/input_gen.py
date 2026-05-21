import sys

# P101v0618 | 계산기 만들기
# 입력 도메인: 정수 연산자 정수 (공백 구분)
# 케이스 수: 15
# 예외 케이스: 나누기 0, 잘못된 연산자 명시적 포함

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print("0 + 0")       # 최소 경계
elif case_num == 2:
    print("5 + 3")       # 예시 1
elif case_num == 3:
    print("7 & 2")       # 예시 2 (잘못된 연산자)
elif case_num == 4:
    print("9 / 0")       # 예시 3 (나누기 0)
elif case_num == 5:
    print("10 - 4")      # 정상 뺄셈
elif case_num == 6:
    print("6 * 7")       # 정상 곱셈
elif case_num == 7:
    print("20 / 4")      # 정상 나눗셈
elif case_num == 8:
    print("-5 + 10")     # 음수 포함
elif case_num == 9:
    print("100 * 0")     # 곱하기 0
elif case_num == 10:
    print("8 # 3")       # 잘못된 연산자
elif case_num == 11:
    print("4 @ 5")       # 잘못된 연산자
elif case_num == 12:
    print("0 / 5")       # 0을 나누기
elif case_num == 13:
    print("1234 % 5")    # 잘못된 연산자 (switch에 없음)
elif case_num == 14:
    print("0 / 0")       # 나누기 0 특수 케이스
elif case_num == 15:
    print("1000 * 1000") # 큰 수 정상
