# Unity U09 Animator

## 학습 목표
- Animator의 상태(State), 전환(Transition), 파라미터(Parameter) 구조를 문제 풀이 기준으로 구분합니다.
- 점프 클립을 물리적 순서에 맞게 배치하는 방법을 이해합니다.
- `SetInteger`, `SetFloat`, `SetBool`, `SetTrigger`를 인수 형태에 맞게 정확히 선택합니다.
- `animator.SetBool("Attacking", false);`처럼 인스턴스 변수로 호출하는 문법을 익힙니다.
- reset 전환에서 Trigger와 Bool 파라미터의 역할을 나누어 이해합니다.

## 범위
- 키워드: `Entry`, `Default State`, `Sub-State Machine`, `Any State`, `Transition`, `Has Exit Time`, `SetInteger`, `SetFloat`, `SetBool`, `SetTrigger`

## 먼저 큰 그림
이번 단원은 "어떤 애니메이션 클립을 어디에 놓는가", "상태 시스템이 어떻게 이어지는가", "파라미터 타입마다 어떤 `Set` 함수를 쓰는가"를 묻는 문제를 풀기 위한 단원입니다.

W09에서는 특히 아래 5가지를 바로 연결할 수 있어야 합니다.
- 점프 클립은 `정점 -> 느린 낙하 -> 빠른 낙하 -> 착지` 순서로 배치합니다.
- `Entry`는 시작점이고, `Default State`는 반드시 있어야 합니다.
- `Sub-State Machine`은 상태를 묶는 별도 그룹이며, 상태에서 그 안으로 전환할 수도 있습니다.
- `1 / .5f / false / 값 없음`을 보면 각각 `SetInteger / SetFloat / SetBool / SetTrigger`를 떠올려야 합니다.
- `Animator` 타입명이 아니라 `animator` 같은 실제 변수명으로 메서드를 호출해야 합니다.

![스테이트 머신 기본 구조](../images/unity_u09_animator_state_machine.png)
*캡션: Animator 창에서 `Entry`, 기본 상태, 상태 노드들이 어떻게 연결되는지 보여 주는 예시입니다. 출처: 직접 캡처*

## 핵심 패턴
```csharp
public class PlayerAnimController : MonoBehaviour
{
    private Animator animator;

    void Start()
    {
        animator = GetComponent<Animator>();
    }

    void Update()
    {
        animator.SetFloat("Speed", playerSpeed);

        if (Input.GetKeyDown(KeyCode.Space))
        {
            animator.SetTrigger("Search");
        }

        animator.SetBool("Attacking", false);
    }
}
```

이 패턴 안에는 W09의 핵심 답안 요소가 많이 들어 있습니다.
- `animator`는 `Animator` 타입의 인스턴스 변수입니다.
- Float 파라미터 `"Speed"`는 `SetFloat`로 바꿉니다.
- Trigger 파라미터는 값 없이 `SetTrigger("...")`로 발동합니다.
- Bool 파라미터는 `SetBool("...", true/false)`로 바꿉니다.

## 문항 핵심 포인트

### 1) 점프 상태 클립 배치
이 개념을 알면 무엇이 쉬워지나?
- P01에서 Z1~Z4에 어떤 클립을 놓아야 하는지 바로 고를 수 있습니다.

- 개념: 점프 애니메이션은 이름만 외우는 것이 아니라, 실제 움직임의 순서를 따라 읽어야 합니다. 최고 정점, 느린 낙하, 빠른 낙하, 착지 순서에 맞게 클립을 배치해야 자연스럽습니다.
- 왜 헷갈리나?: `SlowFall`과 `FastFall`은 둘 다 낙하라서 위치를 바꿔 쓰기 쉽고, `JumpApex`를 "점프니까 시작"처럼 잘못 생각할 수 있습니다.
- 어떻게 구별하나?: 문제에서 "정점"이 보이면 `JumpApex`, "천천히 떨어짐"이면 `SlowFall`, "빠르게 떨어짐"이면 `FastFall`, "착지"면 `FastLand`를 연결합니다.
- 짧은 유사 예시:
  - 달리기 점프라도 순서는 같습니다.
  - 정점 -> 느린 낙하 -> 빠른 낙하 -> 착지

