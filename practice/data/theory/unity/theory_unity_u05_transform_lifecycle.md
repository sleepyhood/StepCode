# Unity U05 Transform 및 Lifecycle 기초

## 학습 목표
- 자주 발생하는 배열 반환형 문법 오류를 잡고 올바른 함수 반환형을 작성한다.
- `OnEnable`, `Awake`, `Start` 등 유니티 생명주기(Lifecycle) 이벤트 함수의 호출 시점과 특징을 구분한다.
- 서로 다른 스크립트의 클래스 객체에 접근하는 방법(GetComponent, Inspector 할당)을 이해하고 적용한다.

## 범위
- 키워드: 배열 반환형, OnEnable, OnDisable, Awake, Start, GetComponent, MonoBehaviour 참조

## 핵심 패턴
```csharp
public class Player : MonoBehaviour
{
    // 서로 다른 오브젝트의 스크립트(컴포넌트)에 접근하기 위해 public으로 선언
    public GameManager gameManager; 
    
    // 1. 객체가 비활성화 상태여도, 스크립트가 로드되는 최초 1회 무조건 실행
    private void Awake()
    {
        Debug.Log("Awake: Init");
    }

    // 2. 오브젝트가 켜질(활성화될) 때마다 매번 다시 실행
    private void OnEnable()
    {
        // 3. 나 자신(같은 게임오브젝트)에 붙어있는 다른 컴포넌트에 접근할 때 사용
        Transform myTransform = GetComponent<Transform>();
    }
}
```

## 문항 핵심 포인트

### 1) 배열을 반환하는 함수의 반환형 선언
- 개념: 함수가 배열 형태의 값을 `return`할 때에는, 함수의 정의부에도 반드시 반환형이 배열(예: `int[]`) 구조임을 명시해야 한다.
- 오답 포인트: 데이터는 배열(예: `new int[5]`)을 반환하면서, 함수 선언 부에는 `[]` 기호를 빼먹고 단일 자료형(예: `int`)으로 잘못 선언하는 경우이다.
- 정답 판별: 함수 선언부의 반환형 타입(예: `int[]`)과 실제 `return`하는 변수가 가지고 있는 자료형 타입이 동일한지 확인한다.

![배열 반환형 오류](./data/theory/images/unity_u05_array_return_error.svg)
*캡션: 반환형을 int[]가 아닌 int로 선언하였을 때 IDE에서 발생하는 CS0029 타입 변환 오류 코드 화면. 출처: 자체 제작*

### 2) 생명주기: OnEnable과 OnDisable 함수
- 개념: `OnEnable` 함수는 스크립트가 부착된 게임 오브젝트가 활성화(Active) 상태로 켜질 때마다 매번 실행되는 이벤트 함수이다. 반대로 오브젝트가 꺼지면 `OnDisable` 함수가 동작한다.
- 오답 포인트: 오브젝트를 처음 생성할 때 단 한번만 실행된다고 착각하거나, 스크립트를 코드로 `SetActive(true)` 하는 기능과 혼동하는 경우이다.
- 정답 판별: 객체가 켜지는 순간인지(혹은 인스펙터 체크박스가 켜지는 순간인지) 파악하고, 그때마다 해당 이벤트 함수가 반복해서 호출됨을 숙지했는지 묻는다.

![OnEnable 기능 확인](./data/theory/images/unity_u05_transform_lifecycle_onenable.png)
*캡션: 유니티 인스펙터 좌측 상단의 체크박스를 통해 오브젝트를 껐다 켤 때마다 OnDisable과 OnEnable 함수가 차례로 실행된다. 출처: 직접 캡처*

### 3) 생명주기: Awake 함수
- 개념: `Awake` 함수는 `Start` 함수보다 먼저 호출되는 함수로, 스크립트 컴포넌트의 체크박스가 **꺼져 있더라도(비활성화 상태여도) 오브젝트 자체가 켜져 있다면 최초 로드 시점에 무조건 1회 실행**되는 특수한 성질을 갖는다.
- 오답 포인트: 스크립트 체크박스(활성화/비활성화) 설정이 꺼져 있으면 `Awake` 마저 동작하지 않을 것이라 생각하는 경우이다. (`Start` 함수는 꺼져있으면 발생하지 않음)
- 정답 판별: 생명주기 호출 순서상 "Awake -> OnEnable -> Start" 순임을 인지하고, 스크립트 활성화 토글과 무관하게 `Awake`는 무조건 실행된다는 특징을 이해하는지 확인한다.

