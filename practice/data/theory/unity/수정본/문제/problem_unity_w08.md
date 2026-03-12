# Unity 주차 문제지 W08

## 주차 주제
- 유닛: U08 UI
- 핵심 개념: UI Text 갱신, 메서드 선언(반환형/이름/매개변수), OnMouseUp, Button.onClick 등록 시점

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] 점수 UI 코드 3요소 쓰기
- 출처: 원문 6번
- 유형: 단답
- 문제:
  코드 조각을 사용하여 **점수(score)를 UI 텍스트로 올바르게 표시**하세요.
올바른 코드 조각을 선택해 아래 코드의 빈칸(3곳)에 배치하여 코드를 완성하십시오.

### 자료(미완성 코드)

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ ① ]

public class ScoreManager : MonoBehaviour
{
    public int score = 0;

    [ ② ]

    public void Score(int points)
    {
        Debug.Log("Scored points");
        score += points;

        [ ③ ]
    }
}
```

### 드래그 토큰(선택지)

- `using UnityEngine.Text;`
- `using UnityEngine.UI;`
- `public text myText;`
- `public Text myText;`
- `myText.settext = ("Score: " + score.ToString());`
- `myText.text = ("Score: " + score.ToString());`

### [P02] SetMessageToDisplay 선언 완성
- 출처: 원문 7번
- 유형: 단답
- 문제:
  아래 클래스에서 `OnTriggerEnter(Collider other)` 안에서 `SetMessageToDisplay("...")`를 호출하고 있습니다.
이 호출에서 전달된 **문자열 인수**를 받아 `Text` 컴포넌트의 텍스트를 설정하는 **올바른 메서드 선언**을 완성하세요.

드롭다운 목록에서 알맞은 옵션을 선택해 코드를 완성하십시오.

### 자료(코드)

```csharp
using UnityEngine;
using UnityEngine.UI;

public class UnlockGate : MonoBehaviour
{
    public Text textToDisplay;

    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.CompareTag("Gate"))
        {
            other.gameObject.SetActive(false);
            SetMessageToDisplay("Congratulations! You have unlocked the gate!");
        }
        else
        {
            gameObject.SetActive(false);
            SetMessageToDisplay("Unfortunately, you have broken your key. You tried to unlock something other than a gate.");
        }
    }

    private [①] [②] [③]
    {
        textToDisplay.text = stringToDisplay;
    }
}
```

### 보기(드롭다운 후보 예)

- **① 반환형**: `bool`, `float`, `GameObject`, `int`, `void`
- **② 메서드명**: `setMessageToDisplay`, `SetMessageToDisplay`, `SetMessageTODisplay`, `setmessagetodisplay`
- **③ 매개변수**: `()`, `(string message)`, `(string "message")`, `(string stringToDisplay)`, `(string stringtodisplay)`, `(string messageToDisplay)`

### [P03] OnMouseUp 함수 선언 완성
- 출처: 원문 16번
- 유형: 단답
- 문제:
  게임 오브젝트(패널)를 **켜거나/끄는 함수(이 스크립트에서만 사용 가능)**를 만들어 달라는 요청을 받았습니다.
이 오브젝트는 장면에 있는 3D 오브젝트를 **마우스로 클릭**했을 때 토글 방식으로 제어됩니다.

아래 코드에서 메서드 선언부의 빈칸 3개에 들어갈 **올바른 코드 조각**을 선택해 배치하세요.

### 자료(코드)

```csharp
using UnityEngine;

public class TurnOnDisplay : MonoBehaviour
{
    public GameObject displayPane;

    private void Start()
    {
        displayPane.SetActive(false);
    }

    [ ① ] [ ② ] [ ③ ]
    {
        if (displayPane.activeInHierarchy == false)
        {
            displayPane.SetActive(true);
        }
        else
        {
            displayPane.SetActive(false);
        }
    }
}
```

### 드래그 토큰(선택지)

- `public`
- `private`
- `void`
- `MouseInfo`
- `OnMouseEnter()`
- `OnMouseUp()`

### [P04] 버튼 이벤트 등록 위치 T/F
- 출처: 원문 30번
- 유형: 단답
- 문제:
  아래 샘플 코드를 검토하세요. 그리고 아래 설명(1~3)이 **참인지 거짓인지** 선택하세요.
_(참고: 각 정답에 대해 부분 크레딧이 적립될 수 있습니다.)_

### 자료(코드)

```csharp
public class UILightOn : MonoBehaviour
{
    public Image lightAsset;
    public Button button1;
    public Button button2;
    public Button button3;

    void Start()
    {
        button1.onClick.AddListener(LightBulbOn);
    }

    void Update()
    {
        button2.onClick.AddListener(LightBulbOn);
    }

    void OnTriggerEnter2D(Collider2D collision)
    {
        button3.onClick.AddListener(LightBulbOn);
    }

    void LightBulbOn()
    {
        lightAsset.color = Color.green;
    }
}
```

### 문항

1. `onClick.AddListener`는 `Start` 함수 내부에서 호출되므로 `button1`은 `lightAsset`의 `color`를 녹색으로 바꿉니다.
2. `OnTriggerEnter2D` 함수는 버튼 누름을 감지하는 데 사용해야 하므로 `button3`만 `lightAsset`의 `color`를 녹색으로 바꿉니다.
3. `onClick.AddListener`는 `Update` 함수 내부에서 호출할 수 있으므로 `button2`는 `lightAsset`의 `color`를 녹색으로 바꿉니다.

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - UI 버튼 리스너 1회 등록 코드
- 출처 개념: U08 UI
- 유형: 코드
- 문제:
  - `button2` 클릭 시 `LightBulbOn`이 실행되도록, 중복 등록이 없게 리스너를 1회 등록하는 핵심 코드를 작성하세요.
- 의도: `Start/Awake/OnEnable` 1회 등록 원칙 적용

### [X02] 함정 - AddListener 등록 위치 선택
- 출처 개념: U08 UI
- 유형: 객관식
- 문제:
  - 일반적인 단일 버튼 리스너 등록 위치로 가장 적절한 것을 고르세요.
- 보기:
  - A. `Update()`
  - B. `Start()`
  - C. `OnTriggerEnter2D()`
  - D. `LateUpdate()`
- 의도: 매 프레임 중복 등록 실수 방지

## 주차 체크
- 원문 대응 문항 수: 4
- 확장 문항 수: 2
- 총 문항 수: 6
