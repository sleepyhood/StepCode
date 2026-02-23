# Unity 주차 정답지 W09

## 메타
- 대상 문제지: `problem_unity_w09.md`
- 유닛: U09 Animator

## 정답표
| 문항 ID | 정답 | 한 줄 근거 |
|---|---|---|
| P01 | Z1 `JumpApex`, Z2 `SlowFall`, Z3 `FastFall`, Z4 `FastLand` | 원문 15번 상태 배치 정답 |
| P02 | 1 참, 2 거짓, 3 참, 4 거짓 | 원문 31번 상태 전환 판단 |
| P03 | ① `SetInt` ② `SetFloat` ③ `SetBool` ④ `SetTrigger` | 값 타입별 Animator API 대응 |
| P04 | ① `animator` ② `("Attacking", false);` | `SetBool(string,bool)` 시그니처 충족 |
| P05 | ① `Search` ② `Friendly` | reset 전환 조건과 파라미터 일치 |
| X01 | `animator.SetFloat("Speed", playerSpeed);` | float 파라미터는 `SetFloat` 사용 |
| X02 | B | Trigger 파라미터는 `SetTrigger`로 발동 |

## 해설
### P01
- 개념 정의: 점프 정점/낙하/착지 상태를 그래프 위치와 의미에 맞춰 배치해야 합니다.
- 오답 포인트: `SlowFall`과 `FastFall`의 좌우 위치를 바꿔 쓰는 경우가 많습니다.
- 판별 기준: Z1~Z4가 `JumpApex/SlowFall/FastFall/FastLand` 순서면 정답입니다.

### P02
- 개념 정의: Entry, Default State, Sub-State Machine, Transition 가능 방향을 구분해야 합니다.
- 오답 포인트: 상태에서 상태 머신으로 전환이 불가능하다고 오해하기 쉽습니다.
- 판별 기준: 1 참, 2 거짓, 3 참, 4 거짓이면 정답입니다.

### P03
- 개념 정의: 리터럴 타입(int/float/bool/trigger)에 맞는 Set 함수를 매칭합니다.
- 오답 포인트: Trigger를 `SetBool`로 처리하거나 float를 `SetInt`로 처리합니다.
- 판별 기준: ①Int ②Float ③Bool ④Trigger 순서가 맞아야 합니다.

### P04
- 개념 정의: 타입명(`Animator`)이 아니라 변수(`animator`)에 메서드를 호출해야 합니다.
- 오답 포인트: 문자열/불리언 리터럴에 잘못된 따옴표를 사용합니다.
- 판별 기준: `animator.SetBool("Attacking", false);` 형태면 정답입니다.

### P05
- 개념 정의: reset 전환을 유도하는 Trigger와 Bool 파라미터를 정확히 선택해야 합니다.
- 오답 포인트: `Friendly`를 Trigger로, `Search`를 Bool로 뒤바꿉니다.
- 판별 기준: ① `Search`, ② `Friendly` 조합이면 정답입니다.

### X01
- 개념 정의: 런타임 값으로 Animator float 파라미터를 갱신할 때는 `SetFloat`를 사용합니다.
- 오답 포인트: `SetInt`나 `SetBool`로 타입을 섞어 호출합니다.
- 판별 기준: 파라미터명 `"Speed"`와 float 값 전달이 모두 포함되어야 합니다.

### X02
- 개념 정의: Trigger는 값 저장형이 아니라 발동형이므로 `SetTrigger`로 호출합니다.
- 오답 포인트: Trigger를 bool/int/float 파라미터처럼 설정합니다.
- 판별 기준: 정답은 `animator.SetTrigger("Search");`입니다.

## 운영 메모
- 다음 주차 이월 보강 포인트: Material/Color API에서 문자열 프로퍼티명과 타입 일치
- 반복 오답 키워드: `SetTrigger`/`SetBool` 혼동, 타입명과 변수명 혼동
