# Unity U04 Null/예외 기초

## 학습 목표
- NullReferenceException의 발생 원인을 파악하고 안전한 참조 코드를 작성한다.
- 서로 다른 데이터 타입 간의 올바른 비교 연산 규칙을 이해한다.
- Dictionary 초기화 및 foreach, var 키워드의 올바른 사용법을 익힌다.

## 범위
- 키워드: null, NullReferenceException, Dictionary, 타입 불일치 비교, var, foreach

## 핵심 패턴
```csharp
public class GameManager : MonoBehaviour
{
    private Dictionary<string, int> scoreDictionary;
    public Transform target; // 외부(Inspector)에서 할당하지 않으면 null 상태

    void Start()
    {
        // 1. 객체(컬렉션) 초기화 없이 접근 -> NullReferenceException (함정)
        // scoreDictionary.Add("Player1", 100); 

        // 2. 정상 초기화 후 사용 (기본)
        scoreDictionary = new Dictionary<string, int>();
        scoreDictionary.Add("Player1", 100);

        // 3. 참조 타입 null 체크 패턴 (기본)
        if (target != null)
        {
            Debug.Log(target.position);
        }
    }
}
```

## 문항 핵심 포인트

### 1) NullReferenceException과 객체 생성 (`new`)
- 개념: 클래스 변수는 선언만으로는 공간(이름표)만 만들어질 뿐이며, 실제 메모리 공간(객체)을 할당하려면 반드시 `new 클래스명()`을 호출해야 한다. 초기화 없이 변수 내부의 멤버(필드, 메서드)에 접근하면 변수가 비어있는 `null` 상태이므로 런타임에 에러가 발생한다.
- 오답 포인트: 클래스의 멤버에 접근하는 코드에서 해당 객체가 스크립트 상에서 `new`로 생성되었는지, 혹은 유니티 Inspector 등 외부에서 참조가 올바로 할당되어 있는지 확인하지 않는 경우이다.
- 정답 판별: 오류가 발생하는 줄에서 접근 대상 객체가 이전에 `new` 연산자로 정상 초기화가 이루어졌는지 먼저 파악한다. 그렇지 않다면 예외 상황이다.

![NullReference Exception 콘솔 에러](./data/theory/images/unity_u04_null_exception_console.svg)
*캡션: 인스턴스가 존재하지 않는 객체 변수에 접근할 때 Unity Console에서 출력되는 대표적인 NullReferenceException 메시지 예시.*

### 2) 데이터 타입 비교와 타입 불일치 (Type Mismatch)
- 개념: `==`, `<`, `>` 같은 비교 연산자는 기본적으로 자료형(타입)이 서로 같은 것들끼리 수행해야 한다. 단, `int`와 `float`처럼 컴파일러가 크기 손실 없이 자동으로 형 변환을 해줄 수 있는 숫자형끼리는 안전하게 비교가 가능하다.
- 오답 포인트: 데이터의 의미 자체가 다른 기준(예: 문자열 `string`과 정수 `int`)을 억지로 `==` 연산자로 비교하려고 시도하는 경우이다. 이 경우 프로그램이 아예 실행(컴파일)되지 않는다.
- 정답 판별: 비교 연산자 좌우의 변수 타입이 동일한지, 혹은 정수와 실수처럼 의미상 호환 가능한 허용된 타입인지 확인한다.

![Type Mismatch 에러](./data/theory/images/unity_u04_type_mismatch_error.svg)
*캡션: 호환되지 않는 타입(문자열과 정수) 사이에서 비교 연산자(==)를 사용하려 할 때 발생하는 C# IDE 컴파일 에러 예시.*

### 3) Dictionary (딕셔너리) 초기화 및 사용 문법
- 개념: Dictionary는 특정 `key`(인덱스 역할)를 통해 `value`(값)를 저장하고 읽어오는 컬렉션 구조이다. 배열은 인덱스가 0, 1, 2 등의 자연수(int)로 고정되어 있지만, Dictionary는 `string`, `class` 등 다양한 타입을 키(key)로 활용할 수 있다. 사용 시에는 `new Dictionary<키_타입, 값_타입>()` 구문으로 필수 초기화를 거쳐야 한다.
- 오답 포인트: Dictionary 변수를 선언만 해두고, `new`를 통한 초기화를 빼먹은 채 `d["ABCD"] = 5;` 처럼 요소를 즉시 삽입하려 하는 경우 NullException을 발생시킨다.
- 정답 판별: 제네릭 타입 종류(Key, Value 대응)와 초기화 구문(`new Dictionary()`)이 선언부에 정확히 명시되어 있는지 확인한다.

