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
- 유형: 객관식
- 문제:
  - 아래 코드가 수행하는 구체적인 동작을 가장 정확히 설명한 보기 2개를 고르고, 그 조합이 올바른 선택지를 선택하세요.
  - 코드 예시:
    ```csharp
    Rigidbody clone = Instantiate(projectile, spawnPoint.position, spawnPoint.rotation);
    clone.velocity = transform.forward * speed;
    ```
  - 보기:
    - A. 원본 프리팹(`projectile`) 오브젝트를 씬에서 영구적으로 삭제한다.
    - B. `spawnPoint`의 위치와 회전 정보를 본떠서 새로운 물체 사본을 생성한다.
    - C. 생성된 물체에 로컬 전방(Z축) 방향으로 일정한 물리 속도를 부여한다.
    - D. 발사체가 적에게 명중할 때까지 자동으로 경로를 추적하여 이동시킨다.
- 선택지:
  - A. A, B
  - B. B, C
  - C. C, D
  - D. A, D

### [P02] rb 변수 타입 선택
- 출처: 원문 11번
- 유형: 객관식
- 문제:
  - 아래의 코드에서 `rb` 변수가 에러 없이 `GetComponent` 결과를 담고 물리 메서드를 호출할 수 있도록 `rb`의 선언 타입으로 가장 알맞은 것을 고르세요.
  - 코드 예시:
    ```csharp
    (  ①  ) rb;

    void Start() {
        rb = GetComponent<Rigidbody>();
    }

    void FixedUpdate() {
        rb.MovePosition(rb.position + transform.forward * Time.fixedDeltaTime);
    }
    ```
- 보기:
  - A. `Vector3`
  - B. `Collider`
  - C. `Rigidbody`
  - D. `CharacterController`

### [P03] AddForce 빈칸 2개 선택
- 출처: 원문 24번
- 유형: 단답
- 문제:
  - 오브젝트가 현재 바라보고 있는 앞쪽 방향으로, 인스펙터에서 설정한 힘(`speedForce`)만큼 밀어내고자 합니다. 아래 코드의 빈칸 ①, ②에 들어갈 올바른 변수/속성을 순서대로 쓰세요.
  - 코드 예시:
    ```csharp
    public float speedForce = 10f;
    private Rigidbody rigidBody;

    void Update() {
        if (Input.GetKeyDown(KeyCode.Space)) {
            rigidBody.AddForce([ ① ] * [ ② ]);
        }
    }
    ```
  - 답안 형식 예: `transform.forward, speedForce`

### [P04] 풀링 발사체 함수 선택
- 출처: 원문 23번
- 유형: 단답
- 문제:
  - 오브젝트 풀링(Pooling) 방식으로 재사용되는 발사체 스크립트입니다. 아래 코드의 빈칸 ①(재사용 시 호출할 초기화 함수), ②(Trigger 충돌 감지 이벤트)에 들어갈 이름을 순서대로 쓰세요.
  - 코드 예시:
    ```csharp
    public void [ ① ](Vector3 pos) {
        transform.position = pos;
        hp = 3;
    }

    void [ ② ] (Collider other) {
        if (other.CompareTag("Enemy")) { 
            // 데미지 처리
        }
    }
    ```
  - 답안 형식 예: `Init, OnTriggerEnter`

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - 발사체 생성 + 전방 속도 부여 코드 선택
- 출처 개념: U07 Spawn/Physics
- 유형: 객관식
- frictionless:
  - `Fire1` 마우스 왼쪽 버튼을 눌렀을 때, `projectile` 프리팹을 현재 위치/회전값으로 생성하고, 생성된 복제본(`clone`)의 `Rigidbody` 컴포넌트를 이용해 앞쪽 방향으로 `10f`의 속도를 부여하고자 합니다. 다음 중 `if (Input.GetButtonDown("Fire1"))` 블록 내부에 들어갈 핵심 2줄의 코드로 가장 올바른 것을 고르세요.
- 보기:
  - A.
    ```csharp
    GameObject clone = Instantiate(projectile, transform.position, transform.rotation);
    clone.velocity = Vector3.forward * 10f;
    ```
  - B.
    ```csharp
    Rigidbody clone = Instantiate(projectile, transform.position, transform.rotation);
    clone.velocity = transform.forward * 10f;
    ```
  - C.
    ```csharp
    Rigidbody clone = Instantiate(projectile, transform.position, transform.rotation);
    clone.AddForce(transform.forward * 10f);
    ```
  - D.
    ```csharp
    Instantiate(projectile, transform.position, transform.rotation);
    projectile.velocity = transform.forward * 10f;
    ```
- 의도: 조건 입력 판별부터 프리팹 인스턴스화, 물리 속성 동기화까지의 발사 루틴을 올바르게 구별하는 능력을 함양합니다.

### [X02] 함정 - Trigger/Collision 이벤트 구분
- 출처 개념: U07 Spawn/Physics
- 유형: 객관식
- 문제:
  - 총알의 Collider 컴포넌트에서 `IsTrigger`가 **체크(True)**되어 있을 때, 적과 부딪히는 순간 유니티 엔진이 스크립트에서 찾아 실행시키는 이벤트 함수로 올바른 것을 고르세요.
- 보기:
  - A. `OnCollisionEnter(Collision other)`
  - B. `OnTriggerEnter(Collider other)`
  - C. `Update()`
  - D. `OnCollisionStay(Collision other)`
- 의도: 물리 이벤트 선택 오개념 제거

## 주차 체크
- 원문 대응 문항 수: 4
- 확장 문항 수: 2
- 총 문항 수: 6
