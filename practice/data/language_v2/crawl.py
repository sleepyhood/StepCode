from playwright.sync_api import sync_playwright
from lxml import html
import json
import os
import re
import shutil
import tempfile
import zipfile

SECTION_HEADINGS = {
    "description": ["문제 설명", "문제설명", "설명"],
    "input": ["입력"],
    "output": ["출력"],
    "hint": ["힌트"],
}
REQUIRED_FIELD_PLACEHOLDERS = {"", "(내용 없음)"}
DOINGCODING_CSRF_SEED_URL = "http://edu.doingcoding.com/api/profile"
DOINGCODING_CSRF_FALLBACK_URL = "http://edu.doingcoding.com/api/website"
DOINGCODING_ADMIN_LOGIN_URL = "http://edu.doingcoding.com/admin/login"
DOINGCODING_ADMIN_PROBLEMS_URL = "http://edu.doingcoding.com/admin/problems"
DOINGCODING_ADMIN_ID_SELECTOR = 'xpath=//*[@id="app"]/form/div[1]/div/div/input'
DOINGCODING_ADMIN_PASSWORD_SELECTOR = 'xpath=//*[@id="app"]/form/div[2]/div/div/input'
DOINGCODING_ADMIN_LOGIN_BUTTON_SELECTOR = 'xpath=//*[@id="app"]/form/div[3]/div/button'
DOINGCODING_ADMIN_SEARCH_SELECTORS = [
    'xpath=//*[@id="app"]/div/div[3]/div[1]/div[1]/header/div[2]/div/div/input',
    'xpath=//*[@id="app"]//header//input',
    'css=header input',
    'css=input[type="text"]',
]
DOINGCODING_ADMIN_ROW_SELECTORS = [
    'xpath=//*[@id="app"]/div/div[3]/div[1]/div[1]/div/div[1]/div[4]/div[2]/table/tbody/tr',
    'xpath=//*[@id="app"]//table/tbody/tr',
    'css=table tbody tr',
]
DOINGCODING_ADMIN_DOWNLOAD_BUTTON_SELECTORS = [
    'xpath=//*[@id="app"]/div/div[3]/div[1]/div[1]/div/div[1]/div[4]/div[2]/table/tbody/tr/td[7]/div/div/div[2]/button',
    'xpath=//*[@id="app"]//table/tbody/tr[1]//button',
    'css=table tbody tr button',
]


def _clean_text(value):
    if not value:
        return ""
    value = value.replace("\xa0", " ")
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def _normalize_heading(text):
    cleaned = _clean_text(text)
    return re.sub(r"[\s:：\-\[\]\(\)]", "", cleaned)


def _matches_heading(text, candidates):
    normalized = _normalize_heading(text)
    return any(normalized == _normalize_heading(candidate) for candidate in candidates)


def _iter_direct_children(element):
    for child in element.xpath("./*"):
        yield child


def _element_text(element):
    return _clean_text("".join(element.itertext()))


def _has_pre_descendant(element):
    return bool(element.xpath(".//pre"))


def _looks_like_section_heading(text):
    return any(_matches_heading(text, candidates) for candidates in SECTION_HEADINGS.values())


def _extract_section_after_heading(content_root, labels):
    children = list(_iter_direct_children(content_root))
    for index, child in enumerate(children):
        text = _element_text(child)
        if not _matches_heading(text, labels):
            continue

        chunks = []
        for sibling in children[index + 1:]:
            sibling_text = _element_text(sibling)
            if not sibling_text:
                continue
            if _looks_like_section_heading(sibling_text):
                break
            if _has_pre_descendant(sibling):
                break
            chunks.append(sibling_text)

        if chunks:
            return "\n\n".join(chunks)

    return ""


def _find_doingcoding_content_root(tree):
    roots = tree.xpath('//*[@id="problem-content"]')
    return roots[0] if roots else None


