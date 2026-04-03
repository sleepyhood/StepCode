# Pygame Marp Course

이 폴더는 `선생님이 수업하기 쉬운 반완성형` Pygame 코스의 source of truth를 보관한다.

핵심 원칙:

- 새 코스는 기존 `practice/data/content/pygame/`와 분리된 별도 운영 루트다.
- 각 차시의 핵심 원본은 `lesson/slide.md` 하나다.
- 문제지, interactive, 문제 코드 세트는 이 코스의 기본 산출물이 아니다.
- HTML/PDF는 필요 시 빌드 산출물로 취급하며 이 루트의 source of truth로 저장하지 않는다.

권장 구조:

```text
pygame_marp_course/
  README.md
  curriculum.md
  shared/
    assets/
    themes/
    snippets/
  lesson01_intro/
    category.meta.yml
    lesson/slide.md
    assets/
    teacher_notes/
  lesson02_input_loop/
    category.meta.yml
    lesson/slide.md
    assets/
    teacher_notes/
  lesson03_sprite_motion/
    category.meta.yml
    lesson/slide.md
    assets/
    teacher_notes/
  Archives/
```

운영 규칙:

- 새 코스는 기존 `py_pygame_w01` 계열 ID를 재사용하지 않는다.
- 차시 폴더는 `lessonXX_topic` 패턴을 사용한다.
- 공통 자산은 `shared/`에, 차시 전용 자산은 각 차시 `assets/`에 둔다.
- 수업 진행 메모는 `teacher_notes/`에 둔다.
- 초안, 폐기안, 이전 버전은 `Archives/`에 둔다.

현재 포함된 초기 차시:

- `lesson01_intro`
- `lesson02_input_loop`
- `lesson03_sprite_motion`

주의:

- 이 폴더는 구조 설계와 원본 정리를 위한 초기 스캐폴드다.
- 기존 `scripts/generate_content_indexes.py`는 현재 `lesson/lesson.md` 중심 규칙을 기대하므로, 이 루트는 아직 기존 generated index 파이프라인에 연결하지 않는다.
