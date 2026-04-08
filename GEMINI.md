# StepCode - 프로젝트 컨텍스트 가이드

StepCode는 프로그래밍 초심자를 위한 **실행 추적(Trace) · MCQ(객관식) · 코드 작성 연습** 플랫폼입니다. 이 문서는 AI 에이전트가 프로젝트 구조를 이해하고, 일관된 규칙에 따라 콘텐츠를 관리 및 개발하기 위한 지침을 제공합니다.

## 1. 프로젝트 개요
*   **목적:** 로컬 환경에서 가볍게 구동되는 인터랙티브 프로그래밍 연습장 및 교육 콘텐츠 관리.
*   **주요 언어:** C, Python, Java, C# (Unity).
*   **핵심 기술:** 
    *   **Frontend:** HTML5, Vanilla JS, CSS3, Prism.js, CodeMirror.
    *   **Backend/Tools:** Python 3.x, PowerShell.
    *   **Data:** JSON (웹 렌더링용), Markdown/YAML (원본 소스).

## 2. 프로젝트 구조 (PARA 방법론)
이 프로젝트는 **PARA(Projects, Areas, Resources, Archives)** 체계에 따라 디렉토리를 관리합니다.

*   **Projects/active/**: 현재 진행 중인 단기 작업 및 실험적 스크립트.
*   **Areas/learning_platform/**: 지속 운영되는 핵심 자산.
    *   `practice/`: 웹 애플리케이션 엔진 및 정적 자산.
    *   `docs/`: 학습 파트별 가이드 및 마크다운 문서.
*   **Resources/reference/**: 반복 참조되는 가이드, 명명 규칙, 템플릿, 이미지 자료.
*   **Archives/**: 완료된 작업, 임시 산출물(`generated_outputs/`), 백업 데이터.

## 3. 실행 및 빌드 가이드

### 3.1 로컬 테스트 서버
브라우저 보안 정책(CORS)으로 인해 JSON 로드를 위해 반드시 로컬 서버를 사용해야 합니다.
```bash
cd practice
python -m http.server 8000
```
*   메인 목록: `http://localhost:8000/index.html`

### 3.2 콘텐츠 파이프라인
원본(`data/content/`)을 수정하거나 추가한 후에는 반드시 인덱스를 재생성해야 합니다.
*   **인덱스 생성:** `python scripts/generate_content_indexes.py`
*   **정합성 체크:** `powershell -ExecutionPolicy Bypass -File scripts/check_sets_index.ps1` (문제 수 및 ID 중복 검사)

## 4. 개발 및 운영 규칙 (Mandates)

### 4.1 네이밍 및 경로 규칙
*   모든 파일 및 폴더명은 **영문 소문자 snake_case**를 사용합니다.
*   경로명에 **공백 또는 한글 사용을 절대 금지**합니다. (본문 텍스트 제외)
*   의미 없는 `_` 접두사 사용을 자제합니다.

### 4.2 교육적 출제 컨벤션
*   **Python 출력 스타일:** 입출력 패턴의 일관성을 위해 Python 문제의 출력은 **C-style 서식 문자**를 사용합니다.
    *   예: `print('%d x %d = %d' % (n, i, n * i))`
*   **C 언어:** 항상 `scanf`와 `printf`(`\n` 포함) 구조를 기본으로 사용합니다.

### 4.3 문제 스키마 (Problem Schema)
*   `mcq`: 객관식 (보기 배열 및 정답 인덱스 포함).
*   `short`: 단답형 (정답 텍스트 또는 후보 배열 포함).
*   `code`: 코드 작성 (정규화된 텍스트 비교 채점).

## 5. 표준 작업 워크플로우

1.  **스캐폴딩 생성:** `scripts/new_*.py` 도구를 사용하여 신규 단원/레슨/워크시트 틀 생성.
2.  **원본 작성:** `practice/data/content/` 하위의 YAML/MD/JSON 파일에 실제 문제 및 개념 작성.
3.  **인덱스 빌드:** `generate_content_indexes.py` 실행으로 웹 앱 반영.
4.  **검증:** `check_sets_index.ps1`으로 데이터 오류 확인.
5.  **테스트:** 로컬 서버에서 실제 풀이 및 채점 동작 확인.

---
**주의:** `practice/data/` 하위의 레거시 JSON 파일을 직접 수정하기보다 `data/content/` 원본을 통한 자동 생성 파이프라인 사용을 우선합니다.
