

# 0. 무엇을 설치하나요?

* **Python 3.x** (권장: 3.10~3.12)
* **Visual Studio Code (VS Code)** 에디터
* **VS Code용 Python 확장** (Microsoft 제공)
* **pygame** (pip로 설치)

VS Code와 Python 확장은 공식 문서대로 설치·설정합니다. ([Visual Studio Code][1])

---

# 1. Python 설치 & 확인

## Windows

1. [python.org](https://www.python.org)에서 최신 설치 파일 다운로드 → **Install Now** 클릭 전, **“Add Python to PATH”** 체크! ([Python documentation][2])
2. 설치 후 터미널(명령 프롬프트/PowerShell)에서 버전 확인:

```powershell
py -V
# 또는
python --version
```

## macOS / Linux

터미널에서:

```bash
python3 --version
```

> pip가 없다면 공식 가이드의 `get-pip.py`로 설치할 수 있어요. (대부분은 최신 Python에 기본 포함) ([pip.pypa.io][3])

---

# 2. Visual Studio Code 설치

* 공식 다운로드 페이지에서 **Windows/macOS/Linux**에 맞는 설치 파일로 설치합니다. ([Visual Studio Code][4])

---

# 3. VS Code에 Python 확장 설치

1. VS Code 실행 → 왼쪽 **Extensions(확장)** 아이콘
2. “**Python**” 검색 → **Python (ms-python.python)** 설치
3. (권장) “**Pylance**”, “Jupyter”도 함께 설치하면 편리합니다.
4. 확장 설치법은 **Extension Marketplace** 문서에 자세히 나와 있어요. ([Visual Studio Code][5])

---

# 4. 프로젝트 폴더 만들기 & 열기

1. 예: `C:\pygame-starter`(Windows) 또는 `~/pygame-starter`(macOS/Linux) 폴더 생성
2. VS Code에서 **File → Open Folder…** 로 폴더를 엽니다. (빠른 시작 문서 참고) ([Visual Studio Code][6])

---

# 5. 가상환경 만들기(권장)

## Windows (PowerShell)

```powershell
cd C:\pygame-starter
py -m venv .venv
.venv\Scripts\activate
```

> PowerShell에서 실행 정책 때문에 활성화가 막히면, **한 번만** 아래 명령을 실행 후 다시 활성화:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## macOS / Linux

```bash
cd ~/pygame-starter
python3 -m venv .venv
source .venv/bin/activate
```

### VS Code에서 인터프리터 선택

* **Command Palette (Ctrl/⌘+Shift+P)** → **Python: Select Interpreter** → 목록에서 **.venv** 선택. 상태바에 선택된 인터프리터가 표시됩니다. ([Visual Studio Code][7])

---

# 6. pygame 설치

가상환경이 **활성화된 터미널**에서:

```bash
python -m pip install --upgrade pip
pip install pygame
```

* pygame 공식 “Getting Started”와 문서에서도 pip 설치를 안내합니다. ([pygame.org][8])

### 설치 검증

```bash
python -c "import pygame; print(pygame.__version__)"
python -m pygame.examples.aliens   # 예제 게임 실행
```

(예제 모듈 실행법은 공식 examples 레퍼런스에 정리되어 있어요.) ([pygame.org][9])

> **Linux에서 드물게** 패키지 의존성으로 에러가 나면 SDL2 관련 개발 패키지를 추가 설치해야 할 수 있습니다(대부분의 경우 pip wheel로 불필요). Ubuntu 계열 예시:
> `sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev python3-dev` ([GitHub][10])

---

# 7. 첫 실행: “빈 창” 예제

프로젝트 폴더에 `main.py`를 만들고 아래 코드를 붙여 넣은 뒤 **Run ▶**:

```python
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pygame setup test")

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((20, 20, 20))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

> VS Code에서 **Run and Debug** 또는 **Run → Run Without Debugging**로 실행하세요. (Python 튜토리얼/빠른 시작 문서 참고) ([Visual Studio Code][11])

---

# 8. 확장: 우리 수업용 폴더 구조 제안

```
pygame-starter/
├─ .venv/               # 가상환경
├─ assets/              # 이미지/사운드 (bgm.ogg, bounce.wav 등)
├─ main.py              # 실행 파일
└─ README.md            # 과제/미션 체크리스트
```

---

# 9. 문제 해결(FAQ)

* **VS Code에서 Python 인터프리터가 안 보임**

  * Command Palette → *Python: Select Interpreter* 에서 수동 선택. (환경 문서 참고) ([Visual Studio Code][7])
* **명령어 ‘python/py’가 안 됨(Windows)**

  * 설치 시 “Add Python to PATH” 미체크 가능성. 재설치 또는 PATH 설정. (Windows용 공식 문서 및 pygame 위키 참고) ([Python documentation][2])
* **pygame 설치는 됐는데 예제가 실행 안 됨**

  * 가상환경 활성화 여부, Python 버전 확인, 터미널을 VS Code 내에서 열어 실행. `python -m pygame.examples.aliens` 권장. ([pygame.org][9])
* **Linux에서 빌드/의존성 에러**

  * SDL2 관련 개발 패키지 설치 후 다시 `pip install pygame`. ([GitHub][10])

---


[1]: https://code.visualstudio.com/?utm_source=chatgpt.com "Visual Studio Code - Code Editing. Redefined"
[2]: https://docs.python.org/3/using/windows.html?utm_source=chatgpt.com "4. Using Python on Windows"
[3]: https://pip.pypa.io/en/stable/installation/?utm_source=chatgpt.com "Installation - pip documentation v25.2"
[4]: https://code.visualstudio.com/download?utm_source=chatgpt.com "Download Visual Studio Code - Mac, Linux, Windows"
[5]: https://code.visualstudio.com/docs/languages/python?utm_source=chatgpt.com "Python in Visual Studio Code"
[6]: https://code.visualstudio.com/docs/python/python-quick-start?utm_source=chatgpt.com "Quick Start Guide for Python in VS Code"
[7]: https://code.visualstudio.com/docs/python/environments?utm_source=chatgpt.com "Python environments in VS Code"
[8]: https://www.pygame.org/wiki/GettingStarted?utm_source=chatgpt.com "GettingStarted — wiki"
[9]: https://www.pygame.org/docs/ref/examples.html?utm_source=chatgpt.com "pygame.examples — pygame v2.6.0 documentation"
[10]: https://github.com/pygame-community/pygame-ce/wiki/Compiling-on-Linux?utm_source=chatgpt.com "Compiling on Linux · pygame-community/pygame-ce Wiki"
[11]: https://code.visualstudio.com/docs/python/python-tutorial?utm_source=chatgpt.com "Getting Started with Python in VS Code"
