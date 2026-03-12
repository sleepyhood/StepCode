# Unity U11 ECS
## Goal
- Understand when a code snippet is using Unity ECS/Entities.
- Distinguish ECS from classic MonoBehaviour patterns.

## Scope
- Topic: ECS(Entities) usage 판단
- Source map: from practice/temp/유니티 목차.md
## 문항 핵심 포인트
### 1) ECS
- ECS는 여러분이 아마 한 번도 사용해보지 않았을 겁니다. 우리는 그 동안 MonoBehaviour라는 걸 사용해왔습니다. Start, Update 같은 함수가 자동으로 실행되고 hierarchy창에서 오브젝트를 드래그 해서 변수에 집어넣는 이런 기능들은 사실 MonoBehaviour가 해주는 거였습니다. ECS는 우리가 그동안 해왔던 MonoBehaviour 방식과는 많이 다르기 때문에 간단하게만 알아보고 문제를 풀기 위한 핵심 키워드만 알아봅시다.<br>
뱀파이어 서바이버즈 같은 게임을 한 번 생각해봅시다.<br><br>
![ECS1](../사진/ECS1.png)<br><br>

    수백, 수천 어쩌면 수만마리의 몬스터가 있습니다. 이런 게임을 만든다면 어떻게 만들어야 할까요? Instantiate 함수를 이용해서 계~속 몬스터를 만들면 될까요? 물론 되긴 될겁니다. 하지만 몬스터 수가 너무 많아지면 컴퓨터가 힘들어 할 겁니다. 몬스터 한 마리당 체력, 애니메이션, 이동 관련 코드, 아이템 드랍확률 관련 코드... 많은 정보를 가지고 있습니다. 몬스터 한 마리당 1MB의 용량을 차지한다고 가정하면 몬스터 1만마리는 약 10GB의 용량을 차지합니다. 이게 우리가 그동안 사용해온 MonoBehaviour 방식입니다. MonoBehaviour 방식은 각각의 오브젝트가 각자의 코드대로 움직이기 때문에 10마리가 있으면 10개의 코드, 100마리가 있으면 100개의 코드가 실행되지만 ECS 방식은 하나의 코드가 여러 몬스터에게 명령을 내리는 방식이라 몇 마리가 있든 상관없이 하나의 코드만 실행되면 됩니다.

### 2) ECS 관련 키워드
- ECS는 위에서 설명한 정도로만 알아두고 관련 키워드를 알아봅시다. 
MonoBehaviour 대신 ComponentSystem, SystemBase, ISystem, IComponentData, IJobEntity 를 상속하고 있으면 ECS 방식을 사용하고 있는 겁니다. 또한, OnUpdate, OnCreate와 같은 함수를 사용하고 있다면 이 역시 ECS 방식을 사용하고 있다는 증거입니다.<br>
반대로 MonoBehaviour를 상속하거나 Update, Start, OnCollisionEnter와 같은(우리가 지금까지 많이 사용했던 것들)함수를 사용하고 있다면 ECS 방식을 사용하지 않는 것입니다.



## Linked Sets
- Basic: unity_u11_ecs_b01
- Challenge: unity_u11_ecs_c01