정답 판단:
- Z1 `JumpApex`
- Z2 `SlowFall`
- Z3 `FastFall`
- Z4 `FastLand`

10초 점검:
- `FastLand`를 Z1에 놓으면 왜 어색할까요?
- 답: `FastLand`는 착지 순간 클립이라 정점 위치와 물리적 의미가 맞지 않기 때문입니다.

### 2) `Entry`, `Default State`, `Sub-State Machine`
이 개념을 알면 무엇이 쉬워지나?
- P02의 참거짓 4문장을 바로 판별할 수 있습니다.

- 개념: `Entry`는 Animator가 시작할 때 처음 들어갈 방향을 정하는 시작점입니다. `Default State`는 기본 시작 상태이며 반드시 존재합니다. `Sub-State Machine`은 여러 상태를 묶어 정리하는 별도의 그룹입니다.
- 왜 헷갈리나?: `Entry`와 `Default State`를 같은 것으로 생각하거나, `Sub-State Machine`은 폴더처럼 보이기만 하고 실제 전환은 안 된다고 오해하기 쉽습니다.
- 어떻게 구별하나?: 시작 관련 질문이면 `Entry`와 `Default State`를 봅니다. 상태를 묶는 구조냐를 묻는다면 `Sub-State Machine`입니다. 상태에서 서브 머신으로 선을 잇는 것도 가능합니다.
- 짧은 유사 예시:
  - `Entry -> Idle`은 가능합니다.
  - `Walk -> Combat Sub-State Machine` 전환도 가능합니다.

![전환 트랜지션 옵션 설정](../images/unity_u09_animator_transition_inspector.png)
*캡션: 상태 전환에서 조건과 전환 규칙을 설정하는 Inspector 예시입니다. 출처: 직접 캡처*

정답 판단:
- Entry에서 나가는 전환으로 시작 상태를 제어할 수 있습니다.
- 기본 상태는 없이 만들 수 없습니다.
- `Sub-State Machine`은 독립적인 그룹처럼 정리에 도움을 줍니다.
- 일반 상태에서 `Sub-State Machine`으로 전환하는 것도 가능합니다.

자주 헷갈리는 비교:
- `Entry`: 시작점
- `Default State`: 시작 시 실제로 들어가는 기본 상태
- `Sub-State Machine`: 상태 묶음 그룹
- `Any State`: 어디서든 끼어드는 특수 시작점

### 3) 파라미터 타입과 `Set` 함수 4종
이 개념을 알면 무엇이 쉬워지나?
- P03과 X01, X02를 동시에 해결할 수 있습니다.

- 개념: Animator 파라미터는 `Int`, `Float`, `Bool`, `Trigger` 네 종류가 있고, 각각 전용 함수가 있습니다.
  - `SetInteger("Animation", 1)`
  - `SetFloat("Animation", .5f)`
  - `SetBool("Animation", false)`
  - `SetTrigger("Animation")`
- 왜 헷갈리나?: 이름이 비슷해서 `Trigger`에도 `true`를 넣고 싶어지거나, `.5f`를 보고도 `SetInteger`를 고르는 실수가 생깁니다.
- 어떻게 구별하나?: 괄호 안 두 번째 값의 형태를 먼저 봅니다. 정수면 `SetInteger`, 실수면 `SetFloat`, 불리언이면 `SetBool`, 값이 없으면 `SetTrigger`입니다.
- 짧은 유사 예시:
  ```csharp
  animator.SetFloat("Speed", playerSpeed);
  ```
  `playerSpeed`가 실수형이므로 `SetFloat`를 씁니다.

정답 판단:
- ① `SetInteger`
- ② `SetFloat`
- ③ `SetBool`
- ④ `SetTrigger`

생각 질문:
- Trigger에 `SetBool("Search", true)`를 쓰면 왜 의도와 달라질까요?

### 4) `animator.SetBool("Attacking", false);` 읽기
이 개념을 알면 무엇이 쉬워지나?
- P04의 두 빈칸을 정확히 채울 수 있습니다.

