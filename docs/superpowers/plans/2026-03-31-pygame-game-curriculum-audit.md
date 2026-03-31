# Pygame Game Curriculum Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `practice/data/content/pygame/py_*.py` 게임 5개를 커리큘럼 편입 가능성 기준으로 점검하고, `사용 가능 / 축소 필요 / 제외` 판정을 문서에 반영한다.

**Architecture:** 먼저 각 게임의 런타임 의존성, 자산 요구사항, 코드 규모, 입력 방식, 수업용 분해 가능성을 확인한다. 그 다음 공통 판정 기준표를 만들고, 각 게임을 같은 기준으로 평가해 `커리큘럼.md`와 `README.md`에 반영한다.

**Tech Stack:** Python, pygame, tkinter, PowerShell, Markdown 문서

---

### Task 1: 후보 게임 인벤토리 확정

**Files:**
- Modify: `docs/superpowers/plans/2026-03-31-pygame-game-curriculum-audit.md`
- Test: `practice/data/content/pygame/py_RhythmGame.py`
- Test: `practice/data/content/pygame/py_같은 그림 찾기.py`
- Test: `practice/data/content/pygame/py_뱀서.py`
- Test: `practice/data/content/pygame/py_벽돌깨기.py`
- Test: `practice/data/content/pygame/py_에임트래커.py`

- [ ] **Step 1: 파일 목록 확인**

Run: `Get-ChildItem -Path "practice/data/content/pygame" -Filter "py_*.py" | Select-Object Name,Length`
Expected: `py_RhythmGame.py`, `py_같은 그림 찾기.py`, `py_뱀서.py`, `py_벽돌깨기.py`, `py_에임트래커.py` 5개가 출력된다.

- [ ] **Step 2: 후보 목록을 계획 문서에 기록**

```md
감사 대상 파일:

- `practice/data/content/pygame/py_RhythmGame.py`
- `practice/data/content/pygame/py_같은 그림 찾기.py`
- `practice/data/content/pygame/py_뱀서.py`
- `practice/data/content/pygame/py_벽돌깨기.py`
- `practice/data/content/pygame/py_에임트래커.py`
```

- [ ] **Step 3: 크기와 구조를 확인**

Run:

```powershell
@'
from pathlib import Path
root = Path(r"practice/data/content/pygame")
for p in sorted(root.glob("py_*.py")):
    lines = p.read_text(encoding="utf-8").splitlines()
    classes = sum(1 for ln in lines if ln.lstrip().startswith("class "))
    defs = sum(1 for ln in lines if ln.lstrip().startswith("def "))
    print(f"{p.name}: lines={len(lines)} classes={classes} defs={defs}")
'@ | python -
```

Expected: 각 파일별 line/class/def 수치가 출력된다.

- [ ] **Step 4: 결과를 계획 문서에 기록**

```md
현재 확인된 규모:

- `py_RhythmGame.py`: 약 496줄, 클래스 3개, 함수 19개
- `py_같은 그림 찾기.py`: 약 311줄, 클래스 1개, 함수 17개
- `py_뱀서.py`: 약 427줄, 클래스 3개, 함수 21개
- `py_벽돌깨기.py`: 약 383줄, 함수 10개
- `py_에임트래커.py`: 약 301줄, 함수 9개
```

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/plans/2026-03-31-pygame-game-curriculum-audit.md
git commit -m "docs: add pygame game curriculum audit plan"
```

### Task 2: 런타임 및 자산 의존성 점검

**Files:**
- Modify: `docs/superpowers/plans/2026-03-31-pygame-game-curriculum-audit.md`
- Test: `practice/data/content/pygame/py_같은 그림 찾기.py`
- Test: `practice/data/content/pygame/py_RhythmGame.py`
- Test: `practice/data/content/pygame/py_뱀서.py`
- Test: `practice/data/content/pygame/py_벽돌깨기.py`
- Test: `practice/data/content/pygame/py_에임트래커.py`

- [ ] **Step 1: 외부 자산/GUI 프레임워크 사용 여부를 찾기**

Run:

```powershell
@'
from pathlib import Path
root = Path(r"practice/data/content/pygame")
for p in sorted(root.glob("py_*.py")):
    lines = p.read_text(encoding="utf-8").splitlines()
    hits = [ln.strip() for ln in lines if "image.load" in ln or "assets" in ln.lower() or "PhotoImage" in ln or "tkinter" in ln or "mixer" in ln]
    print(f"FILE: {p.name}")
    for item in hits[:12]:
        print("  " + item)
    print("---")
