# Unity 주차 정답지 W05

## 메타
- 대상 문제지: `problem_unity_w05.md`
- 유닛: U05 Transform/Lifecycle

## 정답표
| 문항 ID | 정답 | 한 줄 근거 |
|---|---|---|
| P01 | B | `turretMount`는 `Mount` 멤버이므로 배열 요소 타입이 `Mount`여야 함 |
| P02 | C | `result`가 `Transform[]`이며 그대로 반환 |
| P03 | B -> C -> A -> D | Awake에서 스펙 읽기 후 OnEnable에서 장착 |
| X01 | 예: `Transform[] result = new Transform[root.childCount]; for (...) result[i] = root.GetChild(i);` | childCount/GetChild 패턴 완성 |
| X02 | B | 데이터 초기화는 Awake, 활성화 후 부착은 OnEnable이 적절 |

## 해설
### P01
- 개념 정의: 중첩 클래스의 필드를 사용하려면 배열 요소 타입도 그 클래스여야 합니다.
- 오답 포인트: `turretMount`가 `Transform` 타입이니 배열도 `Transform[]`라 오해합니다.
- 판별 기준: 접근하려는 멤버(`turretMount`)가 어느 타입에 정의됐는지 확인합니다.

### P02
- 개념 정의: 함수 반환 타입은 실제 `return`되는 객체 타입과 일치해야 합니다.
- 오답 포인트: 단일 `Transform`과 `Transform[]`를 혼동합니다.
- 판별 기준: 내부에서 생성/반환하는 변수가 배열인지 단일 객체인지 확인합니다.

### P03
- 개념 정의: 초기 스펙 로딩과 활성화 시 장착 동작은 호출 시점이 다릅니다.
- 오답 포인트: 장착 로직을 Awake에 넣어 활성화 조건과 섞습니다.
- 판별 기준: 데이터 준비는 Awake, 활성화 조건부 동작은 OnEnable로 분리합니다.

### X01
- 개념 정의: 자식 순회는 `childCount`와 `GetChild(i)`의 반복 패턴으로 구현합니다.
- 오답 포인트: 배열 크기와 순회 범위가 어긋나 인덱스 오류가 납니다.
- 판별 기준: 배열 크기를 `childCount`로 맞추고 `0..childCount-1`을 순회합니다.

### X02
- 개념 정의: Unity 라이프사이클은 역할에 따라 메서드를 분리해 배치해야 합니다.
- 오답 포인트: 모든 동작을 Start/Update에 몰아넣습니다.
- 판별 기준: 초기화(한 번)와 활성화 시 동작(반복 가능)을 구분합니다.

## 운영 메모
- 다음 주차 이월 보강 포인트: U06 입력 처리에서도 Update/FixedUpdate 역할 구분 유지
- 반복 오답 키워드: 타입 선언 불일치, 배열 반환형 혼동, 라이프사이클 역할 혼동