- 개념: C#에서 메서드는 클래스 타입명이 아니라 실제 객체를 담은 변수로 호출합니다. 그래서 `Animator.SetBool(...)`가 아니라 `animator.SetBool(...)`처럼 인스턴스 변수명을 써야 합니다.
- 왜 헷갈리나?: `Animator`와 `animator`가 글자 하나 차이라서 클래스명과 변수명을 섞기 쉽습니다.
- 어떻게 구별하나?: 점 앞에 오는 것이 "타입 이름"인지 "실제로 값을 들고 있는 변수"인지 확인합니다. 문제에서 `Animator animator;`가 선언되어 있다면 호출 주체는 `animator`입니다.
- 짧은 유사 예시:
  ```csharp
  animator.SetBool("Attacking", false);
  ```
  `"Attacking"`이라는 Bool 파라미터를 `false`로 바꾸는 코드입니다.

정답 판단:
- ① `animator`
- ② `("Attacking", false)`

실무 팁:
- Animator 파라미터 이름은 대소문자까지 정확히 맞아야 합니다. `"attacking"`처럼 다르게 쓰면 연결되지 않습니다.

### 5) reset 전환용 파라미터 역할 나누기
이 개념을 알면 무엇이 쉬워지나?
- P05에서 `Search`와 `Friendly`를 역할에 맞게 고를 수 있습니다.

- 개념: reset 전환에서는 "한 번 발동하는 신호"와 "계속 유지되는 상태값"을 나눠 생각해야 합니다. Trigger는 1회성 발동에, Bool은 상태 유지/해제에 어울립니다.
- 왜 헷갈리나?: `Search`, `Friendly`, `Attack`, `Speed`처럼 이름만 보고 막 고르면 Trigger 역할과 Bool 역할이 뒤바뀌기 쉽습니다.
- 어떻게 구별하나?: 문제 문장에서 `발동시키고`라고 하면 Trigger를, `false로 전환`이라고 하면 Bool을 찾습니다.
- 짧은 유사 예시:
  - Trigger: 한 번 눌러서 전환 시작
  - Bool: 켜짐/꺼짐 상태 유지

정답 판단:
- Trigger 파라미터: `Search`
- Bool 파라미터: `Friendly`

## 자주 하는 실수
- `JumpApex`를 정점이 아니라 점프 시작 위치에 놓습니다.
- `Default State` 없이도 Animator를 만들 수 있다고 착각합니다.
- `.5f`를 넘기면서 `SetInteger`를 고릅니다.
- `animator` 대신 `Animator.SetBool(...)`처럼 타입명을 호출 주체로 씁니다.
- Trigger 파라미터인데 `SetBool("Search", true)`를 씁니다.
- `Friendly`와 `Search`의 역할을 뒤바꿉니다.

## 빠른 체크리스트
- 점프 클립을 물리적 순서대로 배치할 수 있는가?
- `Entry`와 `Default State`의 차이를 설명할 수 있는가?
- `Sub-State Machine`으로 상태를 묶고, 상태에서 그 안으로 전환할 수 있음을 아는가?
- `1 / .5f / false / 값 없음`을 보고 각각 맞는 `Set` 함수를 고를 수 있는가?
- `animator.SetBool("Attacking", false);`를 완전한 문장으로 재현할 수 있는가?
- reset 전환에서 Trigger와 Bool의 역할을 구분할 수 있는가?

## 미니 체크
### Q1
`animator.[빈칸]("Animation")`처럼 값 없이 발동만 시키는 함수는 무엇일까요?

- 정답: `SetTrigger`입니다.

### Q2
`Animator animator;`가 선언되어 있을 때, `"Attacking"` Bool 값을 끄는 완전한 코드는 무엇일까요?

- 정답: `animator.SetBool("Attacking", false);`

### Q3
점프 정점 자리에 가장 어울리는 클립은 무엇일까요?

- 정답: `JumpApex`입니다.

## 연결 세트
- Basic: `unity_u09_animator_b01`
- Challenge: `unity_u09_animator_c01`
