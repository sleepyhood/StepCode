---
name: stepcode-marp-architect
description: Marp 슬라이드 제작 및 Pygame 교육 콘텐츠 설계를 위한 전문 스킬. Pygame 코스(lesson01~05)의 슬라이드 레이아웃, 시각적 일관성, 교육적 'Logic Hole' 설계를 자동화하고 검증할 때 사용합니다.
---

# Stepcode Marp Architect

## Overview
이 스킬은 StepCode 프로젝트의 Pygame 교육용 Marp 슬라이드를 제작할 때 사용합니다. 슬라이드는 단순한 설명서가 아니라 **'수업 진행 스크립트'**이며, 학생들의 인지 부하를 줄이고 능동적 참여를 유도하는 데 최적화되어야 합니다.

## 핵심 워크플로우

### 1. 코드 분석 및 마커 설계
- `src/` 폴더의 실제 작동하는 코드를 분석하여 핵심 함수(예: `move_ship`, `spawn_meteor`)를 추출합니다.
- 슬라이드 설명 텍스트와 코드를 매칭하기 위해 `[A]`, `[B]` 마커를 코드 블록 내 주석으로 배치합니다.

### 2. 교육적 '의도적 실패(Logic Hole)' 설계
- 학생이 코드만 베끼지 않도록 중요 수치나 변수명을 `???`로 치환합니다.
- 예: `speed = ???`, `if keys[pygame.K_???]:`

### 3. Marp 레이아웃 및 CSS 적용
- **심플리시티 퍼스트:** 기본적으로 단일 컬럼 흐름을 사용하여 가독성을 확보합니다. 불필요한 레이아웃 태그(`slide-2column`) 사용을 지양합니다.
- **예외적 컬럼 활용:** 이미지와 텍스트를 나란히 배치해야 하거나 대조가 필요한 경우에만 `slide-2column`을 사용합니다.
- **Frontmatter 표준:** 커스텀 테마 적용을 위해 반드시 아래 형식을 준수합니다.
  ```yaml
  theme: default
  style: |
    @import '../../shared/themes/pygame_theme.css';
  ```
- 모든 슬라이드 타이틀은 `<h1>`을 사용하며, `pygame_theme.css`의 상단 고정 스타일(34px)을 따릅니다.

### 4. 최종 정합성 검증
- 목차의 번호 체계(1.1, 1.1.1 등)와 본문의 `<h1>` 번호가 일치하는지 확인합니다.
- 슬라이드 전환 시 타이틀 위치가 흔들리지 않는지(CSS 클래스 적용 여부) 체크합니다.

## 레이아웃 가이드라인

| 클래스 | 추천 상황 |
| :--- | :--- |
| `ratio-64` | 설명 텍스트가 많고 이미지가 보조적일 때 |
| `ratio-55` | 텍스트와 코드/이미지의 비중이 대등할 때 |
| `ratio-46` | 코드가 길거나 상세한 도식이 핵심일 때 |

## 참고 리소스
- 상세한 작성 표준 및 체크리스트는 [guidelines.md](references/guidelines.md)를 참조하세요.
- 구체적인 레이아웃 패턴 예시는 [layout_patterns.md](references/layout_patterns.md)에서 확인할 수 있습니다.
