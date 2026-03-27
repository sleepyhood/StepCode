# Project - language_v2 crawler

현재 진행 중인 `language_v2` 크롤러/변환 작업을 추적하는 프로젝트 폴더입니다.

1차, 2차 PARA 적용에서는 아래 실제 작업 경로를 이동하지 않고 유지합니다.

- `practice/data/language_v2/`

실제 작업 범위:

- `practice/data/language_v2/`
- `practice/data/language_v2/crawl.py`
- `practice/data/language_v2/gui_crawler.py`
- `practice/data/language_v2/test_*.py`
- `practice/data/language_v2/source_docs/`
- `practice/data/language_v2/notes/`
- `practice/data/language_v2/generated_notes/`

정리 원칙:

- 기준 문서와 외부 원본은 `source_docs/`
- 현재 조사/메모는 `notes/`
- 중간 수집본과 임시 산출물은 `generated_notes/`
- 웹앱 운영 경로에 편입되기 전까지 새 실험 산출물은 `practice/data` 대신 이 프로젝트 폴더 또는 별도 `Projects`에서 시작

네이밍 예외:

- `practice/data/language_v2/_tmp_collect_testcases/`는 테스트 코드가 직접 참조하는 임시 수집 폴더라서 이번 단계에서 유지
- `practice/data/language_v2/lv*/_docs/reference/`는 내부 기준자료 경로라서 이번 단계에서 유지
- 위 두 경로는 새 작업의 기본값이 아니며, 새 보조 폴더는 `lowercase snake_case`로 만듭니다