def _find_doingcoding_title(tree):
    xpath_candidates = [
        '//*[@id="problem-main"]//*[self::h1 or self::h2 or self::h3][1]',
        '//*[@id="problem-main"]/div[3]/div[1]/div/div',
        '//*[@id="problem-main"]//*[contains(@class, "title")][1]',
    ]
    for xpath_expr in xpath_candidates:
        nodes = tree.xpath(xpath_expr)
        if not nodes:
            continue
        text = _element_text(nodes[0])
        if text:
            return text

    nodes = tree.xpath('//*[@id="problem-main"]//*')
    for node in nodes:
        text = _element_text(node)
        if text and len(text) <= 200:
            return text
    return ""


def _missing_required_fields(field_map):
    missing = []
    for name, value in field_map.items():
        text = _clean_text(value)
        if text in REQUIRED_FIELD_PLACEHOLDERS:
            missing.append(name)
    return missing


def _extract_sample_pairs(content_root):
    samples = []
    for child in _iter_direct_children(content_root):
        text = _element_text(child)
        if _matches_heading(text, SECTION_HEADINGS["hint"]):
            break

        pre_nodes = child.xpath(".//pre")
        if len(pre_nodes) < 2:
            continue

        pre_texts = [_clean_text("".join(node.itertext())) for node in pre_nodes]
        pre_texts = [text for text in pre_texts if text or text == ""]

        pair_count = len(pre_texts) // 2
        for index in range(pair_count):
            sample_input = pre_texts[index * 2]
            sample_output = pre_texts[index * 2 + 1]
            samples.append((sample_input, sample_output))

    return samples


