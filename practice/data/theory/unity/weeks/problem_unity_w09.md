# Unity 주차 문제지 W09

## 주차 주제
- 유닛: U09 Animator
- 핵심 개념: 상태 배치, 상태 전환 T/F, 파라미터 타입별 Set 함수, `SetBool`, reset 전환 파라미터 선택

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] 점프 상태 클립 배치
- 출처: 원문 15번
- 유형: 단답
- 문제:
  - 점프 상태 배치 정답을 순서대로 쓰세요.
  - Z1(정점), Z2(왼쪽 낙하), Z3(오른쪽 낙하), Z4(오른쪽 착지)
  - 답안 형식 예: `Z1 JumpApex, Z2 SlowFall, Z3 FastFall, Z4 FastLand`

### [P02] Animator 상태 시스템 전환 T/F
- 출처: 원문 31번
- 유형: 단답
- 문제:
  - 아래 4문장의 참/거짓을 순서대로 쓰세요.
  - 1. Entry 전환으로 시작 상태를 제어할 수 있다.
  - 2. 기본 상태를 포함하거나 제외하고 상태 시스템을 생성할 수 있다.
  - 3. 하위 상태 머신은 별도의 상태 시스템처럼 동작한다.
  - 4. 상태에서 상태 시스템으로는 전환할 수 없다.

### [P03] Set 함수 매칭
- 출처: 원문 32번
- 유형: 단답
- 문제:
  - 아래 빈칸에 들어갈 함수명을 쓰세요.
  - ① `(\"Animation\", 1)`
  - ② `(\"Animation\", .5f)`
  - ③ `(\"Animation\", false)`
  - ④ `(\"Animation\")`
  - 답안 형식 예: `① SetInt, ② SetFloat, ③ SetBool, ④ SetTrigger`

### [P04] `SetBool` 코드 완성
- 출처: 원문 33번
- 유형: 단답
- 문제:
  - `Animator` 변수로 `\"Attacking\"`을 `false`로 설정하기 위한 정답 2개를 쓰세요.
  - ① 호출 주체
  - ② 인수 형태
  - 답안 형식 예: `① animator, ② ("Attacking", false);`

### [P05] reset 전환 파라미터 선택
- 출처: 원문 35번
- 유형: 단답
- 문제:
  - 문장 빈칸 정답 2개를 쓰세요.
  - "트리거 [①] 및 Bool을 [②] false로 설정하십시오."

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - 이동 속도 파라미터 갱신 코드
- 출처 개념: U09 Animator
- 유형: 코드
- 문제:
  - `Animator animator`가 있을 때, float 파라미터 `\"Speed\"`를 `playerSpeed` 변수값으로 갱신하는 1줄 코드를 작성하세요.
- 의도: 타입-함수 매칭을 실제 코드로 전이

### [X02] 함정 - Trigger 호출 문법 선택
- 출처 개념: U09 Animator
- 유형: 객관식
- 문제:
  - Trigger 파라미터 `Search`를 발동하는 올바른 코드를 고르세요.
- 보기:
  - A. `animator.SetBool("Search", true);`
  - B. `animator.SetTrigger("Search");`
  - C. `animator.SetInt("Search", 1);`
  - D. `animator.SetFloat("Search", 1f);`
- 의도: 파라미터 타입과 API 오용 방지

## 주차 체크
- 원문 대응 문항 수: 5
- 확장 문항 수: 2
- 총 문항 수: 7
