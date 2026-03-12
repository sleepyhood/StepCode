# Unity 주차 문제지 W06

## 주차 주제
- 유닛: U06 Input
- 핵심 개념: GetKey/Down/Up 구분, Translate 기반 이동

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] 입력 메서드 매핑
- 출처: 원문 38번
- 유형: 단답
- 문제:
  아래 `Update()` 코드의 3개 `if`문은 각각 **(1) 누르고 있는 동안**, **(2) 한 번 눌린 순간**, **(3) 떼는 순간**에 맞춰 로그를 출력해야 합니다.
각 `if (Input.[빈칸])`에 들어갈 **올바른 입력 메서드**를 드롭다운에서 선택해 코드를 완성하세요. _(부분 점수 있음)_

---

### 자료(코드)

```csharp
void Update()
{
    if (Input.[드롭다운 ①])
    {
        Debug.Log("Left Arrow key is being held down");
    }

    if (Input.[드롭다운 ②])
    {
        Debug.Log("Up Arrow key was pressed once");
    }

    if (Input.[드롭다운 ③])
    {
        Debug.Log("Down Arrow key was released");
    }
}
```

### 보기(각 드롭다운 후보)

- `GetKey(KeyCode.LeftArrow)`
- `GetKeyDown(KeyCode.LeftArrow)`
- `GetKeyUp(KeyCode.LeftArrow)`

---

### [P02] 이동 메서드 선택
- 출처: 원문 22번
- 유형: 객관식
- 문제:
GameObject의 `transform` 구성 요소를 사용해 **간단한 이동 스크립트**를 완성하려고 합니다.
아래 API 정의를 참고하여, 코드의 빈칸(`transform.____( … );`)에 들어갈 **올바른 메서드**를 드롭다운에서 선택하세요.

### 자료(API 정의)

- `public void SetPositionAndRotation(Vector3 position, Quaternion rotation);`
- `public Vector3 TransformDirection(Vector3 direction);`
- `public Vector3 TransformVector(Vector3 vector);`
- `public void Translate(Vector3 translation);`

### 자료(코드)

```csharp
using UnityEngine;

public class ExampleScript : MonoBehaviour
{
    public float speed = 20f;
    private Vector3 move;

    private void Update()
    {
        move = new Vector3(Input.GetAxis("Horizontal"), 0f, Input.GetAxis("Vertical"));

        transform.____ (move * Time.deltaTime * speed);
    }
}
```

### 보기(드롭다운 후보)

- `TransformVector`
- `SetPositionAndRotation`
- `Translate`
- `TransformDirection`

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - 축 입력 이동 코드 완성
- 출처 개념: U06 Input
- 유형: 코드
- 문제:
  - `Update()`에서 `Horizontal/Vertical` 축 입력으로 이동 벡터를 만들고, `transform.Translate(...)`로 적용하는 핵심 2줄을 작성하세요.
- 의도: 입력 읽기 + 이동 적용 루틴을 직접 구성

### [X02] 함정 - GetKey 계열 오개념 판별
- 출처 개념: U06 Input
- 유형: 객관식
- 문제:
  - 다음 중 틀린 설명을 고르세요.
- 보기:
  - A. `GetKey`는 누르는 동안 매 프레임 true다.
  - B. `GetKeyDown`은 누른 프레임에만 true다.
  - C. `GetKeyUp`은 누르는 동안 계속 true다.
  - D. `GetKeyUp`은 뗀 프레임에 true다.
- 의도: Down/Up 조건 혼동 제거

## 주차 체크
- 원문 대응 문항 수: 2
- 확장 문항 수: 2
- 총 문항 수: 4
