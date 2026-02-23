# Unity 주차 정답지 W11

## 메타
- 대상 문제지: `problem_unity_w11.md`
- 유닛: U11 ECS

## 정답표
| 문항 ID | 정답 | 한 줄 근거 |
|---|---|---|
| P01 | 코드1 거짓, 코드2 거짓, 코드3 참 | `ComponentSystem` 상속 코드만 ECS 실사용 |
| P02 | 코드1 거짓, 코드2 거짓, 코드3 거짓 | 3개 모두 ECS 핵심 요소 부재 |
| X01 | 예: `public partial class EnemyMoveSystem : SystemBase {}` | ECS 시스템 타입 직접 사용 |
| X02 | C | `using`만으로는 불충분, 실제 ECS 타입/코드 필요 |

## 해설
### P01
- 개념 정의: ECS 판별은 네임스페이스 선언이 아니라 ECS 타입/시스템의 실제 사용 여부로 판단합니다.
- 오답 포인트: 코드 2처럼 `using Unity.Entities;`만 보고 참으로 선택하기 쉽습니다.
- 판별 기준: 코드1 거짓, 코드2 거짓, 코드3 참이면 정답입니다.

### P02
- 개념 정의: `MonoBehaviour` 기반 일반 OOP 스크립트는 기본적으로 ECS 코드가 아닙니다.
- 오답 포인트: `using Unity.Entities;` 한 줄 때문에 코드1을 참으로 착각합니다.
- 판별 기준: 세 코드 모두 ECS 핵심 요소(`IComponentData`, `SystemBase`, `EntityManager` 등)가 없으므로 전부 거짓입니다.

### X01
- 개념 정의: ECS 사용 인정의 최소 단위는 ECS 타입을 선언/상속/사용하는 코드입니다.
- 오답 포인트: `using Unity.Entities;`만 쓰고 실제 타입 사용을 생략합니다.
- 판별 기준: `SystemBase`, `ISystem`, `IComponentData` 중 하나라도 실제 코드에 등장하면 정답 처리 가능합니다.

### X02
- 개념 정의: 네임스페이스 선언은 "사용 가능" 상태일 뿐 "실사용" 증거가 아닙니다.
- 오답 포인트: 선언 자체를 사용으로 간주합니다.
- 판별 기준: 정답은 C입니다.

## 운영 메모
- 다음 주차 이월 보강 포인트: 없음(11주차 종결), 필요 시 종합 복습 세트로 연결
- 반복 오답 키워드: `using` 선언 과신, `MonoBehaviour`와 ECS 개념 혼동
