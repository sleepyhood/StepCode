# Unity 주차 정답지 W07

## 메타
- 대상 문제지: `problem_unity_w07.md`
- 유닛: U07 Spawn/Physics

## 정답표
| 문항 ID | 정답 | 한 줄 근거 |
|---|---|---|
| P01 | C, D | 위치/회전 인스턴스화 + 전방(Z축) 속도 부여 설명 |
| P02 | C | `GetComponent<Rigidbody>()`와 `MovePosition`에 맞는 타입 |
| P03 | ① `transform.forward`, ② `speedForce` | 방향 벡터 + Inspector 조절 필드 조합 |
| P04 | ① `Init`, ② `OnTriggerEnter` | 풀링 초기화 + Trigger 충돌 처리 |
| X01 | 예: `Rigidbody clone = Instantiate(projectile, transform.position, transform.rotation); clone.velocity = transform.TransformDirection(Vector3.forward * 10);` | 생성 후 전방 속도 부여 |
| X02 | B | IsTrigger 충돌은 `OnTriggerEnter(Collider)` 사용 |

## 해설
### P01
- 개념 정의: Instantiate는 생성 위치/회전을 지정하고, velocity는 초기 이동을 만듭니다.
- 오답 포인트: 코드에 없는 동작(원본 삭제, 타겟 보장)을 주석에 넣기 쉽습니다.
- 판별 기준: 코드에 직접 나타난 동작만 설명한 선택지를 고릅니다.

### P02
- 개념 정의: 컴포넌트 대입과 메서드 호출은 타입 일치가 필수입니다.
- 오답 포인트: `Rigidbody`와 무관한 타입으로 선언해 형 변환 오류가 납니다.
- 판별 기준: `GetComponent<Rigidbody>()` 반환 타입과 동일해야 합니다.

### P03
- 개념 정의: `AddForce`는 방향 벡터와 힘 크기 스칼라를 곱해 전달합니다.
- 오답 포인트: 방향 대신 숫자, Inspector 값 대신 private 고정값을 넣습니다.
- 판별 기준: 요구 조건(바라보는 방향 + Inspector 설정값)을 동시에 만족해야 합니다.

### P04
- 개념 정의: 풀링 오브젝트는 재사용 시 초기화 함수가 필요하고 Trigger는 전용 이벤트로 처리합니다.
- 오답 포인트: `Start`를 재사용 초기화 용도로 고정하거나 `OnCollisionEnter`를 선택합니다.
- 판별 기준: 풀링 초기화는 `Init`, Trigger 충돌은 `OnTriggerEnter(Collider)`를 사용합니다.

### X01
- 개념 정의: 발사 루틴은 입력 감지 -> 생성 -> 속도 부여의 3단계로 구성됩니다.
- 오답 포인트: 생성만 하고 속도를 주지 않거나, 로컬/월드 방향 변환을 누락합니다.
- 판별 기준: Instantiate와 velocity 할당이 모두 포함되어야 합니다.

### X02
- 개념 정의: Trigger 콜라이더는 Collision 이벤트가 아니라 Trigger 이벤트를 호출합니다.
- 오답 포인트: `OnCollisionEnter`를 습관적으로 사용합니다.
- 판별 기준: Collider 시그니처가 맞는 `OnTriggerEnter(Collider)`인지 확인합니다.

## 운영 메모
- 다음 주차 이월 보강 포인트: U08에서 UI 이벤트(onClick) 등록 시점과 실행 조건 연결
- 반복 오답 키워드: Trigger/Collision 혼동, Rigidbody 타입 선언 오류
