# Unity U08 UI

## 학습 목표
- UI `Text` 컴포넌트를 코드로 연결하고, 문자열을 화면에 표시하는 기본 흐름을 이해합니다.
- 메서드 선언 시그니처에서 `반환형 + 메서드명 + 매개변수`를 정확히 맞추는 법을 익힙니다.
- `OnMouseUp()` 같은 유니티 내장 메시지 함수의 역할과 선언 형태를 구분합니다.
- `Button.onClick.AddListener(...)`를 어디에서 등록해야 안전한지 판단할 수 있습니다.

## 범위
- 키워드: `UnityEngine.UI`, `Text`, `.text`, `ToString()`, `Button`, `onClick.AddListener`, `OnMouseUp`, `Start`

## 먼저 큰 그림
이번 단원은 "UI 글자를 바꾸는 코드", "문자열을 받는 메서드 선언", "마우스 메시지 함수", "버튼 리스너 등록 위치"를 묻는 문제를 풀기 위한 단원입니다.

W08에서는 특히 아래 4가지를 바로 연결할 수 있어야 합니다.
- UI `Text`를 쓰려면 `using UnityEngine.UI;`, `public Text 변수;`, `.text = 문자열`이 필요합니다.
- `SetMessageToDisplay("게임 오버!")`가 되려면 선언부도 같은 이름과 매개변수를 가져야 합니다.
- 마우스를 눌렀다가 뗐을 때 자동 호출되는 함수는 `private void OnMouseUp()`입니다.
- `button.onClick.AddListener(콜백)`은 `Start()` 같은 1회성 초기화 구간에 등록해야 안전합니다.

![Text 컴포넌트 연결 구조](../images/unity_u08_ui_text_inspector.png)
*캡션: `Text` 컴포넌트를 스크립트의 public 변수에 Inspector로 연결하는 예시입니다. 출처: 직접 캡처*

## 핵심 패턴
```csharp
using UnityEngine;
using UnityEngine.UI;

public class UIManager : MonoBehaviour
{
    public Text myText;
    public Button button2;

    void Start()
    {
        int score = 50;
        myText.text = "Score: " + score.ToString();
        button2.onClick.AddListener(LightBulbOn);
    }

    public void SetMessageToDisplay(string stringToDisplay)
    {
        myText.text = stringToDisplay;
    }

    private void OnMouseUp()
    {
        gameObject.SetActive(!gameObject.activeSelf);
    }

    void LightBulbOn()
    {
        Debug.Log("Light On");
    }
}
```

이 패턴 안에는 W08의 핵심 답안 요소가 거의 다 들어 있습니다.
- `using UnityEngine.UI;`
- `public Text myText;`
- `myText.text = "Score: " + score.ToString();`
- `public void SetMessageToDisplay(string stringToDisplay)`
- `private void OnMouseUp()`
- `button2.onClick.AddListener(LightBulbOn);`

## 문항 핵심 포인트

### 1) UI Text에 점수 표시하는 3요소
이 개념을 알면 무엇이 쉬워지나?
- P01에서 요구하는 3개 코드를 한 번에 적을 수 있습니다.

- 개념: UI 글자를 코드로 바꾸려면 3단계가 필요합니다. 먼저 `using UnityEngine.UI;`로 UI 네임스페이스를 불러오고, 그다음 `Text` 변수를 선언해 Inspector에서 연결하며, 마지막으로 `.text`에 문자열을 넣어 화면을 갱신합니다.
- 왜 헷갈리나?: `Text` 타입 선언만 기억하고, 네임스페이스나 문자열 변환을 빠뜨리는 경우가 많습니다. 특히 `score`가 정수인데 그대로 넣으려다 에러가 나는 경우가 자주 나옵니다.
- 어떻게 구별하나?: 문제에서 "UI Text에 점수를 표시"하라고 하면 `네임스페이스`, `컴포넌트 변수`, `문자열 대입` 3요소가 모두 있는지 확인합니다.
- 짧은 유사 예시:
  ```csharp
  using UnityEngine.UI;
  public Text hpText;
  hpText.text = "HP: " + hp.ToString();
  ```
  점수 대신 체력을 표시하는 같은 구조입니다.

