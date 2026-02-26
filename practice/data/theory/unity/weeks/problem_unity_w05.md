# Unity 주차 문제지 W05

## 주차 주제
- 유닛: U05 Transform/Lifecycle
- 핵심 개념: 중첩 클래스 타입 선언, 자식 Transform 배열 반환, Awake/OnEnable 역할 분리

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] 빈칸 채우기
- 출처: 원문 4번
- 유형: 객관식
- 문제:
  - 아래 코드의 ①, ②에 들어갈 타입을 고르세요. 
  - 드롭다운에서 올바른 옵션을 선택해 **오류가 나지 않도록 배열 타입과 생성 타입을 수정**하세요.

### 자료(코드)

```csharp
using UnityEngine;

public class WeaponControl : MonoBehaviour
{
    [System.Serializable]
    public class Mount
    {
        public Transform turretMount;
        public Transform turretCache;
    }

    public ①[] tMounts = new ②[2];

    public void Start()
    {
        tMounts[0].turretMount = null;
        tMounts[1].turretMount = null;
    }
}
```
- 보기:
  - A. ① `Transform`, ② `Transform`
  - B. ① `Mount`, ② `Mount`
  - C. ① `GameObject`, ② `GameObject`
  - D. ① `WeaponControl`, ② `WeaponControl`

### [P02] 자식 Transform 반환 타입
- 출처: 원문 14번
- 유형: 객관식
- 문제:
  - 다음 메서드의 반환 타입으로 올바른 것을 고르세요.
  - ```csharp
    public 반환 타입 GetChildren(Transform tr)
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

### [P03] Awake/OnEnable 블록 순서
- 출처: 원문 26번
- 유형: 단답
- 문제:
  - 플레이어가 아닌 캐릭터의 손 오브젝트에 **소품(Prop)** 을 연결하는 구성 요소를 만들고 있습니다.
  - 소품 오브젝트에는 `PropSpecs` 컴포넌트가 붙어 있으며, 여기서 **damage / durability** 같은 데이터를 가져옵니다.
  - 장면이 시작될 때 소품과 소품 데이터가 준비되어야 하므로, **초기 데이터 읽기**가 필요합니다.
  - 이 구성 요소가 활성화(Enable)된 경우에만 소품을 캐릭터 손(`transform`)에 **부착(Parent 설정 + 위치/회전 맞춤)** 해야 합니다.
  - 아래 **코드 블록들을**, 올바른 순서로 배치해 스크립트를 완성하세요.
  ### 코드 블록(섞여 있음)

**블록 A**

```csharp
private void OnEnable() {
```

**블록 B**

```csharp
public class AttachProp : MonoBehaviour {

    public Transform prop;

    private PropSpecs propSpecs;

    private float damage;
    private float durability;

    private void Awake () {
```

**블록 C**

```csharp
        propSpecs = prop.GetComponent<PropSpecs>();

        this.damage = propSpecs.damage;
        this.durability = propSpecs.durability;
    }
```

**블록 D**

```csharp
        prop.parent = transform;
        prop.position = transform.localPosition;
        prop.rotation = transform.localRotation;
    }
}
```

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - 자식 Transform 배열 유틸 함수 작성
- 출처 개념: U05 Transform/Lifecycle
- 유형: 코드
- 문제:
  - `Transform root`를 받아 모든 직계 자식을 `Transform[]`로 반환하는 메서드 본문 핵심 3줄을 작성하세요.
  - (배열 생성, `for` 순회, `GetChild` 할당 포함)
- 의도: childCount/GetChild 패턴을 독립 구현으로 전이

### [X02] 함정 - 라이프사이클 배치 판별
- 출처 개념: U05 Transform/Lifecycle
- 유형: 객관식
- 문제:
  - 아래 중 가장 적절한 배치를 고르세요.
- 보기:
  - A. `OnEnable`에서 `GetComponent`로 초기 데이터 읽고, `Awake`에서 장착
  - B. `Awake`에서 데이터 읽고, `OnEnable`에서 장착
  - C. 둘 다 `Start`에만 배치
  - D. 둘 다 `Update`에 배치
- 의도: 초기화와 활성화 시점의 책임 분리

## 주차 체크
- 원문 대응 문항 수: 3
- 확장 문항 수: 2
- 총 문항 수: 5