![Awake 함수 씬 실행 화면](./data/theory/images/unity_u05_transform_lifecycle_awake.png)
*캡션: 스크립트 컴포넌트 체크박스가 꺼져 있어도 Awake 함수 안의 코드는 예외적으로 실행됨을 보여주는 참조. 출처: 직접 캡처*

### 4) 다른 스크립트(컴포넌트)에 접근하는 방법
- 개념: 게임 진행을 위해 스크립트끼리 데이터를 주고받으려면 상대방의 참조(주소)를 가져와야 한다. 이때 접근 대상이 **나와 같은 오브젝트에 부착되어 있는지** 아니면 **서로 다른 오브젝트에 있는지**에 따라 방식이 나뉜다.
- 오답 포인트: 외부 다른 오브젝트의 스크립트에 접근할 때 단순히 `GetComponent`를 호출해서 Null エ러를 터뜨리거나, `public` 참조 필드로 만들어놓고 Inspector에서 직접 드래그 앤 드롭으로 연결해주지 않아 오류를 발생시키는 경우이다.
- 정답 판별: 
  - (1) 동일한 게임 오브젝트 내 다른 스크립트 가져오기: `GetComponent<클래스명>()`
  - (2) 아예 다른 게임 오브젝트의 스크립트 가져오기: `public 대상클래스명 변수명;` (이후 인스펙터 연결)
  두 가지 방식의 사용처를 제대로 구분하고 있는지를 판별한다.

![GetComponent 동일 오브젝트 접근](./data/theory/images/unity_u05_transform_lifecycle_getcomponent.png)
*캡션: 같은 오브젝트(Test) 안에 있는 스크립트 B의 참조를 가져오기 위해 GetComponent를 사용하는 모습. 출처: 직접 캡처*

![public 필드를 통한 참조 연결](./data/theory/images/unity_u05_transform_lifecycle_reference3.png)
*캡션: 서로 다른 오브젝트 간 연결을 위해 코드로 public B class_b; 를 선언한 뒤, 인스펙터 창에서 빈칸에 직접 대상 객체(Test2)를 끌어다 놓는 장면. 출처: 직접 캡처*

## 자주 하는 실수
- 배열을 반환하는 함수에서 반환형 끝에 대괄호(`[]`)를 빠뜨려 오류를 유발함
- `OnEnable`이 `Start`처럼 게임 시작 시 1회만 호출된다고 혼동함
- 스크립트 체크박스를 껐는데 왜 해당 스크립트 내부의 `Awake` 함수가 실행되냐며 디버깅을 해맴
- 다른 게임오브젝트 객체의 스크립트를 가져와야 하는데 엉뚱하게 `GetComponent`를 남발함

## 빠른 체크리스트
- 함수가 배열 값을 `return`할 때 반환형 이름 뒤에 `[]`를 정확히 기입했는가?
- 유니티 라이프사이클 3대장(`Awake`, `OnEnable`, `Start`)의 실행 순서와 특수한 실행 조건(스크립트 Disabled 상태)을 차이점 위주로 설명할 수 있는가?
- 같은 오브젝트 소속은 `GetComponent`, 다른 오브젝트 소속은 `public 변수 선언 후 인스펙터 연결`이라는 공식을 숙지했는가?

## 미니 체크
### Q1
반환값이 1차원 정수 배열(`new int[10]`) 형태인 함수를 선언할 때, 가장 올바른 반환형 표기는 무엇인가?
- 정답: `int[]`

### Q2
스크립트 컴포넌트의 체크박스를 해제(Disabled)해 둔 채로 게임을 실행했다. 해당 스크립트 안에 있는 `Awake` 함수 내부의 코드는 실행되는가?
- 정답: 예 (스크립트의 Enabled 설정과 무관하게, 게임 오브젝트 본체만 켜져 있다면 최초 1회 호출된다.)

### Q3
동일한 게임오브젝트에 부착되어 있는 `GameManager` 컴포넌트(스크립트)를 런타임에 C# 코드로 직접 가져오려 할 때 사용하는 내장 함수 이름은 무엇인가?
- 정답: `GetComponent<GameManager>()` (또는 GetComponent)

## 연결 세트
- 기초: unity_u05_transform_lifecycle_b01
- 챌린지: unity_u05_transform_lifecycle_c01
