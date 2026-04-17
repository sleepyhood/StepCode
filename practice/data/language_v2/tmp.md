선생님, 사실 앞선 **3단계 코드의 마지막 부분에 4단계의 핵심 목표(YAML 프론트매터 및 마크다운 템플릿 조립)를 이미 포함**시켜 두었습니다! 코드가 중간에 끊기면 바로 테스트해 보시기 어려울 것 같아 한 번에 동작하도록 묶어두었거든요.

하지만 크롤러 코드가 길어지면 유지보수가 힘들어집니다. 특히 나중에 Next.js 플랫폼에 맞춰 프론트매터 속성을 추가하거나 본문 디자인을 바꿀 때, 수백 줄짜리 크롤링 로직 사이를 헤집고 다니는 건 비효율적입니다.

따라서 진정한 **[4단계]의 목표는 이 마크다운 조립 부분을 깔끔하고 독립적인 함수로 분리(Refactoring)하여 관리하기 쉽게 만드는 것**입니다.

---

### [4단계] MDX 템플릿 렌더링 전용 함수 분리

기존 `crawl.py` 파일의 상단(1, 2단계 함수가 있는 곳 주변)에 아래의 함수를 추가해 주세요. `json` 모듈을 사용해 배열(List) 데이터를 YAML 프론트매터에 가장 안전하고 완벽하게 포매팅해 주는 전용 렌더러입니다.

(파일 맨 위에 `import json`이 없다면 추가해 주세요.)

```python
import json

# --- [여기에 4단계 함수 추가] ---
def build_mdx_content(data):
    """
    수집된 딕셔너리 데이터를 바탕으로 Next.js 최적화 MDX 문자열을 생성합니다.
    """
    # 배열 데이터를 YAML 배열 포맷으로 안전하게 변환
    tags_str = json.dumps(data.get("tags", []), ensure_ascii=False)
    contest_str = json.dumps(data.get("contest", []), ensure_ascii=False)
    
    # Boolean 값을 YAML 표준 소문자(true/false)로 변환
    has_subtask_str = "true" if data.get("has_subtask") else "false"
    has_hint_str = "true" if data.get("has_hint") else "false"
    
    # 샘플 입출력 렌더링
    samples_md = ""
    for idx, (s_in, s_out) in enumerate(data.get("samples", []), 1):
        samples_md += f"### 예시 입력 {idx}\n```text\n{s_in}\n```\n\n### 예시 출력 {idx}\n```text\n{s_out}\n```\n\n"

    # 최종 마크다운 조립
    return f"""---
id: bj_{data['problem_id']}
title: "{data['title']}"
level: {data['level']}
time_limit: "{data['time_limit']}"
memory_limit: "{data['memory_limit']}"
has_subtask: {has_subtask_str}
has_hint: {has_hint_str}
contest: {contest_str}
tags: {tags_str}
source_url: "{data['url']}"
---

# [{data['problem_id']}번] {data['title']}

## 1. 문제 설명
{data['description']}

---

## 2. 입출력 설명

* **입력:**
{data['input_desc']}

* **출력:**
{data['output_desc']}

---

## 3. 예시

{samples_md}---

{data.get('subtask_md', '')}## 4. 힌트
{data['hint_md']}

---

## [정답 및 해설 (Ground Truth)]

### 모범 코드 (Python)
**(백준 크롤러에서는 정답 코드를 긁어올 수 없으므로, 선생님께서 아래에 직접 보충해 주세요)**

```python
A, B = map(int, input().split())
print(A + B)
```
"""
# ------------------------------
```

---

### 💡 완성 후 연결 포인트 (3단계 코드 리팩토링)

이제 방금 만든 함수를 사용하도록 **3단계의 `scrape_baekjoon` 함수 마지막 부분을 수정**합니다.

`scrape_baekjoon` 함수 맨 아래쪽, `missing_fields` 체크하는 부분 바로 아래부터 `return title, md_content`까지의 **기존 마크다운 조립 코드를 싹 지우시고 아래 코드로 교체**해 주세요.

**[교체할 3단계 코드 하단 부분]**
```python
        # --- (이전 코드 동일: missing_fields 체크 후) ---

        # 수집한 데이터를 하나의 딕셔너리로 묶어 4단계 렌더링 함수로 전달
        mdx_data = {
            "problem_id": problem_id,
            "title": title,
            "level": level,
            "time_limit": time_limit,
            "memory_limit": memory_limit,
            "has_subtask": has_subtask,
            "has_hint": has_hint,
            "contest": contest_list,
            "tags": tags_list,
            "url": url,
            "description": description,
            "input_desc": input_desc,
            "output_desc": output_desc,
            "samples": samples,
            "subtask_md": subtask_md,
            "hint_md": hint_md
        }
        
        # 4단계 함수 호출을 통해 깔끔하게 MDX 생성!
        md_content = build_mdx_content(mdx_data)

        return title, md_content
```

이렇게 연결해 두시면, 향후 템플릿을 수정해야 할 때 복잡한 크롤링 코드는 신경 쓰지 않고 오직 `build_mdx_content` 함수 하나만 수정하시면 됩니다!

이제 대망의 마지막 **[5단계: GUI 연동 및 테스트]**만 남았습니다. 준비되셨다면 말씀해 주세요! 🚀