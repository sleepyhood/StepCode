# Unity U05 Transform 및 Lifecycle 기초

## 학습 목표
- 배열을 반환하는 함수의 반환형을 정확히 구분하고 작성합니다.
- `Awake`, `OnEnable`, `OnDisable`, `Start`의 역할 차이를 설명할 수 있습니다.
- 같은 오브젝트와 다른 오브젝트의 스크립트 참조 방법을 구분할 수 있습니다.

## 범위
- 키워드: 배열 반환형, 중첩 클래스, `Transform[]`, `childCount`, `GetChild`, `Awake`, `OnEnable`, `OnDisable`, `Start`, `GetComponent`, Inspector 참조 연결

## 먼저 큰 그림
이 단원은 크게 세 가지로 보면 쉽습니다.
- 첫째, 배열을 돌려주는 함수는 반환형도 배열이어야 합니다.
- 둘째, Unity 생명주기 함수는 이름이 비슷해 보여도 맡은 역할이 다릅니다.
- 셋째, 다른 스크립트에 접근할 때는 "같은 오브젝트인지, 다른 오브젝트인지"를 먼저 따져야 합니다.

왜 이걸 먼저 보나?
- W05 문제는 전부 따로 노는 것처럼 보여도, 실제로는 `타입을 정확히 선언했는가`, `라이프사이클 책임을 나눴는가`, `참조를 올바르게 가져왔는가`를 반복해서 묻습니다.
- 그래서 배열 타입, 생명주기 순서, 참조 방식 세 가지를 먼저 잡아야 합니다.

## 핵심 패턴
```csharp
public class AttachProp : MonoBehaviour
{
    public Transform prop;
    public GameManager gameManager;

    private PropSpecs propSpecs;

    private void Awake()
    {
        propSpecs = prop.GetComponent<PropSpecs>();
    }

    private void OnEnable()
    {
        prop.parent = transform;
        prop.position = transform.localPosition;
        prop.rotation = transform.localRotation;
    }
}
```

### 패턴 해설
- `public GameManager gameManager;`
  - 다른 오브젝트에 붙은 스크립트를 연결할 때 자주 쓰는 기본 형태입니다.
  - 이 경우 Inspector에서 직접 연결해 주는 방식이 자연스럽습니다.
- `private void Awake()`
  - `Awake`는 초기 준비와 캐싱에 어울립니다.
  - 자주 다시 바뀌지 않는 참조를 먼저 읽어 둘 때 유용합니다.
- `propSpecs = prop.GetComponent<PropSpecs>();`
  - 같은 오브젝트나 같은 참조 대상 안에서 컴포넌트를 찾을 때 `GetComponent`를 씁니다.
  - 즉, "이미 대상 오브젝트를 알고 있을 때 그 안의 다른 컴포넌트를 꺼내는 방식"입니다.
- `private void OnEnable()`
  - `OnEnable`은 오브젝트나 스크립트가 활성화될 때마다 다시 실행됩니다.
  - 그래서 화면 장착, 표시 갱신, 이벤트 연결처럼 반복 가능 동작에 잘 어울립니다.
- `prop.parent = transform;`
  - 실제 장착이나 위치 동기화 같은 시각적 적용은 `Awake`보다 `OnEnable`에 두면 역할이 더 분명해집니다.

### 생각 질문
왜 데이터 읽기와 실제 장착을 같은 함수 안에 몰아넣지 않고, `Awake`와 `OnEnable`로 나눠 두는 것이 더 안전할까요?

## 문항 핵심 포인트
### 1) 중첩 클래스 배열과 배열 반환형
이 개념을 알면 무엇이 쉬워지나?
- 커스텀 클래스 배열 문제와 `Transform[]` 반환형 문제를 함께 풀기 쉬워집니다.

- 개념:
  - 배열을 `return`하면 함수의 반환형도 배열이어야 합니다.
  - `Transform[] result`를 돌려준다면 반환형도 `Transform[]`입니다.
  - 중첩 클래스 안의 필드에 접근하려면 배열 원소 타입 자체가 그 중첩 클래스여야 합니다.
- 왜 헷갈리나?
  - 배열 안의 최종 필드가 `Transform`이라서, 배열 전체 타입도 `Transform[]`이라고 착각하기 쉽습니다.
  - `return result;`만 보고 원소 타입만 떠올리고, 배열 기호 `[]`를 빼먹는 경우가 많습니다.
- 어떻게 구별하나?
  - `tMounts[0].turretMount`가 가능하려면 `tMounts[0]` 자체가 `.turretMount`를 가진 타입이어야 합니다.
  - 따라서 이 경우 배열 타입은 `Transform[]`가 아니라 `Mount[]`입니다.
  - 반대로 `result` 자체가 `Transform` 배열이면 함수 반환형은 `Transform[]`입니다.
- 짧은 유사 예시:
  - `public Mount[] tMounts = new Mount[2];`
  - `public Transform[] GetChildren(Transform tr)`

