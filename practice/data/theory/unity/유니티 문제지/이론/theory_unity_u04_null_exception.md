# Unity U04 Null/예외 기초
## 학습 목표
- NullReferenceException의 원인을 빠르게 찾는다.
- null 체크/컬렉션 초기화 코드를 정확히 작성한다.
## 범위
- 출처 매핑: `practice/temp/유니티 1차 문제 풀이.md`의 1, 10, 37, 39번
- 키워드: null, NullReferenceException, Dictionary, 타입 불일치
## 문항 핵심 포인트
### 1) 객체를 선언하는 방법
- 아래와 같이 Example 이라는 클래스가 있을 때 이 클래스에 해당하는 객체를 선언하려면 Example ex = new Example(); 라고 해주면 된다.<br> 

    ```csharp
    class Example{
        ...
    }
    ```
    <br>class 안에 다른 클래스 변수가 있다면 어떨까?
    ```csharp
    
    class Example{
        ...
        
    }
    class Example2{
        public int a = 3;
        public Example Ex;
    }

    Example2 Ex2 = new Example2();
    Ex2.Ex = new Example(); // 이 부분이 없으면 아래 코드는 오류가 발생한다. Ex2만 존재하고 Ex2 내부의 Ex는 존재하지 않기 때문.
    Ex2.Ex.a += 1; 
    ```
    
 
### 2) 비교할 때는 자료형이 동일해야 한다.
- ==, <, > 와 같이 비교연산을 할 때에는 서로 자료형(타입)이 같은 것 끼리 비교를 해야한다. <br>
서로 타입이 다른 것 끼리 비교를 하려고 하면 오류가 발생한다. ex) string과 int를 비교하려고 하는 경우<br>
하지만, int와 float는 비교가 가능하다. 왜냐면 int와 float를 비교할 때에는 컴파일러가 int를 자동으로 float로 바꿔주기 때문.<br><br>
결론)<br>
자료형이 다르더라도 정수와 실수처럼 비교하는 게 자연스럽다면 비교 연산이 허용되고,<br>
string과 int의 비교처럼 비교의 기준이 명확하지 않다면 허용되지 않는다.


### 3) Dictionary
- Dictionary는 간단하게 말하면 배열과 비슷한데 조금 다르다. 
    예를 들어, 배열은 아래와 같이 사용할 수 있다.(C와 C#에서 배열 선언 방식이 조금 다르다.)<br>
    ```csharp
    int[] a = new int[10]; a[5] = 3;
    ```
    이렇게 하면 a라는 배열의 5번 인덱스의 값이 3이 된다. 여기서 **값**의 자료형을 바꾸려면 int[] a를 float[] a로 바꾸는 방식으로 가능하다.<br>
    하지만 배열의 **인덱스**는 항상 자료형이 고정이다. (0, 1, 2, 3...)항상 0을 포함한 자연수이다.<br>
    반면에 dictionary는 인덱스의 자료형을 바꾸는게 가능하다. (dictionary에서는 인덱스가 아니라 **key** 라고 표현한다) dictionary는 아래와 같이 사용한다.<br>
    ```csharp
    Dictionary<string, int> d = new Dictionary<string, int>();
    d["ABCD"] = 5;
    ```
    위와 같이 작성하면 인덱스(key)의 자료형은 string이고 값의 자료형은 int가 된다. <br>
    d["ABCD"] = 5는 "ABCD"라는 위치에 5가 들어간 것이다.<br>
    "ABCD"라는 자리가 기존에 존재했으면 5로 값이 바뀌는거고 없었다면 새로 만들면서 5를 집어넣는다.<br>

### 4) var
- 우리는 변수를 만들 때 보통 다음과 같이 했다. int a = 3; float b = 3.14f; string c = "abcd";<br>
변수 안에 들어갈 값에 맞게 적절하게 자료형을 적어줘야 했는데 var은 아래와 같이 어떤 자료형이든 사용이 가능하다.<br>
var a = 3; var b = 3.14; var c = "abcd";<br>
var은 **=** 의 오른쪽을 보고 알아서 해석해서 자료형을 결정해준다.<br>
때문에 아래와 같은 주의점이 있다.<br>
    ```csharp
    var a;
    a = 3;
    ```
    이런건 안 된다. var a; 가 실행되는 시점에 a에 무슨 값이 들어가는지가 정해져 있지 않아서 오류가 발생한다. 
    var a = 3; 이렇게 한 줄에 써줘야 한다.

### 5) foreach
- for문과 비슷한데 조금 다르다. 기본적인 사용법은 아래와 같다.
    ```csharp
    int[] arr = {1,2,3};
    foreach(int i in arr){
        // i의 값에 1, 2, 3이 순서대로 들어가면서 반복된다.
    }
    ```
    in 뒤에는 배열뿐만 아니라 위에서 배운 dictionary 같이 **여러개의 값을 갖는 자료**가 올 수 있다.<br>
    여러개의 값이 순서대로 i에 들어가면서 반복문이 실행된다. 마지막 값이 i에 들어간 상태에서 foreach 내부 코드가 실행되고 반복은 끝나게 된다.
## 핵심 패턴
~~~csharp
private Dictionary<string, GameObject> dictionary;

void Start()
{
    dictionary = new Dictionary<string, GameObject>();
    if (projectile == null)
    {
        Debug.Log("Object is null");
    }
}
~~~
### 패턴 해설
- `dictionary = new Dictionary<string, GameObject>();`는 컬렉션 사용 전 초기화의 기본 규칙이다. 초기화 이전 `Add` 호출은 런타임 오류로 이어진다.
- `if (projectile == null)`은 참조 타입 안전성 확인 패턴이며, 멤버 접근 전에 방어적으로 검사할 때 사용한다.
- NullReferenceException은 대부분 "null 객체의 멤버 접근"에서 발생한다. 따라서 접근 전에 null 검사 여부를 먼저 확인한다.
- 타입 불일치 비교(예: `dictionary == list`)는 런타임 이전에 컴파일 단계에서 막힌다. null 문제와 타입 문제를 구분해서 진단해야 한다.
- 실전 디버깅 순서는 "초기화 여부 -> null 검사 -> 타입 일치 여부"로 잡으면 문제 원인을 빠르게 좁힐 수 있다.
## 자주 하는 실수
- null 객체(`book.Author`)의 멤버를 바로 접근함
- 비교 불가능한 타입을 `==`로 비교함
- Dictionary를 초기화하지 않고 바로 사용함
## 미니 체크
### Q1
NullReferenceException의 직접 원인은?
- 정답: null 참조 역참조
### Q2
`projectile` null 체크 식을 쓰세요.
- 정답: `projectile == null`
## 연결 세트
- 기초: unity_u04_null_exception_b01
- 챌린지: unity_u04_null_exception_c01
