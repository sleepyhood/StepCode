# Unity 주차 문제지 W10

## 주차 주제
- 유닛: U10 Material/Color
- 핵심 개념: `Color` 변수 출력 문법, `Material.SetColor(string, Color)` 시그니처와 셰이더 프로퍼티명 규칙

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] Color 변수 값 출력식 완성
- 출처: 원문 20번
- 유형: 단답
- 문제:
  - 다음 코드에서 인스펙터에 노출된 `color` 변수의 RGBA 값을 콘솔 창에 출력하고자 합니다. 빈칸에 들어갈 알맞은 변수명을 쓰세요. (대소문자 주의)
  - 코드 예시:
    ```csharp
    public Color color;

    void Start() {
        Debug.Log("Current Color: " + [  빈칸  ]);
    }
    ```

### [P02] Material.SetColor 두 인자 완성
- 출처: 원문 40번
- 유형: 단답
- 문제:
  - 3D 오브젝트의 머티리얼(Material) 색상을 C# 스크립트 런타임에서 빨간색으로 동적 변경하려고 합니다.
  - `Material.SetColor(string propertyName, Color color)` API의 시그니처에 맞게 아래 코드의 빈칸 ①, ②에 들어갈 요소를 순서대로 쉼표로 구분하여 작성하세요.
  - `material.SetColor( [ ① ], [ ② ] );`
  - 답안 형식 예: `"_Color", Color.red`

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - 파란색으로 머티리얼 메인 색상 변경 코드 선택
- 출처 개념: U10 Material/Color
- 유형: 객관식
- 문제:
  - 스크립트에 `Material mat;` 변수가 선언되어 있습니다. 이 머티리얼의 메인 알베도 색상을 파란색으로 즉시 변경하고자 할 때 들어갈 C# 한 줄 코드로 가장 적절한 것을 고르세요.
- 보기:
  - A. `mat.SetColor(_Color, Color.blue);`
  - B. `mat.SetColor("_Color", Color.blue);`
  - C. `mat.SetColor("Color", Color.blue);`
  - D. `mat.SetColor("_Color", blue);`
- 의도: 셰이더 프로퍼티명 규칙과 Color API의 범용적 활용 능력을 검증합니다.

### [X02] 함정 - SetColor 첫 번째 인자의 올바른 형식 판별
- 출처 개념: U10 Material/Color
- 유형: 객관식
- 문제:
  - `Material.SetColor`의 첫 번째 인자에는 셰이더 프로퍼티 이름을 전달해야 합니다. 다음 보기 중 C# 컴파일 오류 없이 올바르게 셰이더 프로퍼티에 접근할 수 있는 형식을 고르세요.
- 보기:
  - A. `_Color` (따옴표 없음)
  - B. `"_Color"` (언더스코어 포함 문자열)
  - C. `Color` (타입 이름)
  - D. `"Color"` (언더스코어 없는 문자열)
- 의도: 셰이더 프로퍼티 참조 시 문자열 리터럴 형식과 언더스코어 관례를 만족하는지 검증합니다.

## 주차 체크
- 원문 대응 문항 수: 2
- 확장 문항 수: 2
- 총 문항 수: 4
