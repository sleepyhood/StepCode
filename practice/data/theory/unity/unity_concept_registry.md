# Unity Concept Registry

## 목적
- Unity 이론서, 주차 문제, 세트 JSON에서 같은 개념을 같은 ID로 추적하기 위한 기준 문서입니다.
- `conceptRef`는 대표 개념 1개, `conceptRefs`는 보조 개념 목록으로 사용합니다.
- 학생에게 보이는 배지명은 내부 ID와 분리합니다.

## ID 규칙
- 형식: `uNN_cM`
- 예: `u01_c1`, `u02_c4`, `u09_c3`
- `id`는 짧고 안정적으로 유지합니다.
- 화면용 이름은 `label`, 간단 배지는 `badge`를 사용합니다.

## 개념 설계 원칙
- 한 개념은 문항 1~3개가 공통으로 참조할 수 있는 최소 학습 단위로 자릅니다.
- 대표 개념(`conceptRef`)은 정답 판단의 중심이 되는 개념 1개만 둡니다.
- 보조 개념(`conceptRefs`)은 해설에 실질적으로 등장하는 개념만 1~3개까지 둡니다.
- `conceptRef`는 반드시 `conceptRefs`에도 포함합니다.

## U01
- `u01_c1`
  - label: `Inspector 기본 기능`
  - badge: `Inspector`
  - summary: `Static, Tag, Prefab의 역할과 오답 포인트`
- `u01_c2`
  - label: `Unity 주요 창 역할`
  - badge: `Editor`
  - summary: `Hierarchy, Scene, Project, Inspector의 역할 구분`
- `u01_c3`
  - label: `External Script Editor 설정`
  - badge: `IDE`
  - summary: `External Tools와 External Script Editor 옵션 구분`
- `u01_c4`
  - label: `Scene 배치 도구와 좌표계`
  - badge: `Scene`
  - summary: `Local/Global, Universal Tool, Vertex Snapping, Transform 수치 입력`
- `u01_c5`
  - label: `Inspector 필드 노출`
  - badge: `SerializeField`
  - summary: `public, private, [SerializeField]에 따른 Inspector 노출 규칙`
- `u01_c6`
  - label: `Tag 검색 API`
  - badge: `Tag`
  - summary: `FindGameObjectsWithTag와 배열 반환 패턴`

## U02
- `u02_c1`
  - label: `Debug.Log와 콘솔 출력`
  - badge: `Debug.Log`
  - summary: `Unity 콘솔 출력 API와 문자열 결합 기본형`
- `u02_c2`
  - label: `기본 연산자 구분`
  - badge: `Operators`
  - summary: `=, ==, !=, ++, +의 역할 구분`
- `u02_c3`
  - label: `OR 조건식과 나머지 연산`
  - badge: `Conditions`
  - summary: `||, %, ==, !=를 이용한 조건식과 짝수/홀수 판별`
- `u02_c4`
  - label: `Unity/C# 명명 규칙`
  - badge: `Naming`
  - summary: `MonoBehaviour, OnTriggerEnter, CompareTag, enabled, public의 대소문자 규칙`

## U03
- `u03_c1`
  - label: `반환형과 매개변수`
  - badge: `Function`
  - summary: `void, return, parameter 기본 구문`
- `u03_c2`
  - label: `Unity 이벤트 함수와 일반 함수`
  - badge: `Lifecycle`
  - summary: `Start, Update 같은 이벤트 함수와 사용자 함수 구분`
- `u03_c3`
  - label: `static 필드와 static 메서드`
  - badge: `static`
  - summary: `정적 문맥과 인스턴스 문맥의 차이`
- `u03_c4`
  - label: `함수 시그니처 조립`
  - badge: `Signature`
  - summary: `접근 제한자, 반환형, 이름, 매개변수 조합`

## U04
- `u04_c1`
  - label: `NullReferenceException 추적`
  - badge: `Null`
  - summary: `null 참조 원인과 접근 순서 추적`
- `u04_c2`
  - label: `값 타입과 참조 타입`
  - badge: `Type`
  - summary: `null 비교 가능 여부와 타입 차이`
- `u04_c3`
  - label: `컬렉션 초기화와 순회`
  - badge: `Collection`
  - summary: `Dictionary 초기화, foreach, Add 순서`
- `u04_c4`
  - label: `삼항 연산자와 var`
  - badge: `Syntax`
  - summary: `조건식과 타입 추론 기본 흐름`

## U05
- `u05_c1`
  - label: `배열과 반환형`
  - badge: `Array`
  - summary: `중첩 클래스 배열과 배열 반환형`
