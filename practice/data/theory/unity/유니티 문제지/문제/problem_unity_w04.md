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
```csharp
public class Person { public int Age { get; set; } }
public class Book { public Person Author { get; set; } }

public class PublishBook
  {
    private string publisher;
    private Genre genre;

    public void Start()
    {
      Book book = new Book();
      int authorAge = book.Author.Age; // ❌ 예외 발생 지점
      Debug.Log(publisher);
      Debug.Log(genre);
    }
  }
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
```csharp
[드롭다운 ①: 변수 선언]

void Start()
{
    if ([드롭다운 ②])
    {
        Debug.Log("Object is null");
    }
    else
    {
        projectile = GameObject.FindWithTag("Projectile");
    }
}
```
- 위 코드를 보고 드롭다운 ①과 ②에 들어갈 것으로 올바른 것을 고르세요.
- 보기:
  - 드롭다운 ①(변수 선언): `public bool hasTurned;`, `public GameObject projectile;`, `public int score;`
  - 드롭다운 ②(조건식): `(projectile == null)`, `(hasTurned == null)`, `(score == null)`

### [P03] 드롭영역에 들어갈 수 없는 비교식 3개 찾기
- 출처: 원문 37번
- 유형: 객관식
- 문제:
  - 아래 코드에는 **변수 비교(Comparison)** 때문에 컴파일이 실패하는 부분이 있습니다.
보기 중에서 **컴파일 오류를 발생시키는 비교식 3개**를 골라 답안 영역에 배치하세요.

---

### 자료(코드)

```csharp
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

---

### 보기(드래그 후보)

- `dictionary == myInt`
- `myFloat > myInt`
- `myString == list`
- `dictionary == list`
- `myFloat <= 100`

---

### [P04] Dictionary 초기화 순서
- 출처: 원문 39번
- 유형: 코드
- 문제:
  - 다음 Unity 스크립트에서 `gameObjects` 목록을 사용해 `dictionary` 변수를 초기화하세요.
  - **키(key)** 는 각 `GameObject`의 **이름(`gameObject.name`)** 이어야 합니다.
  - 아래 코드의 `Start()` 내부 `// your code will go here.` 위치에 들어갈 **올바른 코드 조각 4개를 골라**, **올바른 순서로** 배치하세요.

---

### 자료(코드)

```csharp
using System.Collections.Generic;
using UnityEngine;

public class MyClass : MonoBehaviour
{
    [SerializeField]
    List<GameObject> gameObjects;

    private Dictionary<string, GameObject> dictionary;

    private void Start()
    {
        // your code will go here.
    }
}
```

### 보기(코드 조각)

A.

```csharp
foreach (var gameObject in dictionary) {
```

B.

```csharp
gameObjects.Add(gameObject);
```

C.

```csharp
dictionary.Add(gameObject.name, gameObject);
```

D.

```csharp
dictionary = new Dictionary<string, GameObject>();
```

E.

```csharp
foreach (var gameObject in gameObjects) {
```

F.

```csharp
}
```

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
