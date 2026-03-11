# Unity U06 Input
## Goal
- Understand the core idea of this unit before solving problems.
- Review common mistakes first.
## Scope
- Topic: GetKey/GetKeyDown/GetKeyUp/GetAxis
- Source map: from practice/temp/유니티 목차.md

## 문항 핵심 포인트
### 1) 키보드/마우스를 눌렀을 때 실행되는 함수
(글이 길지만 어렵지 않으니 천천히 읽어봅시다)
- 키보드를 눌렀을 때를 감지하여 실행되는 함수의 예시는 아래와 같다.
    ```csharp
    public class KeyDownExample : MonoBehaviour
    {
        void Update()
        {
            if (Input.GetKeyDown(KeyCode.Space)) // 스페이스바를 눌렀을 때 한 번 실행됨.
            {
                Debug.Log("스페이스바");
            }
            if (Input.GetKeyDown(KeyCode.A))// A 키를 눌렀을 때 한 번 실행됨.
            {
                Debug.Log("A");
            }
            if (Input.GetKey(KeyCode.A))// A 키를 누르고 있는 동안 계속 실행됨.
            {
                Debug.Log("A");
            }
            if (Input.GetKeyUp(KeyCode.A))// A 키를 눌렀다가 뗄 때 한 번 실행됨.
            {
                Debug.Log("A");
            }
        }
    }
    ```


    ---

<br>

- 마우스를 눌렀을 때 실행되는 함수도 비슷하게 생겼다

    ```csharp
    public class KeyDownExample : MonoBehaviour
    {
        void Update()
        {
            if (Input.GetMouseButtonDown(0)) // 0 = 좌클릭, 1 = 우클릭, 2 = 휠클릭
            {
                Debug.Log("누를 때 한 번");
            }
            if (Input.GetMouseButton(0)) // 좌클릭을 누르고 있는동안 계속 실행됨.
            {
                Debug.Log("누르고 있는동안 계속");
            }
            if (Input.GetMouseButtonUp(0)) // 좌클릭을 눌렀다가 뗄 때 한 번 실행됨.
            {
                Debug.Log("눌렀다가 뗄 때");
            }
        }
    }
    ```

    Down = 눌렀을 때, Up = 뗐을 때, 아무것도 안 붙어있으면 = 누르고 있는동안 계속.<br>    

    ---

<br>

- 추가로 input manager를 이용하는 방식이 있다. input manger는 유니티 화면 좌측상단 Edit > Project Settings를 누르면 확인할 수 있다(버전마다 조금 다를 수 있다)<br><br>
![Input_horizontal](../사진/Input_horizontal.png)<br><br>
Input Manger를 들어가보면 위 사진처럼 되어있다. 빨간색으로 표시되어 있는 부분들을 주의깊게 보면 된다.<br>
이름이 Horizontal로 설정되어있다(이름이 마음에 안 들면 바꿔도 된다)<br>
Negative Button left는 왼쪽 방향키를 누르면 음수 값을 반환하겠다는 뜻이다. <br>
Positive Button right는 오른쪽 방향키를 누르면 양수 값을 반환하겠다는 뜻이다. <br>
그 아래에 Alt Negative Button a 라고 되어있는건 왼쪽 방향키 대신 a키를 눌러도 동일하게 동작하도록 하겠다는 뜻이다.<br>
마찬가지로 그 아래는 오른쪽 방향키 대신 d키를 눌러도 된다는 뜻. 아래와 같이 코드를 작성해서 확인해 볼 수 있다.
    ```csharp
    private void Update()
    {
        // GetAxis()괄호 안에는 Input Manager에서 Name에 해당하는 부분이 들어간다.
        // 이름을 바꿨다면 바뀐 이름을 넣어줘야 정상적으로 동작한다.
        if(Input.GetAxis("Horizontal") < 0) 
        {
            Debug.Log("왼쪽 방향키 눌렀음");
        }
        if (Input.GetAxis("Horizontal") > 0)
        {
            Debug.Log("오른쪽 방향키 눌렀음");
        }
    }
    ```
    input manager에서 키를 내 마음대로 바꿀 수 있다. 
    <br>Negative Button을 right로 설정하고 Positive Button을 left로 설정해서 왼쪽을 누르면 오른쪽으로 이동하고 오른쪽을 누르면 왼쪽으로 이동하게 하는 걸 구현할 수도 있다.<br><br>
    Input.GetAxis와 비슷하게 Input Manager를 이용하는 함수가 몇 가지 더 있다. 사용법은 거의 동일하므로 아래 표를 보고 간단하게 알아두자.

    | | Input.GetAxis | Input.GetAxisRaw | Input.GetButton | 
    |:------:|:------:|:------:|:------:|
    | Negative Button을 눌렀을 때 | 음수값을 반환(길게 누를수록 점점 -1에 가까워짐) | -1을 반환(짧게 누르든 길게 누르든 상관없음) | true |
    | Positive Button을 눌렀을 때 | 양수값을 반환(길게 누를수록 점점 1에 가까워짐)  | 1을 반환(짧게 누르든 길게 누르든 상관없음) |  true | 
    | 해당하는 키를 누르지 않았을 때 | 0 | 0 | false |

    Input.GetAxis, GetAxisRaw는 Negative를 눌렀을 때와 Positive를 눌렀을 때 다른 값을 반환하므로 방향이 있는 이동 같은 것을 구현할 때 사용하면 좋다는 걸 알 수 있다(음수면 왼쪽, 양수면 오른쪽)<br>
    반면, Input.GetButton은 뭘 누르든 그냥 true를 반환하니 눌렀는지 안 눌렀는지만 확인하면 되는 경우, 예를 들면 점프, 총 쏘기 같은 곳에 사용하면 적절하다.<br>
    그리고 Input.GetAxis는 짧게 누르면 (절대값이)작은 값이 나오고 길게 누르면 큰 값이 나온다. 방향키를 짧게 누르면 살짝 움직이고 길게 누르면 빠르게 움직이는 걸 구현하고 싶다면 Input.GetAxis의 반환값에 비례하는 속도로 움직이게 하면 편하게 구현 가능하다.
    

