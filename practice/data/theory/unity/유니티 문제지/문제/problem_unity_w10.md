# Unity 주차 문제지 W10

## 주차 주제
- 유닛: U10 Material/Color
- 핵심 개념: `Color` 값 출력, `Material.SetColor(string, Color)` 인자 타입/형식

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] Color 변수 출력식 완성
- 출처: 원문 20번
- 유형: 단답
- 문제:아래 `Player` 클래스의 `color` 변수 값을 콘솔에 다음과 같이 출력하려고 합니다.

- 출력 예: `Color: (0.258,0.525,0.956,1)`

드롭다운 목록에서 올바른 옵션을 선택해 `Debug.Log` 코드를 완성하세요.

### 자료(코드)

```csharp
using UnityEngine;

public class Player : MonoBehaviour
{
    public Color color;

    public void Start()
    {
        // 로그가 여기에 표시됩니다.
    }
}
```

### 답안 영역(완성해야 할 형태)

```csharp
Debug.Log("Color:" + [드롭다운]);
```

### 보기(드롭다운 후보)

- `color`
- `Color`
- `new Color(Color.Red)`
- `(0.258,0.525,0.956,1)`

### [P02] SetColor 두 인자 완성
- 출처: 원문 40번
- 유형: 단답
- 문제:
  다음 API를 사용해 **Unity 기본 제공 셰이더에서 공통으로 사용하는 color 속성 이름**과, **빨간색(Color.red)** 값을 설정하는 코드를 완성하세요.

- API: `Material.SetColor(string name, Color value)`
  - `name` : 셰이더의 **색상 속성 이름**(예: `"_Color"`)
  - `value` : 설정할 **Color 값**

아래 `material.SetColor( ___ , ___ );`의 **두 빈칸**에 들어갈 올바른 옵션을 각각 선택하세요.

---

### 자료(코드)

```csharp
material.SetColor( ___ , ___ );
```

---

### 보기

#### (1) name 자리

- A. `_Color`
- B. `"_Color"`
- C. `"Color"`
- D. `Color`

#### (2) value 자리

- A. `Red`
- B. `Color.red`
- C. `new Color(red)`
- D. `(0,1,0)`


## 확장 문항 (변형/함정/응용)
### [X01] 변형 - 파란색으로 머티리얼 색 변경 코드
- 출처 개념: U10 Material/Color
- 유형: 코드
- 문제:
  - `Material mat`이 있을 때, 메인 색을 파란색으로 설정하는 1줄 코드를 작성하세요.
- 의도: `_Color` 문자열 + `Color` 상수 조합 전이

### [X02] 함정 - SetColor 첫 인자 선택
- 출처 개념: U10 Material/Color
- 유형: 객관식
- 문제:
  - `SetColor`의 첫 인자로 올바른 표현을 고르세요.
- 보기:
  - A. `_Color`
  - B. `"_Color"`
  - C. `Color`
  - D. `"Color"`
- 의도: 문자열 리터럴/식별자 혼동 방지

## 주차 체크
- 원문 대응 문항 수: 2
- 확장 문항 수: 2
- 총 문항 수: 4
