# Unity U11 ECS

## 학습 목표
- ECS(Entity Component System)의 기본 목적을 짧게 설명할 수 있습니다.
- `using Unity.Entities;` 선언과 실제 ECS 사용을 구분할 수 있습니다.
- `MonoBehaviour` 코드와 ECS 코드의 판별 기준을 문제 풀이 수준에서 구분할 수 있습니다.
- ECS를 "실제로 사용한 코드"로 인정되는 최소 조건을 말할 수 있습니다.

## 범위
- 키워드: `ECS`, `Unity.Entities`, `MonoBehaviour`, `SystemBase`, `ComponentSystem`, `IComponentData`, `EntityManager`

## 먼저 큰 그림
이번 단원은 "이 코드가 정말 ECS를 사용하고 있는가?"를 판별하는 단원입니다.

W11에서는 특히 아래 4가지를 바로 연결할 수 있어야 합니다.
- `using Unity.Entities;`만 있으면 아직 ECS 사용으로 보지 않습니다.
- `MonoBehaviour`만 상속한 코드는 기본적으로 ECS 코드가 아닙니다.
- `SystemBase`, `ComponentSystem`, `IComponentData`, `EntityManager` 같은 ECS 전용 타입이 실제 코드에 등장해야 합니다.
- ECS 실사용 최소 코드는 `using` 선언 + ECS 전용 타입 상속/구현입니다.

![ECS 1만 개 렌더링 한계 극복](../images/unity_u11_ecs_massive_entities.png)
*캡션: 대량의 개체를 한꺼번에 처리하는 ECS 개념을 시각적으로 보여 주는 예시입니다. 출처: 자체 촬영*

## 핵심 패턴
```csharp
using Unity.Entities;

public partial class MovementSystem : SystemBase
{
}
```

이 코드는 W11 기준에서 "ECS를 실제로 사용한다"고 판정할 수 있는 최소 형태에 가깝습니다.
- `using Unity.Entities;`가 있습니다.
- `SystemBase`라는 ECS 전용 타입을 실제로 상속합니다.

반대로 아래 코드는 ECS가 아닙니다.

```csharp
using Unity.Entities;
using UnityEngine;

public class EnemyAI : MonoBehaviour
{
    void Start() { Debug.Log("Enemy initialized"); }
}
```

- `using Unity.Entities;`는 있지만
- 실제 본문은 `MonoBehaviour` 패턴이고 ECS 전용 타입 사용이 없습니다.

## 문항 핵심 포인트

### 1) ECS는 왜 나왔을까?
이 개념을 알면 무엇이 쉬워지나?
- 코드 판별 문제에서 ECS가 무엇을 위한 구조인지 배경을 짧게 이해할 수 있습니다.

- 개념: ECS는 많은 수의 개체를 더 효율적으로 처리하기 위해 나온 데이터 중심 구조입니다. 기존 `MonoBehaviour` 방식보다 대량 처리와 구조적 분리에 강합니다.
- 왜 헷갈리나?: "최신 기술"이라는 말만 듣고, 모든 프로젝트에서 무조건 써야 하는 구조처럼 받아들이기 쉽습니다.
- 어떻게 구별하나?: W11에서는 성능 세부 설명보다 "ECS는 별도 전용 타입을 가진 다른 구조"라는 점이 핵심입니다.
- 짧은 유사 예시:
  - `PlayerController : MonoBehaviour` -> 전통적 컴포넌트 방식
  - `MovementSystem : SystemBase` -> ECS 방식

정답 판단:
- W11에서는 ECS의 목적을 길게 외우기보다, `MonoBehaviour와 다른 전용 타입 체계`라는 점을 먼저 잡으면 됩니다.

### 2) `using Unity.Entities;`만으로는 왜 부족할까?
이 개념을 알면 무엇이 쉬워지나?
- P01, P02, X02를 바로 풀 수 있습니다.

- 개념: `using Unity.Entities;`는 ECS 네임스페이스에 접근할 수 있게 해 주는 선언일 뿐입니다. 이 한 줄만으로는 "ECS를 사용했다"라고 판정하지 않습니다.
- 왜 헷갈리나?: 라이브러리를 import했으니 이미 그 기술을 쓴 것처럼 느껴지기 쉽습니다.
- 어떻게 구별하나?: `using` 다음에 실제 코드 본문을 봅니다. `MonoBehaviour`만 있고 ECS 타입이 없다면 거짓입니다.
- 짧은 유사 예시:
  ```csharp
  using Unity.Entities;
  using UnityEngine;

  public class UIManager : MonoBehaviour
  {
      public void ShowPanel() { gameObject.SetActive(true); }
  }
  ```
  이 코드는 `using`은 있지만 ECS 실사용은 아닙니다.

