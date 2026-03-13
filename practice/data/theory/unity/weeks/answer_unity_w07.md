# Unity 주차 정답지 W07

## 메타
- 대상 문제지: `problem_unity_w07.md`
- 유닛: U07 Spawn/Physics

## 정답표
| 문항 ID | 정답 | 한 줄 근거 |
|---|---|---|
| P01 | B, C | B: 현재 총구의 위치/회전을 본따서 프리팹을 복제 생성(Instantiate)하는 동작 설명, C: 복제된 물체에 로컬 전방(Z축) 방향으로 등속 물리 속도(velocity)를 대입하는 동작 설명 |
| P02 | C | `GetComponent<Rigidbody>()`가 돌려주는 반환 타입이 `Rigidbody`이므로, 대입 받는 변수도 정확히 동일한 `Rigidbody` 자료형이어야 컴파일 통과 |
| P03 | ① `transform.forward`, ② `speedForce` | ①은 캐릭터가 현재 바라보는 전방 단위 방향 벡터, ②는 Inspector에서 조절 가능하도록 `public`으로 선언된 힘 크기 실수형 변수 |
| P04 | ① `Init`, ② `OnTriggerEnter` | ①은 풀에서 꺼낼 때마다 속도/체력을 리셋하는 커스텀 초기화 함수, ②는 `IsTrigger=true` 콜라이더 투과 충돌을 감지하는 엔진 내장 이벤트 |
| X01 | 예: `if (Input.GetButtonDown("Fire1")) {`<br>`Rigidbody clone = Instantiate(projectile, transform.position, transform.rotation);`<br>`clone.velocity = transform.forward * 10f;` | 입력 감지(Fire1 Down) -> 프리팹 복제 생성(Instantiate) -> 전방 속도 할당(velocity)의 3단계 발사 로직 |
| X02 | B | `IsTrigger=true` Collider는 물리적 반발 없이 겹침만 감지하므로, 유니티 엔진이 호출하는 이벤트는 `OnTriggerEnter(Collider other)` |

## 해설
### P01
- 개념 정의: `Instantiate(프리팹, 위치, 회전)`는 지정 위치에 원본 오브젝트의 물리적 사본(Clone)을 생성하는 유니티 핵심 API이며, 생성 직후 `velocity` 속성에 값을 넣어주면 해당 방향으로 등속도 선형 이동이 즉시 시작됩니다.
- 오답 포인트: 원본 프리팹(`projectile`)을 파괴한다거나, 인공지능 요소로 유도 명중한다는 등 코드에 절대 존재하지 않는 부가 동작을 지어내서 주석에 포함시킵니다.
- 판별 기준: 2줄 코드 각각이 수행하는 **실재하는 단일 동작**(위치-회전 기반 복제(Instantiate), 전방 방향 등속도 부여(velocity))만 정확히 기술한 보기를 고릅니다.

### P02
- 개념 정의: C#에서 제네릭 메서드 `GetComponent<T>()`가 반환하는 타입은 `<T>` 안에 기입한 컴포넌트 타입 그 자체이며, 대입 받는 좌변 변수도 이 타입과 반드시 일치해야 형 안전(Type Safety)이 보장됩니다.
- 오답 포인트: `Rigidbody` 대신 `Vector3`(좌표 데이터 구조체)나 `Collider`(충돌 감지 전용 컴포넌트) 등 얼핏 물리 관련으로 비슷해 보이는 허풍 타입을 선택해 컴파일 에러를 유발합니다.
- 판별 기준: `GetComponent<Rigidbody>()`의 꺾쇠 안에 정의된 타입과 변수 선언 타입이 문자 그대로 동일한지 확인합니다.

### P03
- 개념 정의: `Rigidbody.AddForce(Vector3)` 메서드는 내부적으로 방향(Direction)과 크기(Magnitude)를 곱한 단일 벡터를 힘으로 받아들이므로, `방향벡터 * 스칼라크기` 형태의 곱연산이 가장 직관적인 파라미터 구성입니다.
- 오답 포인트: 방향 자리에 숫자 리터럴을 넣거나, Inspector에서 자유롭게 세기를 바꿔야 하는 필드를 `private` 고정 상수로 묶어서 개발 유연성을 차단합니다.
- 판별 기준: ①이 오브젝트의 현재 전방 방향 단위벡터(`transform.forward`)이고, ②가 `public float`으로 선언되어 에디터 창에 노출된 변수(`speedForce`)인지 동시에 확인합니다.

### P04
- 개념 정의: 오브젝트 풀링(Pooling)에서는 `Destroy` 대신 비활성화(`SetActive(false)`) 후 재사용하므로, `Start()`처럼 최초 한 번만 호출되는 함수가 아니라 매번 꺼냈을 때 상태를 초기화해주는 **별도의 커스텀 초기화 함수**가 필요합니다. 또한 `IsTrigger=true`로 세팅된 콜라이더는 물리적 반발 없이 관통 감지만 하므로, 유니티 이벤트 시스템 중 `OnCollisionEnter`가 아닌 `OnTriggerEnter`가 호출됩니다.
- 오답 포인트: 풀링 재활용 시 `Start()`를 초기화 용도로 기대하지만 `Start()`는 오브젝트 생애 최초 1회만 호출되며, Trigger 설정인데도 습관적으로 `OnCollisionEnter`를 적어 이벤트가 영원히 발동되지 않는 버그를 만듭니다.
- 판별 기준: ①이 재사용마다 수동 호출 가능한 커스텀 함수명(`Init`)이고, ②가 `Collider other` 시그니처를 가진 `OnTriggerEnter`인지 확인합니다.

### X01
- 개념 정의: FPS/TPS 무기 발사 시스템의 기본 구조는 **① 입력 감지** → **② 프리팹 복제 생성** → **③ 물리 속성 대입**의 3단계입니다.
- 오답 포인트: 생성(`Instantiate`)만 하고 방향 속도를 주지 않아 탄막이 그 자리에 멈춰 있거나, 입력 확인 분기(`GetButtonDown`) 없이 매 프레임 무한 발사하는 치명적 로직을 만듭니다.
- 판별 기준: `if (Input.GetButtonDown("Fire1"))` 조건문, `Instantiate` 생성 캐싱, `clone.velocity` 방향 속도 대입이 3줄에 걸쳐 올바른 순서와 문법으로 기재되어 있는지 확인합니다.

### X02
- 개념 정의: 유니티 물리 시스템은 콜라이더의 `IsTrigger` 체크박스 状態에 따라 **완전히 다른 이벤트 함수**를 호출합니다. 체크되어 있으면(`true`) `OnTriggerEnter(Collider)`를, 체크 해제면(`false`) `OnCollisionEnter(Collision)`를 각각 자동 분배합니다.
- 오답 포인트: 두 이벤트의 파라미터 타입(`Collider` vs `Collision`)이 다르고 호출 조건도 상이한데, 이름 유사성 때문에 `Collision` 계열을 지정했다가 이벤트가 호출되지 않는 무반응(Silent Failure) 함정에 빠집니다.
- 판별 기준: `IsTrigger=true`가 전제되어 있으므로 반드시 `OnTriggerEnter(Collider other)`만이 유일한 정답임을 인식해야 합니다.

## 운영 메모
- 다음 주차 이월 보강 포인트: U08에서 UI 이벤트(onClick) 등록 시점과 실행 조건 연결
- 반복 오답 키워드: Trigger/Collision 이벤트 혼동, Rigidbody 타입 선언 불일치, velocity 미할당
