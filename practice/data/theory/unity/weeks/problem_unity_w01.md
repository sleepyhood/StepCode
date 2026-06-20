# Unity 주차 문제지 W01

## 주의 사항
유니티 자격증 시험은 한국어 번역 상태가 좋지 못합니다. 문장이나 표현이 어색한 부분들이 많습니다.<br>

## 주차 주제
- 유닛: U01 Inspector
- 핵심 개념: Inspector 기본 기능, 창 역할 구분, IDE 설정, Scene 배치 도구, 필드 노출 규칙

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] Inspector 기능 판별
- 출처: 원문 2번
- 유형: 참거짓
- 문제:
  - 다음은 유니티 에디터의 Inspector(검사기) 창 및 주요 속성에 대한 설명입니다.
  - 각 문장의 참/거짓을 판별하세요. (문장별 부분 점수 가능)
  - (1) 오브젝트의 Static 체크박스는 라이트맵 베이킹, 네비게이션 메시 등 화면과 물리 환경의 정적 최적화 워크플로에 활용되는 설정이다.
  - (2) 오브젝트의 Tag(태그) 정보는 C# 스크립트에서 같은 분류 of 오브젝트 그룹을 손쉽게 찾거나 충돌 시 대상을 식별하는 데 사용할 수 있다.
  - (3) Prefab(프리팹)으로 만들어진 인스턴스를 하이어라키 창에 배치한 이후에는 인스펙터(Inspector) 창에서 개별 프로퍼티를 수정하거나 오버라이드(Override)할 수 없다.
  - **답안 작성 주의**: 아래의 형식 예와 띄어쓰기, 괄호, 쉼표를 정확히 일치시켜 입력하세요.
  - 답안 형식 예: `(1) 참, (2) 참, (3) 거짓`

### [P02] Unity 창 역할 매칭
- 출처: 원문 9번
- 유형: 매칭
- 문제:
  - 유니티 에디터를 구성하는 아래의 4가지 주요 창 이름을 가장 올바른 기능과 1:1로 연결하세요.
  - 창 목록: `Hierarchy`, `Scene`, `Project`, `Inspector`
  - 기능 후보:
    - A. 현재 열려 있는 씬(Scene) 내에 존재하는 모든 게임 오브젝트의 계층 구조 목록을 보여준다.
    - B. 시각적으로 2D/3D 환경을 오가며 오브젝트를 화면에 배치하고 트랜스폼 도구로 조작하는 실제 작업 공간이다.
    - C. 게임 개발에 필요한 머티리얼, 스크립트, 오디오 원본 에셋(Asset) 파일들을 폴더별로 보관 및 탐색한다.
    - D. 현재 마우스로 선택된 특정 게임 오브젝트나 에셋의 세부 컴포넌트 목록과 속성 파라미터 값을 보여주고 조작하게 해준다.
  - 답안 형식 예: `Hierarchy-A, Scene-B, Project-C, Inspector-D`

### [P03] IDE 설정 위치
- 출처: 원문 18번
- 유형: 객관식
- 문제:
  - Unity 상단 메뉴의 Edit > Preferences 창에서, Visual Studio나 VS Code 같은 C# 스크립트 편집기(IDE) 프로그램을 연결하기 위해 지정하는 드롭다운 옵션의 정확한 이름을 고르세요. (힌트: External Tools 탭에 위치합니다)
- 보기:
  - A. `External Tool Editor`
  - B. `External Script Editor`
  - C. `External IDE Connector`
  - D. `Script Editor Tool`

### [P04] Scene 배치 설명 참/거짓
- 출처: 원문 29번
- 유형: 참거짓
- 문제:
  - 다음 문장의 참/거짓을 판별하세요.
  - (1) Scene View에서 오브젝트를 조작할 때, 툴 핸들의 기준 좌표계를 Local(로컬)과 Global(글로벌) 모드 간에 전환할 수 있다.
  - (2) 툴바 상단의 Transform(또는 Universal) 도구를 선택하면, 이동(Move), 회전(Rotate), 스케일(Scale) 조작 기즈모가 한데 결합되어 표시된다.
  - (3) Vertex Snapping(꼭지점 스냅)은 선택한 모델 메시의 꼭지점을 반드시 장면의 그리드에만 맞추는 용도로만 허용된다.
  - (4) 게임 오브젝트의 이동 좌표, 회전 각도, 스케일 크기 수치는 3D Scene View 화면에서 마우스로 드래그해야만 조정할 수 있다.
  - **답안 작성 주의**: 아래의 형식 예와 띄어쓰기, 괄호, 쉼표를 정확히 일치시켜 입력하세요.
  - 답안 형식 예: `(1) 참, (2) 참, (3) 거짓, (4) 거짓`

### [P05] Inspector 변수 노출
- 출처: 원문 13번
- 유형: 단답
- 문제:
  - 외부 클래스에서의 무분별한 접근을 막는 캡슐화(`private`)를 유지하면서도, 유니티 에디터의 Inspector 창에서는 값을 GUI로 설정할 수 있게 하려고 합니다.
  - 아래 코드의 ①번 빈칸에 들어갈 유니티 C# 특성(Attribute)의 이름을 쓰세요.
  ```csharp
  [①]
  private int speed;
  ```
  - **답안 작성 주의**: 대괄호 `[` 와 `]` 를 제외하고 영문 특성 이름만 대소문자를 정확히 구별하여 한 단어로 작성하세요.

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - Tag 검색 API 작성
- 출처 개념: U01 / Inspector 기본 + Tag
- 유형: 객관식
- ...
- 문제:
  - 유니티 C# 스크립트 내에서 `Enemy` 태그를 가지고 있는 모든 게임 오브젝트를 찾아내어, `GameObject[]` 타입의 배열 변수 `enemies`를 선언함과 동시에 할당(초기화)하는 가장 올바른 코드를 고르세요.
- 보기:
  - A. `GameObject enemy = GameObject.FindWithTag("Enemy");`
  - B. `GameObject[] enemies = GameObject.FindWithTag("Enemy");`
  - C. `GameObject[] enemies = GameObject.FindGameObjectsWithTag("Enemy");`
  - D. `GameObject[] enemies = FindGameObjectsWithTag("Enemy");`
- 의도: Tag 기반 대량 검색 패턴 및 배열 타입과 복수형 API 매칭 능력을 검증

### [X02] 함정 - 필드 노출 가능 여부 판단
- 출처 개념: U01 / Inspector 필드 직렬화
- 유형: 객관식
- 문제:
  - `MonoBehaviour`를 상속받는 유니티 C# 스크립트 클래스 안에서, 별도의 추가 작업 없이 기본 상태 그대로는 유니티 에디터의 Inspector 창에 노출(표시)되지 않아 수치를 입력할 수 없는 변수 선언 코드를 고르세요.
- 보기:
  - A. `public int hp;`
  - B. `[SerializeField] private float moveSpeed;`
  - C. `private int score;`
  - D. `public string playerName;`
- 의도: public / private / SerializeField의 직렬화 노출 속성 규칙의 명확한 구분 확인

## 주차 체크
- 원문 대응 문항 수: 5
- 확장 문항 수: 2
- 총 문항 수: 7