### 자주 헷갈리는 비교
| 상황 | 올바른 타입 |
|---|---|
| `tMounts[0].turretMount`에 접근 | `Mount[]` |
| `result`가 `new Transform[childCount]` | `Transform[]` |
| 자식 하나만 반환 | `Transform` |
| 자식 여러 개를 배열로 반환 | `Transform[]` |

### 10초 점검
`return result;` 앞에서 `result`가 `Transform[]`라면, 함수 반환형 뒤에도 무엇이 붙어야 할까요?
- 정답 판단: `[]`

### 2) 자식 Transform 순회 패턴 (`childCount` + `GetChild`)
이 개념을 알면 무엇이 쉬워지나?
- X01 같은 자식 Transform 배열 반환 유틸 문제를 그대로 풀 수 있습니다.

- 개념:
  - `childCount`는 현재 부모의 직계 자식 수입니다.
  - `GetChild(i)`는 `i`번째 직계 자식을 가져옵니다.
  - 자식들을 배열에 모을 때는 보통 `배열 생성 -> for 순회 -> GetChild(i) 대입` 순서로 갑니다.
- 왜 헷갈리나?
  - 배열 길이를 임의 숫자로 넣거나, `Find` 같은 다른 API와 섞어 쓰기 쉽습니다.
  - `childCount`를 알고도 반복문의 끝 조건을 잘못 쓰는 경우가 있습니다.
- 어떻게 구별하나?
  - 먼저 `root.childCount` 크기로 배열을 만듭니다.
  - 그다음 `0`부터 `childCount - 1`까지 반복합니다.
  - 각 칸에 `root.GetChild(i)`를 넣습니다.
- 짧은 유사 예시:
  - `Transform[] result = new Transform[root.childCount];`
  - `for (int i = 0; i < root.childCount; i++)`
  - `result[i] = root.GetChild(i);`

### 실무 팁
- 자식 순회 문제는 먼저 "몇 개가 있나?"를 구하고, 그다음 "하나씩 넣는다"로 생각하면 코드 순서가 잘 안 꼬입니다.

### 생각 질문
왜 자식 수를 모른 채 배열을 먼저 만들면, 나중에 인덱스 오류나 누락이 생기기 쉬울까요?

### 3) 생명주기: `Awake`, `OnEnable`, `OnDisable`, `Start`
이 개념을 알면 무엇이 쉬워지나?
- 라이프사이클 블록 순서 배열 문제와 책임 분리 함정 문제를 동시에 대비할 수 있습니다.

- 개념:
  - `Awake`는 초기 준비와 캐싱에 자주 씁니다.
  - `OnEnable`은 활성화될 때마다 반복 실행되는 동작에 어울립니다.
  - `OnDisable`은 비활성화될 때 정리할 일이 있을 때 씁니다.
  - `Start`는 보통 `Awake`와 `OnEnable` 다음 시점의 초기 시작 로직에 자주 둡니다.
- 왜 헷갈리나?
  - `Awake`, `OnEnable`, `Start`가 모두 "처음에 실행되는 것처럼" 보여서 차이를 흐리게 외우기 쉽습니다.
  - `OnEnable`을 게임 시작 시 1회만 도는 함수처럼 오해하는 경우가 많습니다.
- 어떻게 구별하나?
  - 한 번 읽어 두면 되는 준비 데이터는 `Awake`
  - 켜질 때마다 다시 처리해야 하는 장착/표시/이벤트는 `OnEnable`
  - 꺼질 때 정리하는 것은 `OnDisable`
  - 초기 시작 로직은 `Start`
- 짧은 유사 예시:
  - `Awake`: `GetComponent<PropSpecs>()`로 스펙 캐싱
  - `OnEnable`: 손에 소품 장착
  - `OnDisable`: 이벤트 해제

### 자주 헷갈리는 비교
| 함수 | 주로 맡는 역할 |
|---|---|
| `Awake` | 초기 준비, 캐싱 |
| `OnEnable` | 활성화될 때마다 반복 동작 |
| `OnDisable` | 비활성화 시 정리 |
| `Start` | 초기 시작 로직 |

### 10초 점검
데이터를 한 번 읽어 두는 작업과, 켜질 때마다 손에 붙이는 작업 중 `OnEnable`에 더 어울리는 것은 어느 쪽일까요?
- 정답 판단: 켜질 때마다 손에 붙이는 작업

### 4) 같은 오브젝트 vs 다른 오브젝트의 스크립트 접근
이 개념을 알면 무엇이 쉬워지나?
- `GetComponent`를 써야 할 때와 Inspector 연결을 써야 할 때를 구분할 수 있습니다.

- 개념:
  - 같은 오브젝트에 붙은 다른 컴포넌트는 `GetComponent<클래스명>()`로 자주 가져옵니다.
  - 다른 오브젝트의 스크립트를 참조하려면 `public` 필드를 만들고 Inspector에서 연결하는 방식이 자주 쓰입니다.
