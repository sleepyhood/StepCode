# practice/data PARA Notes

`practice/data`는 2차 PARA 정리에서 아래 기준으로 다룹니다.

## 운영 핵심

다음 경로는 웹앱과 생성기에서 직접 읽거나 생성하는 자산이므로 위치를 유지합니다.

- `content/`
- `generated/`
- `sets/`
- `theory/`
- `curriculum/`
- `categories.json`
- `sets.index.json`
- `theory.index.json`

## 현재 프로젝트

다음 경로는 운영 자산과 분리해 읽어야 하는 현재 프로젝트 작업 영역입니다.

- `language_v2/`

## 참고 자산

다음 저장소는 운영 경로 밖 참고 자산으로 최종 분리했습니다.

- `Resources/reference/pygame_ocr/`

## 네이밍 기준

`practice/data` 하위에서 새로 만드는 경로명은 `lowercase snake_case`를 기본값으로 사용합니다.

이번 단계에서 반영한 항목:

- `content/excalidraw/`
- `theory/excalidraw/`

이번 단계에서 예외로 남긴 항목:

- `language_v2/_tmp_collect_testcases/`
- `language_v2/lv*/_docs/reference/`
- `theory/canva/Week01` ~ `Week08`
- `theory/canva/강민승/`
- `content/.obsidian/`
- `theory/.obsidian/`

예외 경로는 참조 범위가 넓거나 개인 워크스페이스 흔적이므로, 다음 정리 단계 전까지 문서상 예외로만 관리합니다.

## 운영 밖으로 분리한 보조 파일

다음 파일은 런타임이 직접 참조하지 않는 마이그레이션/백업 성격으로 보고 아카이브로 분리했습니다.

- `Archives/tools_experiments/data_migration/audit_migration.py`
- `Archives/tools_experiments/data_migration/migrate_lang.py`
- `Archives/migration_backups/practice_data/*.bak`