### 2) Time.deltaTime
- Time.deltaTime에 대해 설명하기 전에 알아야 할 것: Update 함수는 1프레임마다 한 번씩 실행된다.<br> 
Time.deltaTime은 현재 프레임과 이전 프레임 사이에 몇 초가 흘렀는지 알 수 있는 변수이다.<br> 
예를 들어, 60fps로 게임을 실행하는 경우 60프레임 = 1초, 1프레임 = 0.01666...초<br>
즉, 60fps 환경에서 Time.deltaTime은 0.1666 이라는 값을 갖게 된다. <br>
144fps인 경우, 144프레임 = 1초, 1프레임 = 0.0069444..초이므로 이 경우 Time.deltaTime = 0.0069444 이다.<br>
이걸 어디에 사용할까? 타이머 같은걸 제작할 때 사용할 수 있다. 60fps, 144fps는 계산하기 힘드니 그냥 10fps, 20fps를 기준으로 해보자.<br>
10fps 기준 1프레임 = 0.1초. 그럼 Update함수가 10번 실행되면 1초가 지났다! 라고 할 수 있을까? <br>
20fps로 게임을 돌리는 사람은 0.5초만 지나도 Update함수가 10번 실행됐을 것이다. 때문에 이런 식으로는 안된다. <br>
Time.deltaTime의 값을 누적 시키는 방식으로 이를 해결할 수 있다.
    ```csharp
    float sum = 0f;
    void Update(){
        sum += Time.deltaTime;
        if(sum >= 0){
            Debug.Log("1초 지남!");
        }
    }
    ```
    위와 같이 코드를 작성하면 fps가 달라지더라도 동일하게 시간을 잴 수 있다.<br>
    10fps 기준: 현실에서 1초가 흐름 = 10프레임 = Update함수 10번 실행 = Time.deltaTime(0.1)을 sum에 10번 더함 -> sum은 1이 됨<br>
    20fps 기준: 현실에서 1초가 흐름 = 20프레임 = Update함수 20번 실행 = Time.deltaTime(0.05)을 sum에 20번 더함 -> sum은 1이 됨
    <br><br>
    fps에 상관없이 일정하게 이동하게 만들 때에도 이걸 활용할 수 있다. 보통 프레임마다 (이동속도 * Time.deltaTime)만큼 이동하도록 구현한다.<br>
    이동속도 = 100이라고 하면    
    10fps 기준: 현실에서 1초가 흐름 = 10프레임 = Update함수 10번 실행 = Time.deltaTime(0.1) * 100만큼 10번 이동 -> 0.1 * 100 * 10 = 100만큼 이동    
    20fps 기준: 현실에서 1초가 흐름 = 20프레임 = Update함수 20번 실행 = Time.deltaTime(0.05) * 100만큼 20번 이동 -> 0.05 * 100 * 20 = 100만큼 이동
### 3) 오브젝트를 이동시킬 때 사용하는 함수
- 오브젝트를 이동시킬 때 사용하는 함수는 크게 transform을 이용하는 방식과 rigidbody를 이용하는 방식으로 나뉜다.<br>
rigidbody를 이용하는 방식은 뒤에서 배운다.

    #### transform을 이용하는 방식 

    ```csharp
    transform.Translate(new Vector3(1,2,3));// 오브젝트의 위치와 방향 기준으로 x축으로1, y축으로2, z축으로3만큼 이동시킨다.(로컬좌표)
    transform.position = new Vector3(1,2,3);// 오브젝트의 위치나 방향과 관계없이 절대좌표 1,2,3으로 이동시킨다.
    ```

## Core Pattern
~~~csharp
// TODO: add 2-4 representative code snippets for this unit
~~~
## Common Mistakes
- TODO: add at least 3 mistakes learners make
## Mini Check
### Q1
- TODO
### Q2
- TODO
## Linked Sets
- Basic: unity_u06_input_b01
- Challenge: unity_u06_input_c01

