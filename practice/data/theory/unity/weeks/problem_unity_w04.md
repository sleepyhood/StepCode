# Unity 주차 문제지 W04

## 주차 주제
- 유닛: U04 Null/Exception
- 핵심 개념: NullReference 원인 추적, null 비교 가능 타입, 타입 불일치 비교, Dictionary 초기화

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] NullReferenceException 원인
- 출처: 원문 1번
- 유형: 객관식
- 문제:
  - 아래 코드에서 `Start()` 실행 시 `NullReferenceException`이 발생하는 직접 원인을 고르세요.
  - ```csharp
    Book book = new Book();
    int authorAge = book.Author.Age;
    ```
- 보기:
  - A. `book`이 null이다.
  - B. `Age`가 null이다.
  - C. `publisher`가 null이라서 예외가 난다.
  - D. `Author`가 null이다.

### [P02] null 비교 가능한 선언/조건식 선택
- 출처: 원문 10번
- 유형: 객관식
- 문제:
  - 아래 두 드롭다운 조합 중 올바른 것을 고르세요.
  - 드롭다운 ①(변수 선언): `public bool hasTurned;`, `public GameObject projectile;`, `public int score;`
  - 드롭다운 ②(조건식): `(projectile == null)`, `(hasTurned == null)`, `(score == null)`
- 보기:
  - A. ① `public bool hasTurned;` + ② `(hasTurned == null)`
  - B. ① `public int score;` + ② `(score == null)`
  - C. ① `public GameObject projectile;` + ② `(projectile == null)`
  - D. ① `public bool hasTurned;` + ② `(projectile == null)`

### [P03] 드롭영역에 들어갈 수 없는 비교식 3개 찾기
- 출처: 원문 37번
- 유형: 객관식
- 문제:
  - 아래 코드의 `if` 드롭영역 2개에 넣어 컴파일 가능한 비교식은 2개뿐입니다.
  - 후보 중 드롭영역에 **들어갈 수 없는 비교식 3개 조합**을 고르세요.
  - ```csharp
    public class MyClass : MonoBehaviour
    {
        [SerializeField]
        List<GameObject> gameObjects;

        Dictionary<string, GameObject> dictionary;
        int myInt;
        string myString;
        List<GameObject> list;
        float myFloat;

        private void Start()
        {
            if (/* [드롭영역 1] */)
            {
                // 작업을 수행합니다.
            }

            if (/* [드롭영역 2] */)
            {
                // 작업을 수행합니다.
            }
        }
    }
    ```
  - 후보 비교식:
    - `dictionary == myInt`
    - `myFloat > myInt`
    - `myString == list`
    - `dictionary == list`
    - `myFloat <= 100`
  - 보기:
    - A. `myFloat > myInt`, `myFloat <= 100`, `dictionary == list`
    - B. `dictionary == myInt`, `myFloat > myInt`, `myString == list`
    - C. `dictionary == myInt`, `myString == list`, `dictionary == list`
    - D. `myFloat <= 100`, `myString == list`, `dictionary == list`

### [P04] Dictionary 초기화 순서
- 출처: 원문 39번
- 유형: 코드
- 문제:
  - `gameObjects` 목록으로 `Dictionary<string, GameObject> dictionary`를 초기화하는 코드를 작성하세요.
  - 조건:
    - key는 `gameObject.name`
    - value는 `gameObject`

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - null 안전 접근
- 출처 개념: U04 Null/Exception
- 유형: 코드
- 문제:
  - `projectile`이 null이면 0, 아니면 `projectile.transform.position.x`를 `xPos`에 담는 한 줄 코드를 작성하세요.
- 의도: null 검사 + 안전 대체값 패턴 전이

### [X02] 함정 - 타입 비교 가능성 판별
- 출처 개념: U04 Null/Exception
- 유형: 객관식
- 문제:
  - 컴파일 오류 없이 비교 가능한 식을 고르세요.
- 보기:
  - A. `dictionary == myInt`
  - B. `myString == list`
  - C. `dictionary == list`
  - D. `myFloat > myInt`
- 의도: 타입 불일치 비교와 숫자 비교를 구분

## 주차 체크
- 원문 대응 문항 수: 4
- 확장 문항 수: 2
- 총 문항 수: 6