def _normalize_code_text(value):
    if not value:
        return ""
    text = value.replace("\xa0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def _pick_best_code(candidates):
    normalized = []
    for candidate in candidates:
        text = _normalize_code_text(candidate)
        if text:
            normalized.append(text)
    if not normalized:
        return ""
    normalized.sort(key=lambda item: (item.count("\n"), len(item)), reverse=True)
    return normalized[0]


def _extract_editor_code(page):
    candidates = page.evaluate(
        """() => {
            const values = [];

            document.querySelectorAll('.CodeMirror').forEach((element) => {
                const editor = element.CodeMirror;
                if (editor && typeof editor.getValue === 'function') {
                    values.push(editor.getValue());
                }
            });

            document.querySelectorAll('textarea').forEach((element) => {
                if (element.value) {
                    values.push(element.value);
                }
            });

            document.querySelectorAll('.CodeMirror-code').forEach((element) => {
                const text = element.innerText || element.textContent || '';
                if (text) {
                    values.push(text);
                }
            });

            document.querySelectorAll('pre code, pre').forEach((element) => {
                const text = element.innerText || element.textContent || '';
                if (text) {
                    values.push(text);
                }
            });

            return values;
        }"""
    )
    return _pick_best_code(candidates)


def _goto_with_retries(page, url, wait_until="domcontentloaded", timeout=10000, ready_selector=None, attempts=3):
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            response = page.goto(url, wait_until=wait_until, timeout=timeout)
            status = response.status if response is not None else "no-response"
            print(f"[접속] {url} (시도 {attempt}/{attempts}, 상태: {status})")
            if ready_selector:
                page.wait_for_selector(ready_selector, timeout=timeout)
            return response
        except Exception as exc:
            last_error = exc
            print(f"[재시도] {url} (시도 {attempt}/{attempts}) 실패: {exc}")
            if attempt < attempts:
                page.wait_for_timeout(500 * attempt)
    raise last_error


def _emit_log(logger, message):
    if callable(logger):
        logger(message)
    print(message)


def _find_first_working_selector(page, selectors, timeout=10000, require_visible=False):
    state = "visible" if require_visible else "attached"
    last_error = None
    for selector in selectors:
        try:
            page.wait_for_selector(selector, timeout=timeout, state=state)
            return selector
        except Exception as exc:
            last_error = exc
    raise last_error


def extract_cookie_value(cookies, name, domain_hint="edu.doingcoding.com"):
    matches = [cookie for cookie in cookies if cookie.get("name") == name]
    if not matches:
        return None

    prioritized = []
    for cookie in matches:
        domain = cookie.get("domain", "")
        path = cookie.get("path", "")
        score = 0
        if domain_hint and domain_hint in domain:
            score += 2
        if "/admin" in path:
            score += 1
        prioritized.append((score, len(path), cookie))

    prioritized.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return prioritized[0][2].get("value")


def debug_admin_cookie_state(context):
    cookies = context.cookies()
    csrftoken = extract_cookie_value(cookies, "csrftoken")
    sessionid = extract_cookie_value(cookies, "sessionid")
    return {
        "cookie_count": len(cookies),
        "has_csrftoken": csrftoken is not None,
        "has_sessionid": sessionid is not None,
    }


def ensure_doingcoding_admin_csrf(page, logger=None):
    def _read_document_cookie():
        try:
            document_cookie = page.evaluate("() => document.cookie")
        except Exception:
            return None

        for token in document_cookie.split(";"):
            name, _, value = token.strip().partition("=")
            if name == "csrftoken" and value:
                return value
        return None

    _emit_log(logger, "[관리자 로그인 준비] /api/profile 접속")
    response = _goto_with_retries(
        page,
        DOINGCODING_CSRF_SEED_URL,
        wait_until="domcontentloaded",
        timeout=10000,
        ready_selector=None,
        attempts=3,
    )
    status = response.status if response is not None else "no-response"
    _emit_log(logger, f"[관리자 로그인 준비] /api/profile 상태: {status}")

    csrftoken = extract_cookie_value(page.context.cookies(), "csrftoken")
    if not csrftoken:
        csrftoken = _read_document_cookie()

    if not csrftoken:
        _emit_log(logger, "[관리자 로그인 준비] /api/website 접속")
        fallback_response = _goto_with_retries(
            page,
            DOINGCODING_CSRF_FALLBACK_URL,
            wait_until="domcontentloaded",
            timeout=10000,
            ready_selector=None,
            attempts=3,
        )
        fallback_status = fallback_response.status if fallback_response is not None else "no-response"
        _emit_log(logger, f"[관리자 로그인 준비] /api/website 상태: {fallback_status}")
        csrftoken = extract_cookie_value(page.context.cookies(), "csrftoken") or _read_document_cookie()

    if not csrftoken:
        _emit_log(logger, "[관리자 로그인 준비] /admin/login 접속")
        _goto_with_retries(
            page,
            DOINGCODING_ADMIN_LOGIN_URL,
            wait_until="domcontentloaded",
            timeout=10000,
            ready_selector=DOINGCODING_ADMIN_ID_SELECTOR,
            attempts=3,
        )
        csrftoken = extract_cookie_value(page.context.cookies(), "csrftoken") or _read_document_cookie()

    if csrftoken:
        _emit_log(logger, "[관리자 로그인 준비] csrftoken 확보 성공")
        return csrftoken

    _emit_log(logger, "[관리자 로그인 준비] csrftoken 없음")
    raise RuntimeError("관리자 로그인 전 csrftoken 쿠키를 확보하지 못했습니다.")


def _wait_for_admin_login_success(page, timeout=5000):
    page.wait_for_function(
        """() => {
            const path = window.location.pathname || "";
            return !path.includes('/admin/login');
        }""",
        timeout=timeout,
    )


def _attempt_admin_login_submit(page, logger=None):
    password_locator = page.locator(DOINGCODING_ADMIN_PASSWORD_SELECTOR)
    login_button = page.locator(DOINGCODING_ADMIN_LOGIN_BUTTON_SELECTOR)
    go_button = page.locator('button:has-text("GO")').first

    try:
        _emit_log(logger, "[관리자 로그인] 제출 시도 1: locator Enter")
        password_locator.click()
        password_locator.press("Enter")
        _wait_for_admin_login_success(page, timeout=5000)
        return
    except Exception:
        pass

    try:
        _emit_log(logger, "[관리자 로그인] 제출 시도 2: keyboard Enter")
        password_locator.click()
        page.keyboard.press("Enter")
        _wait_for_admin_login_success(page, timeout=5000)
        return
    except Exception:
        pass

    try:
        _emit_log(logger, "[관리자 로그인] 제출 시도 3: form requestSubmit")
        password_locator.evaluate(
            """(element) => {
                const form = element.form || element.closest('form');
                if (form && typeof form.requestSubmit === 'function') {
                    form.requestSubmit();
                    return true;
                }
                if (form) {
                    form.submit();
                    return true;
                }
                return false;
            }"""
        )
        _wait_for_admin_login_success(page, timeout=5000)
        return
    except Exception:
        pass

    try:
        _emit_log(logger, "[관리자 로그인] 제출 시도 4: GO 버튼 force click")
        go_button.click(force=True)
        _wait_for_admin_login_success(page, timeout=5000)
        return
    except Exception:
        pass

    try:
        _emit_log(logger, "[관리자 로그인] 제출 시도 5: 로그인 버튼 force click")
        login_button.click(force=True)
        _wait_for_admin_login_success(page, timeout=5000)
        return
    except Exception:
        pass

    _emit_log(logger, "[관리자 로그인] 제출 시도 6: 로그인 버튼 JS click")
    login_button.evaluate(
        """(element) => {
            element.click();
        }"""
    )
    _wait_for_admin_login_success(page, timeout=5000)


def attempt_admin_login_via_request(context, username, password, csrftoken, logger=None):
    _emit_log(
        logger,
        "[관리자 로그인] 네트워크 기반 fallback은 비활성 상태입니다. 성공 요청 payload 확인 후 활성화가 필요합니다.",
    )
    return False


def _load_testcase_info_from_dir(extract_dir):
    info_candidates = [
        os.path.join(extract_dir, "info"),
        os.path.join(extract_dir, "info.json"),
    ]
    for candidate in info_candidates:
        if not os.path.exists(candidate):
            continue
        with open(candidate, "r", encoding="utf-8") as info_file:
            return json.load(info_file)
    return {}


def _read_text_file(path):
    with open(path, "r", encoding="utf-8") as source_file:
        return source_file.read().replace("\r\n", "\n").replace("\r", "\n")


def _pair_testcase_files(extract_dir, info):
    paired = []
    info_cases = info.get("test_cases", {}) if isinstance(info, dict) else {}
    if info_cases:
        def _sort_key(item):
            key = item[0]
            return (0, int(key)) if str(key).isdigit() else (1, str(key))

        for case_id, meta in sorted(info_cases.items(), key=_sort_key):
            input_name = meta.get("input_name")
            output_name = meta.get("output_name")
            if not input_name or not output_name:
                continue
            input_path = os.path.join(extract_dir, input_name)
            output_path = os.path.join(extract_dir, output_name)
            if not os.path.exists(input_path) or not os.path.exists(output_path):
                continue
            paired.append(
                {
                    "id": str(case_id),
                    "input_name": input_name,
                    "output_name": output_name,
                    "input_text": _read_text_file(input_path),
                    "output_text": _read_text_file(output_path),
                    "meta": meta,
                }
            )
        return paired

    discovered_inputs = {}
    discovered_outputs = {}
    for entry in os.listdir(extract_dir):
        full_path = os.path.join(extract_dir, entry)
        if not os.path.isfile(full_path):
            continue
        stem, ext = os.path.splitext(entry)
        if ext == ".in":
            discovered_inputs[stem] = entry
        elif ext == ".out":
            discovered_outputs[stem] = entry

    for stem in sorted(set(discovered_inputs) & set(discovered_outputs), key=lambda value: (0, int(value)) if value.isdigit() else (1, value)):
        paired.append(
            {
                "id": stem,
                "input_name": discovered_inputs[stem],
                "output_name": discovered_outputs[stem],
                "input_text": _read_text_file(os.path.join(extract_dir, discovered_inputs[stem])),
                "output_text": _read_text_file(os.path.join(extract_dir, discovered_outputs[stem])),
                "meta": {},
            }
        )
    return paired


def parse_testcase_bundle(bundle_path, extract_dir):
    with zipfile.ZipFile(bundle_path) as archive:
        archive.extractall(extract_dir)

    info = _load_testcase_info_from_dir(extract_dir)
    cases = _pair_testcase_files(extract_dir, info)
    return {"info": info, "cases": cases, "extract_dir": extract_dir}


def render_testcases_md(testcase_bundle, section_number=5):
    cases = testcase_bundle.get("cases", [])
    info = testcase_bundle.get("info", {})
    if not cases:
        return ""

    sections = [f"## {section_number}. 채점용 테스트케이스", ""]
    if info:
        sections.extend(
            [
                "### 메타데이터",
                "```json",
                json.dumps(info, ensure_ascii=False, indent=4),
                "```",
                "",
            ]
        )

    for case in cases:
        case_id = case["id"]
        sections.extend(
            [
                f"### 테스트케이스 {case_id} 입력",
                "```text",
                case["input_text"].rstrip("\n"),
                "```",
                "",
                f"### 테스트케이스 {case_id} 출력",
                "```text",
                case["output_text"].rstrip("\n"),
                "```",
                "",
            ]
        )

    sections.append("---")
    sections.append("")
    return "\n".join(sections)


def render_templates_md(templates, section_number=5):
    if not templates:
        return ""
    templates_md = [f"## {section_number}. 코드 템플릿", ""]
    for lang, code in templates.items():
        lang_tag = "python" if "Python" in lang else lang.lower()
        templates_md.extend(
            [
                f"### {lang}",
                f"```{lang_tag}",
                code,
                "```",
                "",
            ]
        )
    templates_md.extend(["---", ""])
    return "\n".join(templates_md)


def login_doingcoding_admin(page, username, password, logger=None):
    if not username or not password:
        raise ValueError("관리자 로그인 계정 정보가 필요합니다.")

    csrftoken = ensure_doingcoding_admin_csrf(page, logger=logger)
    _emit_log(logger, "[관리자 로그인] csrf 확보 후 /admin/login 재진입")
    _goto_with_retries(
        page,
        DOINGCODING_ADMIN_LOGIN_URL,
        wait_until="domcontentloaded",
        timeout=10000,
        ready_selector=DOINGCODING_ADMIN_ID_SELECTOR,
        attempts=3,
    )
    page.wait_for_selector(DOINGCODING_ADMIN_PASSWORD_SELECTOR, timeout=10000, state="attached")
    _emit_log(logger, "[관리자 로그인] 로그인 폼 확인 완료")

    page.locator(DOINGCODING_ADMIN_ID_SELECTOR).click()
    page.locator(DOINGCODING_ADMIN_ID_SELECTOR).fill(username)
    page.locator(DOINGCODING_ADMIN_PASSWORD_SELECTOR).click()
    page.locator(DOINGCODING_ADMIN_PASSWORD_SELECTOR).fill(password)
    cookie_state = debug_admin_cookie_state(page.context)
    _emit_log(
        logger,
        f"[관리자 로그인] 제출 전 상태: url={page.url}, csrftoken={'있음' if bool(csrftoken) else '없음'}, cookies={cookie_state['cookie_count']}",
    )

    try:
        _attempt_admin_login_submit(page, logger=logger)
    except Exception as exc:
        cookie_state = debug_admin_cookie_state(page.context)
        _emit_log(
            logger,
            f"[관리자 로그인] 최종 실패: url={page.url}, csrftoken={'있음' if cookie_state['has_csrftoken'] else '없음'}, sessionid={'있음' if cookie_state['has_sessionid'] else '없음'}",
        )
        attempt_admin_login_via_request(page.context, username, password, csrftoken, logger=logger)
        raise RuntimeError("관리자 로그인 실패: CSRF cookie/token mismatch 가능성") from exc

    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)
    _goto_with_retries(
        page,
        DOINGCODING_ADMIN_PROBLEMS_URL,
        wait_until="domcontentloaded",
        timeout=10000,
        ready_selector=None,
        attempts=3,
    )
    _find_first_working_selector(page, DOINGCODING_ADMIN_SEARCH_SELECTORS, timeout=15000, require_visible=False)
    return True


