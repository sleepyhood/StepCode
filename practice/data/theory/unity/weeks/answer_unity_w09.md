# Unity 주차 정답지 W09

## 메타
- 대상 문제지: `problem_unity_w09.md`
- 유닛: U09 Animator

## 정답표
| 문항 ID | 정답 | 한 줄 근거 |
|---|---|---|
| P01 | Z1 `JumpApex`, Z2 `SlowFall`, Z3 `FastFall`, Z4 `FastLand` | 점프 궤적의 물리적 단계(정점→느린 낙하→빠른 낙하→착지)에 각각 대응하는 클립명 |
| P02 | 1 참, 2 거짓, 3 참, 4 거짓 | Entry 전환은 가능(참), 기본 상태 제외 불가(거짓), Sub-State Machine은 독립 동작(참), 상태→머신 전환 가능(거짓) |
| P03 | ① `SetInteger` ② `SetFloat` ③ `SetBool` ④ `SetTrigger` | 인수의 리터럴 타입(정수/실수/불리언/값 없음)에 정확히 대응하는 전용 Set 함수 |
| P04 | ① `animator` ② `("Attacking", false)` | 타입명이 아닌 인스턴스 변수명으로 호출하고, 문자열 파라미터명과 bool 값을 정확한 시그니처로 전달 |
| P05 | ① `Search` ② `Friendly` | reset 전환을 위해 Trigger는 `Search`를 발동, Bool은 `Friendly`를 false로 설정 |
| X01 | `animator.SetFloat("Speed", playerSpeed);` | Float 타입 파라미터는 반드시 `SetFloat` API로 실수형 값을 전달 |
| X02 | B | Trigger는 값을 저장하지 않는 1회성 신호이므로 `SetTrigger("Search")`만이 유일한 올바른 호출 |

## 해설
### P01
- 개념 정의: Animator 컨트롤러의 상태 노드에 배치할 애니메이션 클립은 캐릭터의 물리적 동작 궤적(상승 정점, 느린 낙하, 빠른 낙하, 착지)의 각 단계와 의미가 일치해야 자연스러운 전환이 이루어집니다.
- 오답 포인트: `SlowFall`(천천히 떨어짐)과 `FastFall`(빠르게 떨어짐)의 좌/우 배치 위치를 바꿔 쓰거나, `JumpApex`(정점)를 착지 슬롯에 넣는 경우가 잦습니다.
- 판별 기준: 물리적 순서(상승 끝 → 서서히 낙하 → 급속 낙하 → 지면 착지)에 맞게 Z1~Z4에 `JumpApex → SlowFall → FastFall → FastLand` 순으로 정확히 대응시켰는지 확인합니다.

### P02
- 개념 정의: Animator의 State Machine 아키텍처에서 Entry 노드는 시작 상태를 결정하고, Default State(주황색)는 반드시 존재해야 하며, Sub-State Machine은 독립 그룹으로 동작하고, 개별 상태에서 Sub-State Machine으로의 전환도 설정 가능합니다.
- 오답 포인트: "기본 상태 없이도 생성 가능하다"(문장 2)를 참으로, "상태→머신 전환 불가능하다"(문장 4)를 참으로 착각하는 경향이 있습니다. 실제로 기본 상태는 필수이며 상태→머신 전환도 가능합니다.
- 판별 기준: 각 문장의 핵심 키워드(Entry 전환, Default State 필수 여부, Sub-State Machine 독립성, 전환 방향성)를 유니티 공식 문서 기준으로 교차 검증합니다.

