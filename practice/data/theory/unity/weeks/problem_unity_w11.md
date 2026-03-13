# Unity 주차 문제지 W11

## 주차 주제
- 유닛: U11 ECS
- 핵심 개념: ECS(Entity Component System) 실사용 판별 기준 — `using` 네임스페이스 선언만으로는 불충분하며, ECS 전용 타입/시스템의 실제 코드 사용이 있어야 "ECS를 사용한다"고 판정

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] 코드 3개의 ECS 사용 여부 판별
- 출처: 원문 5번
- 유형: 참거짓
- 문제:
  - 다음 3개의 C# 코드 조각을 각각 살펴보고, 해당 코드가 유니티의 **ECS(Entity Component System) 라이브러리를 실제로 사용**하고 있는지 여부를 참/거짓으로 판별하세요.
  - **판별 핵심 기준**: 단순히 `using Unity.Entities;` 네임스페이스를 선언(import)한 것만으로는 ECS를 "사용"한 것으로 보지 **않습니다**. 코드 본문에서 ECS 전용 타입(`IComponentData`, `SystemBase`, `ComponentSystem`, `EntityManager` 등)을 **직접 상속하거나 인스턴스화하여 호출**해야만 "ECS 실사용"으로 판정합니다.

  **코드 1**
  ```csharp
  using UnityEngine;

  public class PlayerController : MonoBehaviour
  {
      void Update() { transform.Translate(Vector3.forward); }
  }
  ```

  **코드 2**
  ```csharp
  using UnityEngine;
  using Unity.Entities;

  public class EnemyAI : MonoBehaviour
  {
      void Start() { Debug.Log("Enemy initialized"); }
  }
  ```

  **코드 3**
  ```csharp
  using Unity.Entities;

  public class MovementSystem : ComponentSystem
  {
      protected override void OnUpdate()
      {
          Entities.ForEach((ref Translation t) => { t.Value.y += 1; });
      }
  }
  ```

  - 답안 형식 예: `코드1 거짓, 코드2 거짓, 코드3 참`

### [P02] 코드 조각 3개의 ECS 사용 여부 추가 판별
- 출처: 원문 34번
- 유형: 참거짓
- 문제:
  - 다음 3개의 코드 조각도 동일한 기준으로 ECS 실사용 여부를 판별하세요.
  - 판별 기준은 P01과 동일합니다: `using` 선언만으로는 불충분하며, ECS 핵심 타입의 **실제 코드 레벨 사용**이 있어야 참입니다.

  **코드 1**
  ```csharp
  using Unity.Entities;
  using UnityEngine;

  public class UIManager : MonoBehaviour
  {
      public void ShowPanel() { gameObject.SetActive(true); }
  }
  ```

  **코드 2**
  ```csharp
  using UnityEngine;

  public class CameraFollow : MonoBehaviour
  {
      public Transform target;
      void LateUpdate() { transform.position = target.position; }
  }
  ```

  **코드 3**
  ```csharp
  using UnityEngine;
  using Unity.Entities;

  public class ScoreManager : MonoBehaviour
  {
      private int score = 0;
      public void AddScore(int value) { score += value; }
  }
  ```

  - 답안 형식 예: `코드1 거짓, 코드2 거짓, 코드3 거짓`

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - ECS 실사용으로 판정되는 최소 코드 작성
- 출처 개념: U11 ECS
- 유형: 코드
- 문제:
  - P01과 P02에서 학습한 판별 기준을 적용하여, **"이 코드는 ECS 라이브러리를 실제로 사용한다"**고 판정받을 수 있는 가장 간결한 최소 C# 코드를 작성하세요.
  - 작성 조건:
    - `using Unity.Entities;` 네임스페이스 선언은 당연히 포함해야 합니다.
    - 단, 그것만으로는 부족하므로, **ECS 전용 타입(`SystemBase`, `ISystem`, `IComponentData`, `ComponentSystem` 등) 중 하나를 실제로 상속하거나 구현하는 클래스 선언부**가 최소 1줄 이상 포함되어야 합니다.
  - (클래스 내부 본문은 비어 있어도 무방합니다.)
- 의도: "ECS를 사용했다"라는 판정의 최소 충족 조건이 무엇인지를 직접 코드로 증명하게 하여, 선언과 실사용의 경계를 체화시킵니다.

### [X02] 함정 - `using Unity.Entities;`만 선언했을 때의 판정
- 출처 개념: U11 ECS
- 유형: 객관식
- 문제:
  - C# 스크립트 최상단에 `using Unity.Entities;`가 적혀 있지만, 클래스 본문은 `MonoBehaviour`를 상속하고 내부에 ECS 관련 타입이나 API 호출이 전혀 없는 코드가 있습니다. 이 코드의 ECS 사용 판정에 대해 **가장 정확한 설명**을 고르세요.
- 보기:
  - A. `using Unity.Entities;` 네임스페이스 선언이 있으므로 ECS를 사용한 것으로 판정한다. import한 시점에서 이미 ECS 기능이 활성화된다.
  - B. `using Unity.Entities;`가 있고 클래스가 `MonoBehaviour`를 상속하면, 유니티 엔진이 자동으로 해당 스크립트를 ECS 파이프라인에 편입시켜 준다.
  - C. `using` 선언은 해당 네임스페이스의 타입에 **접근할 수 있는 가능성만 열어줄 뿐**이며, 코드 본문에서 ECS 전용 타입(`IComponentData`, `SystemBase` 등)이나 엔티티 처리 로직을 **실제로 사용해야만** "ECS 사용"으로 판정된다.
  - D. 파일명이나 클래스명에 "ECS" 또는 "Entity"라는 단어가 포함되어 있으면 ECS를 사용한 것으로 자동 판정된다.
- 의도: `using` 선언(가능성 확보)과 실제 코드 레벨 사용(실사용 증거)의 본질적 차이를 명확히 구별하고, 네임스페이스 import만으로 기능이 활성화된다는 흔한 초보자 오개념을 완전히 제거합니다.

## 주차 체크
- 원문 대응 문항 수: 2
- 확장 문항 수: 2
- 총 문항 수: 4
