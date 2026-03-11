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
| X01 | 변형 | `SetColor` 색상 상수 변형 | 40 | 같은 패턴으로 다른 색상 적용 |
| X02 | 함정 | 첫 인자 문자열 리터럴 | 40 | 식별자/문자열 혼동 제거 |

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
