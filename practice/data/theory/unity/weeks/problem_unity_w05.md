# Unity 주차 문제지 W05

## 주차 주제
- 유닛: U05 Transform/Lifecycle
- 핵심 개념: 중첩 클래스 타입 선언, 자식 Transform 배열 반환, Awake/OnEnable 역할 분리

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] `Transform` 멤버 오류 수정
- 출처: 원문 4번
- 유형: 객관식
- 문제:
  - 아래 코드의 빈칸 ①, ②에 들어갈 타입을 고르세요.
  - ```csharp
    public class Mount
    {
        public Transform turretMount;
        public Transform turretCache;
    }

    public [①][] tMounts = new [②][2];
    ```
- 보기:
  - A. ① `Transform`, ② `Transform`
  - B. ① `Mount`, ② `Mount`
  - C. ① `GameObject`, ② `GameObject`
  - D. ① `WeaponControl`, ② `WeaponControl`

### [P02] 자식 Transform 반환 타입
- 출처: 원문 14번
- 유형: 객관식
- 문제:
  - 다음 메서드의 반환 타입으로 올바른 것을 고르세요.
  - ```csharp
    public [반환 타입] GetChildren(Transform tr)
    {
        int childCount = tr.childCount;
        Transform[] result = new Transform[childCount];
        for (int i = 0; i < childCount; ++i)
        {
            result[i] = tr.GetChild(i);
        }
        return result;
    }
    ```
- 보기:
  - A. `Transform`
  - B. `List<Transform>`
  - C. `Transform[]`
  - D. `void`

### [P03] Awake/OnEnable 블록 순서
- 출처: 원문 26번
- 유형: 단답
- 문제:
  - 코드 블록 A/B/C/D의 올바른 배치 순서를 쓰세요.
  - 블록 요약:
    - A: `private void OnEnable() {`
    - B: 클래스 선언 + `Awake()` 시작부
    - C: `PropSpecs`를 읽어 `damage/durability` 세팅 후 `Awake` 닫기
    - D: `prop.parent/position/rotation` 부착 로직 + 클래스 닫기
  - 힌트: 초기 데이터 읽기는 `Awake`, 손 장착은 `OnEnable`

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - 자식 Transform 배열 유틸 함수 작성
- 출처 개념: U05 Transform/Lifecycle
- 유형: 코드
- 문제:
  - `Transform root`를 받아 모든 직계 자식을 `Transform[]`로 반환하는 메서드 본문 핵심 3줄을 작성하세요.
  - (배열 생성, `for` 순회, `GetChild` 할당 포함)
- 의도: childCount/GetChild 패턴을 독립 구현으로 전이

### [X02] 함정 - 라이프사이클 배치 판별
- 출처 개념: U05 Transform/Lifecycle
- 유형: 객관식
- 문제:
  - 아래 중 가장 적절한 배치를 고르세요.
- 보기:
  - A. `OnEnable`에서 `GetComponent`로 초기 데이터 읽고, `Awake`에서 장착
  - B. `Awake`에서 데이터 읽고, `OnEnable`에서 장착
  - C. 둘 다 `Start`에만 배치
  - D. 둘 다 `Update`에 배치
- 의도: 초기화와 활성화 시점의 책임 분리

## 주차 체크
- 원문 대응 문항 수: 3
- 확장 문항 수: 2
- 총 문항 수: 5
