# Unity 주차 매핑 W11

## 매핑 기준
- 원문 기준: `practice/temp/유니티 1차 문제 풀이.md`
- 주차 기준: `practice/temp/유니티 주차-문항 매핑.md`
- 이론 기준: `practice/data/theory/unity/theory_unity_u11_ecs.md`

## 원문 대응 매핑
| 문제지 ID | 원문 번호 | 원문 제목 | 연결 이론 섹션 |
|---|---:|---|---|
| P01 | 5 | 코드 조각이 ECS(Entities) 라이브러리를 사용하는가? | Core Pattern(예정), Common Mistakes(예정) |
| P02 | 34 | Unity ECS 사용 여부 참/거짓 판별 | Core Pattern(예정), Common Mistakes(예정) |

## 확장 문항 매핑
| 문제지 ID | 유형 | 기반 개념 | 원문 참조 번호 | 확장 의도 |
|---|---|---|---:|---|
| X01 | 변형 | ECS 실사용 최소 코드 | 5, 34 | 판별 기준을 코드 작성으로 전이 |
| X02 | 함정 | `using` 선언 vs 실사용 | 5, 34 | 네임스페이스 선언 과신 방지 |

## 커버리지 점검
- 주차 원문 번호 목록: 5, 34
- 실제 반영된 원문 번호: 5, 34
- 누락 원문 번호: 없음
- 추가 확장 개념: 실사용 최소 코드, 선언/사용 구분

## JSON 변환 체크
- 목표 세트 ID(basic/challenge): `unity_u11_ecs_b01`, `unity_u11_ecs_c01`
- `practice/data/sets/unity/*.json` 반영 여부: 완료
- `practice/data/sets.index.json` 반영 여부: 기존 존재
- `practice/data/theory.index.json` 매핑 동기화 여부: 점검 필요
