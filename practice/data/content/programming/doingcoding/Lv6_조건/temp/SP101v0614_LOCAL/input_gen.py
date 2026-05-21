import sys

# SP101v0614 | 도형 넓이 계산기
# 입력 도메인: 문자 정수 정수 (공백 구분)
# 케이스 수: 15
# 예외 포함: T/t/R/r 및 정상 범위, 잘못된 길이, 잘못된 도형 조합

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print("T 4 5")   # 예시 1 (정상 삼각형)
elif case_num == 2:
    print("r 3 6")   # 예시 2 (정상 사각형)
elif case_num == 3:
    print("T 0 5")   # 예시 3 (도형 정상, 가로 0)
elif case_num == 4:
    print("Q 4 5")   # 예시 4 (도형 비정상)
elif case_num == 5:
    print("Q 0 5")   # 특수 케이스: 둘 다 비정상 -> 도형 비정상 우선
elif case_num == 6:
    print("t 10 10") # 정상 삼각형 (소문자)
elif case_num == 7:
    print("R 5 5")   # 정상 사각형 (대문자)
elif case_num == 8:
    print("T 5 -3")  # 도형 정상, 세로 음수
elif case_num == 9:
    print("R -1 -1") # 도형 정상, 둘 다 음수
elif case_num == 10:
    print("Z 10 20") # 잘못된 도형
elif case_num == 11:
    print("r 0 0")   # 도형 정상, 둘 다 0
elif case_num == 12:
    print("t -5 10") # 도형 정상, 가로 음수
elif case_num == 13:
    print("A -5 -5") # 둘 다 비정상 -> 도형 비정상 우선
elif case_num == 14:
    print("T 7 3")   # 정상 삼각형 (홀수 계산 버림)
elif case_num == 15:
    print("R 100 100") # 정상 큰 값
