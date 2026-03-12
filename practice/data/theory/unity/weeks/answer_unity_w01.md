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
| P04 | (1) 참, (2) 참, (3) 거짓, (4) 거짓 | 툴 핸들의 좌표계 전환, Universal 도구 등 조작 방식 이해 |
| P05 | `[SerializeField] private int speed;` | 캡슐화 유지(`private`) + Inspector 직렬화 노출 속성 결합 |
| X01 | `GameObject[] enemies = GameObject.FindGameObjectsWithTag("Enemy");` <br> (또는 `var enemies = ...`) | Tag 기반 다중 검색 API(`FindGameObjectsWithTag`) |
| X02 | C | 아무 특성 지정 없는 `private`만 쓰면 에디터에 비노출됨 |

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
  - (1) 참: 오브젝트를 조작하는 툴 핸들의 축 방향 기준은 Local/Global 모드로 자유롭게 전환이 가능합니다.
  - (2) 참: Transform(Universal) Tool은 이동, 회전, 스케일을 모두 결합한 올인원 도구입니다.
  - (3) 거짓: Vertex Snapping은 그리드뿐만 아니라 씬 내에 있는 다른 오브젝트의 꼭지점이나 표면에 정렬시킬 때 더 자주 사용됩니다.
  - (4) 거짓: 오브젝트 이동 수치 등은 Inspector 창의 Transform 컴포넌트에서 직접 정밀한 숫자를 기입해 조정할 수도 있습니다.
- 오답 포인트: Vertex Snapping을 Grid Snapping과 동일하게 취급하거나, 조작 위치를 오직 Scene View 화면 마우스 드래그로만 한정하는 착각이 잦습니다.

### P05
- 개념 정의: Unity는 직렬화 가능한 필드를 Inspector에 표시합니다.
- 오답 포인트: Inspector에 보이기 위해서는 무조건 `public`으로만 선언해야 한다고 오해하기 쉽습니다.
- 판별 기준: 캡슐화(정보 은닉)를 유지하려면 멤버 접근 제한자를 `private`으로 남겨두고 코드 윗줄이나 옆에 `[SerializeField]` 특성(Attribute)을 명시적으로 붙여 주어야 합니다.

### X01
- 개념 정의: 같은 태그를 가진 여러 오브젝트 집합을 한 번에 배열 형태로 찾아올 때 `GameObject.FindGameObjectsWithTag` 배열 반환 API를 사용합니다.
- 오답 포인트: 단일 객체만 찾아오는 `GameObject.FindWithTag`와 혼동하거나, 접근 클래스인 `GameObject` 명칭 자체를 누락하는 경우가 있습니다.
- 판별 기준: 결과 변수의 타입이 `GameObject[]` (배열) 인지, 그리고 호출하는 함수명에 `s`(`Objects`)가 정확히 포함되었는지 점검합니다. (`var` 키워드 추론도 정답 인정 가능)

### X02
- 개념 정의: 스크립트 클래스의 변수가 Inspector 창에 기본 표시되려면 `public` 이어야 하며, `private`이나 `protected` 필드는 앞에 `[SerializeField]` 특성을 선언해주어야 합니다.
- 오답 포인트: `[SerializeField]`가 붙은 구문도 단어 내 `private`이 보인다는 이유만으로 표시되지 않는다고 혼동하기 쉽습니다.
- 판별 기준: 다른 어노테이션 특성이 전혀 없는 단순 멤버 필드인 `private int score;` 만이 기본적으로 Inspector에서 감춰집니다.

## 운영 메모
- 다음 주차 이월 보강 포인트: U02에서 API 대소문자 규칙(CompareTag, OnTriggerEnter) 반복 점검
- 반복 오답 키워드: Hierarchy/Project 혼동, SerializeField 누락
