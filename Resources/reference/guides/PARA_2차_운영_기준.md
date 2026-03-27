# PARA 2차 운영 기준

## 목적

2차 정리는 루트 정리 이후 남은 혼재 구역을 정리하는 단계입니다.

핵심 원칙:

- 실행 경로 안정성이 구조 미관보다 우선입니다.
- 참조되는 자산은 제자리를 유지하고 문서상 소속만 먼저 정합니다.
- 참조되지 않는 백업, 마이그레이션, 실험 도구부터 이동합니다.

## 현재 분류 기준

- `practice/data`의 `content`, `generated`, `sets`, `theory`, `curriculum`, 인덱스 JSON은 `Areas`
- `practice/data/language_v2`는 현재 `Projects`
- `practice/data/Pygame`는 `Resources/reference/pygame_ocr/`로 분리
- 루트 `images/week01`는 `Resources/reference/images/week01/`로 분리
- `scripts/new_*`, `generate_content_indexes.py`, `check_sets_index.ps1`는 `Areas`
- 일회성 변환/캡처/업스케일링 도구는 `Archives` 또는 개별 `Projects`

## 후속 정리 우선순위

1. `.bak`와 마이그레이션 스크립트 분리
2. 실험성 스크립트 정리
3. `language_v2` 내부 산출물 세분화
4. `Pygame`와 `images`의 최종 소속 판정

## 현재까지 반영된 2차 조치

- `practice/data/*.bak`는 `Archives/migration_backups/practice_data/`로 이동
- `practice/data`의 마이그레이션 스크립트는 `Archives/tools_experiments/data_migration/`로 이동
- `scripts`의 PDF 캡처, opendataloader, 업스케일링 도구는 `Archives/tools_experiments/script_utils/`로 이동

## 3차 확정 조치

- `practice/data/Pygame`는 `Resources/reference/pygame_ocr/`로 이동
- 루트 `images/week01`는 `Resources/reference/images/week01/`로 이동
- `practice/data/language_v2`는 `source_docs/`, `notes/`, `generated_notes/` 구조를 추가
- `lesson_test_5vl5v24a` 예외 폴더는 루트에서 제거

## 네이밍 후속 기준

3차 이후 미관 정리 단계에서는 아래 규칙을 추가로 적용합니다.

- 신규 경로명은 `lowercase snake_case`
- 런타임/테스트/스크립트가 직접 참조하는 경로는 즉시 rename하지 않음
- 안전한 보조 경로부터 rename하고, 보류 항목은 rename map에 기록
- `practice/temp/contest_c`와 `content/theory`의 `excalidraw` 같은 저위험 경로부터 우선 정리
