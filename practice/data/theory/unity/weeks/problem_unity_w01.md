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
  - 아래 문장은 Inspector(검사기) 기본 기능 설명입니다.
  - 각 문장의 참/거짓을 판별하세요. (문장별 부분 점수 가능)
  - (1) Static 체크는 정적 최적화 워크플로에 활용된다.
  - (2) Tag는 스크립트에서 같은 분류의 오브젝트를 찾는 데 사용할 수 있다.
  - (3) Prefab은 Inspector에서 수정할 수 없다.
  - 답안 형식 예: `(1) 참, (2) 참, (3) 거짓`

### [P02] Unity 창 역할 매칭
- 출처: 원문 9번
- 유형: 매칭
- 문제:
  - 아래 창 이름을 올바른 기능과 연결하세요.
  - 창: `Hierarchy`, `Scene`, `Project`, `Inspector`
  - 기능 후보:
    - A. 현재 씬 오브젝트 목록
    - B. 씬 배치/조작 작업 공간
    - C. 에셋 보관/탐색
    - D. 선택 대상 상세 설정
  - 답안 형식 예: `Hierarchy-A, Scene-B, Project-C, Inspector-D`

### [P03] IDE 설정 위치
- 출처: 원문 18번
- 유형: 단답
- 문제:
  - Unity Preferences(또는 Edit > Preferences)에서 스크립트 편집기(IDE)를 지정할 때 사용하는 옵션 이름을 쓰세요.
  - 정확한 옵션명(영문)으로 작성하세요.

### [P04] Scene 배치 설명 참/거짓
- 출처: 원문 29번
- 유형: 참거짓
- 문제:
  - 다음 문장의 참/거짓을 판별하세요.
  - (1) Local/Global 전환은 가능하다.
  - (2) Transform(Universal) 도구는 이동/회전/스케일 도구를 결합한다.
  - (3) Vertex Snapping은 선택 메시의 꼭지점을 장면 그리드에 맞추는 용도로만 사용된다.
  - (4) 오브젝트의 이동/회전/스케일은 3D Scene View에서만 조정할 수 있다.
  - 답안 형식 예: `(1) 참, (2) 참, (3) 거짓, (4) 거짓`

### [P05] Inspector 변수 노출
- 출처: 원문 13번
- 유형: 코드
- 문제:
  - 기본 상태에서 `private` 필드는 Inspector에 표시되지 않습니다.
  - `private int speed;`를 캡슐화를 유지하면서 Inspector에 노출하도록 한 줄로 수정하세요.

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - Tag 검색 API 작성
- 출처 개념: U01 / Inspector 기본 + Tag
- 유형: 코드
- 문제:
  - `Enemy` 태그를 가진 모든 오브젝트를 배열 변수 `enemies`에 담는 코드를 한 줄로 작성하세요.
- 의도: Tag 기반 대량 검색 패턴을 코드로 전이

### [X02] 함정 - 필드 노출 가능 여부 판단
- 출처 개념: U01 / Inspector 필드 직렬화
- 유형: 객관식
- 문제:
  - 기본 상태에서 Inspector에 노출되지 않는 필드를 고르세요.
- 보기:
  - A. `public int hp;`
  - B. `[SerializeField] private float moveSpeed;`
  - C. `private int score;`
  - D. `public string playerName;`
- 의도: public / private / SerializeField 구분 확인

## 주차 체크
- 원문 대응 문항 수: 5
- 확장 문항 수: 2
- 총 문항 수: 7
