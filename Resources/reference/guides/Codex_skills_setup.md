# Codex Skills Setup

이 문서는 StepCode 프로젝트에서 사용하는 Codex 로컬 스킬 환경을 정리한다.

이 문서의 위치는 PARA 기준으로 `Resources/reference/guides/`가 적절하다.

- 프로젝트 코드가 아니다.
- 특정 작업 하나의 단기 산출물도 아니다.
- 여러 환경에서 반복 참조하는 운영 가이드다.

---

## 1. 핵심 원칙

- Codex 스킬은 기본적으로 `git`으로 관리되지 않는다.
- 설치 대상은 저장소 내부가 아니라 사용자 로컬 환경이다.
- 다른 컴퓨터에서 같은 저장소를 `git clone` 또는 `git pull` 해도 스킬은 자동으로 따라오지 않는다.
- 새 컴퓨터에서는 스킬을 다시 설치해야 동일한 작업 환경이 된다.
- 저장소 내부에 버전관리되는 프로젝트 전용 스킬은 별도로 둘 수 있다.

기본 설치 위치 예시:

```text
C:\Users\<username>\.codex\skills\
```

예:

```text
C:\Users\osw\.codex\skills\playwright
C:\Users\osw\.codex\skills\screenshot
C:\Users\osw\.codex\skills\python-testing-patterns
C:\Users\osw\.codex\skills\powershell-windows
C:\Users\osw\.codex\skills\test-fixing
C:\Users\osw\.codex\skills\docs-architect
C:\Users\osw\.codex\skills\architect-review
```

프로젝트 내부 커스텀 스킬 위치:

```text
<repo-root>\.codex\skills\
```

---

## 2. 현재 프로젝트 권장 스킬

현재 StepCode 프로젝트의 작업 성격은 다음에 가깝다.

- Python 스크립트 유지보수
- Playwright 기반 크롤링
- Tkinter GUI 보조 도구
- aiohttp 기반 로컬 대시보드 서버
- Windows PowerShell 환경
- 테스트 보강 및 회귀 수정

권장 스킬:

### 공식 카탈로그

- `playwright`
- `screenshot`

### 커뮤니티 스킬

- `python-testing-patterns`
- `powershell-windows`
- `test-fixing`
- `docs-architect`
- `architect-review`

추가 후보:

- `webapp-testing`
- `security-review`

### 프로젝트 내부 커스텀 스킬

- `stepcode-content-workflow`
- `stepcode-problem-set-editor`
- `stepcode-para-governance`

---

## 3. 현재 설치된 스킬

이 문서를 작성한 시점에 확인된 설치 대상:

- `playwright`
- `screenshot`
- `python-testing-patterns`
- `powershell-windows`
- `test-fixing`
- `docs-architect`
- `architect-review`
- `stepcode-content-workflow`
- `stepcode-problem-set-editor`
- `stepcode-para-governance`

주의:

- Codex는 새로 설치한 스킬을 바로 인식하지 않을 수 있다.
- 설치 후에는 Codex를 재시작하는 것이 안전하다.

---

## 4. 새 컴퓨터에서 다시 맞추는 방법

### 4.1 공식 스킬

```text
[$skill-installer](C:\Users\osw\.codex\skills\.system\skill-installer\SKILL.md) playwright
[$skill-installer](C:\Users\osw\.codex\skills\.system\skill-installer\SKILL.md) screenshot
```

### 4.2 커뮤니티 스킬

```text
[$skill-installer](C:\Users\osw\.codex\skills\.system\skill-installer\SKILL.md) python-testing-patterns
[$skill-installer](C:\Users\osw\.codex\skills\.system\skill-installer\SKILL.md) powershell-windows
[$skill-installer](C:\Users\osw\.codex\skills\.system\skill-installer\SKILL.md) test-fixing
[$skill-installer](C:\Users\osw\.codex\skills\.system\skill-installer\SKILL.md) docs-architect
[$skill-installer](C:\Users\osw\.codex\skills\.system\skill-installer\SKILL.md) architect-review
```

설치 후:

```text
Restart Codex to pick up new skills.
```

