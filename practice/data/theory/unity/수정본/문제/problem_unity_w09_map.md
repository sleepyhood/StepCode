# Unity 주차 매핑 W09

## 매핑 기준
- 원문 기준: `practice/temp/유니티 1차 문제 풀이.md`
- 주차 기준: `practice/temp/유니티 주차-문항 매핑.md`
- 이론 기준: `practice/data/theory/unity/theory_unity_u09_animator.md`

## 원문 대응 매핑
| 문제지 ID | 원문 번호 | 원문 제목 | 연결 이론 섹션 |
|---|---:|---|---|
| P01 | 15 | Animator 점프 상태에 클립 배치하기 | Core Pattern(예정), Common Mistakes(예정) |
| P02 | 31 | Unity Animator 상태 시스템 전환: 참/거짓 | Scope(예정), Core Pattern(예정) |
| P03 | 32 | Unity Animator 파라미터 타입에 맞는 Set 함수 연결 | Core Pattern(예정), Common Mistakes(예정) |
| P04 | 33 | Unity Animator.SetBool로 `"Attacking"`을 false로 설정 | Core Pattern(예정), Common Mistakes(예정) |
| P05 | 35 | Unity Animator 파라미터 선택: reset으로 돌아가기 | Scope(예정), Core Pattern(예정) |

## 확장 문항 매핑
| 문제지 ID | 유형 | 기반 개념 | 원문 참조 번호 | 확장 의도 |
|---|---|---|---:|---|
| X01 | 변형 | 타입-함수 매칭 코드화 | 32 | 실전 코드 적용 |
| X02 | 함정 | Trigger API 선택 | 35, 32 | 파라미터 타입 오개념 제거 |

## 커버리지 점검
- 주차 원문 번호 목록: 15, 31, 32, 33, 35
- 실제 반영된 원문 번호: 15, 31, 32, 33, 35
- 누락 원문 번호: 없음
- 추가 확장 개념: 파라미터 실전 갱신, Trigger 호출 함정

## JSON 변환 체크
- 목표 세트 ID(basic/challenge): `unity_u09_animator_b01`, `unity_u09_animator_c01`
- `practice/data/sets/unity/*.json` 반영 여부: 완료
- `practice/data/sets.index.json` 반영 여부: 기존 존재
- `practice/data/theory.index.json` 매핑 동기화 여부: 점검 필요
