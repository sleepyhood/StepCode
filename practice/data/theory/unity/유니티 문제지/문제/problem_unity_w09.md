# Unity 주차 문제지 W09

## 주차 주제
- 유닛: U09 Animator
- 핵심 개념: 상태 배치, 상태 전환 T/F, 파라미터 타입별 Set 함수, `SetBool`, reset 전환 파라미터 선택

## 안내
- 아래 문항은 원문 대응 문항과 확장 문항으로 구성되어 있습니다.
- 이 문서의 `n번` 표기는 `practice/temp/유니티 1차 문제 풀이.md` 기준 문제 번호입니다.

## 원문 대응 문항
### [P01] 점프 상태 클립 배치
- 출처: 원문 15번
- 유형: 단답
- 문제:
  캐릭터의 점프 애니메이션 컨트롤러를 구성하려고 합니다.
  
  - 점프는 **Slow Jump** / **Fast Jump** 두 종류가 있습니다.
  - 점프 전에는 **Idle** 애니메이션 1개만 사용합니다.
  - 점프 정점(최고점) 구간은 **JumpApex** 애니메이션 1개만 사용합니다.
  - 제공된 애니메이션 클립을 선택하여, 그래프의 알맞은 상태(State)에 배치해 상태 시스템을 완성하세요.
  
  ![](유니티_15번.svg)
  
  ### 드래그 토큰(제공 클립)
  
  - `JumpApex`
  - `SlowFall`
  - `FastFall`
  - `FastLand`

### [P02] Animator 상태 시스템 전환 T/F
- 출처: 원문 31번
- 유형: 단답
- 문제:
  - 아래는 상태 시스템(State Machine) 전환에 대한 설명입니다. 
  - 아래 4문장의 참/거짓을 순서대로 쓰세요.
  - 1. Entry 전환으로 시작 상태를 제어할 수 있다.
  - 2. 기본 상태를 포함하거나 제외하고 상태 시스템을 생성할 수 있다.
  - 3. 하위 상태 머신은 별도의 상태 시스템처럼 동작한다.
  - 4. 상태에서 상태 시스템으로는 전환할 수 없다.

### [P03] Set 함수 매칭
- 출처: 원문 32번
- 유형: 단답
- 문제:
  - 아래 빈칸에 들어갈 함수명을 쓰세요.
  - ① `(\"Animation\", 1)`
  - ② `(\"Animation\", .5f)`
  - ③ `(\"Animation\", false)`
  - ④ `(\"Animation\")`
  - 답안 형식 예: `① SetInt, ② SetFloat, ③ SetBool, ④ SetTrigger`

### [P04] `SetBool` 코드 완성
- 출처: 원문 33번
- 유형: 단답
- 문제:
  `Animator` 참조 변수에 대해, 드롭다운을 사용하여 Boolean 매개 변수 `"Attacking"`을 **false**로 설정하세요.
드롭다운 목록에서 올바른 옵션을 선택하여 코드를 완성하십시오.

### 자료(코드)

```csharp
Animator animator;

void OnTriggerEnter2D(Collider2D collider)
{
    GameObject obj = collider.gameObject;

    if (obj.GetComponent<Player>())
    {
        [드롭다운 ①].SetBool [드롭다운 ②]
    }
}
```

### 보기(드롭다운 후보)

**드롭다운 ① (호출 주체)**

- `Animator`
- `animator`

**드롭다운 ② (인수 형태)**

- `(Attacking, false);`
- `("Attacking", "false");`
- `("Attacking", false);`
- `(Attacking, "false");`

### [P05] reset 전환 파라미터 선택
- 출처: 원문 35번
- 유형: 단답
- 문제:다음 조건을 만족하도록 문장을 완성해야 합니다.

- 장면은 **재생(Play) 모드**입니다.
- 현재 Animator의 상태는 **`friendly`** 입니다.
- **`Search` 매개변수(Trigger)** 는 **`reset`** 상태로 전환하는 데 사용됩니다.

그래픽(Animator 그래프/파라미터 목록)을 참고하여, 드롭다운에서 올바른 옵션을 선택해 문장을 완성하세요.

![](유니티_35번.svg)

---

### 답안 문장(빈칸)

> 트리거 **[ ① ]** 및 Bool을 **[ ② ]** `false`로 설정하십시오.

### 보기(드롭다운 후보)

- `LockOn`
- `Search`
- `Friendly`
- `Enemy`


## 확장 문항 (변형/함정/응용)
### [X01] 변형 - 이동 속도 파라미터 갱신 코드
- 출처 개념: U09 Animator
- 유형: 코드
- 문제:
  - `Animator animator`가 있을 때, float 파라미터 `\"Speed\"`를 `playerSpeed` 변수값으로 갱신하는 1줄 코드를 작성하세요.
- 의도: 타입-함수 매칭을 실제 코드로 전이

### [X02] 함정 - Trigger 호출 문법 선택
- 출처 개념: U09 Animator
- 유형: 객관식
- 문제:
  - Trigger 파라미터 `Search`를 발동하는 올바른 코드를 고르세요.
- 보기:
  - A. `animator.SetBool("Search", true);`
  - B. `animator.SetTrigger("Search");`
  - C. `animator.SetInt("Search", 1);`
  - D. `animator.SetFloat("Search", 1f);`
- 의도: 파라미터 타입과 API 오용 방지

## 주차 체크
- 원문 대응 문항 수: 5
- 확장 문항 수: 2
- 총 문항 수: 7