### 4.3 프로젝트 내부 커스텀 스킬

프로젝트 내부 스킬은 저장소와 함께 버전관리된다.

경로:

```text
.codex/skills/
```

예:

```text
.codex/skills/stepcode-content-workflow
.codex/skills/stepcode-problem-set-editor
.codex/skills/stepcode-para-governance
```

주의:

- 다른 컴퓨터에서 저장소를 받은 뒤 Codex가 이 경로를 읽을 수 있는지 확인한다.
- 필요하면 프로젝트 루트 기준으로 해당 스킬 경로를 명시해 호출한다.

---

## 5. 실제 활용 예시

### Playwright

```text
playwright를 써서 practice/data/language_v2/crawl.py의 doingcoding 관리자 로그인 흐름을 점검해줘.
로그인 페이지 진입, selector 확인, /admin/problems 도달 여부까지 확인해줘.
```

### Python testing patterns

```text
python-testing-patterns를 써서 practice/data/language_v2/test_crawl_stage1.py에
selector fallback 케이스와 재로그인 회귀 테스트를 추가해줘.
```

### Test fixing

```text
test-fixing을 써서 practice/data/language_v2/test_crawl_stage1.py의 실패 테스트를
공통 원인 기준으로 묶어 분석하고 수정해줘.
```

### PowerShell Windows

```text
powershell-windows를 써서 이 프로젝트의 Windows 실행 커맨드를 정리해줘.
dashboard_server.py 실행, gui_crawler.py 실행, 테스트 실행 커맨드를 표준화해줘.
```

### Docs architect

```text
docs-architect를 써서 Resources/reference/guides/ 문서 구조를 정리해줘.
README 진입점, guides 인덱스, 개별 가이드 간 링크 흐름을 재설계해줘.
```

### Architect review

```text
architect-review를 써서 이 저장소의 PARA 분류가 맞는지 검토해줘.
Projects, Areas, Resources, Archives 경계가 모호한 폴더를 찾아 기준과 함께 정리해줘.
```

### StepCode content workflow

```text
stepcode-content-workflow를 써서 새 Python 단원 카테고리와 lesson, worksheet를 생성해줘.
생성기 순서와 인덱스 재생성까지 포함해줘.
```

```text
stepcode-content-workflow를 써서 기존 Python lv07_for 단원에 새 worksheet 회차를 추가해줘.
기존 round 패턴과 id 충돌까지 확인해줘.
```

### StepCode problem set editor

```text
stepcode-problem-set-editor를 써서 기존 세트에 문제를 1개 추가하고
sets.index.json의 numProblems와 관련 메타데이터를 같이 맞춰줘.
```

### StepCode PARA governance

```text
stepcode-para-governance를 써서 새 운영 문서를 어디에 둘지 판정해줘.
Projects, Areas, Resources, Archives 중 근거와 함께 정리해줘.
```

```text
stepcode-para-governance를 써서 practice/data/language_v2/_tmp_collect_testcases를
PARA 기준으로 남길지 이동할지 판정해줘.
```

---

## 6. 운영 규칙

- 프로젝트 README에는 스킬 전체 설명을 길게 넣지 않는다.
- 로컬 작업환경 문서는 이 문서에서 관리한다.
- 새로 유용한 스킬을 도입하면 이 문서의 `권장 스킬`과 `재설치 목록`을 같이 갱신한다.
- 팀이나 다른 PC로 작업을 옮길 때는 이 문서를 먼저 확인한다.

---

## 7. 체크리스트

- [ ] 새 컴퓨터에서 Codex 설치 완료
- [ ] 공식 스킬 설치 완료
- [ ] 커뮤니티 스킬 설치 완료
- [ ] Codex 재시작 완료
- [ ] Playwright 관련 작업 정상 인식 확인
- [ ] 테스트 관련 작업 정상 인식 확인
- [ ] PowerShell 관련 작업 정상 인식 확인
- [ ] 문서 구조 작업 스킬 정상 인식 확인
- [ ] PARA 검토 작업 스킬 정상 인식 확인
- [ ] 프로젝트 내부 커스텀 스킬 정상 인식 확인
