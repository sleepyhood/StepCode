# Unity U03 함수/static 기초

## 학습 목표
- 올바른 함수 선언 형식을 구분하고 작성합니다.
- 반환형, 매개변수, `return`의 관계를 설명할 수 있습니다.
- `static` 멤버의 사용 규칙과 문맥 충돌 원리를 이해합니다.

## 범위
- 키워드: 반환형, 매개변수, `void`, `null`, 메서드 시그니처, 일반 함수, 이벤트 함수, `static` 메서드, `static` 필드

## 먼저 큰 그림
이 단원은 크게 세 덩어리로 보면 쉽습니다.
- 첫째, 함수 선언부를 어떤 순서로 쓰는지입니다.
- 둘째, 함수가 값을 돌려주는지, 어떤 값을 받아들이는지입니다.
- 셋째, `static`이 붙은 멤버가 무엇을 할 수 있고 무엇을 못 하는지입니다.

왜 이걸 먼저 보나?
- W03 문제는 겉보기에는 참/거짓, 빈칸, 시그니처 작성 문제로 나뉘지만, 실제로는 `함수 문법`과 `static 문맥`을 반복해서 묻습니다.
- 그래서 "함수는 어떻게 선언되는가"와 "`static`은 누구에게 접근할 수 있는가"를 먼저 잡아야 합니다.

## 핵심 패턴
```csharp
public class Example
{
    static float statFloat = 0f;
    int count = 3;

    private static int Add(int a, int b)
    {
        return a + b;
    }

    private static void ResetStat()
    {
        statFloat = 1f;
    }

    private void ShowCount()
    {
        Debug.Log(count);
    }
}
```

### 패턴 해설
- `private static int Add(int a, int b)`
  - 메서드 선언은 보통 `접근제어자 -> 지정자(static) -> 반환형 -> 메서드명 -> 매개변수` 순서로 읽으면 됩니다.
  - 반환형이 `int`이므로, 본문 끝나기 전에 `int` 값이 `return`되어야 합니다.
- `(int a, int b)`
  - 매개변수는 함수 바깥에서 값을 전달받는 자리입니다.
  - 같은 타입 두 개도 가능하고, 서로 다른 타입 여러 개도 가능합니다.
- `static float statFloat = 0f;`
  - `static` 필드는 객체마다 따로 생기지 않고, 클래스 기준으로 하나만 둡니다.
- `private static void ResetStat()`
  - `static` 메서드 안에서는 같은 `static` 멤버에는 바로 접근할 수 있습니다.
  - 반대로 `count`처럼 인스턴스 멤버에는 객체 없이 바로 접근할 수 없습니다.
- `private void ShowCount()`
  - `static`이 없는 일반 메서드는 객체에 속한 값(`count`)을 자연스럽게 다룰 수 있습니다.

### 메서드 시그니처 순서 규칙
C# 메서드를 선언할 때는 아래 순서를 기억하면 안전합니다.

> **접근제어자** -> **지정자(static 등)** -> **반환형** -> **메서드명** -> **(매개변수 목록)**

예를 들어 `private static int Add(int a, int b)`를 분해하면 다음과 같습니다.

| 순서 | 역할 | 코드 |
|---|---|---|
| 1 | 접근제어자 | `private` |
| 2 | 지정자 | `static` |
| 3 | 반환형 | `int` |
| 4 | 메서드명 | `Add` |
| 5 | 매개변수 | `(int a, int b)` |

시험에서 시그니처를 직접 작성하라는 문항이 나오면, 이 5단계 순서를 떠올리고 조립하면 됩니다.

### 생각 질문
왜 `private static int Multiply(int a, int b)`에서 `Multiply` 앞에 `int`가 오고, 뒤가 아니라 앞에 올까요?

## 문항 핵심 포인트
### 1) 함수의 반환형과 매개변수
이 개념을 알면 무엇이 쉬워지나?
- 함수 설명 참/거짓 문제와 시그니처 작성 문제를 함께 풀기 쉬워집니다.

- 개념:
  - 함수는 반환형과 매개변수를 가질 수 있습니다.
  - 반환형은 함수가 끝날 때 돌려주는 값의 종류입니다.
  - 매개변수는 함수가 실행될 때 바깥에서 전달받는 값의 자리입니다.
  - 반환형이 `void`라면 돌려줄 값이 없다는 뜻입니다.
  - 하나의 함수 안에 서로 다른 타입의 매개변수를 여러 개 둘 수 있습니다.
- 왜 헷갈리나?
  - `void`를 `null`과 같은 뜻으로 오해하기 쉽습니다.
  - 반환형이 `int`나 `float`인데도 `return` 없이 끝내는 실수가 자주 나옵니다.
  - 매개변수는 하나의 타입만 받을 수 있다고 좁게 외우는 경우도 있습니다.
