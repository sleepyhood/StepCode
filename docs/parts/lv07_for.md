# for

## C
### 리뉴얼 목표
- “푸는 문제”보다 **실행 과정을 이해**하는 문제로 구성
- MCQ 최소화, **Trace(Grid) + 역추적** 중심

### 학습 개념(필수)
- for문의 3요소 흐름: 초기식 → 조건식 → 본문 → 증감식
- 반복 종료 직후 값(조건이 깨진 순간의 i)
- 누적 변수(sum) 패턴
- 반복문 안 조건문(if) 동작
- step/증감식 변화가 반복 횟수에 미치는 영향
- 실행 추적을 표(grid)로 기록

### 문항 구성(권장)
- Trace(Grid) 3~5문항
  - 기본 출력 흐름, 누적(sum), 조건 포함 누적
- 역추적 1~2문항
  - 출력/최종 상태 → 초기값 또는 반복 횟수 추론
- 중간 상태 복원 1문항
  - “3회 반복 직후 i, sum” 등
- Short 1문항
  - 반복 종료 직후 i 값
- MCQ 0~1문항 (찍기 불가한 비교형만)

### 세트별 구성 예시
- `c_lv07_for_b01`: 기본 흐름 + 누적 + 종료값
- `c_lv07_for_b02`: step/증감식 변형 + 중간 상태 복원
- `c_lv07_for_b03`: if 포함 누적 + 분기 경로 추론
- `c_lv07_for_b04`: 입력 포함 + 역추적 강화
- `c_lv07_for_c01`: 역추적 비중 증가 + 복합 조건

### C 파트 문항 목차(상세 초안)
#### c_lv07_for_b01
1. Trace(Grid) 기본 출력 추적. 의도: 초기식/조건식/증감식 흐름 확인. 코드: `for (int i = 0; i < 3; i++) printf("%d\n", i);` 표: 반복 1~3회에 대해 `i, 출력`.
2. Trace(Grid) 누적 합. 의도: 누적 변수 패턴 이해. 코드: `sum=0; for (int i=1; i<=4; i++) sum+=i;` 표: `i, sum`.
3. Short 종료 직후 i. 의도: 종료 조건의 의미 이해. 코드: `for (i=1; i<=3; i++) {}` 정답: `i=4`.
4. Trace(Grid) step 변화. 의도: 증감식이 반복 횟수에 미치는 영향. 코드: `for (int i=0; i<6; i+=2)` 표: `i, 출력`.
5. 역추적(Reverse) 출력 → 반복 횟수. 의도: 출력 패턴에서 횟수 추론. 코드: `for (int i=1; i<=?; i++) printf("%d ", i);` 출력 제시 후 `?` 추론.
6. (선택) MCQ 1개. 의도: 코드 A/B 출력 차이 비교. 찍기 불가하게 설명형 오답 구성.

#### c_lv07_for_b02
1. Trace(Grid) 음수 step. 의도: 감소 반복 이해. 코드: `for (int i=5; i>=1; i-=2)` 표: `i, 출력`.
2. Trace(Grid) 중간 상태 복원. 의도: 3회 반복 직후 값. 코드: `sum=0; for (int i=1; i<=6; i++) sum+=i;` 질문: 3회 직후 `i, sum`.
3. 역추적(Reverse) 초기값 추론. 의도: 출력 패턴으로 시작값 추론. 코드: `for (int i=?; i<=5; i++) printf("%d\n", i);` 출력 제시.
4. Trace(Grid) 조건 포함. 의도: if가 참일 때만 갱신. 코드: `if (i%2==0) sum+=i;` 표: `i, sum`.
5. Short 종료 직후 i. 의도: 조건식의 경계 이해. 코드: `for (i=0; i<5; i++) {}` 정답: `i=5`.
6. (선택) MCQ 1개. 의도: step 방향 오류 결과 비교.

#### c_lv07_for_b03
1. Trace(Grid) 입력 값과 인덱스 구분. 의도: i와 num 차이 이해. 코드: 입력 n개를 읽고 조건 검사. 표: `i, num, count` 또는 `i, num, sum`.
2. Trace(Grid) 조건 누적. 의도: 짝수만 더하기. 코드: `if (num%2==0) sum+=num;` 표: `num, sum`.
3. 역추적(Reverse) 조건 만족 횟수. 의도: if 참 횟수 추론. 출력으로 `count` 제공.
4. 중간 상태 복원. 의도: 특정 반복 직후 `count` 값. 코드: `count++` 위치 확인.
5. Short 종료 직후 i 또는 count. 의도: 루프 종료 시점 이해.

