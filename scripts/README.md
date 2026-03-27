# scripts PARA Notes

`scripts/`는 2차 PARA 정리에서 아래 기준으로 다룹니다.

## 운영 필수 스크립트

위치를 유지합니다.

- `generate_content_indexes.py`
- `new_content_category.py`
- `new_lesson.py`
- `new_worksheet.py`
- `content_scaffold_lib.py`
- `check_sets_index.ps1`
- `check_set_quality.py`

## 장기 보조 도구

당장 이동하지 않고, 사용 빈도와 재실행 필요성을 기준으로 후속 정리합니다.

- `generate_py_contest_checklists.py`
- `download_unity_u*.ps1`

## 프로젝트/실험 도구

런타임 직접 참조가 없는 도구는 아카이브로 분리했습니다.

- `Archives/tools_experiments/script_utils/00_pdf_page_capture_gui.py`
- `Archives/tools_experiments/script_utils/01_opendataloader.py`
- `Archives/tools_experiments/script_utils/img_upscaling/`

## 네이밍 기준

`scripts/` 아래 신규 스크립트명은 `lowercase snake_case`를 사용합니다.

- 예: `generate_content_indexes.py`
- 예: `new_content_category.py`

기존 레거시 스크립트명은 참조 관계가 불분명하면 즉시 바꾸지 않고, rename map에 기록한 뒤 후속 단계에서 정리합니다.
