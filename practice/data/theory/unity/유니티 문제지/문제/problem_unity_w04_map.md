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
| X01 | 변형 | null 안전 접근(삼항 연산) | 1, 10 | null 체크를 실코드 한 줄 패턴으로 전이 |
| X02 | 함정 | 타입 불일치 비교 판별 | 37 | 컴파일 오류/정상 비교를 즉시 구분 |

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
