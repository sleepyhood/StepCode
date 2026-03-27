# language_v2 PARA Notes

`practice/data/language_v2`는 현재 진행 중인 프로젝트 작업 영역입니다.

## working files

아래 파일은 현재 유지되는 코드와 테스트 경로이므로 루트에 둡니다.

- `crawl.py`
- `gui_crawler.py`
- `test_crawl_stage1.py`
- `test_gui_stage5.py`

## source docs

문제 원문과 기준 원본은 `source_docs/`에 둡니다.

## notes

작업 메모와 참고 노트는 `notes/`에 둡니다.

## generated notes

중간 수집본, 임시 산출물은 `generated_notes/`에 둡니다.

## internal references

`lv*/_docs/reference/`는 장기 공용 자료가 아니라 이 프로젝트 내부 기준자료로 유지합니다.

## naming notes

`language_v2` 내부 신규 보조 폴더명은 `lowercase snake_case`를 사용합니다.

현재 예외:

- `_tmp_collect_testcases/`
- `lv*/_docs/reference/`

예외 사유:

- `_tmp_collect_testcases/`는 `test_crawl_stage1.py`가 직접 참조합니다.
- `lv*/_docs/reference/`는 기존 기준 문서와 노트가 그대로 가리키는 레거시 내부 경로입니다.

따라서 이번 단계에서는 예외로 유지하고, 새 보조 자료는 `source_docs/`, `notes/`, `generated_notes/` 같은 표준 폴더에 둡니다.
