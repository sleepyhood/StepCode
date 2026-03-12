# Unity 주차 문제지 W02

## 주차 주제
- 유닛: U02 Log/Operator
- 핵심 개념: Debug.Log, 연산자 구분(=, ==, !=, ||, %), 명명 규칙, API 대소문자

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] 콘솔 출력 API
- 출처: 원문 8번
- 유형: 객관식
- 문제:
  - Unity 콘솔에 문자열 `"Hello World!"`를 출력하는 올바른 코드를 고르세요.
- 보기:
  - A. `Console.Log("Hello World!");`
  - B. `Debug.Log("Hello World!");`
  - C. `print.log("Hello World!");`
  - D. `System.Log("Hello World!");`

### [P02] 연산자 의미 매칭
- 출처: 원문 3번
- 유형: 매칭
- 문제:
  - 다음 연산자를 의미와 연결하세요.
  - 연산자: `=`, `==`, `!=`, `++`, `+`
  - 의미 후보: 할당, 같음 비교, 같지 않음 비교, 1 증가, 문자열 연결
  - 답안 형식 예: `` `=`-할당, `==`-같음, `!=`-같지 않음, `++`-1 증가, `+`-문자열 연결 ``

### [P03] OR 조건식 판별
- 출처: 원문 12번
- 유형: 객관식
- 문제:
  - `hp <= 0` 또는 `timeOver == true`일 때 실행되어야 합니다. 알맞은 조건식을 고르세요.
- 보기:
  - A. `if (hp <= 0 && timeOver == true)`
  - B. `if (hp <= 0 || timeOver == true)`
  - C. `if (hp <= 0 = timeOver == true)`
  - D. `if (hp <= 0 != timeOver == true)`

### [P04] 나머지 연산
- 출처: 원문 27번
- 유형: 단답
- 문제:
  - 변수 `i`가 짝수인지 판별하는 조건식을 작성하세요.
  - `if (...)` 전체가 아닌 괄호 안 조건식만 작성해도 정답 처리됩니다.

### [P05] 명명 규칙 판별 1
- 출처: 원문 17번
- 유형: 참거짓
- 문제:
  - 아래 문장의 참/거짓을 판별하세요.
  - (1) `MonoBehaviour`는 대소문자를 정확히 맞춰야 한다.
  - (2) 이벤트 함수명은 `ontriggerenter`처럼 소문자로 시작해도 정상 호출된다.
  - 답안 형식 예: `(1) 참, (2) 거짓`

### [P06] 명명 규칙 판별 2
- 출처: 원문 21번
- 유형: 객관식
- 문제:
  - 올바른 Unity API/키워드 조합을 고르세요.
- 보기:
  - A. `compareTag`, `Enabled`, `Public`
  - B. `CompareTag`, `enabled`, `public`
  - C. `Comparetag`, `enabled`, `Public`
  - D. `comparetag`, `Enabled`, `public`

## 확장 문항 (변형/함정/응용)
### [X01] 변형 - 로그 + 판별 결과 출력
- 출처 개념: U02 / `%`, `==`, `Debug.Log`
- 유형: 코드
- 문제:
  - `n`이 홀수인지 판별해 `isOdd=`와 함께 콘솔 출력하는 두 줄 코드를 작성하세요.
- 의도: 계산 -> 비교 -> 출력의 표준 흐름 전이

### [X02] 함정 - 대소문자 오류 찾기
- 출처 개념: U02 / Unity 식별자 대소문자
- 유형: 객관식
- 문제:
  - 아래 중 컴파일 또는 호출 실패를 유발하는 코드를 고르세요.
- 보기:
  - A. `other.CompareTag("Player")`
  - B. `void OnTriggerEnter(Collider other)`
  - C. `void onTriggerEnter(Collider other)`
  - D. `Debug.Log("ok")`
- 의도: 이벤트 함수명 대소문자 함정 제거

## 주차 체크
- 원문 대응 문항 수: 6
- 확장 문항 수: 2
- 총 문항 수: 8
