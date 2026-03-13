# Unity 주차 정답지 W11

## 메타
- 대상 문제지: `problem_unity_w11.md`
- 유닛: U11 ECS

## 정답표
| 문항 ID | 정답 | 한 줄 근거 |
|---|---|---|
| P01 | 코드1 거짓, 코드2 거짓, 코드3 참 | 코드1: ECS 네임스페이스 자체 없음, 코드2: using 선언만 있고 MonoBehaviour 상속+본문에 ECS 타입 없음, 코드3: `ComponentSystem` 상속 + `Entities.ForEach` 실사용 |
| P02 | 코드1 거짓, 코드2 거짓, 코드3 거짓 | 3개 모두 MonoBehaviour 상속이며 ECS 전용 타입(IComponentData, SystemBase 등)의 실제 코드 레벨 사용이 전혀 없음 |
| X01 | 예: `using Unity.Entities; public partial class EnemyMoveSystem : SystemBase { }` | ECS 전용 타입(`SystemBase`)을 실제로 상속한 클래스 선언이 있으므로 실사용 판정 충족 |
| X02 | C | `using` 선언은 접근 가능성만 열어줄 뿐이며, ECS 전용 타입의 실제 코드 사용이 있어야 실사용 판정 |

## 해설
### P01
- 개념 정의: ECS(Entity Component System) "실사용" 판정의 핵심은 `using Unity.Entities;` 네임스페이스 선언 유무가 **아니라**, 코드 본문에서 ECS 전용 타입(`ComponentSystem`, `SystemBase`, `IComponentData`, `EntityManager` 등)을 **직접 상속하거나 인스턴스화하여 호출**하고 있는지입니다.
- 오답 포인트: **코드 2**처럼 `using Unity.Entities;`가 상단에 적혀 있으면 "ECS 관련 라이브러리를 불러왔으니 사용한 것"이라고 속단하기 쉽습니다. 하지만 이 코드의 클래스는 `MonoBehaviour`를 상속하고, 본문에는 `Debug.Log`만 있을 뿐 ECS 타입이 전혀 등장하지 않습니다.
- 판별 기준: **코드 3**만이 `ComponentSystem`을 상속하고 `Entities.ForEach`를 호출하여 ECS 파이프라인을 실제 활용하므로 유일하게 "참"입니다.

### P02
- 개념 정의: `MonoBehaviour` 기반의 전통적 OOP 스크립트는, 설령 `using Unity.Entities;`를 아무리 많이 선언해도 본문에서 ECS 고유 요소를 사용하지 않는 한 기본적으로 ECS 코드가 **아닙니다**.
- 오답 포인트: **코드 1**과 **코드 3**에 `using Unity.Entities;`가 있어서 하나라도 "참"으로 선택하려 하지만, 두 코드 모두 클래스 본문은 완전히 `MonoBehaviour` 패턴(UI 활성화, 점수 누적)이며 ECS 핵심 요소가 부재합니다.
- 판별 기준: 세 코드를 하나씩 살펴 `IComponentData`, `SystemBase`, `EntityManager`, `Entities.ForEach` 등 ECS 전용 키워드가 **코드 본문에 단 한 줄이라도** 등장하는지 검사합니다. 세 코드 모두 해당 없으므로 전부 "거짓"입니다.

### X01
- 개념 정의: "ECS를 실제로 사용했다"는 판정의 **최소 충족 조건**은, `using` 선언 외에 ECS 전용 타입을 상속(`SystemBase`, `ISystem`)하거나 구현(`IComponentData`)하는 클래스 선언이 코드에 최소 1개 존재하는 것입니다.
- 오답 포인트: `using Unity.Entities;` 한 줄만 쓰고 클래스 본문은 기존 `MonoBehaviour` 패턴 그대로 두는 경우, 겉보기에는 ECS를 "사용"한 것 같지만 실제로는 선언만 한 것이므로 판정 기준을 충족하지 못합니다.
- 판별 기준: 제출된 코드에 `SystemBase`, `ISystem`, `IComponentData`, `ComponentSystem` 중 하나라도 상속/구현 형태로 실제 등장하면 정답 처리합니다. 클래스 내부 본문이 비어 있어도 타입 사용 자체가 곧 실사용 증거입니다.

### X02
- 개념 정의: C#의 `using` 지시문은 해당 네임스페이스에 정의된 타입들에 **접근할 수 있는 경로를 열어주는 편의 기능**일 뿐이며, 이것만으로 해당 라이브러리의 기능이 프로젝트에 "활성화"되거나 코드에 "적용"되는 것은 아닙니다.
- 오답 포인트: 보기 A처럼 "import한 시점에서 이미 기능이 활성화된다"거나, 보기 B처럼 "엔진이 자동으로 ECS 파이프라인에 편입시킨다"는 것은 완전한 오해입니다. `MonoBehaviour` 상속 클래스에 `using Unity.Entities;`를 달아봤자 유니티 엔진은 그 스크립트를 전통적 OOP 컴포넌트로 취급합니다.
- 판별 기준: `using` = **가능성 확보**, 실제 타입 사용 = **실사용 증거**라는 두 층위를 정확히 구별하여, 보기 C만이 유일한 정답임을 확정합니다.

## 운영 메모
- 다음 주차 이월 보강 포인트: 없음 (11주차 종결). 필요 시 W01~W11 전 범위를 아우르는 종합 복습 세트로 연결
- 반복 오답 키워드: `using` 선언과 실사용 혼동, `MonoBehaviour` 상속 코드를 ECS로 오판
