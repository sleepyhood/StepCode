# Unity 주차 매핑 W05

## 매핑 기준
- 원문 기준: `practice/temp/유니티 1차 문제 풀이.md`
- 주차 기준: `practice/temp/유니티 주차-문항 매핑.md`
- 이론 기준: `practice/data/theory/unity/theory_unity_u05_transform_lifecycle.md`

## 원문 대응 매핑
| 문제지 ID | 원문 번호 | 원문 제목 | 연결 이론 섹션 |
|---|---:|---|---|
| P01 | 4 | `Transform`에 없는 멤버 오류 수정하기 | Core Pattern(예정), Common Mistakes(예정) |
| P02 | 14 | 자식 Transform들을 배열로 반환하기 | Core Pattern(예정), Common Mistakes(예정) |
| P03 | 26 | 소품 데이터 읽기 + 손 장착 순서 | Scope/라이프사이클 구분(예정) |

## 확장 문항 매핑
| 문제지 ID | 유형 | 기반 개념 | 원문 참조 번호 | 확장 의도 |
|---|---|---|---:|---|
| X01 | 변형 | childCount/GetChild 배열 패턴 | 14 | 순회 패턴을 독립 코드로 전이 |
| X02 | 함정 | Awake vs OnEnable 역할 분리 | 26 | 라이프사이클 오개념 사전 제거 |

## 커버리지 점검
- 주차 원문 번호 목록: 4, 14, 26
- 실제 반영된 원문 번호: 4, 14, 26
- 누락 원문 번호: 없음
- 추가 확장 개념: 자식 순회 유틸 구현, 라이프사이클 책임 분리

## JSON 변환 체크
- 목표 세트 ID(basic/challenge): `unity_u05_transform_lifecycle_b01`, `unity_u05_transform_lifecycle_c01`
- `practice/data/sets/unity/*.json` 반영 여부: 완료
- `practice/data/sets.index.json` 반영 여부: 기존 존재
- `practice/data/theory.index.json` 매핑 동기화 여부: 점검 필요
