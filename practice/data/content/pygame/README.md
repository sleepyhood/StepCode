# Pygame 콘텐츠 구조

`pygame` 콘텐츠는 회차별 폴더로 관리합니다.

## 폴더 규칙

- `round01/`
- `round02/`
- `round03/`

각 회차 폴더는 아래 구조를 기본으로 사용합니다.

```text
roundXX/
  source/
  lesson/
  interactive/
  worksheets/
```

## 역할

- `source/`: 원본 수업 자료, 추출 md/json, 이미지
- `lesson/`: 회차 공통 설명 및 운영 메모
- `interactive/`: 인터랙티브 문제 세트
- `worksheets/`: 출력용 활동지와 정답

## 현재 구성

- `round01`: 1주차 pygame 창, 이벤트, 화면 갱신, 응용수업 설계
