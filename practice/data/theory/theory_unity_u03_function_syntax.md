# Unity U03 함수/static 기초
## 학습 목표
- 올바른 함수 선언 형식을 작성한다.
- static 멤버의 사용 규칙을 이해한다.
## 범위
- 출처 매핑: `practice/temp/유니티 1차 문제 풀이.md`의 25, 28번
- 키워드: 반환형, 매개변수, static 메서드, static 필드
## 핵심 패턴
~~~csharp
private static int Add(int a, int b)
{
    return a + b;
}

private void ShowMessage(string msg)
{
    Debug.Log(msg);
}
~~~
### 패턴 해설
- `private static int Add(int a, int b)`는 "접근제어자 + static + 반환형 + 함수명 + 매개변수"의 기본 시그니처 구조를 보여준다.
- 반환형이 `int`이면 모든 실행 경로에서 `return`으로 값을 돌려줘야 한다.
- `private void ShowMessage(string msg)`는 반환값 없는 함수 패턴이며, 외부 입력(`msg`)을 받아 내부 동작(로그 출력)을 수행한다.
- static 함수는 인스턴스 없이 호출 가능하지만, 인스턴스 필드/메서드를 직접 접근할 수 없다.
- 즉, "유틸성 계산 함수(Add)는 static", "오브젝트 상태를 다루는 함수(ShowMessage)는 instance"처럼 역할을 분리하는 것이 핵심이다.
## 자주 하는 실수
- 반환형이 있는데 `return`을 누락함
- static 문맥에서 인스턴스 멤버를 직접 접근함
- 메서드 이름 대소문자를 틀려 호출이 깨짐
## 미니 체크
### Q1
반환값이 없는 함수의 반환형은?
- 정답: void
### Q2
static 메서드가 인스턴스 필드를 바로 접근할 수 있나요?
- 정답: 아니오
## 연결 세트
- 기초: unity_u03_function_syntax_b01
- 챌린지: unity_u03_function_syntax_c01
