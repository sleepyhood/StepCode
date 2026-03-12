# Unity 주차 문제지 W11

## 주차 주제
- 유닛: U11 ECS
- 핵심 개념: ECS 실사용 판별 기준(`using` 선언 vs 실제 ECS 타입/시스템 사용)

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] 코드 3개 ECS 사용 여부 판별
- 출처: 원문 5번
- 유형: 단답
- 문제:
  아래 코드 조각이 **ECS libraries**(예: `Unity.Entities`)를 실질적으로 사용하는지 평가하시오.  
ECS를 사용하는 코드 조각은 **참**, 사용하지 않는 코드 조각은 **거짓**을 선택하시오.  
(각 문항별 **부분 점수** 가능)

### 보기(코드 조각)

#### [코드 1]

```csharp
using UnityEngine;
using System.Collections;

public class Fireball : MonoBehaviour
{
    public Rigidbody fireballPrefab;
    public Transform firePosition;
    public float fireballSpeed;
}

```

#### [코드 2]

```csharp
using Unity.Entities;
using UnityEngine;

public class ShieldComponent : MonoBehaviour
{
    public float Protection;
    public float Size;
}

```

#### [코드 3]

```csharp
using Unity.Entities;
using UnityEngine;

public class EnemyMovementSystem : ComponentSystem
{
    public Rigidbody Rigidbody;
    public InputComponent Inputcomponent;
}

```

### [P02] 코드 조각 ECS 사용 여부 T/F
- 출처: 원문 34번
- 유형: 단답
- 문제:
  참/거짓을 선택하여 각 코드 조각이 **ECS를 사용하는지 여부**를 판단하세요.

### 코드 조각 1

```csharp
using Unity.Entities;
using UnityEngine;

public class KeyboardComponent : MonoBehavior
{
    public float Horizontal;
    public float Vertical;
}
```

### 코드 조각 2

```csharp
using UnityEngine;
using System.Collections;

public class KeyboardScript : MonoBehaviour
{
    public class Wizard
    {
        public int fireballs;
        public int shields;
        public int missiles;
    }
}
```

### 코드 조각 3

```csharp
using UnityEngine;
using System.Collections;

public class Movement : MonoBehaviour
{
    public float speed;
    public float turnSpeed;

    void Update()
    {
        Movement();
    }
}
```


## 확장 문항 (변형/함정/응용)
### [X01] 변형 - ECS 실사용 최소 예시 작성
- 출처 개념: U11 ECS
- 유형: 코드
- 문제:
  - "ECS 라이브러리를 실제 사용한다"고 판정될 수 있도록 최소 1줄의 타입 선언 코드를 작성하세요.
  - 예: ECS 시스템 타입 또는 ECS 데이터 컴포넌트 타입을 직접 사용
- 의도: 판별 기준을 코드 작성으로 전이

### [X02] 함정 - `using Unity.Entities;`만 있을 때 판정
- 출처 개념: U11 ECS
- 유형: 객관식
- 문제:
  - 아래 설명 중 맞는 것을 고르세요.
- 보기:
  - A. `using Unity.Entities;`만 있으면 ECS 사용으로 본다.
  - B. `using Unity.Entities;`가 있고 클래스가 `MonoBehaviour`면 자동으로 ECS다.
  - C. ECS 타입(`IComponentData`, `SystemBase` 등) 또는 엔티티 처리 코드가 실제로 있어야 ECS 사용으로 본다.
  - D. 파일명에 ECS가 들어가면 ECS 사용으로 본다.
- 의도: 네임스페이스 선언만으로 참 처리하는 오개념 제거

## 주차 체크
- 원문 대응 문항 수: 2
- 확장 문항 수: 2
- 총 문항 수: 4
