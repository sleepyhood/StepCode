# Unity 주차 문제지 W07

## 주차 주제
- 유닛: U07 Spawn/Physics
- 핵심 개념: Instantiate, Rigidbody 참조 타입, AddForce 방향/크기, Trigger 이벤트

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] 코드 설명 주석 2개 선택
- 출처: 원문 36번
- 유형: 단답
- 문제:
  - 아래 코드 설명으로 맞는 주석 2개를 쓰세요.
  - 보기: A, B, C, D
  - 코드 핵심:
    - `Instantiate(projectile, transform.position, transform.rotation)`
    - `clone.velocity = transform.TransformDirection(Vector3.forward * 10)`

### [P02] rb 변수 타입 선택
- 출처: 원문 11번
- 유형: 객관식
- 문제:
  - `rb = GetComponent<Rigidbody>();`와 `rb.MovePosition(...)`가 있는 코드에서 `rb`의 선언 타입으로 가장 알맞은 것을 고르세요.
- 보기:
  - A. `Vector3`
  - B. `Collider`
  - C. `RigidBody` (드롭다운 표기 기준)
  - D. `CharacterController`

### [P03] AddForce 빈칸 2개 선택
- 출처: 원문 24번
- 유형: 단답
- 문제:
  - `rigidBody.AddForce([①] * [②]);`에서 아래 조건을 만족하도록 ①, ②를 쓰세요.
  - 조건:
    - ① 현재 바라보는 방향 벡터
    - ② Inspector에서 조절 가능한 힘 크기

### [P04] 풀링 발사체 함수 선택
- 출처: 원문 23번
- 유형: 단답
- 문제:
  - 풀링 발사체 코드에서 빈칸 함수명을 쓰세요.
  - ① 풀에서 꺼낼 때 초기화 함수(매개변수 없음)
  - ② `IsTrigger=true` Collider 충돌 처리 함수(`Collider other`)

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - 발사체 생성 + 전방 속도 부여 코드 작성
- 출처 개념: U07 Spawn/Physics
- 유형: 코드
- 문제:
  - `Fire1` 입력 시 발사체를 생성하고, 생성된 `Rigidbody`에 전방 초기 속도를 주는 핵심 3줄 코드를 작성하세요.
- 의도: 생성/속도 부여 패턴을 독립 구현으로 전이

### [X02] 함정 - Trigger/Collision 이벤트 구분
- 출처 개념: U07 Spawn/Physics
- 유형: 객관식
- 문제:
  - `IsTrigger = true`인 Collider를 사용하는 발사체에 적절한 이벤트를 고르세요.
- 보기:
  - A. `OnCollisionEnter(Collision other)`
  - B. `OnTriggerEnter(Collider other)`
  - C. `Update()`
  - D. `LateUpdate()`
- 의도: 물리 이벤트 선택 오개념 제거

## 주차 체크
- 원문 대응 문항 수: 4
- 확장 문항 수: 2
- 총 문항 수: 6