- 어떻게 구별하나?
  - `void`는 "값이 없음"이고, `null`은 "비어 있는 참조값"입니다.
  - `void`가 아닌 반환형이면, 끝나기 전에 그 타입의 값을 `return`해야 합니다.
  - 매개변수는 `int`, `string`, `bool`처럼 서로 다른 타입을 쉼표로 나눠 함께 선언할 수 있습니다.
- 짧은 유사 예시:
  - `void ShowMessage(string msg)`
  - `int GetScore() { return 10; }`
  - `void SetPlayer(string name, int hp, bool isAlive)`

![함수 반환형 및 매개변수 오류](../images/unity_u03_function_return_error.svg)
*캡션: 반환형이나 매개변수가 맞지 않을 때 IDE에서 어떤 종류의 컴파일 오류가 생기는지 보여주는 예시입니다. 출처: [Microsoft C# 문서 - Compiler Errors](https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/compiler-messages/)*

### 자주 헷갈리는 비교
| 비교 | 구별 기준 |
|---|---|
| `void` vs `null` | `void`는 반환값 없음, `null`은 비어 있는 참조값 |
| 반환형 vs 매개변수 | 반환형은 함수가 내보내는 값, 매개변수는 함수가 받는 값 |
| `int GetX()` vs `void GetX()` | 앞은 값을 돌려줘야 하고, 뒤는 값 없이 끝날 수 있음 |

### 10초 점검
`void` 함수가 `null`을 반환한다는 말은 맞을까요?
- 정답 판단: 아닙니다. `void`는 반환값 자체가 없는 상태입니다.

### 2) 일반 함수와 유니티 이벤트 함수
이 개념을 알면 무엇이 쉬워지나?
- "함수는 호출되지 않으면 실행되지 않는다"는 원칙과 Unity 예외 상황을 함께 구별할 수 있습니다.

- 개념:
  - 일반 함수는 다른 코드가 직접 호출해야 실행됩니다.
  - Unity의 일부 함수(`Start()`, `Update()` 등)는 엔진이 정해진 시점에 자동 호출합니다.
- 왜 헷갈리나?
  - "함수는 항상 직접 호출해야 한다"는 일반 규칙만 외우면 Unity 이벤트 함수를 놓치기 쉽습니다.
  - 반대로 Unity 이벤트 함수도 아무 때나 자동 실행된다고 넓게 오해할 수 있습니다.
- 어떻게 구별하나?
  - 내가 이름을 정해서 만든 일반 함수는 직접 호출이 필요합니다.
  - Unity가 약속한 이름과 시점이 있는 함수는 엔진이 자동 호출합니다.
  - 즉, 일반 함수의 원칙은 "직접 호출", Unity 이벤트 함수의 예외는 "엔진 자동 호출"입니다.
- 짧은 유사 예시:
  - `ShowMessage()`는 다른 코드가 불러야 실행됩니다.
  - `Start()`는 스크립트 시작 시 자동 실행됩니다.
  - `Update()`는 매 프레임 자동 실행됩니다.

```csharp
using UnityEngine;

public class Player : MonoBehaviour
{
    void Start()
    {
        Debug.Log("Game Start!");
    }

    void Update()
    {
        // 매 프레임 반복
    }
}
```

![유니티 이벤트 함수 호출 시점](../images/unity_u03_function_event_execution_order.svg)
*캡션: Unity가 `Start`와 `Update` 같은 이벤트 함수를 어떤 흐름에서 자동 호출하는지 보여주는 예시입니다. 출처: [Unity Manual - Order of execution for event functions](https://docs.unity3d.com/Manual/ExecutionOrder.html)*

### 생각 질문
일반 함수는 직접 호출해야 하는데, 왜 `Start()`와 `Update()`는 따로 부르지 않아도 실행될까요?

### 3) static 필드와 static 메서드
이 개념을 알면 무엇이 쉬워지나?
- static 접근 오류 수정 문제와 함수/static 오개념 판별 문제를 안정적으로 풀 수 있습니다.

- 개념:
  - `static`이 붙은 멤버는 객체를 만들지 않아도 클래스 기준으로 접근할 수 있습니다.
  - `static`이 없는 멤버는 인스턴스에 속합니다.
  - `static` 메서드 안에서 값을 직접 바꾸려면, 그 대상도 `static`이어야 합니다.
- 왜 헷갈리나?
  - 같은 클래스 안에 있으니 아무 변수나 바로 쓸 수 있다고 생각하기 쉽습니다.
  - `static` 메서드와 일반 필드가 같은 위치에 보이기 때문에 문맥 차이를 놓치기 쉽습니다.
- 어떻게 구별하나?
  - 현재 메서드가 `static`이면, 우선 "나는 객체 없이 실행 중"이라고 생각합니다.
  - 객체 없이 실행 중이라면 인스턴스 필드는 바로 만질 수 없습니다.
  - 따라서 `static` 메서드 안에서 직접 접근하려면 대상 필드도 `static`이어야 합니다.
- 짧은 유사 예시:
  - `private static void ResetStat() { statFloat = 1f; }`
  - `private static void WrongAccess() { count = 1; }` 는 문맥 오류입니다.
  - `private void ShowCount() { Debug.Log(count); }` 는 일반 메서드이므로 가능합니다.

![static 멤버 접근 오류](../images/unity_u03_function_static_access_error.svg)
*캡션: `static` 메서드 안에서 인스턴스 필드에 직접 접근하려 할 때 어떤 오류가 생기는지 보여주는 예시입니다. 출처: [Microsoft C# 문서 - Static Classes](https://learn.microsoft.com/ko-kr/dotnet/csharp/programming-guide/classes-and-structs/static-classes-and-static-class-members)*

### 자주 헷갈리는 비교
| 비교 | 구별 기준 |
|---|---|
| `static` 메서드 | 객체 없이 클래스 기준으로 실행 |
| 인스턴스 메서드 | 객체에 속한 상태를 다룸 |
| `static` 필드 | 클래스에 하나 |
| 인스턴스 필드 | 객체마다 따로 존재 |

### 10초 점검
`private static void ThisStat()` 안에서 `float statFloat`를 바로 수정하려면, 그 필드에는 무엇이 필요할까요?
- 정답 판단: `static`

### 4) 함수 시그니처 조립 요령
이 개념을 알면 무엇이 쉬워지나?
- X01 같은 "선언부 첫 줄 완성" 문제를 순서대로 조립할 수 있습니다.

- 개념:
  - 시그니처는 함수의 첫 줄 문법입니다.
  - 요구사항을 순서대로 끼워 넣으면 정확한 선언부를 만들 수 있습니다.
- 왜 헷갈리나?
  - `static` 위치를 빼먹거나, 반환형과 메서드명 순서를 바꾸기 쉽습니다.
  - 조건을 다 읽고도 한 요소를 빠뜨리는 경우가 많습니다.
- 어떻게 구별하나?
  - 먼저 접근제어자를 둡니다.
  - 다음에 `static` 같은 지정자를 둡니다.
  - 그다음 반환형, 메서드명, 매개변수 순서로 붙입니다.
- 짧은 유사 예시:
  - 요구: `private`, `static`, `int`, `Multiply`, `int a`, `int b`
  - 결과: `private static int Multiply(int a, int b)`

### 실무 팁
- 시그니처 작성 문제는 처음부터 한 줄을 통째로 쓰지 말고, 머릿속에서 다섯 칸을 만든 뒤 채워 넣으면 실수가 줄어듭니다.

## 자주 하는 실수
- `void`와 `null`을 같은 뜻으로 오해합니다.
- 반환형이 있는 함수에서 `return`을 빼먹습니다.
- 서로 다른 자료형의 매개변수를 함께 둘 수 없다고 생각합니다.
- 일반 함수와 Unity 이벤트 함수를 모두 같은 규칙으로만 외웁니다.
- `static` 메서드 안에서 인스턴스 필드를 객체 없이 직접 수정하려고 합니다.
- 시그니처에서 `static`, 반환형, 메서드명 순서를 섞어 씁니다.

## 빠른 체크리스트
- 반환형이 `void`가 아니라면 `return`이 필요한 이유를 설명할 수 있는가?
- `void`와 `null`의 차이를 말할 수 있는가?
- 서로 다른 자료형의 매개변수를 한 함수 안에 함께 둘 수 있는가?
- 일반 함수와 Unity 이벤트 함수의 실행 방식을 구분할 수 있는가?
- `static` 메서드 안에서 어떤 필드에 바로 접근할 수 있는지 판단할 수 있는가?
- `private static int Multiply(int a, int b)` 같은 시그니처를 순서대로 조립할 수 있는가?

## 미니 체크
### Q1
반환값이 없는 함수의 반환형은 무엇인가?
- 정답: `void`

### Q2
`void`와 `null`은 같은 뜻인가?
- 정답: 아니다

### Q3
서로 다른 자료형의 매개변수를 한 함수 안에 함께 선언할 수 있는가?
- 정답: 가능하다

### Q4
유니티 스크립트에서 매 프레임마다 자동으로 호출되는 함수는 무엇인가?
- 정답: `Update`

### Q5
`static` 메서드가 인스턴스 필드를 바로 접근할 수 있는가?
- 정답: 아니오

### Q6
`private`, `static`, `int`, `Multiply`, `(int a, int b)`를 순서대로 조립한 선언부는?
- 정답: `private static int Multiply(int a, int b)`

## 연결 세트
- 기초: unity_u03_function_syntax_b01
- 챌린지: unity_u03_function_syntax_c01
