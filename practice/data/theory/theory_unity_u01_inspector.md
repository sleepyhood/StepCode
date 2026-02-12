# Unity U01 인스펙터 기초
## 학습 목표
- Unity 편집기 4대 창(Hierarchy/Scene/Project/Inspector)의 역할을 정확히 구분한다.
- Inspector의 핵심 기능(Static, Tag, Prefab 수정, 필드 노출)을 이해한다.
- Scene 배치 관련 개념(Local/Global, Transform Tool, Snapping)을 실제 문항 수준으로 설명할 수 있다.

## 범위
- 출처 매핑: `practice/temp/유니티 1차 문제 풀이.md`의 2, 9, 13, 18, 29번
- 키워드: Hierarchy, Scene, Project, Inspector, Static, Tag, Prefab, SerializeField, External Script Editor

## 먼저 큰 그림
Unity 편집 화면은 크게 4개로 생각하면 쉽다.
- `Hierarchy`: 지금 씬에 있는 오브젝트 목록(트리)
- `Scene`: 오브젝트를 눈으로 보고 직접 배치/이동/회전하는 작업 공간
- `Project`: 프로젝트 에셋(스크립트, 프리팹, 머티리얼, 이미지 등) 보관함
- `Inspector`: "지금 선택한 대상"의 상세 설정 편집창

이 4개를 정확히 구분하면 `9번` 유형은 거의 바로 풀린다.

## 창 역할을 표로 정리
| 창 | 한 줄 요약 | 자주 하는 작업 |
|---|---|---|
| Hierarchy | 현재 씬 오브젝트 목록 | 오브젝트 선택, 부모-자식 구조 확인 |
| Scene | 씬을 직접 만지는 뷰 | 이동/회전/스케일, 배치, 스냅 |
| Project | 에셋 관리 창 | 스크립트/프리팹/이미지 찾기 |
| Inspector | 선택 대상 상세 설정 | 컴포넌트 값 수정, Tag/Layer/Static 설정 |

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

## 문항 핵심 포인트 (2/9/18/29/13번 대응)
### 1) Inspector 기본 기능 (2번)
- `Static`: 이 오브젝트를 정적 오브젝트로 취급하게 해서 최적화/베이크 관련 기능에 활용된다.
- `Tag`: 스크립트에서 같은 Tag를 가진 여러 오브젝트를 찾을 때 사용한다.
  - 예: `GameObject.FindGameObjectsWithTag("Player")`
- `Prefab`: Inspector에서 값 수정 가능하고, 인스턴스 변경사항은 Overrides/Apply로 원본 반영 가능하다.

즉, 2번의 세 문장은 모두 참으로 볼 수 있다.

### 2) 창 매칭 (9번)
- 씬 오브젝트 목록 = `Hierarchy`
- 씬을 직접 보고 배치 = `Scene`
- 프로젝트 자산 관리 = `Project`
- 선택 대상 세부 설정 = `Inspector`

### 3) IDE 선택 (18번)
- Unity에서 C# 편집기(IDE) 선택 위치:
  - `Edit > Preferences > External Tools > External Script Editor`
- 보기형 문항에서는 `External Script Editor`가 정답 포인트다.

### 4) Scene 배치 T/F (29번)
- Local / Global 전환: 가능 (참)
- Transform(또는 Universal) Tool: 이동/회전/스케일 결합 (참)
- Vertex Snapping:
  - 단순히 "그리드 전용"이라고만 보면 오답 가능
  - 주로 꼭지점 기준 정밀 배치 용도 (문항 맥락상 3번 거짓)
- Transform 조작:
  - Scene 뷰뿐 아니라 Inspector 수치 입력으로도 가능 (4번 거짓)

### 5) Inspector에 변수 안 보임 (13번)
- Inspector는 기본적으로 "직렬화 가능한 필드"를 표시한다.
- `private string playerName;`만 쓰면 기본 상태에서는 Inspector에 안 보인다.
- 해결:
  - `public string playerName;` 또는
  - `[SerializeField] private string playerName;`

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