정답 판단:
- ① `using UnityEngine.UI;`
- ② `public Text myText;`
- ③ `myText.text = ("Score: " + score.ToString());`

10초 점검:
- `myText.text = score;`가 왜 틀릴까요?
- 답: `.text`에는 문자열이 들어가야 하므로 `score.ToString()` 같은 변환이 필요합니다.

### 2) 메서드 선언 시그니처 맞추기
이 개념을 알면 무엇이 쉬워지나?
- P02에서 `void`, `SetMessageToDisplay`, `(string stringToDisplay)`를 정확히 쓸 수 있습니다.

- 개념: 메서드가 컴파일 오류 없이 동작하려면 선언부의 `반환형`, `메서드명`, `매개변수`가 호출 코드와 본문에서 쓰는 이름에 모두 맞아야 합니다.
- 왜 헷갈리나?: 메서드 이름의 대소문자를 조금만 틀려도 다른 함수가 됩니다. 또 본문에서 `stringToDisplay`를 쓰는데 선언부 매개변수 이름을 다르게 적으면 연결이 끊깁니다.
- 어떻게 구별하나?: 호출부와 본문을 같이 봅니다. `SetMessageToDisplay("게임 오버!")`라고 호출하고, 본문에서 `stringToDisplay`를 쓴다면 선언은 그대로 맞춰야 합니다.
- 짧은 유사 예시:
  ```csharp
  public void ShowName(string playerName)
  {
      nameText.text = playerName;
  }
  ```
  호출부와 본문이 같은 이름을 공유해야 하는 예시입니다.

정답 판단:
- 반환형: `void`
- 메서드명: `SetMessageToDisplay`
- 매개변수: `(string stringToDisplay)`

생각 질문:
- 메서드명이 `setMessageToDisplay`처럼 소문자로 시작하면 왜 안 될까요?

### 3) `OnMouseUp()` 내장 메시지 함수
이 개념을 알면 무엇이 쉬워지나?
- P03에서 3칸을 `private`, `void`, `OnMouseUp`으로 바로 채울 수 있습니다.

- 개념: `OnMouseUp()`은 오브젝트 위에서 마우스 버튼을 눌렀다가 뗐을 때 유니티 엔진이 자동으로 호출하는 내장 메시지 함수입니다.
- 왜 헷갈리나?: `OnMouseDown`, `OnMouseEnter`, `OnMouseUp` 이름이 비슷해서 타이밍을 섞어 외우기 쉽습니다. 또 엔진이 알아서 호출해 주는 함수인데 `public`으로 써야 한다고 착각하기도 합니다.
- 어떻게 구별하나?: 문제에서 "눌렀다가 뗐을 때", "외부 스크립트에서 직접 호출할 필요 없음", "가장 좁은 접근 범위"가 보이면 `private void OnMouseUp()`입니다.
- 짧은 유사 예시:
  ```csharp
  private void OnMouseUp()
  {
      panelObject.SetActive(!panelObject.activeSelf);
  }
  ```
  패널 표시 상태를 토글하는 전형적인 예시입니다.

정답 판단:
- 접근 제한자: `private`
- 반환형: `void`
- 메서드명: `OnMouseUp`

자주 헷갈리는 비교:
- `OnMouseDown()`: 누르는 순간
- `OnMouseUp()`: 떼는 순간
- `OnMouseEnter()`: 마우스가 올라온 순간

### 4) `AddListener` 등록 위치와 중복 누적
이 개념을 알면 무엇이 쉬워지나?
- P04의 참거짓과 X01, X02를 동시에 해결할 수 있습니다.