정답 판단:
- `using Unity.Entities;`만 있으면 거짓입니다.
- `MonoBehaviour` 상속 + ECS 타입 미사용이면 거짓입니다.

10초 점검:
- `using Unity.Entities;`가 있고 `MonoBehaviour`만 상속하면 참일까요?
- 답: 아니오. 실제 ECS 타입 사용이 없으므로 거짓입니다.

### 3) 무엇이 보이면 ECS 실사용으로 볼 수 있을까?
이 개념을 알면 무엇이 쉬워지나?
- P01의 코드3, X01 같은 문제를 빠르게 판단할 수 있습니다.

- 개념: ECS 실사용 판정의 핵심은 코드 본문에 ECS 전용 타입이 실제로 등장하는가입니다. 대표 예시는 `SystemBase`, `ComponentSystem`, `IComponentData`, `EntityManager`입니다.
- 왜 헷갈리나?: 이름만 보면 일반 클래스처럼 보여서, 이것이 "ECS 전용 타입"인지 놓칠 수 있습니다.
- 어떻게 구별하나?: 클래스 선언부와 본문을 먼저 봅니다. `: SystemBase`, `: ComponentSystem`, `struct ... : IComponentData` 같은 형태가 있으면 ECS 쪽으로 기웁니다.
- 짧은 유사 예시:
  ```csharp
  using Unity.Entities;

  public class MovementSystem : ComponentSystem
  {
      protected override void OnUpdate() { }
  }
  ```
  `ComponentSystem`을 상속하므로 ECS 실사용입니다.

자주 헷갈리는 비교:
- `MonoBehaviour`: 전통적 GameObject 컴포넌트 방식
- `SystemBase`: ECS 시스템
- `ComponentSystem`: ECS 시스템
- `IComponentData`: ECS 데이터 컴포넌트

정답 판단:
- `SystemBase`, `ComponentSystem`, `IComponentData`, `EntityManager` 같은 타입이 실제 코드에 등장하면 참으로 볼 근거가 생깁니다.

### 4) ECS 실사용 최소 코드
이 개념을 알면 무엇이 쉬워지나?
- X01을 바로 작성할 수 있습니다.

- 개념: W11 기준에서 "이 코드는 ECS를 사용한다"고 판정받기 위한 최소 조건은 `using Unity.Entities;`와 ECS 전용 타입 상속/구현입니다.
- 왜 헷갈리나?: 클래스 이름에 `ECS`나 `Entity`라는 단어만 넣어도 될 것처럼 느껴질 수 있습니다.
- 어떻게 구별하나?: 이름보다 타입을 봅니다. `public partial class EnemyMoveSystem : SystemBase { }`처럼 타입 사용이 있어야 합니다.
- 짧은 유사 예시:
  ```csharp
  using Unity.Entities;

  public partial class EnemyMoveSystem : SystemBase
  {
  }
  ```
  이 정도면 최소 실사용 예시로 충분합니다.

정답 판단:
- 최소한 `using Unity.Entities;`
- 그리고 `SystemBase`, `ISystem`, `IComponentData`, `ComponentSystem` 중 하나의 실제 사용

생각 질문:
- 파일명이나 클래스명에 `ECS`라는 단어만 있으면 왜 증거가 되지 않을까요?

## 자주 하는 실수
- `using Unity.Entities;`만 보고 바로 ECS 코드라고 판정합니다.
- `MonoBehaviour` 상속 코드를 ECS로 착각합니다.
- 클래스 이름에 `Entity`가 들어간다는 이유만으로 ECS라고 생각합니다.
- ECS 판별에서 실제 타입 사용보다 파일 상단 선언만 봅니다.

## 빠른 체크리스트
- `using Unity.Entities;`와 실제 사용을 구분할 수 있는가?
- `MonoBehaviour`만 있으면 기본적으로 거짓이라고 판단할 수 있는가?
- `SystemBase`, `ComponentSystem`, `IComponentData`, `EntityManager`를 ECS 핵심 타입으로 볼 수 있는가?
- ECS 실사용 최소 코드를 직접 한 줄 이상 쓸 수 있는가?

## 미니 체크
### Q1
아래 코드가 ECS 실사용일까요?

```csharp
using Unity.Entities;
using UnityEngine;

public class ScoreManager : MonoBehaviour
{
    private int score = 0;
}
```

- 정답: 아니오. `using`은 있지만 ECS 전용 타입의 실제 사용이 없습니다.

### Q2
아래 선언은 ECS 실사용으로 볼 수 있을까요?

```csharp
using Unity.Entities;

public partial class MoveSystem : SystemBase
{
}
```

- 정답: 예. `SystemBase`를 실제로 상속하고 있기 때문입니다.

## 연결 세트
- Basic: `unity_u11_ecs_b01`
- Challenge: `unity_u11_ecs_c01`
