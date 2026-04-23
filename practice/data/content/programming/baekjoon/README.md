# 📚 BOJ Problem Archive Specification

이 프로젝트는 백준 온라인 저지(Baekjoon Online Judge)의 서비스 종료에 대비하여, 문제 본문과 `solved.ac`의 메타데이터를 결합한 **역사적 아카이브**입니다. 모든 데이터는 Next.js 및 MDX 환경에서 즉시 렌더링 가능한 구조로 설계되었습니다.

## 📝 Front-matter 상세 규격

모든 문제 마크다운 파일 상단에는 다음과 같은 YAML 형식의 메타데이터가 포함됩니다. (예시는 **1000번 문제** 기준)

| 필드명 | 타입 | 설명 | 예시 (1000번) |
| :--- | :--- | :--- | :--- |
| `id` | String | 문제 고유 식별자 | `bj_1000` |
| `title` | String | 문제 공식 제목 | `"A+B"` |
| `platform` | String | 출처 플랫폼 | `"baekjoon"` |
| `is_scraped` | Boolean | 자동 수집 여부 | `true` |
| `archived_at` | Date | 아카이브 스냅샷 날짜 | `"2026-04-18"` |
| `level` | Number | solved.ac 난이도 수치 | `1` |
| `tier` | String | solved.ac 난이도 명칭 | `"브론즈 V"` |
| `sprout` | Boolean | 새싹 문제 여부 | `true` |
| `official` | Boolean | 공식 대회/출제 문제 여부 | `true` |
| `is_solvable` | Boolean | 채점 가능 여부 | `true` |
| `gives_no_rating` | Boolean | 레이팅 미부여 여부 | `false` |
| `accepted_user_count` | Number | 최종 정복자 수 | `370693` |
| `average_tries` | Number | 인당 평균 시도 횟수 | `2.61` |
| `is_level_locked` | Boolean | 난이도 고정 여부 | `true` |
| `voted_user_count` | Number | 난이도 투표 참여자 수 | `652` |
| `time_limit` | String | 시간 제한 | `"2 초"` |
| `memory_limit` | String | 메모리 제한 | `"128 MB"` |
| `has_subtask` | Boolean | 서브태스크 존재 여부 | `false` |
| `has_hint` | Boolean | 힌트 존재 여부 | `true` |
| `badges` | Array | **[NEW]** 특수 문제 배지 리스트 | `["인터랙티브"]` |
| `contest` | Array | 출제 대회 리스트 | `[]` |
| `authors` | Object[] | 역할별 저자 정보 | (하단 참조) |
| `tags` | Array | 한국어 알고리즘 분류 | `["구현", "사칙연산", "수학"]` |
| `tag_keys` | Array | 영문 알고리즘 키값 | `["implementation", "math"]` |
| `source_url` | String | 원본 문제 주소 | `"https://.../1000"` |

---

## 🚀 크롤링 엔진 및 자동화 전략

`crawl.py` 및 `gui_crawler_v26_4_23_1.py`를 통해 고도화된 수집 프로세스를 제공합니다.

### 1. 지능형 수집 모드
*   **표준 모드 (Full Re-crawl):** 문제 본문과 모든 이미지를 포함하여 전체 마크다운을 생성합니다.
*   **라이트 모드 (Light Mode):** 기존 MD 파일의 본문은 유지한 채, `badges` 등 메타데이터 필드만 초고속으로 패치합니다. (이미지/CSS 차단)
*   **동적 모드 (Dynamic Mode):** `STRUCTURE_ALTERING_BADGES`가 포함된 특수 문제에 대해 섹션 단위의 정밀 파싱을 수행합니다.

### 2. 구조 변경 배지 (Structure-Altering Badges)
아래 배지가 포함된 문제는 표준 HTML 구조와 다르므로 **동적 모드** 또는 **Full Re-crawl**이 권장됩니다.
*   `인터랙티브`, `함수 구현`, `클래스 구현`, `투 스텝`

### 3. 성능 및 안정성
*   **병렬 처리:** 멀티스레딩 워커를 통해 동시 수집을 수행합니다. (시스템 사양에 따라 워커 수 조절)
*   **탐지 회피:** 랜덤 User-Agent 로테이션, Deep Shuffle(수집 순서 무작위화), Stealth 스크립트 주입을 통해 안정적인 수집을 보장합니다.
*   **404 격리:** 삭제된 문제는 `404_not_found` 폴더로 자동 격리되어 관리됩니다.

---

## 📂 디렉토리 구조 및 관리 규칙

*   **`scraped/`**: 크롤러에 의해 자동 생성된 데이터 폴더입니다. (Git 관리 대상에서 제외)
*   **`source/`**: 수동으로 검수하거나 큐레이션된 마스터 컨텐츠 폴더입니다.
*   **`404_not_found/`**: 존재하지 않는 문제에 대한 더미 파일이 보관됩니다.

---

### 🎨 Authors 데이터 예시 (1000번)

저자 정보는 역할별로 세분화되어 관리됩니다.

```yaml
authors:
  - role: "creator"
    names: ["baekjoon"]
  - role: "contributor"
    names: ["doju"]
  - role: "author"
    names: ["djm03178"]
```

---

## 💡 프로젝트 활용 가이드

1.  **난이도 기반 필터링:** `level` 속성을 사용하여 브론즈부터 루비까지의 맞춤형 로드맵을 생성할 수 있습니다.
2.  **데이터 신뢰도 검증:** `is_level_locked`가 `true`이고 `voted_user_count`가 높은 문제는 백준이 사라진 이후에도 가장 공신력 있는 학습 자료로 분류됩니다.
3.  **영문 검색 지원:** `tag_keys`를 활용하여 영문 알고리즘 명칭(`geometry`, `dp` 등)으로도 문제를 검색할 수 있도록 구현되었습니다.

---

> **Note:** 2026년 4월 28일 이후 백준 서버는 응답하지 않으므로, 이 문서에 정의된 `archived_at` 이후의 동적 데이터 변화는 반영되지 않는 **최종 기록물**입니다.

---