### P03
- 개념 정의: Animator의 4가지 파라미터 타입(`Int`, `Float`, `Bool`, `Trigger`)은 각각 전용 Set API가 있으며, 인수로 전달되는 **리터럴 값의 C# 자료형**을 보면 어떤 함수를 써야 하는지 즉시 판별됩니다.
- 오답 포인트: Trigger 파라미터에 값이 없는 것을 보고 `SetBool`로 `true`를 넣어 대체하려 하거나, `.5f`(float 리터럴)를 보고도 `SetInteger`를 선택하는 타입 혼동이 발생합니다.
- 판별 기준: 각 호출의 두 번째 인수가 정수(`1`), 실수(`.5f`), 불리언(`false`), 없음(신호만)인지를 파악하여 `SetInteger/SetFloat/SetBool/SetTrigger`를 정확히 매칭했는지 채점합니다.

### P04
- 개념 정의: C#에서 인스턴스 메서드를 호출할 때는 클래스 타입명(`Animator`)이 아니라 인스턴스를 담고 있는 **변수명**(`animator`, 소문자)을 사용합니다. `SetBool`의 시그니처는 `(string name, bool value)`이므로 문자열 파라미터명과 bool 값을 쉼표로 구분하여 전달해야 합니다.
- 오답 포인트: 대문자 `Animator`(클래스 타입)를 호출 주체로 쓰거나, 쌍따옴표 형식을 틀리거나, `false` 대신 `0`을 넣는 타입 혼동이 있습니다.
- 판별 기준: `animator.SetBool("Attacking", false);` 형태가 정확히 완성되었는지 확인합니다.

### P05
- 개념 정의: Animator에서 reset(초기화) 전환을 트리거하려면 특정 Trigger 파라미터를 발동하고, 동시에 관련 Bool 파라미터를 `false`로 되돌려 현재 분기 조건의 진입을 차단해야 합니다.
- 오답 포인트: `Friendly`를 Trigger 타입으로, `Search`를 Bool 타입으로 잘못 매칭하여 역할을 뒤바꿉니다.
- 판별 기준: Trigger 역할(1회성 발동 신호)에 `Search`를, Bool 역할(지속적 상태 플래그)에 `Friendly`를 각각 배치했는지 확인합니다.

### X01
- 개념 정의: 게임 런타임에서 캐릭터의 이동 속도(`playerSpeed`)가 변할 때마다 Animator의 Float 파라미터 `"Speed"`를 실시간으로 동기화해야 걷기/뛰기 블렌드 트리가 속도에 비례하여 자연스럽게 전환됩니다.
- 오답 포인트: Float 파라미터인데 `SetInteger`나 `SetBool`로 호출하여 타입 불일치 에러를 발생시키거나, 파라미터명 `"Speed"`의 대소문자를 틀립니다.
- 판별 기준: `animator.SetFloat("Speed", playerSpeed);` 형태에서 API명(`SetFloat`), 파라미터 문자열(`"Speed"`), 변수값(`playerSpeed`)이 모두 정확한지 채점합니다.

### X02
- 개념 정의: Trigger 파라미터는 Bool/Int/Float과 본질적으로 다르게 "값 저장형"이 아니라 **"1회성 발동 신호(펄스)"** 방식입니다. 한 번 발동되면 자동으로 소멸하므로 전용 API인 `SetTrigger`만이 유일한 호출 방법입니다.
- 오답 포인트: `SetBool("Search", true)`로 Bool 파라미터처럼 값을 저장하면 전환이 일어날 것이라 착각하지만, Trigger는 아예 다른 파라미터 타입이므로 이 코드는 "Search"라는 **Bool 파라미터**에 접근하려 하게 되어 의도한 전환이 발생하지 않습니다.
- 판별 기준: Trigger의 1회성 발동 본질을 이해하고 `animator.SetTrigger("Search");`를 유일한 정답으로 선택했는지 확인합니다.

## 운영 메모
- 다음 주차 이월 보강 포인트: U10 Material/Color API에서도 문자열 프로퍼티명과 타입 일치의 엄격성 유지
- 반복 오답 키워드: SetTrigger/SetBool 혼동, 클래스 타입명과 인스턴스 변수명 혼동, 파라미터 리터럴 타입 미식별
