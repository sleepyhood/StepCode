# Unity 주차 매핑 W01

## 매핑 기준
- 원문 기준: `practice/temp/유니티 1차 문제 풀이.md`
- 주차 기준: `practice/temp/유니티 주차-문항 매핑.md`
- 이론 기준: `practice/data/theory/unity/theory_unity_u01_inspector.md`

## 원문 대응 매핑
| 문제지 ID | 원문 번호 | 원문 제목 | 연결 이론 섹션 |
|---|---:|---|---|
| P01 | 2 | Inspector 창 기본 기능 (Static / Tag / Prefab) | 문항 핵심 포인트 1) Inspector 기본 기능 |
| P02 | 9 | Unity 편집기 창 종류 매칭 | 문항 핵심 포인트 2) 창 매칭 |
| P03 | 18 | Unity에서 사용할 IDE 선택하기 | 문항 핵심 포인트 3) IDE 선택 |
| P04 | 29 | Scene 뷰에서 개체 배치 관련 설명 참/거짓 | 문항 핵심 포인트 4) Scene 배치 T/F |
| P05 | 13 | Inspector에서 변수 안 보이는 이유 | 문항 핵심 포인트 5) Inspector에 변수 안 보임 |

## 확장 문항 매핑
| 문제지 ID | 유형 | 기반 개념 | 원문 참조 번호 | 확장 의도 |
|---|---|---|---:|---|
| X01 | 변형 | Tag 검색 API (`FindGameObjectsWithTag`) | 2 | 기능 설명을 코드 작성으로 전이 |
| X02 | 함정 | 필드 노출 조건(public/private/SerializeField) | 13 | 빈출 오답 패턴을 선지형으로 점검 |

## 커버리지 점검
- 주차 원문 번호 목록: 2, 9, 18, 29, 13
- 실제 반영된 원문 번호: 2, 9, 18, 29, 13
- 누락 원문 번호: 없음
- 추가 확장 개념: Tag 대량 검색, 직렬화 노출 판별

## JSON 변환 체크
- 목표 세트 ID(basic/challenge): `unity_u01_inspector_b01`, `unity_u01_inspector_c01`
- `practice/data/sets/unity/*.json` 반영 여부: 대기
- `practice/data/sets.index.json` 반영 여부: 기존 존재
- `practice/data/theory.index.json` 매핑 동기화 여부: U01 매핑 필드 존재, 세부 업데이트 대기