def download_doingcoding_testcases(page, problem_id, download_dir):
    os.makedirs(download_dir, exist_ok=True)
    search_selector = _find_first_working_selector(
        page,
        DOINGCODING_ADMIN_SEARCH_SELECTORS,
        timeout=15000,
        require_visible=False,
    )
    row_selector = _find_first_working_selector(
        page,
        DOINGCODING_ADMIN_ROW_SELECTORS,
        timeout=15000,
        require_visible=False,
    )
    download_selector = _find_first_working_selector(
        page,
        DOINGCODING_ADMIN_DOWNLOAD_BUTTON_SELECTORS,
        timeout=15000,
        require_visible=False,
    )

    page.fill(search_selector, problem_id)
    page.press(search_selector, "Enter")
    page.wait_for_timeout(1000)
    page.wait_for_selector(row_selector, timeout=15000, state="attached")
    row_text = _clean_text(page.text_content(row_selector) or "")
    if problem_id not in row_text:
        raise RuntimeError(f"관리자 문제 목록에서 문제 ID를 확인하지 못했습니다: {problem_id}")

    with page.expect_download() as download_info:
        page.click(download_selector)
    download = download_info.value
    suggested_filename = download.suggested_filename or f"{problem_id}.zip"
    download_path = os.path.join(download_dir, suggested_filename)
    download.save_as(download_path)
    return download_path