- 왜 헷갈리나?
  - 다른 오브젝트의 스크립트도 무조건 `GetComponent`로 해결하려고 하기 쉽습니다.
  - `public` 필드를 만들었는데 Inspector 연결을 안 해서 `null` 참조가 나는 경우도 많습니다.
- 어떻게 구별하나?
  - 지금 찾는 대상이 "나와 같은 게임 오브젝트 안"에 있으면 `GetComponent`
  - "다른 게임 오브젝트"에 있으면 public 참조 필드 + Inspector 연결
- 짧은 유사 예시:
  - `GetComponent<GameManager>()`
  - `public GameManager gameManager;`

![GetComponent 동일 오브젝트 접근](../images/unity_u05_transform_lifecycle_getcomponent.png)
*캡션: 같은 오브젝트 안의 다른 컴포넌트에 접근할 때 `GetComponent`를 사용하는 상황을 보여주는 예시입니다. 출처: [Unity Scripting API - Component.GetComponent](https://docs.unity3d.com/ScriptReference/Component.GetComponent.html)*

### 생각 질문
왜 다른 오브젝트의 스크립트를 가져와야 하는데도 무조건 `GetComponent`만 쓰면 자주 막히게 될까요?

### 5) 라이프사이클 책임 분리 패턴
이 개념을 알면 무엇이 쉬워지나?
- P03과 X02 같은 블록 재배치 문제에서 어떤 코드를 어디에 두어야 하는지 빠르게 판단할 수 있습니다.

- 개념:
  - 무거운 초기 참조 읽기나 캐싱은 한 번만 실행되는 쪽에 두는 것이 안전합니다.
  - 시각적 장착이나 활성화 반응은 반복 실행 가능한 함수에 두는 것이 자연스럽습니다.
- 왜 헷갈리나?
  - 모든 코드를 `Start` 하나에 몰아 넣으면 일단 돌아가는 것처럼 보여서 역할 분리를 무시하기 쉽습니다.
  - `Update`에 계속 `GetComponent`를 넣는 나쁜 패턴을 떠올릴 수도 있습니다.
- 어떻게 구별하나?
  - 한 번 준비하고 끝나는가? -> `Awake`
  - 켤 때마다 다시 처리해야 하는가? -> `OnEnable`
  - 매 프레임 돌 필요가 있는가? -> 정말 필요한 경우만 `Update`
- 짧은 유사 예시:
  - `Awake`에서 `propSpecs = prop.GetComponent<PropSpecs>();`
  - `OnEnable`에서 `prop.parent = transform;`

## 자주 하는 실수
- 배열을 반환하는 함수인데 반환형에 `[]`를 빼먹습니다.
- `Mount` 배열이어야 할 곳을 `Transform[]`로 선언합니다.
- `OnEnable`을 게임 시작 시 1회 함수처럼 외웁니다.
- `Awake`와 `OnEnable`의 역할을 섞어 씁니다.
- 다른 오브젝트 참조까지 무조건 `GetComponent`로 해결하려고 합니다.
- public 참조 필드를 만들고도 Inspector 연결을 빼먹습니다.
- 자식 순회에서 `childCount`를 무시하고 임의 크기 배열을 만듭니다.

## 빠른 체크리스트
- 배열을 `return`하면 반환형에도 `[]`가 붙는지 확인했는가?
- 커스텀 클래스 내부 필드에 접근하려면 배열 원소 타입이 그 클래스인지 판단할 수 있는가?
- `childCount -> for -> GetChild(i)` 흐름을 재현할 수 있는가?
- `Awake`, `OnEnable`, `OnDisable`, `Start`의 역할 차이를 설명할 수 있는가?
- 같은 오브젝트는 `GetComponent`, 다른 오브젝트는 Inspector 연결이라는 구분을 이해하는가?
- 초기 캐싱과 시각적 장착을 서로 다른 생명주기 함수에 나눌 수 있는가?

## 미니 체크
### Q1
`tMounts[0].turretMount`가 가능하려면 `tMounts`의 원소 타입은 무엇이어야 할까요?
- 정답: `Mount`

### Q2
`Transform[] result`를 반환한다면 함수 반환형은?
- 정답: `Transform[]`

### Q3
직계 자식 수를 가져오는 `Transform` API 이름은?
- 정답: `childCount`

### Q4
활성화될 때마다 반복 실행되는 생명주기 함수는?
- 정답: `OnEnable`

### Q5
같은 오브젝트 안의 다른 컴포넌트를 가져올 때 자주 쓰는 함수는?
- 정답: `GetComponent`

### Q6
다른 게임 오브젝트의 스크립트를 연결할 때 자주 쓰는 방식은?
- 정답: `public` 참조 필드를 만들고 Inspector에서 연결

## 연결 세트
- 기초: unity_u05_transform_lifecycle_b01
- 챌린지: unity_u05_transform_lifecycle_c01
