# Unity 주차 매핑 W07

## 매핑 기준
- 원문 기준: `practice/temp/유니티 1차 문제 풀이.md`
- 주차 기준: `practice/temp/유니티 주차-문항 매핑.md`
- 이론 기준: `practice/data/theory/unity/theory_unity_u07_spawn_physics.md`

## 원문 대응 매핑
| 문제지 ID | 원문 번호 | 원문 제목 | 연결 이론 섹션 |
|---|---:|---|---|
| P01 | 36 | 발사체 생성 + 전방 속도 부여 주석 선택 (객관식) | Core Pattern(예정), Common Mistakes(예정) |
| P02 | 11 | rb 변수 타입 선택 | Core Pattern(예정), Common Mistakes(예정) |
| P03 | 24 | AddForce 방향/힘 크기 빈칸 | Core Pattern(예정), Common Mistakes(예정) |
| P04 | 23 | 풀링 초기화 + Trigger 이벤트 선택 | Scope(예정), Core Pattern(예정) |

## 확장 문항 매핑
| 문제지 ID | 유형 | 기반 개념 | 원문 참조 번호 | 확장 의도 |
|---|---|---|---:|---|
| X01 | 객관식 | 입력-생성-속도 부여 루틴 | 36, 24 | 조건 입력 판별(GetButtonDown)부터 프리팹 인스턴스화(Instantiate), 물리 속성 동기화(velocity)까지의 3단계 무기 발사 루틴을 객관식으로 평가 훈련 |
| X02 | 함정 | Trigger/Collision 이벤트 구분 | 23 | IsTrigger 체크 여부에 따라 엔진이 분배하는 이벤트 함수가 완전히 달라지는 원리를 파악하고, 파라미터 타입(`Collider` vs `Collision`) 혼동 함정까지 사전 제거 |

## 커버리지 점검
- 주차 원문 번호 목록: 36, 11, 24, 23
- 실제 반영된 원문 번호: 36, 11, 24, 23
- 누락 원문 번호: 없음
- 추가 확장 개념: 발사 루틴 조립, Trigger 이벤트 함정

## JSON 변환 체크
- 목표 세트 ID(basic/challenge): `unity_u07_spawn_physics_b01`, `unity_u07_spawn_physics_c01`
- `practice/data/sets/unity/*.json` 반영 여부: 완료
- `practice/data/sets.index.json` 반영 여부: 기존 존재
- `practice/data/theory.index.json` 매핑 동기화 여부: 점검 필요
