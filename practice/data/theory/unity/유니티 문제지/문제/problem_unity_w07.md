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
  - 아래 코드에 대한 주석을 추가하려고 합니다.코드가 수행하는 기능을 **정확하게 설명하는 주석 2개**를 선택하세요. _(2개 선택)_

### 자료(코드)

```csharp
if (Input.GetButtonDown("Fire1")) {
    Rigidbody clone;
    clone = Instantiate(projectile, transform.position, transform.rotation);
    clone.velocity = transform.TransformDirection(Vector3.forward * 10);
}
```

### 보기

- A. `// 원래 개체를 폐기하고 복제본으로 대체합니다.`
- B. `// <위치>에서 복제본을 인스턴스합니다. 발사체가 적에게 발사되도록 합니다.`
- C. `// 이 변환의 위치와 회전에서 발사체를 인스턴스화`
- D. `// 복제된 개체에 현재 개체의 Z 축을 따라 초기 속도를 제공합니다.`

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
  - 이 문제를 해결하려면 **벡터 값과 숫자 값을 곱해 `AddForce`에 전달**해야 합니다.

  - GameObject에 연결된 `Rigidbody`에 **힘을 가해 이동**해야 합니다.
  - 개체가 **현재 바라보는 방향**으로 이동해야 합니다.
  - 힘의 크기는 **Inspector에서 설정할 수 있는 값**을 사용해야 합니다.

    드롭다운 목록에서 올바른 옵션을 선택해 코드를 완성하세요.

### 자료(코드)

```csharp
using UnityEngine;

public class MovingThings : MonoBehaviour
{
    private float speedOfMotion;
    public float speedForce;
    private static float forceSpeed = 10f;
    private Rigidbody rigidBody;

    void Start()
    {
        speedOfMotion = 10f;
        rigidBody = gameObject.GetComponent<Rigidbody>();
    }

    void FixedUpdate()
    {
        rigidBody.AddForce( [①] * [②] );
    }
}
```

### 보기(드롭다운 후보)

- **① (방향/벡터)**
  - `Vector2.facing`
  - `120`
  - `transform.forward`

- **② (힘의 크기/숫자)**
  - `speedOfMotion`
  - `speedForce`
  - `forceSpeed`


### [P04] 풀링 발사체 함수 선택
- 출처: 원문 23번
- 유형: 단답
- 문제:
  - 프로젝트 장르는 탑다운 아케이드입니다. 플레이어가 발사하는 **발사체 프리팹**에는 `IsTrigger = true`로 설정된 `Collider`가 있습니다.

  - 이 발사체는 `Instantiate`로 생성되지 않고 **장면에 Pool**되어 있다가 사용됩니다.
  따라서 **풀에서 꺼낼 때 필요한 초기화**가 필요하며, 충돌 처리도 Trigger 방식으로 동작해야 합니다.

  - 아래 코드에서 빈칸 2곳에 들어갈 **올바른 이벤트/함수 이름**을 선택해 배치하세요.
  (코드는 발사체 프리팹에 붙어 있으며, 플레이어 오브젝트에 붙어 있지 않습니다.)

### 자료(코드)

```csharp
using UnityEngine;

public class Projectile : MonoBehaviour
{
    private PowerUpManagement PUManage;
    private MeshRenderer meshRenderer;
    private Material instancedMaterial;
    public Color initialColor;

    private bool isAlive = true;
    public int penetration = 1;

    private void [ ① ] ()
    {
        PUManage = GameObject.Find("PowerUp_Manager").GetComponent<PowerUpManagement>();
        meshRenderer = GetComponentInChildren<MeshRenderer>();
        instancedMaterial = meshRenderer.material;
        instancedMaterial.SetColor("_TintColor", initialColor);
    }

    private void [ ② ] (Collider other)
    {
        if (isAlive && other.tag != "Player" && other.tag != "CULL")
        {
            isAlive = false;
            PoolManager.Pool["Projectile"].Despawn(transform, penetration);
        }
    }
}
```

### 드래그 토큰(선택지)

- `Init`
- `Start`
- `Update`
- `FixedUpdate`
- `OnTriggerEnter`
- `OnCollisionEnter`

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
