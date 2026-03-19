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

            # 샘플 입출력 추출 (다중 샘플 대응)
            samples = []
            i = 1
            while True:
                in_sel = f"#sample-input-{i}"
                out_sel = f"#sample-output-{i}"
                if page.locator(in_sel).count() > 0 and page.locator(out_sel).count() > 0:
                    s_in = page.locator(in_sel).inner_text().strip()
                    s_out = page.locator(out_sel).inner_text().strip()
                    samples.append((s_in, s_out))
                    i += 1
                else:
                    break


            # 힌트 추출 (있을 수도, 없을 수도 있음)
            hint = ""
            if page.locator("#problem_hint").count() > 0:
                hint = page.locator("#problem_hint").inner_text().strip()

        except Exception as e:
            print(f"크롤링 에러: {e}")
            return None, None
        finally:
            browser.close()

        # 샘플 MD 조립
        samples_md = ""
        for idx, (s_in, s_out) in enumerate(samples, 1):
            samples_md += f"### 예시 입력 {idx}\n```text\n{s_in}\n```\n\n### 예시 출력 {idx}\n```text\n{s_out}\n```\n\n"

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

{samples_md}---

## 4. 힌트
{hint if hint else "(힌트가 없습니다.)"}

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
            
            # 샘플 입출력 추출 (다중 샘플 대응)
            samples = []
            i = 1
            while True:
                in_xpath = f'//*[@id="problem-content"]/div[{i}]/div/div[1]/pre'
                out_xpath = f'//*[@id="problem-content"]/div[{i}]/div/div[2]/pre'
                
                s_in = get_text(in_xpath, timeout=1000)
                s_out = get_text(out_xpath, timeout=1000)
                
                if s_in == "(내용 없음)" and s_out == "(내용 없음)":
                    break
                
                samples.append((s_in, s_out))
                i += 1

            # 힌트 추출 (사용자 제공 XPath)
            hint = get_text('//*[@id="problem-content"]/div[2]/div/div/div')

        except Exception as e:
            print(f"XPath 크롤링 에러({url}): {e}")
            return None, None
        finally:
            browser.close()

        # 샘플 MD 조립
        samples_md = ""
        for idx, (s_in, s_out) in enumerate(samples, 1):
            samples_md += f"### 예시 입력 {idx}\n```text\n{s_in}\n```\n\n### 예시 출력 {idx}\n```text\n{s_out}\n```\n\n"

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

{samples_md}---

## 4. 힌트
{hint if hint and hint != "(내용 없음)" else "(힌트가 없습니다.)"}

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
