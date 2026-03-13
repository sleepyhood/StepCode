# Unity U10 Material and Color

## 학습 목표
- 머티리얼(Material)을 통해 게임 오브젝트의 외형(색깔)이 적용되는 원리를 이해한다.
- `Renderer` 컴포넌트에서 코드로 `Material`에 접근하여 색상(`Color`) 값을 동적으로 변경한다.
- 런타임에 색상 변환과 `Time.deltaTime`을 엮어 주기적인 비주얼 이벤트를 작성할 수 있다.

## 범위
- 키워드: Material, Renderer, SetColor, Color 타입

## 핵심 패턴
```csharp
public class ColorChanger : MonoBehaviour
{
    private Material mat;

    void Start()
    {
        // 1. 오브젝트 외형을 담당하는 Renderer 컴포넌트 가져오기
        Renderer myRenderer = GetComponent<Renderer>();
        
        // 2. 렌더러가 현재 쓰고 있는 머티리얼 참초 연결
        mat = myRenderer.material;     

        // 3. 머티리얼의 메인 컬러 속성("_Color" 또는 "_BaseColor")을 코드로 칠하기
        mat.SetColor("_BaseColor", Color.red);          
    }
}
```

## 문항 핵심 포인트

### 1) 오브젝트의 색상(Material) 조작 원리
- 개념: 유니티에서 게임오브젝트 겉면의 색상이나 질감은 `Material` 에셋 파일이 결정하고, 이 머티리얼을 오브젝트 표면에 씌워주는 코팅지 역할을 하는 것이 `Renderer(MeshRenderer 등)` 컴포넌트다. 따라서 코드로 오브젝트 큐브의 색깔을 파란색으로 스크립트 도중 바꾸려면, 먼저 해당 오브젝트에 붙은 `Renderer`를 받아온 뒤(`.GetComponent<Renderer>()`), 그 렌더러가 사용하는 `.material` 속성에 다시 접근하여 `Color` 객체를 덮어씌워 줘야 한다.
- 오답 포인트: `Renderer`를 거치지 않고 게임오브젝트(`.gameObject.color = ...`) 자체나 `Transform`에 대고 곧바로 색상 변경을 시도해서 컴파일 오류가 발생하는 경우이다.
- 정답 판별: **`Renderer` -> `.material` -> `.color (또는 SetColor)`** 의 접근 3단계 체인 방식을 코드 단에서 올바르게 호출했는지 확인한다.

![머티리얼 컴포넌트 체인](../images/unity_u10_material_color_renderer.svg)
*캡션: Cube 오브젝트 안의 MeshRenderer 컴포넌트를 거쳐 Materials 배열의 Main Color 속성에 도달해야 색상이 변경된다는 구조 모식도. 출처: 자체 제작*

### 2) Color 클래스와 SetColor 함수 사용법
- **Color 변수 출력과 디버깅 (P01 대비)**:
  - `Debug.Log` 등으로 색상을 출력할 때에는 타입 이름(`Color`)이 아니라 실제 데이터가 담긴 **인스턴스 변수명**을 사용해야 한다.
  - 예: `public Color myColor;` -> `Debug.Log(myColor);` (RGBA 수치 출력)
  - 만약 `Debug.Log(Color);` 라고 적으면 타입명 자체를 출력하려 하므로 오류가 나거나 의미 없는 값이 나온다.

### 3) SetColor 함수와 문자열 프로퍼티명 (P02, X02 대비)
- 개념: `mat.SetColor(속성명, 색상)` 함수를 쓸 때 첫 번째 인자인 '속성명'은 반드시 **쌍따옴표로 감싼 문자열("_Color")** 형태여야 한다.
- **문자열의 중요성**:
  - `mat.SetColor(_Color, ...)` — (X) 따옴표가 없으면 C#은 `_Color`라는 이름의 변수를 찾으려다 컴파일 에러를 낸다.
  - `mat.SetColor("_Color", ...)` — (O) 문자열로 넘겨야 셰이더 내부의 이름을 검색할 수 있다.
- **언더스코어`_` 관례**: 유니티 기본 셰이더(Standard)의 메인 색상 프로퍼티명은 관례적으로 언더스코어로 시작하는 `"_Color"`이다. (`"Color"`라고 쓰면 셰이더가 인식하지 못해 색이 안 바뀔 수 있다.)
- 정답 판별: 미리 정의된 색상 상수는 `Color.xxx` 형식을 지켰는지 판단하며, 접근 키워드가 **쌍따옴표 + 언더스코어**를 포함한 문자열 형태인지 식별한다.

### 4) 런타임 주기적 색상 변경 (응용)
- 개념: `Update` 문 안에서 타이머 변수(`m_Time += Time.deltaTime`)를 활용해 일정 초가 지날 때마다 색상 배열이나 랜덤 Color 값을 렌더러에 대입하게 되면, 클러빙 효과나 무적 상태(깜빡임) 비주얼 처리를 매우 손쉽게 코딩 단 한 줄로 구현할 수 있다.
- 오답 포인트: `Time.deltaTime`을 업데이트 문에서 쓰는데 실수로 `+=`가 아니라 `=`으로 대입해서 타이머가 영원히 특정 시간(예: `0.01초`)에만 머물러 색이 안 바뀌는 루프.
- 정답 판별: 시간 축적(누적 변수)과 머티리얼 속성 조작 코드가 연결될 때 문법적 결함을 체크한다.

## 자주 하는 실수
- MeshRenderer에서 머티리얼 참조본(`.material`)을 안 따오고 원본 에셋(`.sharedMaterial`)을 바꾸려다가 씬(Scene) 전체의 큐브 색깔이 단체로 다 같이 시뻘겋게 변해버림
- `new Color(255f, 0, 0)` 로 포토샵 색칠하듯이 숫자를 부어버림. (유니티 퍼센트 비율 체계는 0.0f ~ 1.0f가 100% 임)

## 빠른 체크리스트
- `GetComponent<Renderer>()` 계열을 거치지 않으면 에셋의 색상 프로퍼티 조작이 불가함을 배웠는가?
- 유니티 자체의 상수형 `Color` 목록을 알고 활용할 준비가 되었는가?

## 미니 체크
### Q1
`Renderer.material` 프로퍼티는 해당 오브젝트만의 복사된 개별 머티리얼 인스턴스를 반환하여 다른 큐브들에게 영향을 주지 않는가?
- 정답: 예. `.material` 속성을 호출하면 그 오브젝트만의 독자적인 매터리얼 복사본을 메모리에 생성하여 칠하므로 아주 안전하다.

### Q2
유니티의 `Color` 객체를 생성할 때 `new Color(1f, 1f, 1f)`가 뜻하는 RGB 완전 혼합 색상은 무슨 색인가?
- 정답: 흰색(White)

## 연결 세트
- 기초: unity_u10_material_color_b01
- 챌린지: unity_u10_material_color_c01
