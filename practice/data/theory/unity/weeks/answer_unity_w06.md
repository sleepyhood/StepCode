# Unity 주차 정답지 W06

## 메타
- 대상 문제지: `problem_unity_w06.md`
- 유닛: U06 Input

## 정답표
| 문항 ID | 정답 | 한 줄 근거 |
|---|---|---|
| P01 | ① `GetKey(KeyCode.LeftArrow)` / ② `GetKeyDown(KeyCode.LeftArrow)` / ③ `GetKeyUp(KeyCode.LeftArrow)` | 입력 상태(유지/눌림/뗌)별 API가 다름 |
| P02 | C | `Translate(Vector3)`가 실제 이동 수행 |
| X01 | 예: `move = new Vector3(Input.GetAxis("Horizontal"), 0f, Input.GetAxis("Vertical"));` + `transform.Translate(move * Time.deltaTime * speed);` | 축 입력 벡터를 이동에 적용 |
| X02 | C | `GetKeyUp`은 떼는 프레임에만 true |

## 해설
### P01
- 개념 정의: `GetKey/Down/Up`은 입력 상태 타이밍이 서로 다릅니다.
- 오답 포인트: Down과 Up을 이름만 보고 반대로 고르는 경우가 많습니다.
- 판별 기준: "누르고 있는 동안"인지 "그 프레임 한 번"인지 먼저 구분합니다.

### P02
- 개념 정의: `Translate`는 Transform 위치를 이동시키는 메서드입니다.
- 오답 포인트: `TransformDirection`/`TransformVector`도 이동 함수로 오해합니다.
- 판별 기준: 반환값 변환 함수인지, 실제 위치를 바꾸는 함수인지 확인합니다.

### X01
- 개념 정의: 입력 처리 기본 루틴은 "축 읽기 -> 이동 적용" 순서입니다.
- 오답 포인트: `deltaTime`을 빼먹어 프레임 의존 이동이 됩니다.
- 판별 기준: 축 입력 벡터와 `Translate(move * Time.deltaTime * speed)`가 모두 있어야 합니다.

### X02
- 개념 정의: `GetKeyUp`은 해제 순간 이벤트성 true를 반환합니다.
- 오답 포인트: 누르는 동안 true라고 혼동합니다.
- 판별 기준: "held"와 "released"를 영어 키워드 기준으로 매칭합니다.

## 운영 메모
- 다음 주차 이월 보강 포인트: U07에서 입력-발사 타이밍과 물리 적용(velocity/AddForce) 연결
- 반복 오답 키워드: GetKeyDown/GetKeyUp 혼동, Translate와 벡터 변환 함수 혼동