def collect_doingcoding_testcases(browser, problem_id, admin_username, admin_password, base_download_dir=None, logger=None):
    work_root = base_download_dir or os.getcwd()
    temp_dir = tempfile.mkdtemp(prefix=f"dc_tc_{problem_id}_", dir=work_root)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()
    try:
        login_doingcoding_admin(page, admin_username, admin_password, logger=logger)
        bundle_path = download_doingcoding_testcases(page, problem_id, temp_dir)
        extract_dir = os.path.join(temp_dir, "extract")
        bundle = parse_testcase_bundle(bundle_path, extract_dir)
        return {"info": bundle.get("info", {}), "cases": bundle.get("cases", [])}
    finally:
        context.close()
        shutil.rmtree(temp_dir, ignore_errors=True)


def scrape_baekjoon(url):
    with sync_playwright() as p:
        # headless=False로 띄워야 백준(acmicpc)의 봇 탐지(Cloudflare 등)를 우회하기 좋습니다.
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            _goto_with_retries(
                page,
                url,
                wait_until="domcontentloaded",
                timeout=10000,
                ready_selector="#problem_title",
                attempts=3,
            )

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

        missing_fields = _missing_required_fields(
            {
                "title": title,
                "description": description,
                "input": input_desc,
                "output": output_desc,
            }
        )
        if missing_fields:
            print(f"필수 필드 누락으로 저장하지 않음({problem_id}): {', '.join(missing_fields)}")
            return None, None

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


