import sys

# P101v0613 | switch case break 배우기 (fall-through 관찰)
# 입력 도메인: 1, 2, 3 (총 3개, 입력 제약 그대로)
# 케이스 수: 3
# 핵심: 입력 1이면 3줄 모두, 입력 2이면 2줄, 입력 3이면 1줄 출력

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if case_num == 1:
    print(1)   # → "1입니다\n2입니다\n3입니다"
elif case_num == 2:
    print(2)   # → "2입니다\n3입니다"
elif case_num == 3:
    print(3)   # → "3입니다"
