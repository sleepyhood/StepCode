# Python Contest Week 10 Elementary Problem Set

## 범위
- 모듈 용도 구분
- os 함수 기초
- re fullmatch 기초

## 문제 1
연계 개념: 개념 1) 모듈-용도 매핑 규칙
다음은 파이썬 모듈에 대한 설명이다. 올바르지 않게 짝지어진 것을 고르시오.
⓵ datetime - 날짜를 다루기 위한 모듈
⓶ math - 수학과 관련된 함수가 포함된 모듈
⓷ os - 환경변수나 디렉터리 등을 제어하는 모듈
⓸ pickle - 특정 디렉터리에 있는 파일 이름을 모두 알아야 할 때 사용하는 모듈
⓹ traceback - 프로그램 실행 중 발생한 오류를 추적하는 모듈

## 문제 2
연계 개념: 개념 1) 모듈-용도 매핑 규칙
다음 중 os 모듈에 정의되어 있지 않은 함수를 고르시오.
⓵ getpid
⓶ setregid
⓷ read
⓸ chdir
⓹ seekid

## 문제 3
연계 개념: 개념 2) `os` 함수 존재 여부 판별
다음 프로그램의 실행 결과에서 None을 출력하지 않는 줄은 몇 번 줄인가?
```python
import re
pattern = re.compile('o[gh]')
print(pattern.fullmatch('o'))
print(pattern.fullmatch('oh'))
print(pattern.fullmatch('dog'))
print(pattern.fullmatch('doggie'))
print(pattern.fullmatch('ogre'))
```
⓵ 1번 줄
⓶ 2번 줄
⓷ 3번 줄
⓸ 4번 줄
⓹ 5번 줄

## 문제 4
연계 개념: 개념 3) `re.fullmatch` 전체 매칭
다음 중 `collections` 모듈의 특수 컨테이너가 직접 대체 대상으로 두지 않는 내장 타입을 고르시오.
⓵ list
⓶ dict
⓷ set
⓸ str
⓹ tuple

## 문제 5
연계 개념: 개념 1) 모듈-용도 매핑 규칙
다음 코드의 실행 결과로 올바른 것을 고르시오.
```python
from datetime import datetime
d = datetime(2024, 2, 1, 9, 3)
print(d.strftime('%Y-%m-%d %H:%M'))
```
⓵ 24-02-01 09:03
⓶ 2024-02-01 09:03
⓷ 2024-2-1 9:3
⓸ 2024/02/01 09:03
⓹ 2024-02-01 09:30
