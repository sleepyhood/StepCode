# Unity U06 Input

## 학습 목표
- `Input.GetKey`, `Input.GetKeyDown`, `Input.GetKeyUp`의 차이를 설명할 수 있습니다.
- 축(Axis) 입력과 `Time.deltaTime`을 이용한 기본 이동 루틴을 이해합니다.
- `Translate`와 위치를 실제로 바꾸지 않는 비슷한 함수들을 구분할 수 있습니다.

## 범위
- 키워드: `Input.GetKey`, `Input.GetKeyDown`, `Input.GetKeyUp`, `GetAxis`, `GetAxisRaw`, `Time.deltaTime`, `Transform.Translate`, `TransformDirection`, `TransformVector`, `position`

## 먼저 큰 그림
이 단원은 크게 세 가지 질문으로 정리하면 쉽습니다.
- 지금 필요한 입력은 한 번만 잡아야 하나, 누르는 동안 계속 잡아야 하나?
- 이동은 프레임 수와 상관없이 같은 속도로 일어나야 하나?
- 지금 쓰려는 함수는 진짜로 위치를 움직이는가, 아니면 방향만 계산하는가?

왜 이걸 먼저 보나?
- W06 문제는 모두 겉보기엔 입력, 이동, 축 함수로 나뉘어 있지만, 실제로는 `입력 타이밍`, `프레임 보정`, `실제 이동 함수`를 구분하는 힘을 묻습니다.
- 그래서 `GetKey 계열`, `GetAxis + deltaTime`, `Translate` 세 덩어리를 먼저 잡아야 합니다.

## 핵심 패턴
```csharp
public class PlayerMovement : MonoBehaviour
{
    public float speed = 5.0f;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Debug.Log("Jump!");
        }

        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");

        Vector3 move = new Vector3(h, 0f, v);
        transform.Translate(move * Time.deltaTime * speed);
    }
}
```

### 패턴 해설
- `Input.GetKeyDown(KeyCode.Space)`
  - `GetKeyDown`은 누른 첫 프레임에만 한 번 `true`가 됩니다.
  - 점프, 클릭, 확인 버튼처럼 단발 반응에 어울립니다.
- `Input.GetAxis("Horizontal")`
  - `GetAxis`는 Input Manager에 등록된 축 이름을 문자열로 받아옵니다.
  - 반환값은 보통 `-1`부터 `1` 사이의 실수형입니다.
- `Vector3 move = new Vector3(h, 0f, v);`
  - 3D 이동에서 X축과 Z축 방향을 묶어 이동 벡터를 만듭니다.
  - Y축을 `0f`로 두면 위아래 이동 없이 평면 이동이 됩니다.
- `transform.Translate(move * Time.deltaTime * speed);`
  - `Translate`는 현재 위치를 기준으로 실제 이동시킵니다.
  - `Time.deltaTime`을 곱하면 컴퓨터 성능이 달라도 초당 이동 속도가 비슷하게 유지됩니다.

### 생각 질문
왜 `Update()` 안에서 매 프레임 이동시키는데도, `speed`만 곱하고 `Time.deltaTime`을 빼면 문제가 될까요?

## 문항 핵심 포인트
### 1) `GetKey`, `GetKeyDown`, `GetKeyUp` 입력 타이밍
이 개념을 알면 무엇이 쉬워지나?
- 누르고 있는 동안, 처음 누른 순간, 손을 뗀 순간을 구분하는 문제를 바로 풀 수 있습니다.

- 개념:
  - `Input.GetKey`는 누르고 있는 동안 매 프레임 계속 `true`입니다.
  - `Input.GetKeyDown`은 처음 누른 그 프레임에만 `true`입니다.
  - `Input.GetKeyUp`은 손을 뗀 그 프레임에만 `true`입니다.
- 왜 헷갈리나?
  - 이름이 비슷해서 `GetKeyDown`과 `GetKeyUp`을 단순히 "누름 관련 함수"로 뭉뚱그리기 쉽습니다.
  - `Down`을 "누르고 있는 상태 전체"로 잘못 이해하는 경우가 많습니다.
- 어떻게 구별하나?
  - 유지 상태면 `GetKey`
  - 시작 순간이면 `GetKeyDown`
  - 해제 순간이면 `GetKeyUp`
- 짧은 유사 예시:
  - `Input.GetKey(KeyCode.LeftArrow)`
  - `Input.GetKeyDown(KeyCode.Space)`
  - `Input.GetKeyUp(KeyCode.Return)`

### 자주 헷갈리는 비교
| 함수 | 언제 `true`가 되는가 |
|---|---|
| `GetKey` | 누르고 있는 동안 계속 |
| `GetKeyDown` | 처음 누른 프레임 1회 |
| `GetKeyUp` | 손을 뗀 프레임 1회 |

