# Unity 주차 매핑 W03

## 매핑 기준
- 원문 기준: `practice/temp/유니티 1차 문제 풀이.md`
- 주차 기준: `practice/temp/유니티 주차-문항 매핑.md`
- 이론 기준: `practice/data/theory/unity/theory_unity_u03_function_syntax.md`

## 원문 대응 매핑
| 문제지 ID | 원문 번호 | 원문 제목 | 연결 이론 섹션 |
|---|---:|---|---|
| P01 | 25 | 함수 설명의 참/거짓 판별 | 핵심 패턴, 자주 하는 실수 |
| P02 | 28 | static 메서드에서 필드 접근 오류 수정하기 | 핵심 패턴, 자주 하는 실수 |

## 확장 문항 매핑
| 문제지 ID | 유형 | 기반 개념 | 원문 참조 번호 | 확장 의도 |
|---|---|---|---:|---|
| X01 | 객관식 | 함수 선언 시그니처 조립 | 25 | C# 클래스 메서드를 정의할 때 접근제어자, 지정자, 반환형, 이름, 매개변수 목록을 올바른 문법 순서대로 조립하는 능력 점검 |
| X02 | 객관식 | static-인스턴스 접근 제한 | 28 | static 인스턴스 접근 불가 원리 등 헷갈리기 쉬운 C# 함수의 기본 개념들을 종합 점검하고 함정을 가려냄 |

## 커버리지 점검
- 주차 원문 번호 목록: 25, 28
- 실제 반영된 원문 번호: 25, 28
- 누락 원문 번호: 없음
- 추가 확장 개념: 시그니처 조립, static 접근 제한 함정

## JSON 변환 체크
- 목표 세트 ID(basic/challenge): `unity_u03_function_syntax_b01`, `unity_u03_function_syntax_c01`
- `practice/data/sets/unity/*.json` 반영 여부: 완료
- `practice/data/sets.index.json` 반영 여부: 기존 존재
- `practice/data/theory.index.json` 매핑 동기화 여부: 점검 필요
