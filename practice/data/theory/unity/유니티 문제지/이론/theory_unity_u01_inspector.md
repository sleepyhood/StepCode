# Unity U01 인스펙터 기초
## 학습 목표
- Unity 편집기 4대 창(Hierarchy/Scene/Project/Inspector)의 역할을 정확히 구분한다.
- Inspector의 핵심 기능(Static, Tag, Prefab 수정, 필드 노출)을 이해한다.
- Scene 배치 관련 개념(Local/Global, Transform Tool, Snapping)을 실제 문항 수준으로 설명할 수 있다.

## 범위
- 키워드: Hierarchy, Scene, Project, Inspector, Static, Tag, Prefab, SerializeField, External Script Editor

## 먼저 큰 그림
Unity 편집 화면은 크게 4개로 생각하면 쉽다.
- `Hierarchy`: 지금 씬에 있는 오브젝트 목록(트리)
- `Scene`: 오브젝트를 눈으로 보고 직접 배치/이동/회전하는 작업 공간
- `Project`: 프로젝트 에셋(스크립트, 프리팹, 머티리얼, 이미지 등) 보관함
- `Inspector`: "지금 선택한 대상"의 상세 설정 편집창

이 4개를 정확히 구분하면 창 매칭 유형은 거의 바로 풀린다.