### 10초 점검
키를 1초 동안 계속 누르고 있으면, 그 1초 내내 `true`가 되는 쪽은 `GetKey`일까요 `GetKeyUp`일까요?
- 정답 판단: `GetKey`

### 2) Input Manager와 `GetAxis`, `GetAxisRaw`
이 개념을 알면 무엇이 쉬워지나?
- 축 기반 이동 코드와 즉각 반응/부드러운 반응 차이를 함께 이해할 수 있습니다.

- 개념:
  - `GetAxis("Horizontal")`처럼 축 이름 문자열을 넣어 입력을 읽습니다.
  - `GetAxis`는 보통 부드럽게 변하는 실수값을 줍니다.
  - `GetAxisRaw`는 곧바로 `-1`, `0`, `1`처럼 즉각적인 값을 줍니다.
- 왜 헷갈리나?
  - `GetKey`처럼 `KeyCode`를 넣는 함수와, `"Horizontal"` 같은 문자열을 넣는 함수를 섞기 쉽습니다.
  - `GetAxis`와 `GetButton`의 반환 타입을 섞어 기억할 수 있습니다.
- 어떻게 구별하나?
  - 축 이름을 넣고 실수값을 받으면 `GetAxis`
  - 더 즉각적인 축값이 필요하면 `GetAxisRaw`
  - 키 하나를 직접 검사하면 `GetKey`
- 짧은 유사 예시:
  - `Input.GetAxis("Horizontal")`
  - `Input.GetAxis("Vertical")`
  - `Input.GetAxisRaw("Horizontal")`

