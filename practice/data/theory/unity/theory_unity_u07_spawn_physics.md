# Unity U07 Spawn and Physics

## 학습 목표
- `Instantiate`로 프리팹을 복제하고, 생성 직후 필요한 값을 바로 적용하는 흐름을 이해합니다.
- `GetComponent<Rigidbody>()`와 변수 타입의 관계를 정확히 구별합니다.
- `transform.forward`, `velocity`, `AddForce`를 이용해 전방 발사 로직을 해석하고 작성합니다.
- `OnTriggerEnter(Collider other)`와 `OnCollisionEnter(Collision other)`의 차이를 구분합니다.
- 오브젝트 풀링에서 `Init()` 같은 초기화 함수가 왜 필요한지 이해합니다.

## 범위
- 키워드: `Instantiate`, `Rigidbody`, `velocity`, `AddForce`, `transform.forward`, `TransformDirection`, `OnTriggerEnter`, `OnCollisionEnter`, `Init`, `Object Pooling`

## 먼저 큰 그림
이번 단원은 "발사체를 만든 뒤 어떻게 앞으로 날리고, 어떤 이벤트로 충돌을 처리하느냐"를 묻는 문제를 풀기 위한 단원입니다.

W07에서는 특히 아래 5가지를 바로 연결할 수 있어야 합니다.
- `Instantiate(프리팹, 위치, 회전)`은 복제 생성입니다.
- `GetComponent<Rigidbody>()`를 받는 변수 타입은 `Rigidbody`입니다.
- `transform.forward`는 현재 바라보는 전방 방향입니다.
- `OnTriggerEnter(Collider other)`는 `IsTrigger = true`일 때 쓰는 이벤트입니다.
- 풀링에서는 재사용할 때마다 `Init()` 같은 초기화 함수가 필요합니다.

![프리팹 윈도우](../images/unity_u07_spawn_physics_prefab_window.png)
*캡션: Hierarchy의 오브젝트를 Project 창으로 끌어 프리팹 에셋으로 만든 예시입니다. 출처: 직접 캡처*

## 핵심 패턴
```csharp
if (Input.GetButtonDown("Fire1"))
{
    Rigidbody clone = Instantiate(projectile, transform.position, transform.rotation);
    clone.velocity = transform.forward * 10f;
}
```

이 패턴은 W07의 핵심 3단계를 한 번에 보여 줍니다.
- 입력을 확인합니다.
- 프리팹을 현재 위치와 회전으로 복제합니다.
- 복제된 `Rigidbody`에 전방 속도를 넣습니다.

비슷한 방식으로 힘을 주고 싶다면 이렇게 씁니다.

```csharp
rigidBody.AddForce(transform.forward * speedForce);
```

- `transform.forward`는 방향입니다.
- `speedForce`는 힘의 크기입니다.
- `public float speedForce;`로 선언하면 Inspector에서 세기를 조절할 수 있습니다.

## 문항 핵심 포인트

### 1) Instantiate와 복제 직후 조작
이 개념을 알면 무엇이 쉬워지나?
- P01과 X01에서 "생성"과 "생성 직후 속도 부여"를 바로 읽을 수 있습니다.

- 개념: `Instantiate(프리팹, 위치, 회전)`은 지정한 위치와 회전으로 프리팹 사본을 만드는 함수입니다. 반환값은 복제된 객체이므로 변수에 담아 곧바로 조작할 수 있습니다.
- 왜 헷갈리나?: `Instantiate`를 그냥 "화면에 나타나게만 하는 함수"로 기억하면, 반환값을 저장해서 `velocity`를 주는 흐름을 놓치기 쉽습니다.
- 어떻게 구별하나?: `Instantiate(...)` 뒤의 결과를 변수에 담고 있다면, 그 변수는 "새로 만들어진 복제본"입니다. 원본 프리팹 자체를 바꾸는 것이 아닙니다.
- 짧은 유사 예시:
  ```csharp
  GameObject clone = Instantiate(enemyPrefab, spawnPoint.position, spawnPoint.rotation);
  ```
  위 코드는 적 프리팹을 복제해서 `clone` 변수로 받는 예시입니다.

정답 판단:
- `Instantiate(projectile, transform.position, transform.rotation)`은 현재 위치/회전 기준 복제 생성입니다.
- 생성 직후 변수에 담긴 객체에 `velocity`를 주면, 새로 나온 발사체가 바로 움직입니다.

생각 질문:
- `Instantiate`만 하고 `clone.velocity = ...`를 쓰지 않으면 발사체는 어떤 상태로 남을까요?

### 2) `GetComponent<Rigidbody>()`와 변수 타입
이 개념을 알면 무엇이 쉬워지나?
- P02에서 `rb`의 선언 타입을 바로 고를 수 있습니다.