![Unity 에디터 4대 창 전체 화면 예시 (Hierarchy, Scene, Project, Inspector 위치 확인)](./data/theory/images/unity_u01_inspector_editor_overview.png)
*Unity 에디터의 기본 4대 창 배치를 한 화면에서 확인한다. 출처: [Unity Manual - Using the Unity Interface](https://docs.unity3d.com/es/2019.4/uploads/Main/Editor-Breakdown.png)*

## 창 역할을 표로 정리
| 창 | 한 줄 요약 | 자주 하는 작업 |
|---|---|---|
| Hierarchy | 현재 씬 오브젝트 목록 | 오브젝트 선택, 부모-자식 구조 확인 |
| Scene | 씬을 직접 만지는 뷰 | 이동/회전/스케일, 배치, 스냅 |
| Project | 에셋 관리 창 | 스크립트/프리팹/이미지 찾기 |
| Inspector | 선택 대상 상세 설정 | 컴포넌트 값 수정, Tag/Layer/Static 설정 |

![4대 창 라벨링 다이어그램 (창 역할 매칭 연습용)](./data/theory/images/unity_u01_inspector_window_mapping.png)
*Project 창 중심 UI 예시로 4대 창 역할 매칭을 연습한다. 출처: [Unity Manual - Project Window](https://docs.unity.cn/uploads/Main/project-window-context.png)*

## 핵심 패턴
```csharp
[SerializeField] private int moveSpeed = 5;

void Start()
{
    var enemies = GameObject.FindGameObjectsWithTag("Enemy");
    Debug.Log(enemies.Length);
}
```

### 패턴 해설
- `[SerializeField] private int moveSpeed = 5;`
  - `private`라서 코드 외부에서는 직접 접근을 막는다.
  - 대신 `[SerializeField]`로 Inspector에 보이게 해서 값 조정은 가능하게 만든다.
  - 즉, "보안(캡슐화) + 편의(Inspector 조절)"를 같이 잡는 패턴이다.
- `GameObject.FindGameObjectsWithTag("Enemy")`
  - 같은 Tag의 오브젝트를 "한 번에 배열"로 가져온다.
  - Tag는 오브젝트를 분류하는 라벨이다.
- `Debug.Log(enemies.Length)`
  - 검색 결과를 바로 콘솔에서 확인하는 디버깅 습관이다.

## 문항 핵심 포인트
### 1) Inspector 기본 기능
- `Static`: 이 오브젝트를 정적 오브젝트로 "표시"해 정적 배칭/라이트맵/오클루전 등 최적화·베이크에 활용한다.
  - 주의: 이동 자체를 강제로 막는 스위치는 아니며, 움직이면 결과/성능상 문제가 생길 수 있다.
- `Tag`: 스크립트에서 같은 Tag를 가진 여러 오브젝트를 찾을 때 사용한다.
  - 예: `GameObject.FindGameObjectsWithTag("Player")`
- `Prefab`: Inspector에서 값 수정 가능하고, 인스턴스 변경사항은 Overrides/Apply로 원본 반영 가능하다.

![Inspector 상단 UI 예시 (Static, Tag, Layer, Prefab Overrides 위치)](./data/theory/images/unity_u01_inspector_static_tag_prefab.png)
*Inspector의 Static 관련 UI 위치를 확인한다. 출처: [Unity Manual - Static GameObjects](https://docs.unity.cn/2017.4/Documentation/uploads/Main/GameObjectStaticDropDownMenu.png)*



### 2) 창 매칭
- 씬 오브젝트 목록 = `Hierarchy`
- 씬을 직접 보고 배치 = `Scene`
- 프로젝트 자산 관리 = `Project`
- 선택 대상 세부 설정 = `Inspector`

### 3) IDE 선택
- Unity에서 C# 편집기(IDE) 선택 위치:
  - `Edit > Preferences > External Tools > External Script Editor`
  - macOS/버전에 따라 `Unity > Settings(Preferences) > External Tools`로 보일 수 있다.
- 보기형 문항에서는 `External Script Editor`가 정답 포인트다.

![External Script Editor 설정 화면 예시 (IDE 선택 위치 확인)](./data/theory/images/unity_u01_inspector_external_script_editor.png)
*External Script Editor 설정 위치를 확인한다. 출처: [Unity Manual - Preferences (External Tools)](https://docs.unity3d.com/es/2018.4/uploads/Main/PrefsExtTools.png)*

### 4) Scene 배치 T/F
- Local / Global 전환: 가능 (참)
- Transform(또는 Universal) Tool: 이동/회전/스케일 결합 (참)
- Vertex Snapping:
  - 단순히 "그리드 전용"이라고만 보면 오답 가능
  - 주로 꼭지점 기준 정밀 배치 용도 (거짓)
- Transform 조작:
  - Scene 뷰뿐 아니라 Inspector 수치 입력으로도 가능 (거짓)

![Scene 배치 도구 예시 (Local/Global 토글, Transform Tool, Vertex Snapping)](./data/theory/images/unity_u01_inspector_scene_tools.png)
*Scene 뷰의 Transform 관련 조작 UI를 확인한다. 출처: [Unity Manual - Positioning GameObjects](https://docs.unity.cn/uploads/Main/game-objects-transform-modes.png)*

### 5) Inspector에 변수 안 보임
- Inspector는 기본적으로 "직렬화 가능한 필드"를 표시한다.
- `private string playerName;`만 쓰면 기본 상태에서는 Inspector에 안 보인다.
- 또한 `static`/`readonly` 필드이거나, Unity가 직렬화하지 않는 타입이면 표시되지 않을 수 있다.
- 해결:
  - `public string playerName;` 또는
  - `[SerializeField] private string playerName;`

![Inspector 변수 노출 비교 예시 (public 필드 vs [SerializeField] private 필드)](./data/theory/images/unity_u01_inspector_serializefield_compare.png)
*Inspector에서 스크립트 필드 노출 형태를 확인한다. 출처: [Unity Manual - Inspector Example](https://docs.unity3d.com/es/2019.4/uploads/Main/InspectorExampleObjWithScripts.png)*

## 자주 하는 실수
- Hierarchy와 Project를 바꿔 생각함
- `=`와 `==`처럼 기호는 맞췄지만 창 개념을 헷갈려 오답 선택
- `private` 필드는 Inspector에서 절대 못 본다고 단정(SerializeField 예외를 놓침)
- External Script Editor 메뉴를 기억하지 못함

## 빠른 체크리스트
- 창 이름만 보고 역할을 1초 안에 말할 수 있는가?
- Static / Tag / Prefab 기능을 각각 한 문장으로 설명할 수 있는가?
- `External Script Editor` 경로를 기억하는가?
- `private` + `[SerializeField]` 조합의 의미를 설명할 수 있는가?

## 미니 체크
### Q1
현재 씬의 GameObject 목록이 보이는 창은?
- 정답: Hierarchy

### Q2
Inspector에 private 필드를 노출하려면 무엇을 붙이나?
- 정답: `[SerializeField]`

### Q3
Unity에서 IDE 선택 옵션 이름은?
- 정답: External Script Editor

## 연결 세트
- 기초: unity_u01_inspector_b01
- 챌린지: unity_u01_inspector_c01
