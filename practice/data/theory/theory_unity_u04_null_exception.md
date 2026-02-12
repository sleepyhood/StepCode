# Unity U04 Null/예외 기초
## 학습 목표
- NullReferenceException의 원인을 빠르게 찾는다.
- null 체크/컬렉션 초기화 코드를 정확히 작성한다.
## 범위
- 출처 매핑: `practice/temp/유니티 1차 문제 풀이.md`의 1, 10, 37, 39번
- 키워드: null, NullReferenceException, Dictionary, 타입 불일치
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