- 개념: `GetComponent<Rigidbody>()`는 `Rigidbody` 컴포넌트를 찾아 돌려줍니다. 따라서 대입받는 변수 타입도 `Rigidbody`여야 합니다.
- 왜 헷갈리나?: 물리와 관련된 코드라서 `Vector3`, `Collider`, `CharacterController`도 어울려 보일 수 있습니다. 하지만 반환 타입은 꺾쇠 안의 타입과 정확히 같아야 합니다.
- 어떻게 구별하나?: `GetComponent<T>()`를 보면, 변수 타입은 먼저 `T`를 그대로 읽으면 됩니다. 여기서는 `T`가 `Rigidbody`입니다.
- 짧은 유사 예시:
  ```csharp
  Collider col = GetComponent<Collider>();
  ```
  이 경우에는 변수 타입이 `Collider`여야 맞습니다.

자주 헷갈리는 비교:
- `Rigidbody`: 물리 이동, 속도, 힘 제어
- `Collider`: 충돌 영역 감지
- `Vector3`: 좌표와 방향을 담는 값

정답 판단:
- `rb = GetComponent<Rigidbody>();`라면 `rb` 선언도 `Rigidbody rb;`가 맞습니다.

### 3) `transform.forward`, `TransformDirection`, `AddForce`
이 개념을 알면 무엇이 쉬워지나?
- P01의 속도 설명과 P03의 빈칸 채우기를 동시에 해결할 수 있습니다.

- 개념: `transform.forward`는 오브젝트가 현재 바라보는 전방 방향 벡터입니다. `transform.TransformDirection(Vector3.forward)`와 같은 방향 의미를 더 짧게 표현한 것입니다.
- 왜 헷갈리나?: `Vector3.forward`는 월드 기준의 앞 방향으로만 기억하기 쉽고, `transform.forward`는 "현재 내 몸이 향하는 앞"이라는 점을 놓치기 쉽습니다.
- 어떻게 구별하나?: 오브젝트가 회전해도 그 오브젝트 기준의 앞 방향을 따라가야 하면 `transform.forward`를 봅니다. 문제에서 "현재 바라보는 방향"이라고 하면 거의 이쪽입니다.
- 짧은 유사 예시:
  ```csharp
  rb.velocity = transform.forward * speed;
  ```
  현재 바라보는 방향으로 속도를 주는 코드입니다.

직접 연결:
- `clone.velocity = transform.TransformDirection(Vector3.forward * 10)`은 복제된 물체에 전방 초기 속도를 주는 코드입니다.
- `rigidBody.AddForce(transform.forward * speedForce);`에서 `transform.forward`는 방향, `speedForce`는 힘의 크기입니다.
- `speedForce`를 `public float speedForce;`로 선언하면 Inspector에서 값을 바꿀 수 있습니다.

10초 점검:
- `rigidBody.AddForce([①] * [②]);`
- ① 현재 바라보는 방향 벡터
- ② Inspector에서 조절 가능한 힘 크기
- 답: `transform.forward`, `speedForce`

### 4) Trigger와 Collision 이벤트 구분
이 개념을 알면 무엇이 쉬워지나?
- P04와 X02에서 어떤 이벤트 함수를 써야 하는지 바로 고를 수 있습니다.

- 개념: `IsTrigger = true`이면 물리적으로 막지 않고 겹침만 감지하므로 `OnTriggerEnter(Collider other)`를 사용합니다. 물리적으로 부딪히고 튕기는 상황이면 `OnCollisionEnter(Collision other)`를 사용합니다.
- 왜 헷갈리나?: 함수 이름이 비슷하고 둘 다 "충돌했을 때"처럼 느껴져서, Trigger 상황인데도 습관적으로 `OnCollisionEnter`를 쓰는 경우가 많습니다.
- 어떻게 구별하나?: 문제에서 `IsTrigger = true`, `관통`, `겹침 감지`가 보이면 `OnTriggerEnter(Collider other)`입니다. 반대로 물리 충돌, 반발, 튕김이 보이면 `OnCollisionEnter(Collision other)`입니다.
- 짧은 유사 예시:
  ```csharp
  private void OnTriggerEnter(Collider other)
  {
      gameObject.SetActive(false);
  }
  ```
  발사체가 목표를 통과하며 감지된 뒤 비활성화되는 예시입니다.

![Trigger와 Collision 차이](../images/unity_u07_spawn_physics_trigger_vs_collision.svg)
*캡션: `Is Trigger` 설정 여부에 따라 관통 감지(`OnTriggerEnter`)와 물리 충돌(`OnCollisionEnter`)이 어떻게 갈리는지 비교한 그림입니다. 출처: 자체 제작*