![Input Manager 설정 화면](../images/unity_u06_input_horizontal.png)
*캡션: Input Manager에서 `Horizontal` 축이 문자열 이름으로 등록되어 있고, 방향키 입력과 연결되는 구조를 보여주는 예시입니다. 출처: [Unity Manual - Input Manager](https://docs.unity3d.com/Manual/class-InputManager.html)*

### 생각 질문
왜 `GetAxis("Horizontal")`에는 `KeyCode.LeftArrow`가 아니라 문자열 `"Horizontal"`이 들어가야 할까요?

### 3) `Time.deltaTime`과 프레임 독립 이동
이 개념을 알면 무엇이 쉬워지나?
- X01 같은 연속 이동 문제에서 왜 `deltaTime`이 필요한지 설명할 수 있습니다.

- 개념:
  - `Update()`는 프레임마다 호출되지만, 프레임 수는 컴퓨터마다 다를 수 있습니다.
  - `Time.deltaTime`은 이전 프레임부터 지금까지 지난 시간(초)입니다.
  - 이동량에 `Time.deltaTime`을 곱하면 초당 이동 속도를 비슷하게 유지할 수 있습니다.
- 왜 헷갈리나?
  - 그냥 매 프레임 조금씩 움직이면 된다고 생각해서 `deltaTime`을 빼먹기 쉽습니다.
  - "값이 작아 보이니 없어도 비슷하겠지"라고 넘기기 쉽습니다.
- 어떻게 구별하나?
  - `Update` 안에서 위치를 계속 바꾸는 코드라면 먼저 `Time.deltaTime`을 떠올립니다.
  - 단발성 충돌 이벤트나 한 번 실행되는 로직에는 보통 곱할 필요가 없습니다.
- 짧은 유사 예시:
  - `transform.Translate(move * Time.deltaTime * speed);`
  - `hp -= damage;` 같은 즉시 처리에는 보통 `deltaTime`이 필요 없습니다.

### 자주 헷갈리는 비교
| 상황 | `Time.deltaTime` 필요성 |
|---|---|
| `Update` 안에서 연속 이동 | 필요 |
| 매 프레임 연속 회전/이동 | 필요 |
| 단발 충돌 처리 | 보통 불필요 |
| 버튼 눌림 1회 체크 | 불필요 |

### 10초 점검
`Update()` 안에서 계속 이동하는 코드인데 `Time.deltaTime`이 없다면, 어떤 컴퓨터에서 더 빨라질 가능성이 클까요?
- 정답 판단: 프레임이 더 많이 나오는 컴퓨터

### 4) `Translate` vs 방향 변환 함수 vs 절대 위치 대입
이 개념을 알면 무엇이 쉬워지나?
- 실제 위치를 움직이는 함수와 이름만 비슷한 함정 보기들을 구분할 수 있습니다.

- 개념:
  - `transform.Translate(...)`는 실제 위치를 이동시킵니다.
  - `transform.position = ...`은 절대 좌표를 강제로 지정합니다.
  - `TransformDirection(...)`과 `TransformVector(...)`는 벡터를 변환할 뿐, 위치를 움직이지 않습니다.
- 왜 헷갈리나?
  - 이름에 `Transform`이 들어가서 다 비슷한 이동 함수처럼 보이기 쉽습니다.
  - `position`도 위치를 바꾸니 연속 이동 함수와 같은 느낌으로 오해하기 쉽습니다.
- 어떻게 구별하나?
  - 현재 위치에서 조금씩 밀어가며 움직이고 싶으면 `Translate`
  - 특정 좌표로 바로 옮기고 싶으면 `position = ...`
  - 방향이나 벡터 계산만 하고 싶으면 `TransformDirection`, `TransformVector`
- 짧은 유사 예시:
  - `transform.Translate(Vector3.forward * Time.deltaTime * speed);`
  - `transform.position = new Vector3(0f, 1f, 0f);`
  - `Vector3 worldDir = transform.TransformDirection(Vector3.forward);`

![Translate와 position의 차이](../images/unity_u06_translate_vs_position.svg)
*캡션: `Translate`는 현재 기준으로 누적 이동하고, `position` 대입은 절대 좌표를 직접 찍는다는 차이를 보여주는 예시입니다. 출처: 자체 제작*

### 자주 헷갈리는 비교
| 함수/방식 | 실제 위치 이동 |
|---|---|
| `Translate` | 함 |
| `position = ...` | 함 |
| `TransformDirection` | 안 함 |
| `TransformVector` | 안 함 |

### 생각 질문
앞으로 계속 걷게 만들고 싶은데 `position = 고정값`을 계속 넣으면, 왜 자연스러운 이동이 아니라 이상한 결과가 날 수 있을까요?

### 5) 입력과 이동의 표준 루틴
이 개념을 알면 무엇이 쉬워지나?
- X01의 2줄짜리 이동 루틴을 거의 그대로 재현할 수 있습니다.

- 개념:
  - 축 입력을 읽습니다.
  - 입력값으로 `Vector3` 이동 벡터를 만듭니다.
  - `Translate`와 `Time.deltaTime`, `speed`를 곱해 이동시킵니다.
- 왜 헷갈리나?
  - 축 입력은 읽었는데 `Vector3`로 묶지 않거나, Y축까지 건드려 이상한 움직임이 생길 수 있습니다.
  - `Translate`는 썼는데 `speed`나 `deltaTime` 중 하나를 빼먹기 쉽습니다.
- 어떻게 구별하나?
  - X축은 `Horizontal`, Z축은 `Vertical`
  - Y축은 평면 이동이면 `0f`
  - 마지막에는 `move * Time.deltaTime * speed`
- 짧은 유사 예시:
  - `Vector3 move = new Vector3(Input.GetAxis("Horizontal"), 0f, Input.GetAxis("Vertical"));`
  - `transform.Translate(move * Time.deltaTime * speed);`

## 자주 하는 실수
- 유지 입력이 필요한데 `GetKeyDown`을 씁니다.
- 단발 입력인데 `GetKey`를 써서 여러 프레임 반응하게 만듭니다.
- `GetAxis("Horizontal")` 자리에 `KeyCode`를 넣으려 합니다.
- `Update` 안의 연속 이동에서 `Time.deltaTime`을 빼먹습니다.
- 실제로 이동시켜야 하는데 `TransformDirection`이나 `TransformVector`를 고릅니다.
- `Translate` 대신 `position`에 고정값을 계속 넣어 이상한 움직임을 만듭니다.

## 빠른 체크리스트
- 유지/처음 누름/해제 순간을 `GetKey`, `GetKeyDown`, `GetKeyUp`로 구분할 수 있는가?
- `GetAxis`에는 문자열 축 이름이 들어간다는 점을 기억하는가?
- `Update` 기반 연속 이동에는 `Time.deltaTime`이 필요한 이유를 설명할 수 있는가?
- 실제 위치 이동 함수와 방향 변환 함수의 차이를 구분할 수 있는가?
- 축 입력 -> `Vector3` 생성 -> `Translate` 적용 흐름을 재현할 수 있는가?

## 미니 체크
### Q1
키를 누르고 있는 동안 계속 `true`가 되는 함수는?
- 정답: `Input.GetKey`

### Q2
처음 누른 프레임에만 `true`가 되는 함수는?
- 정답: `Input.GetKeyDown`

### Q3
손을 뗀 프레임에만 `true`가 되는 함수는?
- 정답: `Input.GetKeyUp`

### Q4
`Horizontal` 축을 읽어 오는 함수 예시는?
- 정답: `Input.GetAxis("Horizontal")`

### Q5
실제로 위치를 이동시키는 함수는?
- 정답: `Translate`

### Q6
`Update()` 안의 연속 이동에 자주 곱하는 시간 보정 값은?
- 정답: `Time.deltaTime`

## 연결 세트
- 기초: unity_u06_input_b01
- 챌린지: unity_u06_input_c01
