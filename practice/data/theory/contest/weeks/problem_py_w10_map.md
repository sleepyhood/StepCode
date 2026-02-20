# Python Contest Week 10 분반 매핑표

## 목적
- `problem_py_w10_*`와 `answer_py_w10_*`의 문항 번호를 1:1로 동기화하기 위한 매핑표입니다.

## 파일 대응
- 문제지(초등): `practice/data/theory/contest/weeks/problem_py_w10_elementary.md`
- 정답지(초등): `practice/data/theory/contest/weeks/answer_py_w10_elementary.md`
- 문제지(중등): `practice/data/theory/contest/weeks/problem_py_w10_middle.md`
- 정답지(중등): `practice/data/theory/contest/weeks/answer_py_w10_middle.md`
- 문제지(고등): `practice/data/theory/contest/weeks/problem_py_w10_high.md`
- 정답지(고등): `practice/data/theory/contest/weeks/answer_py_w10_high.md`

## 매핑 규칙
1. 같은 레벨에서는 문제 문항 번호와 정답 문항 번호를 동일하게 유지한다.
2. 원문(`problem_py_w10.md`) 직접 대응이 필요한 경우 `원문 문항` 칸을 채운다.

## Elementary 매핑
| 레벨 | 문제 파일 문항 | 정답 파일 문항 | 원문 회차 | 원문 문항 | 핵심 개념 태그 | 문항 유형 | 난도 배치 근거 | 권장 시간(분) | 예상 오답코드 | 이론 연결 | 해설 | 비고 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E | 1번 | 1번 | PY_1회차 | 1번 | 모듈용도 | 개념판별 | 모듈 기능 매핑 기본 | 1 | READ | W10 개념 1 | `pickle` 설명이 잘못 짝지어진 항목입니다. | 원문 직접대응 |
| E | 2번 | 2번 | PY_1회차 | 2번 | os 모듈 | 개념판별 | API 이름 판별 | 1 | READ | W10 개념 1 | `seekid`는 os에 없습니다. | 원문 직접대응 |
| E | 3번 | 3번 | PY_2회차 | 5번 | re.fullmatch | 코드추적 | 패턴 매칭 기초 | 1 | FLOW | W10 개념 2 | `oh`만 매치됩니다. | 원문 직접대응 |
| E | 4번 | 4번 | PY_2회차 | 4번 | collections | 개념판별 | 컨테이너 분류 | 1 | READ | W10 개념 3 | 직접 대체 아님: `str`. | 원문 직접대응 |
| E | 5번 | 5번 | - | - | datetime | 코드추적 | strftime 출력 해석 | 1 | TYPE | W10 개념 1 | 포맷 출력은 `2024-02-01 09:03`. | 원문 직접대응 없음(개념 보강) |

## Middle 매핑
| 레벨 | 문제 파일 문항 | 정답 파일 문항 | 원문 회차 | 원문 문항 | 핵심 개념 태그 | 문항 유형 | 난도 배치 근거 | 권장 시간(분) | 예상 오답코드 | 이론 연결 | 해설 | 비고 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M | 1번 | 1번 | PY_2회차 | 4번 | collections | 개념판별 | 컨테이너 대체 이해 | 1 | READ | W10 개념 3 | `str`은 직접 대체 대상이 아닙니다. | 원문 직접대응 |
| M | 2번 | 2번 | PY_3회차 | 5번 | re.fullmatch | 코드추적 | 전체 매칭 판별 | 1 | FLOW | W10 개념 2 | `oh`만 None이 아닙니다. | 원문 직접대응 |
| M | 3번 | 3번 | PY_2회차 | 11번 | datetime 포맷 | 개념판별 | 형식코드 구분 | 1 | TYPE | W10 개념 1 | `%Z`는 시간대, AM/PM은 `%p`. | 원문 직접대응 |
| M | 4번 | 4번 | - | - | defaultdict | 코드추적 | 기본값 동작 확인 | 1 | FLOW | W10 개념 3 | `d['c']`는 0으로 처리되어 합 2. | 원문 직접대응 없음(개념 보강) |
| M | 5번 | 5번 | - | - | re.fullmatch | 코드추적 | 정규식 양/음 사례 | 1 | FLOW | W10 개념 2 | `abbbc`만 True, `ac`는 False. | 원문 직접대응 없음(개념 보강) |

## High 매핑
| 레벨 | 문제 파일 문항 | 정답 파일 문항 | 원문 회차 | 원문 문항 | 핵심 개념 태그 | 문항 유형 | 난도 배치 근거 | 권장 시간(분) | 예상 오답코드 | 이론 연결 | 해설 | 비고 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H | 1번 | 1번 | PY_2회차 | 11번 | datetime 포맷 | 코드추적 | 포맷 코드 조합 해석 | 2 | TYPE | W10 개념 1 | `%a %B %M %Y` -> `Thu February 03 2024`. | 원문 변형 |
| H | 2번 | 2번 | PY_2회차 | 5번 | re.fullmatch | 코드추적 | 리스트 필터 결합 | 2 | FLOW | W10 개념 2 | 매치 리스트는 `['oh']`. | 원문 변형 |
| H | 3번 | 3번 | - | - | deque | 코드추적 | 양끝 연산 이해 | 1 | FLOW | W10 개념 3 | appendleft/pop 후 `[0,1,2]`. | 원문 직접대응 없음(개념 보강) |
| H | 4번 | 4번 | - | - | Counter | 코드추적 | 빈도수/최빈값 판별 | 1 | READ | W10 개념 3 | `a` 빈도 3, 최빈 키 `a`. | 원문 직접대응 없음(개념 보강) |
| H | 5번 | 5번 | PY_1회차 | 2번 | os 모듈 | 개념판별 | 속성 존재 여부 확인 | 1 | READ | W10 개념 1 | `chdir=True`, `seekid=False`. | 원문 변형 |

## 운영 체크
1. 각 레벨 문제 수와 정답 수가 동일한가
2. 같은 문항 번호가 문제/정답에 모두 존재하는가
