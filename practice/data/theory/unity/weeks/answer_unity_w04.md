# Unity 주차 정답지 W04

## 메타
- 대상 문제지: `problem_unity_w04.md`
- 유닛: U04 Null/Exception

## 정답표
| 문항 ID | 정답 | 한 줄 근거 |
|---|---|---|
| P01 | D | `book.Author`가 null인데 `.Age`를 접근함 |
| P02 | C | `GameObject`는 참조 타입이라 null 비교 가능 |
| P03 | C | 드롭영역에 넣을 수 있는 2개를 제외한 불가 비교식 3개 조합 |
| P04 | `dictionary = new Dictionary<string, GameObject>(); foreach (var gameObject in gameObjects) { dictionary.Add(gameObject.name, gameObject); }` | 생성 후 순회하며 name을 key로 추가 |
| X01 | `float xPos = projectile == null ? 0f : projectile.transform.position.x;` | null이면 기본값, 아니면 멤버 접근 |
| X02 | D | 숫자형(`float`,`int`) 비교는 가능 |

## 해설
### P01
- 개념 정의: NullReferenceException은 null 참조의 멤버 접근에서 발생합니다.
- 오답 포인트: `book`은 생성되었는데도 `book`이 null이라고 착각합니다.
- 판별 기준: 예외 줄에서 실제 null 객체가 무엇인지 먼저 찾습니다.

### P02
- 개념 정의: 참조 타입은 null 비교가 가능하고 값 타입은 기본적으로 null 비교 대상이 아닙니다.
- 오답 포인트: `bool`, `int`도 null 비교가 된다고 오해합니다.
- 판별 기준: 선언 타입이 `GameObject` 같은 참조 타입인지 확인합니다.

### P03
- 개념 정의: `==` 비교는 양쪽 타입의 비교 가능성이 성립해야 합니다.
- 오답 포인트: 런타임 오류와 컴파일 오류를 섞어 판단합니다.
- 판별 기준: 타입 자체가 다른 컬렉션/기본형 조합인지 먼저 검사합니다.

### P04
- 개념 정의: Dictionary는 생성 후 항목을 추가해야 사용 가능합니다.
- 오답 포인트: `dictionary`를 초기화하지 않고 `Add`를 먼저 호출합니다.
- 판별 기준: 생성 -> 순회 -> `Add(key,value)` 순서를 지키는지 확인합니다.

### X01
- 개념 정의: 삼항 연산자로 null 검사와 대체값 할당을 한 줄로 작성할 수 있습니다.
- 오답 포인트: null 체크 없이 `projectile.transform`에 바로 접근합니다.
- 판별 기준: 조건부 분기에서 null일 때 경로가 명시되어야 합니다.

### X02
- 개념 정의: 숫자형끼리의 크기 비교는 가능하지만 무관 타입끼리의 `==` 비교는 실패합니다.
- 오답 포인트: 컬렉션과 기본형 비교도 가능하다고 오해합니다.
- 판별 기준: 비교 연산자 적용 전에 타입 쌍이 유효한지 점검합니다.

## 운영 메모
- 다음 주차 이월 보강 포인트: U05에서 Transform 접근 시 null 안전성 확인 루틴 유지
- 반복 오답 키워드: null 원인 객체 오판, 타입 불일치 비교