정답 판단:
- `IsTrigger = true`라면 정답은 `OnTriggerEnter(Collider other)`입니다.
- Trigger인데 `OnCollisionEnter(Collision other)`를 쓰면 이벤트가 기대대로 호출되지 않습니다.

### 5) 오브젝트 풀링과 `Init()`
이 개념을 알면 무엇이 쉬워지나?
- P04의 초기화 함수 빈칸을 맞히고, 왜 `Start()` 대신 별도 함수가 필요한지 이해할 수 있습니다.

- 개념: 오브젝트 풀링은 발사체를 매번 `Instantiate`/`Destroy`하지 않고, 미리 만들어 둔 객체를 `SetActive(true/false)`로 꺼내 쓰고 다시 반납하는 방식입니다. 이렇게 재사용되는 객체는 다시 등장할 때 상태를 리셋해야 하므로 `Init()` 같은 초기화 함수를 따로 두는 경우가 많습니다.
- 왜 헷갈리나?: "처음 설정은 `Start()`에서 하면 되지 않나?"라고 생각하기 쉽습니다. 하지만 풀링 객체는 한 번 만들어진 뒤 여러 번 꺼내 쓰므로, 매번 다시 초기화할 별도 함수가 필요합니다.
- 어떻게 구별하나?: 문제에서 "풀에서 꺼낼 때", "재사용", "매개변수 없는 초기화 함수"가 나오면 `Init()` 같은 커스텀 함수를 떠올리면 됩니다.
- 짧은 유사 예시:
  ```csharp
  public void Init()
  {
      rigid.velocity = transform.forward * speed;
  }
  ```
  풀에서 꺼낼 때마다 속도를 다시 넣는 예시입니다.

실무 팁:
- 풀링 발사체는 `Awake()`에서 컴포넌트 참조를 잡고, `Init()`에서 속도나 체력처럼 매번 바뀌는 값을 다시 넣는 구조를 자주 씁니다.

![오브젝트 풀링 개념도](../images/unity_u07_spawn_physics_object_pooling.svg)
*캡션: 발사체를 파괴하지 않고 비활성화 후 다시 꺼내 쓰는 오브젝트 풀링 흐름을 나타낸 그림입니다. 출처: 자체 제작*

정답 판단:
- 풀에서 꺼낼 때 초기화하는 함수 이름은 보통 `Init`입니다.
- `IsTrigger = true`인 발사체의 충돌 처리 함수는 `OnTriggerEnter`입니다.

## 자주 하는 실수
- `Instantiate`는 했지만 반환값을 저장하지 않아, 생성 직후 `velocity`를 주지 못합니다.
- `GetComponent<Rigidbody>()`를 쓰면서 변수 타입을 `Collider`나 `Vector3`로 선언합니다.
- `transform.forward` 대신 월드 고정 방향만 넣어서, 회전한 발사체가 엉뚱한 방향으로 날아갑니다.
- `IsTrigger = true`인데 `OnCollisionEnter`를 써서 이벤트가 호출되지 않습니다.
- 풀링 객체를 재사용하면서 `Init()` 없이 이전 상태를 그대로 남겨 둡니다.

## 빠른 체크리스트
- `Instantiate(프리팹, 위치, 회전)`이 복제 생성이라는 점을 설명할 수 있는가?
- `GetComponent<Rigidbody>()`를 받는 변수 타입이 왜 `Rigidbody`인지 말할 수 있는가?
- `transform.forward`가 "현재 바라보는 방향"임을 구별할 수 있는가?
- `AddForce(transform.forward * speedForce)`에서 방향과 크기를 각각 분리해 설명할 수 있는가?
- `IsTrigger = true`일 때 `OnTriggerEnter(Collider other)`를 고를 수 있는가?
- 풀링에서 `Init()`가 왜 필요한지 설명할 수 있는가?

## 미니 체크
### Q1
아래 코드의 두 번째 줄은 무엇을 뜻하나요?

```csharp
Rigidbody clone = Instantiate(projectile, transform.position, transform.rotation);
clone.velocity = transform.forward * 10f;
```

- 정답: 생성된 발사체 `clone`에 현재 전방 방향으로 초기 속도를 넣는다는 뜻입니다.

### Q2
`rb = GetComponent<Rigidbody>();`가 있을 때 `rb`를 `Collider`로 선언해도 될까요?

- 정답: 안 됩니다. `GetComponent<Rigidbody>()`의 반환 타입이 `Rigidbody`이므로 변수 선언도 같아야 합니다.

### Q3
발사체 Collider의 `IsTrigger`가 켜져 있다면 어떤 이벤트 함수가 맞을까요?

- 정답: `OnTriggerEnter(Collider other)`입니다.

## 연결 세트
- 기초: `unity_u07_spawn_physics_b01`
- 챌린지: `unity_u07_spawn_physics_c01`
