# LV46. 클래스와 상속 (커리큘럼 설계 및 매핑 테이블)

본 단원은 객체지향 프로그래밍(OOP)의 핵심인 클래스 선언부터 상속, 가상 함수/추상 클래스를 거쳐 순수 규격서인 **인터페이스(Interface)**까지 단계적으로 학습하도록 구성되었습니다.

---

## 📌 문제 매핑 테이블

| ID | db_id | Legacy/Source | Status | 핵심 포인트 |
|:---|:---:|:---:|:---:|:---|
| **P501v4601** | 1271 | P501v4601 | 크롤링 보관 | 클래스와 구조체, 접근지정자(`public`, `private`) 기본 |
| **P501v4602** | 1272 | P501v4602 | 크롤링 보관 | 생성자와 소멸자, 객체 수명주기 |
| **P501v4603** | 1274 | P501v4603 | 크롤링 보관 | `this` 포인터 / 파이썬 `self`와 멤버변수 식별 |
| **P501v4604** | 1311 | P501v4604 | 크롤링 보관 | 함수 및 생성자 오버로딩 (시그니처 다변화) |
| **P501v4605** | 1312 | P501v4605 | 크롤링 보관 | 디폴트 매개변수 (오른쪽부터 채우기) |
| **P501v4606** | 1313 | P501v4606 | 크롤링 보관 | 우선순위 큐와 함수 객체(비교 클래스) |
| **P501v4607** | 1335 | P501v4607 | 리팩토링 필요 | 클래스 상속(`extends`, `: public`) 기본 문법 |
| **P501v4608** | 1336 | P501v4608 | 크롤링 보관 | `protected` 접근지정자와 부모-자식 가시성 |
| **P501v4609** | 1337 | P501v4609 | 리팩토링 필요 | 메서드 오버라이딩(재정의) |
| **P501v4610** | 1347 | P501v4610 | 크롤링 보관 | `virtual` 가상 함수와 순수 가상 함수, 추상 클래스 |
| **P501v4611** | LOCAL | - | 신규 제작 | **[인터페이스 1] 인터페이스의 탄생**: 순수 규격 선언과 구현 (`implements`) |
| **P501v4612** | LOCAL | - | 신규 제작 | **[인터페이스 2] public 오버라이딩 규칙**: 가시성 제약과 메서드 완성 |
| **P501v4613** | LOCAL | - | 신규 제작 | **[인터페이스 3] 인터페이스와 다형성**: 업캐스팅 및 규격 기반 제어 |
| **P501v4614** | LOCAL | - | 신규 제작 | **[인터페이스 4] 인터페이스 배열 일괄 제어**: 동일 규격 다중 객체 순회 |
| **P501v4615** | LOCAL | - | 신규 제작 | **[인터페이스 5] 다중 구현**: 단일 상속 한계 극복 (`implements A, B`) |
| **P501v4616** | LOCAL | - | 신규 제작 | **[인터페이스 6] 인터페이스 상속**: 규격의 확장 (`interface C extends A, B`) |
| **P501v4617** | LOCAL | - | 신규 제작 | **[인터페이스 7] 상수와 디폴트 메서드**: 규격 내 상수 및 `default` 공통 로직 |
| **P501v4618** | LOCAL | - | 신규 제작 | **[인터페이스 8] 실전 응용: 전략 패턴**: 인터페이스 기반 동적 알고리즘 교체 |

---

## 💡 다언어(Java / C++ / Python) 인터페이스 대응 가이드

StepCode는 표준 입출력(stdin/stdout)을 기반으로 모든 문제를 채점하므로, 각 언어의 문법 구조를 사용하여 문제를 해결합니다.

- **Java**:
  - `interface InterfaceName { void method(); }`
  - `class ClassName implements InterfaceName { public void method() { ... } }`
- **C++**:
  - `class InterfaceName { public: virtual void method() = 0; virtual ~InterfaceName() {} };`
  - `class ClassName : public InterfaceName { public: void method() override { ... } };`
- **Python**:
  - `from abc import ABC, abstractmethod`
  - `class InterfaceName(ABC): @abstractmethod def method(self): pass`
  - `class ClassName(InterfaceName): def method(self): ...`
