# Unity 주차 매핑 W10

## 매핑 기준
- 원문 기준: `practice/temp/유니티 1차 문제 풀이.md`
- 주차 기준: `practice/temp/유니티 주차-문항 매핑.md`
- 이론 기준: `practice/data/theory/unity/theory_unity_u10_material_color.md`

## 원문 대응 매핑
| 문제지 ID | 원문 번호 | 원문 제목 | 연결 이론 섹션 |
|---|---:|---|---|
| P01 | 20 | Color 변수 값을 Debug.Log로 출력하기 | Core Pattern(예정), Common Mistakes(예정) |
| P02 | 40 | Material.SetColor로 기본 셰이더 색상 설정: `"_Color"` 와 `Color.red` | Core Pattern(예정), Common Mistakes(예정) |

## 확장 문항 매핑
| 문제지 ID | 유형 | 기반 개념 | 원문 참조 번호 | 확장 의도 |
|---|---|---|---:|---|
| X01 | 변형 | `SetColor` 색상 상수 변형 | 40 | P02에서 익힌 `"_Color"` + `Color.red` 조합 패턴을 다른 색상 상수(`Color.blue`)로 전이하여 셰이더 프로퍼티명 규칙의 범용적 활용 능력 검증 |
| X02 | 함정 | 첫 인자 문자열 리터럴 판별 | 40 | 셰이더 프로퍼티명이 반드시 쌍따옴표 문자열 리터럴이어야 하며 언더스코어로 시작한다는 두 가지 규칙을 동시 검증하고, 따옴표 누락/언더스코어 누락 시의 각기 다른 실패 유형을 구분 |

## 커버리지 점검
- 주차 원문 번호 목록: 20, 40
- 실제 반영된 원문 번호: 20, 40
- 누락 원문 번호: 없음
- 추가 확장 개념: 색상 상수 전이, 문자열 인자 함정

## JSON 변환 체크
- 목표 세트 ID(basic/challenge): `unity_u10_material_color_b01`, `unity_u10_material_color_c01`
- `practice/data/sets/unity/*.json` 반영 여부: 완료
- `practice/data/sets.index.json` 반영 여부: 기존 존재
- `practice/data/theory.index.json` 매핑 동기화 여부: 점검 필요
