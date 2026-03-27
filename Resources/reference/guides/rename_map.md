# Rename Map

이번 미관·네이밍 정리에서 실제 변경한 항목과 보류한 항목을 기록합니다.

## Applied

- `practice/temp/contest_c/pdf to md` -> `practice/temp/contest_c/pdf_to_md`
- `practice/temp/contest_c/개념별로 정리` -> `practice/temp/contest_c/concepts_by_topic`
- `practice/temp/contest_c/학교별 문제` -> `practice/temp/contest_c/problems_by_school`
- `practice/data/content/Excalidraw` -> `practice/data/content/excalidraw`
- `practice/data/theory/Excalidraw` -> `practice/data/theory/excalidraw`

## Deferred

- `practice/data/language_v2/_tmp_collect_testcases`
  - `test_crawl_stage1.py`가 직접 참조
  - 하위에 접근 거부 디렉터리 존재
- `practice/data/language_v2/lv*/_docs/reference`
  - 기준 문서와 작업 노트가 기존 경로를 설명에 사용
- `practice/data/theory/canva/Week01` ~ `Week08`
  - Markdown 본문, 보조 스크립트, 절대경로 문자열이 광범위하게 참조
- `practice/data/theory/canva/강민승`
  - 하위에 한글 작업 폴더가 다수 있고 참조 범위 미확정
- `practice/data/content/.obsidian`
- `practice/data/theory/.obsidian`
  - 운영 자산이 아니라 개인 워크스페이스 흔적

## Next Wave Candidates

- `practice/data/theory/canva/Week01` ~ `Week08` -> `week01` ~ `week08`
- `practice/data/theory/canva/강민승` -> 목적 기반 영문 폴더 분해
- `practice/data/theory/contest/PDF` -> `pdf`
- `Resources/reference/guides` 내부 레거시 한글 파일명 정리
