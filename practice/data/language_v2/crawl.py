from playwright.sync_api import sync_playwright
import os


def scrape_baekjoon(url):
    with sync_playwright() as p:
        # headless=False로 띄워야 백준(acmicpc)의 봇 탐지(Cloudflare 등)를 우회하기 좋습니다.
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto(url)

            # CSS Selector(id 기반)를 이용한 핵심 요소 추출
            problem_id = url.split("/")[-1]
            print(problem_id)
            title = page.locator("#problem_title").text_content(timeout=5000).strip()
            description = page.locator("#problem_description").inner_text().strip()
            input_desc = page.locator("#problem_input").inner_text().strip()
            output_desc = page.locator("#problem_output").inner_text().strip()

            # 샘플 입출력 추출
            sample_in = ""
            if page.locator("#sample-input-1").count() > 0:
                sample_in = page.locator("#sample-input-1").inner_text().strip()

            sample_out = ""
            if page.locator("#sample-output-1").count() > 0:
                sample_out = page.locator("#sample-output-1").inner_text().strip()

        except Exception as e:
            print(f"크롤링 에러: {e}")
            return None, None
        finally:
            browser.close()

        # 수석 감수자 권장 마크다운(MD) 템플릿에 맞추어 문자열 포매팅
        md_content = f"""---
id: bj_{problem_id}
tags: [baekjoon, scraped]
source: {url}
---

# [{problem_id}번] {title}

## 1. 문제 설명
{description}

---

## 2. 입출력 설명

* **입력:**
{input_desc}

* **출력:**
{output_desc}

---

## 3. 예시

### 예시 입력 1
```text
{sample_in}
```

### 예시 출력 1
```text
{sample_out}
```

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (Python)
**(백준 크롤러에서는 정답 코드를 긁어올 수 없으므로, 선생님께서 아래에 직접 보충해 주세요)**

```python
A, B = map(int, input().split())
print(A + B)
```
<!-- ANSWER_END -->
"""
        return title, md_content


def scrape_doingcoding(url):
    with sync_playwright() as p:
        # 자체 학원 사이트는 봇 탐지가 약할 수 있으므로 headless=True로 1초 만에 수집 가능
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # 타임아웃을 넉넉하게 주고 네트워크 통신이 끝날 때까지 기다립니다.
            page.goto(url, wait_until="domcontentloaded", timeout=10000)

            problem_id = url.split("/")[-1]

            # 요소가 없을 경우에 봇이 죽지 않도록 방어 코드(Safe Extraction)를 적용합니다.
            def get_text(xpath, timeout=2000):
                try:
                    el = page.locator(xpath).first
                    el.wait_for(timeout=timeout)
                    return el.inner_text().strip()
                except:
                    return "(내용 없음)"

            title = get_text('//*[@id="problem-main"]/div[3]/div[1]/div/div', 5000)
            if title == "(내용 없음)":
                # 제목마저 못가져오면 진짜 아예 페이지가 없거나 로딩이 실패한 것임
                raise Exception("제목 요소를 찾을 수 없음")

            description = get_text('//*[@id="problem-content"]/p[2]')
            input_desc = get_text('//*[@id="problem-content"]/p[4]')
            output_desc = get_text('//*[@id="problem-content"]/p[6]')
            sample_in = get_text('//*[@id="problem-content"]/div[1]/div/div[1]/pre')
            sample_out = get_text('//*[@id="problem-content"]/div[1]/div/div[2]/pre')

        except Exception as e:
            print(f"XPath 크롤링 에러({url}): {e}")
            return None, None
        finally:
            browser.close()

        # 수석 감수자 권장 마크다운(MD) 템플릿에 맞추어 문자열 포매팅
        md_content = f"""---
id: dc_{problem_id}
tags: [doingcoding, scraped]
source: {url}
---

# [{problem_id}번] {title}

## 1. 문제 설명
{description}

---

## 2. 입출력 설명

* **입력:**
{input_desc}

* **출력:**
{output_desc}

---

## 3. 예시

### 예시 입력 1
```text
{sample_in}
```

### 예시 출력 1
```text
{sample_out}
```

---

<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (Python)
**(백준 크롤러에서는 정답 코드를 긁어올 수 없으므로, 선생님께서 아래에 직접 보충해 주세요)**

```python
A, B = map(int, input().split())
print(A + B)
```
<!-- ANSWER_END -->
"""
        return title, md_content


if __name__ == "__main__":
    target_url = "http://edu.doingcoding.com/problem/P101v0701"
    print(f"[크롤링 시작] {target_url}")

    title, md_output = scrape_doingcoding(target_url)

    if md_output:
        # 결과를 현재 폴더에 저장
        save_path = f"01_dc_{target_url.split('/')[-1]}.md"
        with open(save_path, "w", encoding="utf-8-sig") as f:
            f.write(md_output)
        print(f"[성공] 크롤링 완료! 파일이 저장되었습니다: '{save_path}'")
