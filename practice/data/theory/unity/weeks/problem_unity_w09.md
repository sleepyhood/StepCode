# Unity 주차 문제지 W09

## 주차 주제
- 유닛: U09 Animator
- 핵심 개념: 상태 클립 배치, 상태 전환(Transition) 규칙, 파라미터 타입별 Set 함수, SetBool 호출 문법, reset 전환 파라미터

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.

## 원문 대응 문항
### [P01] 점프 상태 클립 배치
- 출처: 원문 15번
- 유형: 단답
- 문제:
  - 유니티 Animator 컨트롤러에서 캐릭터의 점프 동작을 4단계 상태로 나누어 애니메이션 클립을 배치하려고 합니다. 각 위치에는 점프 궤적의 물리적 단계에 맞는 클립이 하나씩 들어가야 합니다.
  - 아래 위치 설명을 읽고, 각 슬롯에 배치될 가장 적절한 클립명을 쓰세요.
  - **Z1 (정점)** — 점프 궤적의 최고 정점(꼭대기): 상승이 끝나고 하강이 시작되는 순간
  - **Z2 (느린 낙하)** — 정점 이후 왼쪽으로 천천히 떨어지는 낙하 구간
  - **Z3 (빠른 낙하)** — 속도가 붙어 오른쪽으로 빠르게 낙하하는 구간
  - **Z4 (착지)** — 지면에 오른쪽으로 빠르게 착지하는 순간
  - 사용 가능한 클립: `JumpApex`, `SlowFall`, `FastFall`, `FastLand`
  - 답안 입력: 각 행의 그리드 입력 양식에 맞추어 작성해 주세요.

### [P02] Animator 상태 시스템 전환 규칙 참/거짓
- 출처: 원문 31번
- 유형: 참거짓
- 문제:
  - 유니티 Animator 컨트롤러의 상태 시스템(State Machine) 구조와 전환(Transition) 규칙에 대한 다음 4가지 설명의 참/거짓을 판별하여 순서대로 쉼표로 구분하여 작성하세요.
  - 문장 1: Entry 노드에서 나가는 전환(Transition)을 설정하면, Animator가 시작될 때 어떤 상태로 진입할지 제어할 수 있다.
  - 문장 2: 상태 시스템(State Machine)은 기본 상태(Default State, 주황색 노드)를 포함하지 않고도 생성할 수 있다.
  - 문장 3: 하위 상태 머신(Sub-State Machine)을 만들면, 해당 그룹은 독립적인 별도의 상태 시스템처럼 동작하므로 복잡한 로직을 깔끔하게 정리할 수 있다.
  - 문장 4: 개별 상태(State) 노드에서 Sub-State Machine 덩어리로는 어떤 전환도 연결할 수 없다.
  - 답안 형식 예: `참, 거짓, 참, 거짓`

### [P03] Animator 파라미터 타입별 Set 함수 매칭
- 출처: 원문 32번
- 유형: 단답
- 문제:
  - 유니티 Animator의 파라미터는 `Int`, `Float`, `Bool`, `Trigger` 4가지 타입이 있으며, 각각 C# 스크립트에서 값을 설정할 때 전용 `Set` 함수를 사용해야 합니다.
  - 아래 호출 형태의 인수(괄호 안 값)를 분석하여, 각 빈칸에 들어갈 정확한 `Set` 함수명을 순서대로 쉼표로 구분하여 작성하세요.
  - ① `animator.[빈칸]("Level", 5)` — 정수형 값 `5`를 전달
  - ② `animator.[빈칸]("Weight", 0.5f)` — 실수형 값 `0.5f`를 전달
  - ③ `animator.[빈칸]("isAlive", false)` — 불리언 값 `false`를 전달
  - ④ `animator.[빈칸]("StartAction")` — 값 없이 발동 신호만 전달
  - 답안 형식 예: `SetInteger, SetFloat, SetBool, SetTrigger`

### [P04] `SetBool` 호출 코드 세부 완성
- 출처: 원문 33번
- 유형: 단답
- problem:
  - 스크립트에 `Animator animator;`로 선언된 멤버 변수가 있습니다. 이 변수를 사용하여 Animator 컨트롤러의 `"Attacking"` 파라미터(Bool 타입)를 `false`로 변경하려고 합니다.
  - 아래의 빈칸 ①, ②에 들어갈 요소를 순서대로 쉼표로 구분하여 작성하세요.
  - `[①].SetBool([②]);`
  - 답안 형식 예: `animator, "Attacking", false`

### [P05] reset 전환용 파라미터 이름 선택
- 출처: 원문 35번
- 유형: 단답
- 문제:
  - Animator 컨트롤러에서 캐릭터가 현재 애니메이션 동작을 중단하고 기본 대기(Idle) 상태로 즉시 되돌아가는 reset 전환을 구현하려 합니다.
  - 아래 문장의 빈칸 ①, ②에 들어갈 파라미터 이름을 사용 가능한 후보 중 골라 순서대로 쉼표로 구분하여 작성하세요.
  - "Trigger 파라미터 [①]을 발동시키고, Bool 파라미터 [②]을 `false`로 전환하면 reset 상태로 돌아갑니다."
  - (사용 가능한 파라미터 후보: `Search`, `Friendly`, `Attack`, `Speed`)
  - 답안 형식 예: `Search, Friendly`

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - 이동 속도 파라미터 실시간 갱신 코드 선택
- 출처 개념: U09 Animator
- 유형: 객관식
- 문제:
  - 플레이어의 이동 속도 변수인 `playerSpeed`(실수형) 값을 Animator 컨트롤러의 Float 타입 파라미터 `"Speed"`에 실시간으로 전달하여 자연스럽게 애니메이션이 전환되도록 하려고 합니다. 다음 중 `Update()` 내부에 작성할 알맞은 한 줄 코드를 고르세요.
- 보기:
  - A. `animator.SetFloat("Speed", playerSpeed);`
  - B. `animator.SetBool("Speed", playerSpeed);`
  - C. `animator.SetFloat(Speed, playerSpeed);`
  - D. `animator.SetInteger("Speed", playerSpeed);`
- 의도: 파라미터 타입(Float)과 전용 API(SetFloat)의 올바른 매칭법을 분별하도록 훈련합니다.

### [X02] 함정 - Trigger 파라미터 발동 API 선택
- 출처 개념: U09 Animator
- 유형: 객관식
- 문제:
  - Animator 컨트롤러에 Trigger 타입으로 정의된 파라미터 `"Search"`가 있습니다. 이 파라미터를 1회성으로 발동하고자 할 때 C# 스크립트에서 사용해야 하는 문법적으로 올바른 코드를 고르세요.
- 보기:
  - A. `animator.SetBool("Search", true);`
  - B. `animator.SetTrigger("Search");`
  - C. `animator.SetInteger("Search", 1);`
  - D. `animator.SetFloat("Search", 1f);`
- 의도: Trigger 파라미터가 1회성 신호(펄스) 방식임을 인지하고, 전용 API인 SetTrigger 사용법을 구별합니다.

## 주차 체크
- 원문 대응 문항 수: 5
- 확장 문항 수: 2
- 총 문항 수: 7