'@ | python -
```

Expected: 자산 폴더 사용, 이미지 로드, tkinter 사용 여부가 파일별로 보인다.

- [ ] **Step 2: `py_같은 그림 찾기.py`를 pygame 커리큘럼에서 제외 후보로 기록**

```md
판정 메모:

- `py_같은 그림 찾기.py`는 `tkinter` 기반이다.
- `assets` 폴더의 PNG 의존성이 있다.
- 따라서 `pygame` 커리큘럼의 직접 예시 게임으로 분류하면 안 된다.
```

- [ ] **Step 3: 자산 의존성이 낮은 게임과 높은 게임을 분리 기록**

```md
의존성 1차 분류:

- 낮음:
  - `py_RhythmGame.py`
  - `py_뱀서.py`
  - `py_벽돌깨기.py`
  - `py_에임트래커.py`
- 높음 또는 별도 프레임워크:
  - `py_같은 그림 찾기.py`
```

- [ ] **Step 4: 실제 자산 폴더 존재 여부를 확인**

Run: `Get-ChildItem -Path "practice/data/content/pygame" -Recurse | Where-Object { $_.PSIsContainer -and $_.Name -eq "assets" } | Select-Object FullName`
Expected: `py_같은 그림 찾기.py`가 참조하는 `assets` 폴더 존재 여부를 확인할 수 있다.

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/plans/2026-03-31-pygame-game-curriculum-audit.md
git commit -m "docs: capture pygame game runtime dependency audit"
```

### Task 3: 수업 적합성 기준표 정의

**Files:**
- Modify: `docs/superpowers/plans/2026-03-31-pygame-game-curriculum-audit.md`
- Test: `practice/data/content/pygame/커리큘럼.md`

- [ ] **Step 1: 판정 기준을 문서에 추가**

```md
수업 적합성 판정 기준:

1. 90분 수업 1~2회 안에 핵심 기능을 설명할 수 있는가
2. 학생용 버전으로 기능 축소가 쉬운가
3. 외부 자산이나 별도 프레임워크 의존이 낮은가
4. 코드 길이가 350줄 전후 이하인가
5. 입력 규칙과 상태 관리가 초급자에게 설명 가능한가
```

- [ ] **Step 2: 판정 레벨을 고정**

```md
판정 레벨:

- `사용 가능`: 현재 구조를 약간만 줄이면 수업에 바로 투입 가능
- `축소 필요`: 원본은 크거나 복잡하지만 핵심 기능만 잘라 수업용 축소판 제작 가능
- `제외`: 현재 커리큘럼 축과 맞지 않거나 프레임워크/자산 의존성이 커서 별도 트랙이 필요
```

- [ ] **Step 3: 커리큘럼과 연결되는 운영 원칙을 덧붙이기**

```md
운영 원칙:

- 필수 12주 커리큘럼에는 `사용 가능` 또는 `축소 필요` 중 낮은 복잡도의 게임만 넣는다.
- `축소 필요` 게임은 원본 파일을 그대로 사용하지 않고 수업용 버전을 별도로 만든다.
- `제외` 게임은 pygame 커리큘럼 문서에서 직접 예시로 넣지 않는다.
```

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/plans/2026-03-31-pygame-game-curriculum-audit.md
git commit -m "docs: define curriculum audit criteria for pygame games"
```

### Task 4: 게임별 최종 판정 작성

**Files:**
- Modify: `docs/superpowers/plans/2026-03-31-pygame-game-curriculum-audit.md`
- Test: `practice/data/content/pygame/py_RhythmGame.py`
- Test: `practice/data/content/pygame/py_같은 그림 찾기.py`
- Test: `practice/data/content/pygame/py_뱀서.py`
- Test: `practice/data/content/pygame/py_벽돌깨기.py`
- Test: `practice/data/content/pygame/py_에임트래커.py`

- [ ] **Step 1: 판정표를 작성**

```md
최종 판정:

| 파일 | 판정 | 이유 |
| --- | --- | --- |
| `py_에임트래커.py` | 사용 가능 | 코드 규모가 가장 작고, 마우스 입력/점수/시간 구조가 수업용으로 직관적이다. |
| `py_벽돌깨기.py` | 축소 필요 | 원본은 길고 시스템이 많지만, 공/패들/벽돌/반사만 남기면 수업용 축소판 제작이 가능하다. |
| `py_RhythmGame.py` | 축소 필요 | 채보, 판정, 파티클, UI 요소가 많아 원본 그대로는 과하지만 축소판은 가능하다. |
| `py_뱀서.py` | 축소 필요 | 플레이어, 적, 총알, 장전, UI가 결합돼 있어 심화 프로젝트용 축소판으로만 적절하다. |
| `py_같은 그림 찾기.py` | 제외 | `tkinter` 기반이고 자산 폴더 의존성이 있어 현재 pygame 커리큘럼 직접 예시로 쓰기 부적절하다. |
```

- [ ] **Step 2: 각 게임의 권장 사용 위치를 덧붙이기**

```md
권장 배치:

