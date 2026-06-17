# Unity 주차 문제지 W05

## 주차 주제
- 유닛: U05 Transform/Lifecycle
- 핵심 개념: 중첩 클래스 타입 선언, 자식 Transform 배열 반환, Awake/OnEnable 역할 분리

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] 빈칸 채우기 (커스텀 클래스 배열)
- 출처: 원문 4번
- 유형: 객관식
- 문제:
  - 컴포넌트 내부에 직접 정의한 중첩 클래스(Nested Class) 데이터들을 인스펙터에 리스트로 노출하려고 합니다.
  - 아래 `WeaponControl` 안의 배열 변수 선언 시, 내부의 `turretMount` 프로퍼티에 접근할 때 타입 충돌 오류가 발생하지 않도록 **①번 항목과 ②번 생성 빈칸에 공통으로 들어갈 가장 알맞은 데이터 타입**을 고르세요.
  ```csharp
  using UnityEngine;

  public class WeaponControl : MonoBehaviour
  {
      // 사용자 정의 중첩 클래스
      [System.Serializable]
      public class Mount
      {
          public Transform turretMount;
          public string mountName;
      }

      // 배열 선언부
      public ①[] tMounts = new ②[2];

      public void Start()
      {
          tMounts[0].turretMount = null;
          tMounts[1].turretMount = null;
      }
  }
  ```
- 보기:
  - A. `① Transform, ② Transform`
  - B. `① Mount, ② Mount`
  - C. `① GameObject, ② GameObject`
  - D. `① WeaponControl, ② WeaponControl`

### [P02] 자식 Transform 반환 타입
- 출처: 원문 14번
- 유형: 객관식
- 문제:
  - 아래 C# 메서드는 특정 대상(부모 `tr`)의 하위에 있는 모든 직계 자식 `Transform`들을 추출하여 하나의 목록 변수(`result`)에 담아 통째로 반환하는 기능을 수행합니다.
  - 코드 본문 내에서 생성된 반환용 변수 `result`의 구조를 파악하고, 이 메서드 전체의 컴파일을 위해 선언되어야 할 **가장 정확한 반환 타입(`public [빈칸] GetChildren...`)** 을 고르세요.
  ```csharp
  public [빈칸] GetChildren(Transform tr)
  {
      int childCount = tr.childCount;
      Transform[] result = new Transform[childCount];
      for (int i = 0; i < childCount; ++i)
      {
          result[i] = tr.GetChild(i);
      }
      return result;
  }
  ```
- 보기:
  - A. `Transform`
  - B. `List<Transform>`
  - C. `Transform[]`
  - D. `void`

### [P03] Awake/OnEnable 역할 기반 블록 순서 배열
- 출처: 원문 26번
- 유형: 객관식
- 문제:
  - 플레이어가 아닌 캐릭터의 손 오브젝트에 특정 **소품(Prop)** 을 연결하는 스크립트를 작성 중입니다.
  - 유니티의 생명주기(Lifecycle) 규칙에 따라 두 단계의 작업으로 분리해야 합니다.
    - 1. **앱 최초 로드 시 무조건 실행할 준비 동작**: 소품 모델에 붙어 있는 `PropSpecs` 컴포넌트로부터 `damage` 및 `durability` 수치를 사전에 읽어와 캐싱해 둡니다.
    - 2. **이 컴포넌트가 활성화(Enabled) 될 때마다 반복해 실행할 동작**: 데이터 준비가 끝난 해당 소품을 실제로 캐릭터의 손 슬롯(현재 `transform`)에 부착시키고 위치 및 회전값을 동기화합니다.
  - 위 설계 의도에 맞게 에러가 나지 않도록, 하단의 **코드 블록 4개를 논리적인 실행 흐름(클래스 선언 -> 초기 준비 -> 활성화 장착) 순서대로 알맞게 조합한 것을 고르세요.**
  - **코드 블록 후보:**
    - **A**:
      ```csharp
      private void OnEnable() {
      ```
    - **B**:
      ```csharp
      public class AttachProp : MonoBehaviour {
          public Transform prop;
          private PropSpecs propSpecs;
          private float damage;
          private float durability;
          private void Awake () {
      ```
    - **C**:
      ```csharp
              propSpecs = prop.GetComponent<PropSpecs>();
              this.damage = propSpecs.damage;
              this.durability = propSpecs.durability;
          }
      ```
    - **D**:
      ```csharp
              prop.parent = transform;
              prop.position = transform.localPosition;
              prop.rotation = transform.localRotation;
          }
      }
      ```
- 보기:
  - A. `A ➔ C ➔ B ➔ D`
  - B. `B ➔ C ➔ A ➔ D`
  - C. `B ➔ D ➔ A ➔ C`
  - D. `C ➔ B ➔ A ➔ D`

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - 자식 Transform 배열 반환 유틸 함수 전체 완성
- 출처 개념: U05 Transform/Lifecycle
- 유형: 객관식
- 문제:
  - 유니티 씬의 특정 `Transform root` 객체를 파라미터로 넘겨받으면, 그 객체가 감싸고 있는 1차 직계 자식들을 모조리 수집하여 `Transform[]` 배열 변수명 `result`에 담아 되돌려주는 완전한 메서드 기능의 핵심 C# 코드로 가장 올바른 조합을 고르세요.
- 보기:
  - A.
    ```csharp
    Transform[] result = new Transform[root.childCount];
    for (int i = 0; i < root.childCount; i++) {
        result[i] = root.GetChild(i);
    }
    return result;
    ```
  - B.
    ```csharp
    Transform[] result = new Transform[root.childCount];
    for (int i = 0; i < root.childCount; i++) {
        result[i] = root.GetChild;
    }
    return result;
    ```
  - C.
    ```csharp
    Transform[] result = new Transform[root.childCount];
    for (int i = 0; i < root.childCount; i++) {
        result[i] = root.childCount;
    }
    return result;
    ```
  - D.
    ```csharp
    Transform result = new Transform[root.childCount];
    for (int i = 0; i < root.childCount; i++) {
        result = root.GetChild(i);
    }
    return result;
    ```
- 의도: C# 코딩 테스트 및 실무에서 자주 쓰이는 자식 탐색 순회 패턴(`childCount` + `GetChild`)의 독립적 구현 능력을 점검합니다.

### [X02] 함정 - 라이프사이클(Lifecycle)의 올바른 책임 분리 판별
- 출처 개념: U05 Transform/Lifecycle
- 유형: 객관식
- 문제:
  - 컴포넌트의 캐싱과 시각적 업데이트에 대해 유니티의 생명주기 체계 관점에서 볼 때, 게임 최적화 및 에러 방지를 위한 가장 올바른 메서드 배치 설계안을 고르세요.
- 보기:
  - A. `OnEnable`에서 `GetComponent`를 매번 수행하여 장착한다.
  - B. `Awake`에서 `GetComponent` 결과를 캐싱하고, `OnEnable`에서 장착 명령만 수행한다.
  - C. 모든 로직을 `Update`에 넣어 매 프레임 확인한다.
  - D. `Start`에서 장착 로직을 단 한 번만 수행한다.
- 의도: 단 1번 호출해야 할 초기화(`Awake/Start`) 시점과, 오브젝트가 껐다 켜질 때마다 활성/비활성화 처리해야 할 이벤트(`OnEnable/OnDisable`) 시점의 책임 책임 분리 한계를 명확히 구별하게 합니다.

## 주차 체크
- 원문 대응 문항 수: 3
- 확장 문항 수: 2
- 총 문항 수: 5
