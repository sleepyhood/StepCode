# Unity 주차 정답지 W01

## 메타
- 대상 문제지: `problem_unity_w01.md`
- 유닛: U01 Inspector

## 정답표
| 문항 ID | 정답 | 한 줄 근거 |
|---|---|---|
| P01 | (1) 참, (2) 참, (3) 거짓 | Static/Tag는 활용 가능, Prefab 편집은 가능 |
| P02 | Hierarchy-A, Scene-B, Project-C, Inspector-D | 각 창의 기본 역할 매칭 |
| P03 | External Script Editor | IDE 선택 옵션의 정확한 명칭 |
| P04 | (1) 참, (2) 참, (3) 거짓, (4) 거짓 | Local/Global 가능, Universal Tool 결합, Vertex Snapping/조작 위치 오해 구분 |
| P05 | `[SerializeField] private int speed;` | private 유지 + Inspector 노출 |
| X01 | `var enemies = GameObject.FindGameObjectsWithTag("Enemy");` | Tag 기반 다중 검색 API |
| X02 | C | `private`만 쓰면 기본 상태에서 노출되지 않음 |

## 해설
### P01
- 개념 정의: Static/Tag/Prefab은 Inspector에서 자주 다루는 핵심 속성입니다.
- 오답 포인트: Prefab은 수정 불가라고 오해하기 쉽습니다.
- 판별 기준: Static은 최적화 워크플로, Tag는 분류/검색, Prefab은 Inspector 편집 가능 여부를 구분합니다.

### P02
- 개념 정의: Unity 4대 창은 씬 오브젝트, 씬 조작, 에셋, 상세 설정으로 역할이 분리됩니다.
- 오답 포인트: Hierarchy와 Project를 바꿔 고르는 경우가 많습니다.
- 판별 기준: "현재 씬 목록"은 Hierarchy, "대화형 편집 뷰"는 Scene, "에셋 저장소"는 Project, "선택 대상 상세"는 Inspector입니다.

### P03
- 개념 정의: 외부 에디터 선택은 Preferences(External Tools) 아래에서 설정합니다.
- 오답 포인트: 메뉴 경로는 기억하지만 옵션 이름을 틀리는 경우가 있습니다.
- 판별 기준: 옵션 이름 `External Script Editor`를 영문 그대로 정확 표기합니다.

### P04
- 개념 정의: Scene 배치 조작은 좌표계(Local/Global), Universal Tool, 스냅 규칙, Inspector 수치 입력을 함께 이해해야 합니다.
- 문항별 판정:
- (1) 참: Move/Rotate/Scale 핸들 방향은 Local/Global 전환이 가능합니다.
- (2) 참: Transform(Universal) Tool은 이동/회전/스케일을 결합한 도구입니다.
- (3) 거짓: Vertex Snapping은 "그리드 전용"이 아니라 다른 오브젝트 꼭지점/표면 정렬에도 사용됩니다.
- (4) 거짓: Transform 값은 Inspector에서도 직접 입력해 조정할 수 있습니다.
- 오답 포인트: Vertex Snapping을 Grid Snapping과 동일 개념으로 착각하거나, 조작 위치를 Scene View로 한정하는 경우가 많습니다.

### P05
- 개념 정의: Unity는 직렬화 가능한 필드를 Inspector에 표시합니다.
- 오답 포인트: `public`으로만 바꾸는 것이 유일한 해법이라고 오해합니다.
- 판별 기준: 캡슐화를 유지하려면 `private`을 유지하고 `[SerializeField]`를 붙입니다.

### X01
- 개념 정의: 같은 태그 오브젝트를 한번에 가져올 때 `FindGameObjectsWithTag`를 사용합니다.
- 오답 포인트: `FindWithTag`(단일)과 혼동합니다.
- 판별 기준: 반환형이 배열인지 확인합니다.

### X02
- 개념 정의: 기본 노출은 public 필드, private은 직렬화 속성이 필요합니다.
- 오답 포인트: `[SerializeField] private`를 비노출로 오해합니다.
- 판별 기준: 속성 없는 `private int score;`만 기본 비노출입니다.

## 운영 메모
- 다음 주차 이월 보강 포인트: U02에서 API 대소문자 규칙(CompareTag, OnTriggerEnter) 반복 점검
- 반복 오답 키워드: Hierarchy/Project 혼동, SerializeField 누락