- `py_에임트래커.py`: 필수 세트 6 후보
- `py_벽돌깨기.py`: 선택 프로젝트 A 후보
- `py_RhythmGame.py`: 선택 프로젝트 C 후보
- `py_뱀서.py`: 선택 프로젝트 D 후보
- `py_같은 그림 찾기.py`: pygame 트랙 제외, 별도 GUI/tkinter 트랙 검토
```

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/plans/2026-03-31-pygame-game-curriculum-audit.md
git commit -m "docs: record final curriculum suitability for pygame game files"
```

### Task 5: 커리큘럼 문서 반영

**Files:**
- Modify: `practice/data/content/pygame/커리큘럼.md`
- Modify: `practice/data/content/pygame/README.md`
- Test: `docs/superpowers/plans/2026-03-31-pygame-game-curriculum-audit.md`

- [ ] **Step 1: `커리큘럼.md`에 후보 게임 판정 요약 섹션 추가**

```md
## 원본 게임 파일 사용 판단

현재 `practice/data/content/pygame/py_*.py` 원본 게임 파일은
전부가 수업용으로 바로 확정된 상태는 아니다.

- `py_에임트래커.py`: 수업용 사용 가능
- `py_벽돌깨기.py`: 축소판 제작 후 사용 권장
- `py_RhythmGame.py`: 축소판 제작 후 사용 권장
- `py_뱀서.py`: 심화용 축소판 제작 후 사용 권장
- `py_같은 그림 찾기.py`: pygame 커리큘럼 직접 사용 제외
```

- [ ] **Step 2: `README.md`에 `round`와 `py_*.py`의 관계를 명시**

```md
원본 `py_*.py` 파일은 수업용 확정본이 아니라
세트/프로젝트 설계를 위한 후보 원본이다.

필요하면 별도의 축소판이나 수업용 예제를 만들어
`roundXX` 세트 안에서 사용한다.
```

- [ ] **Step 3: 수정 후 문서를 다시 읽어 표현 충돌 확인**

Run:

```powershell
Get-Content -Raw "practice/data/content/pygame/커리큘럼.md" -Encoding UTF8
Get-Content -Raw "practice/data/content/pygame/README.md" -Encoding UTF8
```

Expected: 선택 프로젝트와 원본 파일의 관계가 모순 없이 보인다.

- [ ] **Step 4: Commit**

```bash
git add practice/data/content/pygame/커리큘럼.md practice/data/content/pygame/README.md
git commit -m "docs: clarify curriculum readiness of raw pygame game files"
```

### Task 6: 검증 및 handoff

**Files:**
- Modify: `docs/superpowers/plans/2026-03-31-pygame-game-curriculum-audit.md`
- Test: `practice/data/content/pygame/커리큘럼.md`
- Test: `practice/data/content/pygame/README.md`

- [ ] **Step 1: 최종 검증 명령 실행**

Run:

```powershell
@'
from pathlib import Path
for path in [
    Path(r"practice/data/content/pygame/커리큘럼.md"),
    Path(r"practice/data/content/pygame/README.md"),
    Path(r"docs/superpowers/plans/2026-03-31-pygame-game-curriculum-audit.md"),
]:
    text = path.read_text(encoding="utf-8")
    print(path)
    print("사용 가능" in text, "축소 필요" in text, "제외" in text)
'@ | python -
```

Expected: 세 문서 모두 필요한 판정 체계를 포함하거나 참조 상태가 정리돼 있어야 한다.

- [ ] **Step 2: handoff 메모 추가**

```md
후속 구현 우선순위:

1. `py_에임트래커.py`에서 수업용 축소판 여부 최종 확정
2. `py_벽돌깨기.py` 축소판 설계
3. `py_RhythmGame.py`, `py_뱀서.py`는 심화 프로젝트 후보로 별도 문서화
4. `py_같은 그림 찾기.py`는 pygame 트랙에서 제거 또는 tkinter 트랙으로 분리
```

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/plans/2026-03-31-pygame-game-curriculum-audit.md
git commit -m "docs: finalize pygame curriculum audit handoff"
```
