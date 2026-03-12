# Unity 주차 매핑 W04

## 매핑 기준
- 원문 기준: `practice/temp/유니티 1차 문제 풀이.md`
- 주차 기준: `practice/temp/유니티 주차-문항 매핑.md`
- 이론 기준: `practice/data/theory/unity/theory_unity_u04_null_exception.md`

## 원문 대응 매핑
| 문제지 ID | 원문 번호 | 원문 제목 | 연결 이론 섹션 |
|---|---:|---|---|
| P01 | 1 | NullReferenceException (Author가 null) | 핵심 패턴, 자주 하는 실수 |
| P02 | 10 | null 비교가 가능한 변수 선택하기 | 핵심 패턴, 자주 하는 실수 |
| P03 | 37 | Unity C#에서 컴파일을 막는 비교식 3개 찾기 | 핵심 패턴, 자주 하는 실수 |
| P04 | 39 | `gameObjects` 목록으로 `Dictionary` 초기화 | 핵심 패턴, 자주 하는 실수 |

## 확장 문항 매핑
| 문제지 ID | 유형 | 기반 개념 | 원문 참조 번호 | 확장 의도 |
|---|---|---|---:|---|
| X01 | 변형 | null 안전 접근(삼항 연산) | 1, 10 | 단일 구문 내에서 참조 타입 객체의 null 여부를 체크한 뒤 분기 처리하는 방어 코딩 능력 검증 |
| X02 | 함정 | 타입 비교 가능성 판별 | 37 | 컬렉션 간 비교 불가를 인지하고 숫자형 변형들의 정상적인 대소 호환 비교를 구분해 내는 문법 구별력 함양 |

## 커버리지 점검
- 주차 원문 번호 목록: 1, 10, 37, 39
- 실제 반영된 원문 번호: 1, 10, 37, 39
- 누락 원문 번호: 없음
- 추가 확장 개념: null 안전 접근, 비교 가능 타입 판별

## JSON 변환 체크
- 목표 세트 ID(basic/challenge): `unity_u04_null_exception_b01`, `unity_u04_null_exception_c01`
- `practice/data/sets/unity/*.json` 반영 여부: 완료
- `practice/data/sets.index.json` 반영 여부: 기존 존재
- `practice/data/theory.index.json` 매핑 동기화 여부: 점검 필요