#### c_lv07_for_b04
1. Trace(Grid) 입력 포함 누적. 의도: 입력 위치와 누적 순서 이해. 표: `i, 입력, sum`.
2. Trace(Grid) 0 포함 여부. 의도: 경계값 처리. 코드: `for (i=0; i<=n; i++)` vs `< n`.
3. 역추적(Reverse) 입력/조건 추론. 의도: 최종 sum에서 입력값 또는 범위 추론.
4. Short 종료 직후 i. 의도: 종료 조건과 출력 관계 이해.
5. (선택) MCQ 1개. 의도: 입력을 루프 밖/안 차이 비교.

#### c_lv07_for_c01
1. Trace(Grid) 복합 조건 누적. 의도: 조건 2개 이상 결합. 표: `i, sum`.
2. 역추적(Reverse) 출력 → 초기값/범위 추론. 의도: 복합 조건에서 역추론.
3. 중간 상태 복원. 의도: break/continue 영향 추적.
4. Trace(Grid) 감소 + 조건 결합. 의도: 증감/조건 복합 이해.
5. Short 요약. 의도: 종료 직후 변수 값 또는 조건 참 횟수.


## Python
### Python - Lv7 반복1(for) (py_for)

- ?? ??
  - `py_for_b1` - Python for문 기초 1회차
    - ??: `py_lv07_for_b01.json`
    - ?? ?: 9 (mcq 5, short 2, code 2, grid 0)
    - coreCount: -
    - ?? ??:
      - 1. [mcq] MCQ 1. 1부터 5까지 출력 (level: 기초, concept: -)
      - 2. [mcq] MCQ 2. for와 range 실행 결과 (level: 기초, concept: -)
      - 3. [mcq] MCQ 3. 합 구하기 (level: 기초, concept: -)
      - 4. [mcq] MCQ 4. 거꾸로 출력 (level: 기초, concept: -)
      - 5. [mcq] MCQ 5. 짝수만 더하기 (level: 기초, concept: -)
      - 6. [short] Short 1. range(3)의 출력 (level: 단답형, concept: -)
      - 7. [short] Short 2. 합의 결과 (level: 단답형, concept: -)
      - 8. [code] Code 1. 1부터 n까지 출력하는 for문 (level: 코드 작성, concept: -)
      - 9. [code] Code 2. 구구단 한 단 출력 (level: 코드 작성, concept: -)

  - `py_for_c1` - Python for문 챌린지 1회차
    - ??: `py_lv07_for_c01.json`
    - ?? ?: 9 (mcq 5, short 2, code 2, grid 0)
    - coreCount: -
    - ?? ??:
      - 1. [mcq] MCQ 1. 거꾸로 출력 (홀수만) (level: 챌린지, concept: -)
      - 2. [mcq] MCQ 2. break와 continue 함께 쓰기 (level: 챌린지, concept: -)
      - 3. [mcq] MCQ 3. n개의 입력 중 양수 개수 (level: 챌린지, concept: -)
      - 4. [mcq] MCQ 4. n개의 입력 중 최솟값과 최댓값 (level: 챌린지, concept: -)
      - 5. [mcq] MCQ 5. 홀수만 출력하는 코드 고르기 (level: 챌린지, concept: -)
      - 6. [short] Short 1. range(2, 10, 3)의 출력 (level: 챌린지, concept: -)
      - 7. [short] Short 2. n개의 입력 절댓값 합 (level: 챌린지, concept: -)
      - 8. [code] Code 1. 3의 배수만 더하기 (level: 챌린지, concept: -)
      - 9. [code] Code 2. n부터 1까지 거꾸로 출력 (level: 챌린지, concept: -)

  - `py_lv07_for_b02` - Python for문 기초 2회차
    - ??: `py_lv07_for_b02.json`
    - ?? ?: 9 (mcq 5, short 2, code 2, grid 0)
    - coreCount: -
    - ?? ??:
      - 1. [mcq] MCQ 1. range 방향이 잘못되면? (level: 기초, concept: -)
      - 2. [mcq] MCQ 2. 1부터 n까지(끝 포함) 출력 (level: 기초, concept: -)
      - 3. [mcq] MCQ 3. 첫 번째 7의 배수 찾기 (level: 기초, concept: -)
      - 4. [mcq] MCQ 4. 1부터 n까지 3의 배수 개수 (level: 기초, concept: -)
      - 5. [mcq] MCQ 5. 홀수만 더하기 (level: 기초, concept: -)
      - 6. [short] Short 1. 출력이 없는 경우 (level: 단답형, concept: -)
      - 7. [short] Short 2. step이 -2인 range (level: 단답형, concept: -)
      - 8. [code] Code 1. 1부터 n까지 중 첫 7의 배수 (level: 코드 작성, concept: -)
      - 9. [code] Code 2. a부터 b까지 k의 배수 합 (level: 코드 작성, concept: -)

  - `py_lv07_for_b03` - Python for문 기초 3회차
    - ??: `py_lv07_for_b03.json`
    - ?? ?: 9 (mcq 5, short 2, code 2, grid 0)
    - coreCount: -
    - ?? ??:
      - 1. [mcq] MCQ 1. (함정) 짝수 개수인데 i를 검사하면? (level: 기초, concept: -)
      - 2. [mcq] MCQ 2. n개의 입력 중 짝수의 개수 (정답 코드 고르기) (level: 기초, concept: -)
      - 3. [mcq] MCQ 3. (함정) '홀수의 합'을 range로 바꾸면 왜 틀리나? (level: 기초, concept: -)
      - 4. [mcq] MCQ 4. 최소 수정으로 고치기 (i → num) (level: 기초, concept: -)
      - 5. [mcq] MCQ 5. (개념 구분) 아래 중 range를 바꾸는 게 '맞는 경우'는? (level: 기초, concept: -)
      - 6. [short] Short 1. (실행 추적) i를 검사하면 이렇게 된다 (level: 단답형, concept: -)
      - 7. [short] Short 2. (정상 패턴) num을 검사하면? (level: 단답형, concept: -)
      - 8. [code] Code 1. (한 줄) 짝수 개수 세기 - if 한 줄 작성 (level: 코드 작성, concept: -)
      - 9. [code] Code 2. (한 줄) 홀수 합 구하기 - if 한 줄 작성 (level: 코드 작성, concept: -)

  - `py_lv07_for_b04` - Python for문 기초 4회차
    - ??: `py_lv07_for_b04.json`
    - ?? ?: 9 (mcq 5, short 2, code 2, grid 0)
    - coreCount: -
    - ?? ??:
      - 1. [mcq] MCQ 1. range의 끝값은 포함될까? (level: 기초, concept: -)
      - 2. [mcq] MCQ 2. (함정) i를 검사하면 무엇을 더하나? (level: 기초, concept: -)
      - 3. [mcq] MCQ 3. 개수 vs 합 (음수의 개수) (level: 기초, concept: -)
      - 4. [mcq] MCQ 4. 경계값 0 처리 (양수의 합) (level: 기초, concept: -)
      - 5. [mcq] MCQ 5. (함정) 입력을 루프 밖에서 받으면? (level: 기초, concept: -)
      - 6. [short] Short 1. step 방향이 잘못되면? (level: 단답형, concept: -)
      - 7. [short] Short 2. 0 포함 여부 (0 이상 합) (level: 단답형, concept: -)
      - 8. [code] Code 1. 입력 받는 위치 (num 한 줄) (level: 코드 작성, concept: -)
      - 9. [code] Code 2. 홀수만 더하기 (if 한 줄) (level: 코드 작성, concept: -)

  - `py_lv07_for_comment_a01` - Python for문 주석 훈련 A01 (변수 역할 라벨링)
    - ??: `py_lv07_for_comment_a01.json`
    - ?? ?: 9 (mcq 5, short 2, code 2, grid 0)
    - coreCount: -
    - ?? ??:
      - 1. [mcq] MCQ 1. i의 역할은? (level: 기초, concept: -)
      - 2. [mcq] MCQ 2. num의 역할은? (level: 기초, concept: -)
      - 3. [mcq] MCQ 3. cnt의 주석으로 알맞은 것은? (level: 기초, concept: -)
      - 4. [mcq] MCQ 4. s의 주석으로 알맞은 것은? (level: 기초, concept: -)
      - 5. [mcq] MCQ 5. (디버깅) 틀린 주석 고르기 (level: 기초, concept: -)
      - 6. [short] Short 1. (핵심) 조건은 i일까 num일까? (level: 단답형, concept: -)
      - 7. [short] Short 2. 변수 역할 라벨 (level: 단답형, concept: -)
      - 8. [code] Code 1. 주석 한 줄 작성 (num) (level: 코드 작성, concept: -)
      - 9. [code] Code 2. if 한 줄 + 주석 (짝수 필터) (level: 코드 작성, concept: -)
