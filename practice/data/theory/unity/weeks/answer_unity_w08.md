# Unity 주차 정답지 W08

## 메타
- 대상 문제지: `problem_unity_w08.md`
- 유닛: U08 UI

## 정답표
| 문항 ID | 정답 | 한 줄 근거 |
|---|---|---|
| P01 | ① `using UnityEngine.UI;` ② `public Text myText;` ③ `myText.text = ("Score: " + score.ToString());` | UI Text 사용 필수 3요소 |
| P02 | ① `void` ② `SetMessageToDisplay` ③ `(string stringToDisplay)` | 호출/본문과 시그니처 일치 |
| P03 | ① `private` ② `void` ③ `OnMouseUp()` | 요구 조건(내부 사용 + 클릭 업 이벤트) 충족 |
| P04 | 1 참, 2 거짓, 3 참 | 원문 30번 판단과 동일 |
| X01 | 예: `void Start() { button2.onClick.AddListener(LightBulbOn); }` | `Start` 1회 등록으로 중복 방지 |
| X02 | B | 일반적으로 `Start`에서 1회 등록 |

## 해설
### P01
- 개념 정의: UI `Text`를 쓰려면 네임스페이스, 타입 선언, `.text` 대입이 모두 필요합니다.
- 오답 포인트: `UnityEngine.Text`, `text`(소문자 타입), `settext` 같은 잘못된 멤버를 고르기 쉽습니다.
- 판별 기준: 3요소가 모두 정확한 문법으로 작성되었는지 확인합니다.

### P02
- 개념 정의: 메서드 호출 형태와 선언 시그니처(반환형/이름/매개변수)는 일치해야 합니다.
- 오답 포인트: 대소문자 다른 메서드명, 매개변수 이름 불일치로 본문 변수 참조 오류가 발생합니다.
- 판별 기준: `SetMessageToDisplay("...")` 호출과 `textToDisplay.text = stringToDisplay;` 본문을 동시에 만족해야 합니다.

### P03
- 개념 정의: `OnMouseUp()`은 마우스 버튼을 뗄 때 호출되는 Unity 메시지 함수입니다.
- 오답 포인트: `OnMouseEnter()`와 혼동하거나 접근 제한자를 문제 조건과 다르게 선택합니다.
- 판별 기준: `private void OnMouseUp()` 형태면 정답입니다.

### P04
- 개념 정의: `AddListener`는 등록 위치에 따라 동작 안정성이 달라집니다.
- 오답 포인트: `OnTriggerEnter2D`를 버튼 클릭 감지 함수로 오해하거나, `Update` 중복 등록 부작용을 놓칩니다.
- 판별 기준: 1 참, 2 거짓, 3 참을 정확히 구분합니다.

### X01
- 개념 정의: 버튼 리스너는 프레임 루프가 아닌 초기화 시점에 1회 등록하는 것이 기본입니다.
- 오답 포인트: `Update()` 등록으로 클릭 1회에 리스너가 누적 실행됩니다.
- 판별 기준: `Start/Awake/OnEnable` 중 하나에서 1회 `AddListener`를 호출하면 정답 처리 가능합니다.

### X02
- 개념 정의: 일반 UI 버튼은 초기화 구간에서 리스너를 연결합니다.
- 오답 포인트: `Update/LateUpdate` 같은 프레임 루프에 등록합니다.
- 판별 기준: 단일 정답은 `Start()`입니다.

## 운영 메모
- 다음 주차 이월 보강 포인트: UI 이벤트 해제(`RemoveListener`)와 `OnEnable/OnDisable` 패턴 연결
- 반복 오답 키워드: `Update` 중복 등록, `OnTriggerEnter2D` 용도 오해, 메서드명 대소문자
