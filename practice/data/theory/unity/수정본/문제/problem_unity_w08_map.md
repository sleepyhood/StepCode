# Unity 주차 매핑 W08

## 매핑 기준
- 원문 기준: `practice/temp/유니티 1차 문제 풀이.md`
- 주차 기준: `practice/temp/유니티 주차-문항 매핑.md`
- 이론 기준: `practice/data/theory/unity/theory_unity_u08_ui.md`

## 원문 대응 매핑
| 문제지 ID | 원문 번호 | 원문 제목 | 연결 이론 섹션 |
|---|---:|---|---|
| P01 | 6 | UI Text에 점수 표시 코드 완성하기 | Core Pattern(예정), Common Mistakes(예정) |
| P02 | 7 | 문자열 인수를 받아 UI Text를 갱신하는 메서드 선언 | Core Pattern(예정), Common Mistakes(예정) |
| P03 | 16 | OnMouseUp으로 UI 패널 토글 함수 만들기 | Core Pattern(예정), Common Mistakes(예정) |
| P04 | 30 | UI 버튼 이벤트 등록 위치에 따른 동작 판단 | Scope(예정), Core Pattern(예정) |

## 확장 문항 매핑
| 문제지 ID | 유형 | 기반 개념 | 원문 참조 번호 | 확장 의도 |
|---|---|---|---:|---|
| X01 | 변형 | Button 리스너 1회 등록 패턴 | 30 | `Update` 중복 등록 함정 회피 |
| X02 | 함정 | AddListener 등록 위치 판별 | 30 | 초기화 시점 선택 오개념 제거 |

## 커버리지 점검
- 주차 원문 번호 목록: 6, 7, 16, 30
- 실제 반영된 원문 번호: 6, 7, 16, 30
- 누락 원문 번호: 없음
- 추가 확장 개념: 1회 등록 패턴, 등록 위치 선택

## JSON 변환 체크
- 목표 세트 ID(basic/challenge): `unity_u08_ui_b01`, `unity_u08_ui_c01`
- `practice/data/sets/unity/*.json` 반영 여부: 완료
- `practice/data/sets.index.json` 반영 여부: 기존 존재
- `practice/data/theory.index.json` 매핑 동기화 여부: 점검 필요
