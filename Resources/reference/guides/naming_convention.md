# Naming Convention

이 문서는 StepCode 저장소의 경로 네이밍 기준서입니다.

## 기본 규칙

- 새 폴더명과 새 파일명은 `lowercase snake_case`
- 공백 금지
- 한글 경로명 금지
- 대소문자 혼합 경로명 금지
- 의미 없는 `_` 접두사 금지

## 허용 범위

- Markdown 제목, 본문, 문제 설명, 학습 콘텐츠 텍스트는 한글 유지 가능
- 외부 서비스 규칙, 공개 ID, 데이터 키는 기존 형식을 유지

## rename 우선순위

1. 문서/임시/참고/아카이브 경로
2. 작업 중 보조 폴더
3. 런타임과 테스트가 직접 참조하는 경로는 마지막

## 현재 표준 예시

- `practice/temp/contest_c/pdf_to_md`
- `practice/temp/contest_c/concepts_by_topic`
- `practice/temp/contest_c/problems_by_school`
- `practice/data/content/excalidraw`
- `practice/data/theory/excalidraw`
- `practice/data/language_v2/source_docs`
- `practice/data/language_v2/generated_notes`

## 현재 예외

- `practice/data/language_v2/_tmp_collect_testcases`
- `practice/data/language_v2/lv*/_docs/reference`
- `practice/data/theory/canva/Week01` ~ `Week08`
- `practice/data/theory/canva/강민승`
- `practice/data/content/.obsidian`
- `practice/data/theory/.obsidian`

예외는 참조 범위가 넓거나 개인 워크스페이스 흔적이라서, 다음 정리 단계 전까지 문서상으로만 관리합니다.