- `u05_c2`
  - label: `Transform 자식 순회`
  - badge: `Transform`
  - summary: `childCount, GetChild, for 루프 패턴`
- `u05_c3`
  - label: `Awake OnEnable Start 역할 구분`
  - badge: `Lifecycle`
  - summary: `초기화 책임과 호출 시점 분리`

## U06
- `u06_c1`
  - label: `키 입력 타이밍`
  - badge: `Input`
  - summary: `GetKey, GetKeyDown, GetKeyUp 차이`
- `u06_c2`
  - label: `축 입력과 deltaTime`
  - badge: `Axis`
  - summary: `GetAxis, GetAxisRaw, Time.deltaTime 흐름`
- `u06_c3`
  - label: `이동 API 선택`
  - badge: `Movement`
  - summary: `Translate, 방향 벡터, 절대 위치 대입 비교`

## U07
- `u07_c1`
  - label: `Instantiate와 복제 직후 조작`
  - badge: `Instantiate`
  - summary: `복제 생성 후 velocity 초기화 패턴`
- `u07_c2`
  - label: `Rigidbody 타입과 물리 제어`
  - badge: `Rigidbody`
  - summary: `GetComponent<Rigidbody>()와 타입 일치`
- `u07_c3`
  - label: `transform.forward와 AddForce`
  - badge: `Force`
  - summary: `방향 벡터와 힘 크기 조합`
- `u07_c4`
  - label: `Trigger와 Collision 이벤트`
  - badge: `Trigger`
  - summary: `OnTriggerEnter와 OnCollisionEnter 구분`
- `u07_c5`
  - label: `Object Pooling과 Init`
  - badge: `Pooling`
  - summary: `재사용 객체 초기화와 풀링 흐름`

## U08
- `u08_c1`
  - label: `UI Text 갱신 3요소`
  - badge: `UI Text`
  - summary: `UnityEngine.UI, Text 변수, 문자열 대입`
- `u08_c2`
  - label: `메서드 선언 시그니처`
  - badge: `Signature`
  - summary: `반환형, 메서드명, 매개변수 일치`
- `u08_c3`
  - label: `OnMouseUp 메시지 함수`
  - badge: `Mouse`
  - summary: `private void OnMouseUp() 형태와 자동 호출`
- `u08_c4`
  - label: `AddListener 등록 위치`
  - badge: `Button`
  - summary: `Start에서 1회 등록하고 Update 누적을 피하는 규칙`

## U09
- `u09_c1`
  - label: `점프 상태 클립 배치`
  - badge: `Animator`
  - summary: `JumpApex, SlowFall, FastFall, FastLand 순서`
- `u09_c2`
  - label: `상태 머신 전환 구조`
  - badge: `State`
  - summary: `Entry, Default State, Sub-State Machine 역할`
- `u09_c3`
  - label: `Animator Set 함수 매칭`
  - badge: `Set API`
  - summary: `SetInteger, SetFloat, SetBool, SetTrigger 매칭`
- `u09_c4`
  - label: `Animator 인스턴스 호출`
  - badge: `animator`
  - summary: `animator.SetBool("Attacking", false) 문법`
- `u09_c5`
  - label: `reset 전환 파라미터`
  - badge: `Reset`
  - summary: `Trigger와 Bool 파라미터 역할 구분`

## U10
- `u10_c1`
  - label: `Color 타입과 변수명 구분`
  - badge: `Color`
  - summary: `Color 타입과 color 변수명의 차이`
- `u10_c2`
  - label: `Material.SetColor 시그니처`
  - badge: `SetColor`
  - summary: `SetColor(string, Color) 두 인자 구조`
- `u10_c3`
  - label: `셰이더 프로퍼티명 규칙`
  - badge: `"_Color"`
  - summary: `"\"_Color\"" 문자열 리터럴과 언더스코어 규칙`

## U11
- `u11_c1`
  - label: `ECS 실사용 판별`
  - badge: `ECS`
  - summary: `using 선언만으로는 부족하고 ECS 전용 타입 사용이 필요`
- `u11_c2`
  - label: `MonoBehaviour와 ECS 구분`
  - badge: `MonoBehaviour`
  - summary: `MonoBehaviour 상속 코드는 기본적으로 ECS 실사용이 아님`
- `u11_c3`
  - label: `ECS 최소 코드`
  - badge: `SystemBase`
  - summary: `using Unity.Entities와 ECS 전용 타입 상속/구현 최소 조건`