### 4) 암시적 타입 `var`
- 개념: `var` 키워드는 프로그래머가 명시적으로 타입을 쓰지 않아도 대입 연산자(`=`) 오른쪽 값의 출처를 분석해 컴파일러가 스스로 자료형을 결정해주는 문법이다.
- 오답 포인트: 변수 선언 줄에서(`var temp;`) 초기값을 대입하지 않고 아랫줄에 가서야 값(`temp = 3;`)을 넣으려 하는 경우이다. 컴파일러가 처음 만나는 선언 시점에 타입을 구별할 수 없어 오류가 난다.
- 정답 판별: `var` 로 정의된 변수가 **선언하는 즉시 특정 초기값으로 할당(=)** 되었는지 확인한다.

![var 초기화 누락 에러](./data/theory/images/unity_u04_var_initialization_error.svg)
*캡션: var 키워드로 변수를 선언할 때 같은 줄에서 초기화를 수행하지 않으면 발생하는 CS0818 컴파일 오류 화면.*

### 5) foreach 반복문
- 개념: `foreach`는 배열, List, Dictionary 등 다수의 값을 가진 '컬렉션(집합)' 자료형 내부를 처음부터 끝까지 순회할 때 쓰는 반복문이다. 컬렉션의 길이를 알고 있어 인덱스 초과 에러(IndexOutOfRange)를 낼 위험이 적다.
- 오답 포인트: 반복자료 지정 위치(`in` 뒤쪽)에 여러 개의 데이터가 아닌 낱개의 단일 값을 넣으려 하거나, 뽑아낼 변수의 타입(`in` 앞쪽)이 컬렉션 내부 요소의 실제 타입과 일치하지 않는 경우이다.
- 정답 판별: `in` 앞쪽의 변수 타입과 뒷쪽의 컬렉션 아이템 타입이 알맞게 연결되어 있는지 확인한다.

## 자주 하는 실수
- 클래스 내부에 다른 클래스 필드를 선언해놓고, 하위 객체의 `new` 호출을 잊음
- 조건문 안에서 의미가 다른 문자열과 숫자를 `==`로 직접 비교하려 함
- `var`를 값 할당 없이 단독으로 선언만 하여 컴파일 에러 유발
- Dictionary 변수를 선언만 하고 초기화 전 요소(`Add`)를 집어넣음

## 빠른 체크리스트
- 클래스 객체나 컬렉션 사용 전 `new`로 메모리 할당이 올바르게 이루어졌는가?
- 조건식의 양변 데이터 타입이 서로 비교 가능한 안전한 타입(숫자형 대 숫자형 등)인가?
- `var` 변수를 사용할 때 선언 줄에 곧바로 값을 세팅하였는가?
- `foreach` 문법에서 뽑아오는 요소의 타입과 컬렉션 타입이 잘 맞아떨어지는가?

## 미니 체크
### Q1
`var count; count = 10;` 문장은 정상적으로 빌드되는가? 그 이유는?
- 정답: 아니오. `var`를 사용할 때는 반드시 선언과 동시에 초기값이 할당되어야만 타입 추론이 가능하다.

### Q2
`int` 타입과 `float` 타입 변수를 부등호(`<, >`)로 비교할 수 있는가?
- 정답: 대상이 상이한 자료형이더라도 숫자형의 경우 낮은 정밀도(`int`)가 높은 정밀도(`float`)로 자동 변환되어 비교가 성립한다.

### Q3
`public GameObject player;` 라고 선언한 뒤, Inspector에서 할당하지 않은 채 `player.transform.position` 값에 접근하면 콘솔창에는 어떤 에러(Exception)가 기록되는가?
- 정답: NullReferenceException

## 연결 세트
- 기초: unity_u04_null_exception_b01
- 챌린지: unity_u04_null_exception_c01
