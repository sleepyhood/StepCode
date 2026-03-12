# Unity U10 Material and Color
## Goal
- Understand the core idea of this unit before solving problems.
- Review common mistakes first.
## Scope
- Topic: Color logging, Material.SetColor
- Source map: from practice/temp/유니티 목차.md
## 문항 핵심 포인트
### 1) 오브젝트의 색깔 변경하기
- 오브젝트 색깔 변경하기는 이론적인 설명보다는 바로 실습을 해봅시다.
1. Cube 오브젝트를 하나 만듭니다. 다른 걸로 만들어도 상관은 없습니다. 
2. 아래와 같이 코드를 작성해서 1에서 만든 오브젝트에 스크립트를 적용해주고 실행해보면 색깔이 바뀌는 걸 볼 수 있습니다.
```csharp
public class ColorSetter : MonoBehaviour
{
    Material ma;
    void Start()
    {
        Renderer renderer = GetComponent<Renderer>();
        ma = renderer.material;     

        // "_BaseColor"가 안 된다면 "_Color"로 해봅시다.
        // 처음에 유니티 프로젝트를 만들 때 설정에 따라 달라지는 부분입니다.
        ma.SetColor("_BaseColor", Color.red);          
    }
    
}
```
<br><br>
아래 코드는 0.5초마다 색깔이 계속해서 바뀌는 스크립트입니다. 심심하면 한 번 해보세요.

```csharp
public class ColorSetter : MonoBehaviour
{
    int i = 0;
    float t = 0;
    Color[] colors = { Color.red, Color.blue, Color.white, Color.black, Color.green };
    Material ma;
    void Start()
    {
        Renderer renderer = GetComponent<Renderer>();
        ma = renderer.material;       
    }
    private void Update()
    {
        t += Time.deltaTime;
        if(t >= 0.5)
        {
            t = 0;
            i = (i + 1) % 5;
            ma.SetColor("_BaseColor", colors[i]);
        }
    }
}
```

## Linked Sets
- Basic: unity_u10_material_color_b01
- Challenge: unity_u10_material_color_c01

