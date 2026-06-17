# Unity 주차 문제지 W08

## 주차 주제
- 유닛: U08 UI
- 핵심 개념: UI Text 갱신 파이프라인, 메서드 선언 시그니처, OnMouseUp 메시지 함수, Button.onClick 등록 시점

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] UI Text에 점수를 표시하기 위한 필수 3요소 작성
- 출처: 원문 6번
- 유형: 단답
- 문제:
  - 게임 화면에 현재 점수(`score` 변수, 정수형)를 유니티 UI의 `Text` 컴포넌트를 통해 실시간으로 표시하려고 합니다. 아래 코드의 빈칸 ①, ②, ③에 들어갈 핵심 요소를 완성하세요.
  - 코드 예시:
    ```csharp
    // ① 필요한 네임스페이스 가져오기
    using (  ①  );

    public class ScoreBoard : MonoBehaviour {
        // ② 인스펙터에 노출할 텍스트 컴포넌트 변수 선언 (변수명: myText)
        (  ②  );
        
        public void UpdateScore(int score) {
            // ③ 텍스트 UI의 내용을 "Score: 점수" 형태로 갱신 (ToString() 명시 호출)
            (  ③  );
        }
    }
    ```
  - 답안 입력: 각 행의 그리드 입력 양식에 맞추어 작성해 주세요.

### [P02] 문자열 표시 메서드(SetMessageToDisplay) 선언 시그니처 완성
- 출처: 원문 7번
- 유형: 단답
- 문제:
  - 외부에서 `SetMessageToDisplay("게임 오버!")` 형태로 호출하면, 내부에서 `textToDisplay.text = stringToDisplay;` 코드를 실행하여 화면에 메시지를 띄우는 메서드를 만들려 합니다.
  - 아래 코드 빈칸 ①, ②, ③에 들어갈 요소를 순서대로 쉼표로 구분하여 작성하세요.
  - 코드 예시:
    ```csharp
    ( ① ) ( ② ) ( ③ ) 
    {
        textToDisplay.text = stringToDisplay;
    }
    ```
  - 답안 형식 예: `void, SetMessageToDisplay, string stringToDisplay`

### [P03] OnMouseUp 패널 토글 함수 선언부 완성
- 출처: 원문 16번
- 유형: 단답
- 문제:
  - 유니티에서 오브젝트 위에 마우스 버튼을 눌렀다가 뗐을 때 자동으로 호출되는 엔진 내장 메시지 함수를 선언하여 UI 패널 표시를 토글하려고 합니다.
  - 외부 노출을 차단하기 위한 가장 좁은 범위의 접근 제한자를 포함해 아래 코드 빈칸 ①, ②, ③에 들어갈 요소를 순서대로 쉼표로 구분하여 작성하세요.
  - 코드 예시:
    ```csharp
    ( ① ) ( ② ) ( ③ )() 
    { 
        panelObject.SetActive(!panelObject.activeSelf); 
    }
    ```
  - 답안 형식 예: `private, void, OnMouseUp`

### [P04] 버튼 이벤트 등록 위치에 따른 동작 참/거짓 판별
- 출처: 원문 30번
- 유형: 참거짓
- 문제:
  - 유니티 UI Button의 `onClick.AddListener(콜백함수)`를 등록하는 다음 3가지 시나리오의 참/거짓을 순서대로 쉼표로 구분하여 판별하세요.
  - 문장 1: 씬이 시작될 때 단 1회만 호출되는 `Start()` 내부에서 `button1.onClick.AddListener(MyFunc);`을 등록하면, 이후 `button1`을 클릭할 때마다 `MyFunc`이 정상적으로 1번씩 실행된다.
  - 문장 2: `OnTriggerEnter2D(Collider2D other)` 물리 감지 이벤트 안에서 `button3.onClick.AddListener(MyFunc3);`를 호출하면 UI 버튼 클릭과 동일한 효과를 얻을 수 있다.
  - 문장 3: 매 프레임 반복 호출되는 `Update()` 안에서 `button2.onClick.AddListener(LightBulbOn);`을 등록하면, 리스너가 매 프레임 중복 누적되어 클릭 1회에 `LightBulbOn`이 수십~수백 번 실행되는 부작용이 생기지만 동작 자체는 한다.
  - 답안 형식 예: `참, 거짓, 참`

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - UI 버튼 리스너 안전한 1회 등록 코드 선택
- 출처 개념: U08 UI
- 유형: 객관식
- 문제:
  - 씬 시작 시 단 1회만 안전하게 버튼 리스너를 등록하여 중복 실행 버그를 방지하려고 합니다. 변수 `Button button2` 클릭 시 `LightBulbOn` 메서드가 실행되도록 `Start()` 내부에 작성할 알맞은 한 줄 코드를 고르세요.
- 보기:
  - A. `button2.onClick(LightBulbOn);`
  - B. `button2.onClick.AddListener(LightBulbOn);`
  - C. `button2.onClick.AddListener(LightBulbOn());`
  - D. `button2.AddListener(LightBulbOn);`
- 의도: 반복 루프가 아닌 1회성 초기화 메서드에서 안전하게 리스너를 등록하는 표준 API 형태를 구별하도록 훈련합니다.

### [X02] 함정 - AddListener 최적 등록 위치 판별
- 출처 개념: U08 UI
- 유형: 객관식
- 문제:
  - 버튼 리스너(`AddListener`)를 단 한 번만 안전하게 등록하여 중복 호출 사고를 원천 차단하기 위해, 등록 코드를 배치할 가장 안전하고 적절한 유니티 생명주기 메서드를 고르세요.
- 보기:
  - A. `Update()`
  - B. `Start()`
  - C. `OnTriggerEnter2D()`
  - D. `LateUpdate()`
- 의도: 매 프레임 루프(Update/LateUpdate)나 조건부 이벤트(OnTriggerEnter2D) 배치 시의 중복 등록 위험을 인지하고 초기화 메서드를 분별합니다.

## 주차 체크
- 원문 대응 문항 수: 4
- 확장 문항 수: 2
- 총 문항 수: 6
