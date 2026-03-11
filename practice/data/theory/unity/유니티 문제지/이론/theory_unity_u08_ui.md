# Unity U08 UI
## Goal
- Understand the core idea of this unit before solving problems.
- Review common mistakes first.
## Scope
- Topic: Text update, Button.onClick
- Source map: from practice/temp/유니티 목차.md
## 문항 핵심 포인트
### 1) 텍스트 UI
- 텍스트 UI의 내용을 바꾸는 간단한 예시<br>
(요즘은 Text가 아닌 TMP라고 업그레이드 된 버전을 사용하는데 시험에는 아직 옛날 버전인 Text가 나온다)
1. Hierarchy창에 우클릭해서 UI > Legacy > Text를 눌러서 Text 오브젝트를 생성한다.
2. 스크립트를 아래와 같이 작성한다.
    ```csharp
    public Text mytext;
    private void Start(){
        mytext.text = ("Hello");
    }
    ```
3. 스크립트를 오브젝트(아무데나 상관없음)에 적용시켜주고 mytext에 해당하는 부분에 1에서 만든 Text 오브젝트를 드래그해서 넣어준다. 
![TextUI](../사진/TextUI.png)<br>
### 2) Button.onClick.AddListener
- Button을 눌렀을 때 함수를 실행시키는 함수이다. 
    ```csharp
    public class Example : MonoBehaviour
    {
        public Button button;

        void Start()
        {
            button.onClick.AddListener(function);
        }

        void function()
        {
            Debug.Log("버튼을 누르면 이 함수가 실행됩니다.");
        }
    }
    ```
    위에서 했던 것과 마찬가지로 Button UI를 만들고 스크립트에 드래그 해서 집어넣어준다. 
    그럼 그 버튼을 좌클릭할 때 마다 매개변수로 넘겨준 fucntion 이라는 이름의 함수가 실행된다.
    
    Update 같은 곳에서 AddListner를 할 필요없이 Start에서 한 번 해주면 버튼에 해당하는 기능이 생기는거라고 보면 된다.

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
- Basic: unity_u08_ui_b01
- Challenge: unity_u08_ui_c01

