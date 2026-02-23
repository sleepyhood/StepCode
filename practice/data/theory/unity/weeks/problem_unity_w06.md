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
  - 아래 동작 설명에 맞는 메서드를 쓰세요.
  - ① 누르고 있는 동안
  - ② 한 번 눌린 순간
  - ③ 뗀 순간
  - (모두 `KeyCode.LeftArrow` 기준)
  - 답안 형식 예: `① GetKey(...), ② GetKeyDown(...), ③ GetKeyUp(...)`

### [P02] 이동 메서드 선택
- 출처: 원문 22번
- 유형: 객관식
- 문제:
  - 아래 코드의 빈칸 `transform.[드롭다운](move * Time.deltaTime * speed);`에 들어갈 올바른 메서드를 고르세요.
  - 후보 API:
    - `SetPositionAndRotation(Vector3, Quaternion)`
    - `TransformDirection(Vector3)`
    - `TransformVector(Vector3)`
    - `Translate(Vector3)`
- 보기:
  - A. `TransformVector`
  - B. `SetPositionAndRotation`
  - C. `Translate`
  - D. `TransformDirection`

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
