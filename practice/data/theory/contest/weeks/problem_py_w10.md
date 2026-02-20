# Python Contest Week 10 Problem Set

## 주차 주제
- 모듈(datetime, re, collections)

## 실전 문제 묶음
- 아래 문항은 출처 원문에서 주차 목표에 맞게 선별한 실제 문제이다.

### PY_1회차
- 문항: 1, 2

#### 문제 1
1. 다음은 파이썬 모듈에 대한 설명이다. 올바르지 않게 짝지어 진 것을 고르시오. [중고]
⓵ datetime – 날짜를 다루기 위한 모듈
⓶ math – 수학과 관련된 함수가 포함된 모듈
⓷ os – 환경변수나 디렉터리 등을 제어하는 모듈
⓸ pickle – 특정 디렉터리에 있는 파일 이름을 모두 알아야 할 때 사용하는 모듈
⓹ traceback – 프로그램 실행 중 발생한 오류를 추적하는 모듈

---

#### 문제 2
2. 다음 중 os 모듈에 정의되어 있지 않은 함수를 고르시오. [초]
⓵ getpid
⓶ setregid
⓷ read
⓸ chdir
⓹ seekid

---

### PY_2회차
- 문항: 4, 5, 11

#### 문제 4
4. collections 모듈은 파이썬의 범용 내장 컨테이너에 대한 대안을 제공하는 특수 컨테이너가 구현되어 있는 모듈입니다. 이 모듈의 컬렉션들이 구현하고 있는 파이썬 내장 컨테이너가 아닌 것을 고르시오. [초, 중, 고]
⓵ list
⓶ dict
⓷ set
⓸ str
⓹ tuple

---

#### 문제 5
5. 다음 프로그램의 실행 결과에서 None 을 출력하지 않는 줄은 몇 번 줄인가? [초, 중, 고]
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

---

#### 문제 11
11. datetime 의 strftime 함수는 날짜 데이터를 형식을 통해 출력할 수 있도록 도와주는 함수입니다. 다음 중 형식과 그 예시가 올바르게 짝지어지지 않은 것을 고르시오. [초, 중, 고]
⓵ `%a`- Mon
⓶ `%B`- February
⓷ `%M`- 03
⓸ `%Z`- AM
⓹ `%Y`- 2024

---
### PY_3회차
- 문항: 4, 5

#### 문제 4
4. collections 모듈은 파이썬의 범용 내장 컨테이너에 대한 대안을 제공하는 특수 컨테이너가 구현되어 있는 모듈입니다. 이 모듈의 컬렉션들이 구현하고 있는 파이썬 내장 컨테이너가 아닌 것을 고르시오. [초, 중, 고]
⓵ list
⓶ dict
⓷ set
⓸ str
⓹ tuple

---

#### 문제 5
5. 다음 프로그램의 실행 결과에서 None 을 출력하지 않는 줄은 몇 번 줄인가? [초, 중, 고]
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

---


