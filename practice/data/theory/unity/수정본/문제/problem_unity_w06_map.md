# Unity 주차 매핑 W06

## 매핑 기준
- 원문 기준: `practice/temp/유니티 1차 문제 풀이.md`
- 주차 기준: `practice/temp/유니티 주차-문항 매핑.md`
- 이론 기준: `practice/data/theory/unity/theory_unity_u06_input.md`

## 원문 대응 매핑
| 문제지 ID | 원문 번호 | 원문 제목 | 연결 이론 섹션 |
|---|---:|---|---|
| P01 | 38 | 입력 함수 선택(누름/한 번/떼기) | Core Pattern(예정), Common Mistakes(예정) |
| P02 | 22 | Transform 이동 메서드 선택 | Core Pattern(예정), Common Mistakes(예정) |

## 확장 문항 매핑
| 문제지 ID | 유형 | 기반 개념 | 원문 참조 번호 | 확장 의도 |
|---|---|---|---:|---|
| X01 | 변형 | GetAxis + Translate 루틴 | 22 | 입력과 이동 적용을 코드로 전이 |
| X02 | 함정 | GetKey/Down/Up 타이밍 구분 | 38 | 입력 이벤트 오개념 제거 |

## 커버리지 점검
- 주차 원문 번호 목록: 38, 22
- 실제 반영된 원문 번호: 38, 22
- 누락 원문 번호: 없음
- 추가 확장 개념: 축 입력 이동 루틴, 입력 타이밍 함정

## JSON 변환 체크
- 목표 세트 ID(basic/challenge): `unity_u06_input_b01`, `unity_u06_input_c01`
- `practice/data/sets/unity/*.json` 반영 여부: 완료
- `practice/data/sets.index.json` 반영 여부: 기존 존재
- `practice/data/theory.index.json` 매핑 동기화 여부: 점검 필요
