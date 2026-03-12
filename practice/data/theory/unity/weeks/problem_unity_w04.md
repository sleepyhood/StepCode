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
  - 다음은 중첩된 객체 구조를 가진 C# 스크립트 예제입니다. 이 스크립트를 컴파일하고 `Start()` 함수가 호출되어 실행될 때 런타임에서 `NullReferenceException` 오류가 발생하며 게임이 멈춥니다.
  - 해당 예외(Exception)가 발생하는 가장 직접적인 메모리 참조 원인을 하나 고르세요.
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
  - A. `book`의 인스턴스 생성이 실패하여 `book` 변수가 null이다.
  - B. `Age` 프로퍼티 값에 접근하려 했으나 기본값이 없어서 null이다.
  - C. 전역 변수 `publisher`가 초기화되지 않았으므로 null 예외가 난다.
  - D. 새로 생성된 `book` 내부의 멤버 객체인 `Author`가 아직 인스턴스화되지 않아 null 상태이다.

### [P02] null 비교 가능한 선언/조건식 선택
- 출처: 원문 10번
- 유형: 객관식
- 문제:
  - 변수의 자료형(값 타입 vs 참조 타입)에 따라 `null`과 비교될 수 있는지가 결정됩니다. 유니티 C# 스크립트에서 컴파일 오류 없이 안전하게 `[드롭다운 ②]` 조건식 안에서 `null` 비교를 수행하기 위해, `[드롭다운 ①]`에 위치해야 할 변수 선언문과 짝을 이룬 가장 논리적인 항목을 고르세요.
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
- 보기:
  - A. `① public bool hasTurned;` / `② (hasTurned == null)`
  - B. `① public int score;` / `② (score == null)`
  - C. `① public GameObject projectile;` / `② (projectile == null)`

### [P03] 드롭영역에 들어갈 수 없는 비교식 3개 찾기
- 출처: 원문 37번
- 유형: 객관식
- 문제:
  - 다음 코드에는 여러 가지 타입(`List`, `Dictionary`, `int`, `string` 등)의 변수들이 선언되어 있으며, 하단 `if` 문의 비교 조건식으로 활용하려 합니다.
  - 객체의 타입이 서로 본질적으로 달라 **애초에 C# 컴파일러가 등가(==) 비교 자체를 거부하여 컴파일 오류를 발생시키는 무효한 비교식 3개**를 보기 중에서 찾아 답안 영역에 적으세요.

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
  - 다음 Unity 스크립트는 인스펙터에 할당된 게임 오브젝트 목록(`gameObjects`)을 활용하여, 오브젝트의 이름을 키(Key)로, 오브젝트 자체를 값(Value)으로 가지는 새로운 `Dictionary`를 생성하고 안의 요소를 채우는 과정을 보여줍니다.
  - 에러나 `NullReferenceException`이 발생하지 않도록, 아래 `Start()` 내부의 `// your code will go here.` 위치에 들어갈 **C# 코드 조각 4개를 보기에서 골라, 올바른 문법적 흐름이 되도록 위에서부터 순서대로 나열**하세요.

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
  - 현재 씬에 `projectile` 이라는 변수가 있습니다. 이 변수가 참조하는 대상이 소멸되어 `null`일 경우에는 0 값을, 객체가 정상적으로 씬에 존재할 경우에는 해당 객체의 Transform X 좌표 값(`projectile.transform.position.x`)을 가져와서 부동소수점 변수 `xPos`에 할당하고자 합니다.
  - 삼항 연산자(`? :`)를 이용하여 `NullReferenceException` 예외 없이 이 값 할당 과정과 흐름을 완벽하게 처리하는 C# 코드를 단 한 줄로 작성하세요.
- 의도: 단일 구문 내에서 참조 타입 객체의 null 여부를 먼저 체크한 뒤 분기별로 안전한 기본 데이터형을 담는 방어 코딩 숙달을 테스트합니다.

### [X02] 함정 - 타입 비교 가능성 판별
- 출처 개념: U04 Null/Exception
- 유형: 객관식
- 문제:
  - 다음 비교식 목록 중에서 자료형 불일치(Type Mismatch)로 인한 컴파일 에러가 **발생하지 않고**, 정상적으로 컴파일되어 내부적인 논리 판단 구문이 끝까지 실행되는 가장 올바른 비교 연산 수식 형태 한 개를 고르세요.
- 보기:
  - A. `dictionary == myInt` (딕셔너리와 정수형 비교)
  - B. `myString == list` (문자열과 리스트 컴포넌트 비교)
  - C. `dictionary == list` (딕셔너리와 리스트 혼합 비교)
  - D. `myFloat > myInt` (실수형 변수와 정수형 변수 대소 비교)
- 의도: 값의 메모리 형태가 완전히 다른 컬렉션 객체 간의 억지스러운 기형적 비교 한계와, C# 시스템의 원시 숫자 자료형들 간에는 자체 호환 캐스팅 및 비교가 가능함을 엄격히 구분하도록 유도합니다.

## 주차 체크
- 원문 대응 문항 수: 4
- 확장 문항 수: 2
- 총 문항 수: 6