- 개념: `button.onClick.AddListener(콜백)`은 호출될 때마다 리스너가 하나씩 추가됩니다. 그래서 `Start()`처럼 1회만 실행되는 초기화 메서드에 두는 것이 안전합니다.
- 왜 헷갈리나?: `Update()`가 가장 익숙한 반복 함수라서 거기에 넣고 싶어지기 쉽습니다. 하지만 이 경우 버튼을 클릭하기도 전에 리스너가 계속 쌓입니다.
- 어떻게 구별하나?: 문제에서 "1회만 등록", "중복 실행 방지", "가장 안전한 위치"를 묻는다면 `Start()`를 먼저 떠올립니다. `OnTriggerEnter2D()`는 물리 이벤트라서 UI 버튼 클릭과는 무관합니다.
- 짧은 유사 예시:
  ```csharp
  void Start()
  {
      button2.onClick.AddListener(LightBulbOn);
  }
  ```
  가장 기본적인 안전 등록 패턴입니다.

![AddListener 동작 원리 다이어그램](../images/unity_u08_ui_button_addlistener.svg)
*캡션: `AddListener`를 반복 호출하면 리스너가 누적되고, 1회 등록이면 클릭마다 콜백이 1번씩 실행되는 구조를 나타낸 그림입니다. 출처: 자체 제작*

직접 연결:
- `Start()`에서 등록하면 정상적으로 1번씩 실행됩니다.
- `OnTriggerEnter2D()`는 물리 충돌 이벤트이므로 UI 클릭과 같은 효과를 대신하지 못합니다.
- `Update()`에서 등록하면 동작은 하지만 리스너가 중복 누적되어 클릭 1회에 함수가 여러 번 실행됩니다.

실무 팁:
- `AddListener` 안에는 `LightBulbOn`처럼 메서드 이름만 넣습니다. `LightBulbOn()`처럼 괄호를 붙이면 "클릭할 때 실행할 함수"가 아니라 "지금 즉시 실행한 결과"를 넘기려는 형태가 됩니다.

## 자주 하는 실수
- `using UnityEngine.UI;`를 빼먹어 `Text` 타입을 인식하지 못합니다.
- `myText.text = score;`처럼 정수를 문자열 변환 없이 직접 넣습니다.
- `SetMessageToDisplay`의 대소문자를 틀려 호출과 선언이 서로 맞지 않습니다.
- `private void OnMouseUp()` 대신 `OnMouseDown()`이나 `public void OnMouseUp()`를 씁니다.
- `button.onClick.AddListener(MyFunc);`를 `Update()` 안에 넣어 리스너를 매 프레임 누적시킵니다.
- `button.onClick.AddListener(MyFunc());`처럼 괄호를 붙입니다.

## 빠른 체크리스트
- UI `Text`를 쓰기 위한 `using UnityEngine.UI;`를 적었는가?
- `Text` 컴포넌트를 받을 변수를 올바른 타입과 이름으로 선언했는가?
- `.text`에 들어가는 값이 문자열인지 확인했는가?
- 메서드 선언부의 이름과 매개변수 이름이 호출/본문과 정확히 일치하는가?
- `OnMouseUp()`의 의미가 "마우스를 뗄 때"임을 구별할 수 있는가?
- `AddListener`를 `Start()` 같은 1회성 구간에 등록했는가?

## 미니 체크
### Q1
점수 `score`를 UI에 `"Score: 값"` 형태로 표시하려면 어떤 대입문이 맞을까요?

- 정답: `myText.text = ("Score: " + score.ToString());`

### Q2
`SetMessageToDisplay("게임 오버!")`가 되려면 선언부의 반환형은 무엇이어야 할까요?

- 정답: `void`입니다.

### Q3
버튼 리스너를 한 번만 안전하게 등록하려면 보통 어디에 두는 것이 가장 적절할까요?

- 정답: `Start()` 같은 1회성 초기화 메서드입니다.

## 연결 세트
- 기초: `unity_u08_ui_b01`
- 챌린지: `unity_u08_ui_c01`
