# 입력

## Python
### 리뉴얼 목표
1. MCQ를 최소화하고 추적 가능한 문항으로 교체한다.
2. 정답이 단계별 파싱 과정을 요구하도록 구성한다.
3. 입력 파싱과 값 흐름을 강조한다.

### 핵심 개념
1. 한 줄 입력에서 `split()` + `map(int, ...)` 사용.
2. 여러 줄 입력과 읽는 순서.
3. 혼합 타입 입력(문자열 + 정수).
4. 공백 처리: `split()` vs `split(" ")`.
5. 표 작성 형식 예시: `input1=3, input2=5, a=3, b=5, output=8`

### 세트 구성 (상세)
#### py_lv03_input_b01 (기초)
1. Trace: 한 줄 입력, 두 정수 합. 표: input1, input2, a, b, output.
2. Trace: 두 줄 입력, 곱셈. 표: line1, line2, result.
3. Reverse: 출력과 첫 입력이 주어질 때 두 번째 입력 추론.
4. Trace: 세 정수와 식 `a*b+c`. 표: a, b, c, output.
5. Short: 두 토큰 출력 순서 바꾸기.

#### py_lv03_input_b02 (기초)
1. Trace: 여러 공백 입력 + `split()`. 표: input1, input2, 값, output.
2. Trace: 이름 + 나이. 표: name, age, output.
3. Reverse: 출력에서 나이 추론.
4. Trace: 두 줄 혼합 입력. 표: name, x, y, output.
5. Trace: `split(" ")`로 빈 값 발생. 표: value와 길이.

#### py_lv03_input_b03 (기초)
1. Trace: 세 정수 합. 표: a, b, c, output.
2. Trace: 세 토큰 출력 순서 뒤집기.
3. Reverse: 합을 보고 세 번째 입력 추론.
4. Trace: 4줄 입력에서 양수 개수 세기. 표: i, num, count.
5. Trace: 정수 평균(`//`). 표: sum, output.

#### py_lv03_input_c01 (챌린지)
1. Trace: n + 한 줄 리스트, 인덱스 합. 표: i, value, sum.
2. Reverse: 곱 결과로 두 번째 입력 추론.
3. Trace: 이름 + 두 점수, 이름과 합 출력. 표: name, s1, s2, output.
4. Trace: `split(" ")` + 추가 공백, 값 개수 세기.