def scrape_doingcoding(
    url,
    get_templates=False,
    get_testcases=False,
    admin_username=None,
    admin_password=None,
    testcase_download_dir=None,
    show_browser=False,
    logger=None,
):
    with sync_playwright() as p:
        # 자체 학원 사이트는 봇 탐지가 약할 수 있으므로 headless=True로 1초 만에 수집 가능
        browser = p.chromium.launch(headless=not show_browser)
        page = browser.new_page()

        try:
            # 타임아웃을 넉넉하게 주고 네트워크 통신이 끝날 때까지 기다립니다.
            _goto_with_retries(
                page,
                url,
                wait_until="domcontentloaded",
                timeout=10000,
                ready_selector="#problem-main",
                attempts=3,
            )

            problem_id = url.split("/")[-1]
            tree = html.fromstring(page.content())
            content_root = _find_doingcoding_content_root(tree)

            # 요소가 없을 경우에 봇이 죽지 않도록 방어 코드(Safe Extraction)를 적용합니다.
            def get_text(xpath, timeout=2000):
                try:
                    el = page.locator(xpath).first
                    el.wait_for(timeout=timeout)
                    return el.inner_text().strip()
                except:
                    return "(내용 없음)"

            title = _find_doingcoding_title(tree) or get_text('//*[@id="problem-main"]/div[3]/div[1]/div/div', 5000)
            if title == "(내용 없음)" or not _clean_text(title):
                # 제목마저 못가져오면 진짜 아예 페이지가 없거나 로딩이 실패한 것임
                raise Exception("제목 요소를 찾을 수 없음")

            description = ""
            input_desc = ""
            output_desc = ""
            if content_root is not None:
                description = _extract_section_after_heading(content_root, SECTION_HEADINGS["description"])
                input_desc = _extract_section_after_heading(content_root, SECTION_HEADINGS["input"])
                output_desc = _extract_section_after_heading(content_root, SECTION_HEADINGS["output"])

            description = description or get_text('//*[@id="problem-content"]/p[2]')
            input_desc = input_desc or get_text('//*[@id="problem-content"]/p[4]')
            output_desc = output_desc or get_text('//*[@id="problem-content"]/p[6]')
            
            # 샘플 입출력 추출 (다중 샘플 대응)
            samples = _extract_sample_pairs(content_root) if content_root is not None else []
            if not samples:
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

            # 코드 템플릿 추출 (C, C++, Python3, Java) - 옵션 선택 시에만 동작
            templates = {}
            if get_templates:
                try:
                    # 언어 선택 드롭다운이 있는지 확인
                    dropdown = page.locator('div.ivu-select-selection').first
                    if dropdown.count() > 0:
                        for lang_name in ["C", "C++", "Python3", "Java"]:
                            # 드롭다운 클릭
                            dropdown.click()
                            page.wait_for_timeout(500)
                            
                            # 해당 언어 옵션 클릭
                            lang_option = page.locator(f'li.ivu-select-item:has-text("{lang_name}")').first
                            if lang_option.count() > 0:
                                lang_option.click()
                                page.wait_for_timeout(500)
                                
                                # 새로고침(초기화) 버튼 클릭 시도 (템플릿 강제 로드)
                                reset_btn = page.locator('button.ivu-btn-icon-only')
                                if reset_btn.count() > 0:
                                    reset_btn.first.click()
                                    page.wait_for_timeout(500)
                                    # 확인 모달의 '예' 버튼
                                    confirm_btn = page.locator('button.ivu-btn-primary:has-text("예")')
                                    if confirm_btn.count() > 0:
                                        confirm_btn.click()
                                        page.wait_for_timeout(1000)
                                
                                code_text = _extract_editor_code(page)
                                if code_text:
                                    templates[lang_name] = code_text
                except Exception as te:
                    # 템플릿 추출 실패는 전체 크롤링 실패로 간주하지 않음
                    print(f"템플릿 추출 중 경미한 에러 (문제 없음): {te}")

            testcase_bundle = {}
            if get_testcases:
                testcase_bundle = collect_doingcoding_testcases(
                    browser,
                    problem_id,
                    admin_username,
                    admin_password,
                    base_download_dir=testcase_download_dir,
                    logger=logger,
                )

        except Exception as e:
            print(f"XPath 크롤링 에러({url}): {e}")
            return None, None
        finally:
            browser.close()

        missing_fields = _missing_required_fields(
            {
                "title": title,
                "description": description,
                "input": input_desc,
                "output": output_desc,
            }
        )
        if missing_fields:
            print(f"필수 필드 누락으로 저장하지 않음({problem_id}): {', '.join(missing_fields)}")
            return None, None

        # 샘플 MD 조립
        samples_md = ""
        for idx, (s_in, s_out) in enumerate(samples, 1):
            samples_md += f"### 예시 입력 {idx}\n```text\n{s_in}\n```\n\n### 예시 출력 {idx}\n```text\n{s_out}\n```\n\n"

        next_section_number = 5
        testcases_md = ""
        if testcase_bundle:
            testcases_md = render_testcases_md(testcase_bundle, section_number=next_section_number)
            next_section_number += 1

        templates_md = render_templates_md(templates, section_number=next_section_number)

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

{testcases_md}{templates_md}<!-- ANSWER_START -->
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

    title, md_output = scrape_doingcoding(target_url, get_templates=False)

    if md_output:
        # 결과를 현재 폴더에 저장
        save_path = f"01_dc_{target_url.split('/')[-1]}.md"
        with open(save_path, "w", encoding="utf-8-sig") as f:
            f.write(md_output)
        print(f"[성공] 크롤링 완료! 파일이 저장되었습니다: '{save_path}'")
