import json
import shutil
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from practice.data.language_v2.crawl import (
    DoingCodingAdminSession,
    DOINGCODING_CSRF_FALLBACK_URL,
    DOINGCODING_CSRF_SEED_URL,
    DOINGCODING_ADMIN_DOWNLOAD_BUTTON_SELECTORS,
    DOINGCODING_ADMIN_EDIT_BUTTON_SELECTORS,
    DOINGCODING_ADMIN_ID_SELECTOR,
    DOINGCODING_ADMIN_LOGIN_URL,
    DOINGCODING_ADMIN_LOGIN_BUTTON_SELECTOR,
    DOINGCODING_ADMIN_PASSWORD_SELECTOR,
    DOINGCODING_ADMIN_PROBLEMS_URL,
    DOINGCODING_ADMIN_ROW_SELECTORS,
    DOINGCODING_ADMIN_SEARCH_SELECTORS,
    DOINGCODING_ADMIN_TESTCASE_FILE_INPUT_SELECTORS,
    DOINGCODING_ADMIN_TESTCASE_SAVE_BUTTON_SELECTORS,
    DOINGCODING_ADMIN_TESTCASE_UPLOAD_BUTTON_SELECTORS,
    _extract_section_after_heading,
    _extract_sample_pairs,
    _attempt_admin_login_submit,
    debug_admin_cookie_state,
    ensure_doingcoding_admin_csrf,
    extract_cookie_value,
    _find_first_working_selector,
    _goto_with_retries,
    _find_doingcoding_content_root,
    _find_doingcoding_title,
    _missing_required_fields,
    _pick_best_code,
    collect_doingcoding_testcases,
    collect_doingcoding_testcases_with_session,
    download_doingcoding_testcases,
    login_doingcoding_admin,
    open_doingcoding_admin_session,
    close_doingcoding_admin_session,
    open_doingcoding_problem_editor,
    parse_testcase_bundle,
    render_templates_md,
    render_testcases_md,
    SECTION_HEADINGS,
    upload_doingcoding_testcases,
    upload_doingcoding_testcases_with_session,
)
from lxml import html

CURRENT_DIR = Path(__file__).resolve().parent


class DoingCodingStage1ParsingTests(unittest.TestCase):
    def test_extract_cookie_value_prefers_matching_domain_and_admin_path(self):
        cookies = [
            {"name": "csrftoken", "value": "generic", "domain": "example.com", "path": "/"},
            {"name": "csrftoken", "value": "site_root", "domain": "edu.doingcoding.com", "path": "/"},
            {"name": "csrftoken", "value": "admin_path", "domain": "edu.doingcoding.com", "path": "/admin"},
        ]

        self.assertEqual(extract_cookie_value(cookies, "csrftoken"), "admin_path")

    def test_debug_admin_cookie_state_reports_cookie_flags(self):
        class FakeContext:
            def cookies(self):
                return [
                    {"name": "csrftoken", "value": "abc", "domain": "edu.doingcoding.com", "path": "/admin"},
                    {"name": "sessionid", "value": "def", "domain": "edu.doingcoding.com", "path": "/"},
                ]

        state = debug_admin_cookie_state(FakeContext())

        self.assertEqual(state["cookie_count"], 2)
        self.assertTrue(state["has_csrftoken"])
        self.assertTrue(state["has_sessionid"])

    def test_ensure_doingcoding_admin_csrf_uses_profile_endpoint_first(self):
        class FakeContext:
            def __init__(self):
                self.cookie_values = [{"name": "csrftoken", "value": "cookie_token", "domain": "edu.doingcoding.com", "path": "/"}]

            def cookies(self):
                return list(self.cookie_values)

        class FakePage:
            def __init__(self):
                self.context = FakeContext()

            def evaluate(self, _script):
                return ""

        logs = []
        response = type("Response", (), {"status": 200})()
        with patch("practice.data.language_v2.crawl._goto_with_retries", return_value=response) as goto_mock:
            token = ensure_doingcoding_admin_csrf(FakePage(), logger=logs.append)

        self.assertEqual(token, "cookie_token")
        self.assertEqual(goto_mock.call_args_list[0].args[1], DOINGCODING_CSRF_SEED_URL)
        self.assertEqual(
            logs,
            [
                "[관리자 로그인 준비] /api/profile 접속",
                "[관리자 로그인 준비] /api/profile 상태: 200",
                "[관리자 로그인 준비] csrftoken 확보 성공",
            ],
        )
        goto_mock.assert_called_once()

    def test_ensure_doingcoding_admin_csrf_falls_back_to_website_after_profile(self):
        class FakeContext:
            def __init__(self):
                self.cookie_values = []

            def cookies(self):
                return list(self.cookie_values)

        class FakePage:
            def __init__(self):
                self.context = FakeContext()
                self.evaluations = 0

            def evaluate(self, _script):
                self.evaluations += 1
                return ""

        logs = []
        page = FakePage()

        def fake_goto(_page, url, **_kwargs):
            if url == DOINGCODING_CSRF_FALLBACK_URL:
                page.context.cookie_values = [{"name": "csrftoken", "value": "website_token", "domain": "edu.doingcoding.com", "path": "/"}]
            return None

        with patch("practice.data.language_v2.crawl._goto_with_retries", side_effect=fake_goto) as goto_mock:
            token = ensure_doingcoding_admin_csrf(page, logger=logs.append)

        self.assertEqual(token, "website_token")
        self.assertEqual(goto_mock.call_args_list[0].args[1], DOINGCODING_CSRF_SEED_URL)
        self.assertEqual(goto_mock.call_args_list[1].args[1], DOINGCODING_CSRF_FALLBACK_URL)
        self.assertIn("[관리자 로그인 준비] /api/website 접속", logs)
        self.assertEqual(logs[-1], "[관리자 로그인 준비] csrftoken 확보 성공")

    def test_ensure_doingcoding_admin_csrf_falls_back_to_admin_login_after_profile_and_website(self):
        class FakeContext:
            def __init__(self):
                self.cookie_values = []

            def cookies(self):
                return list(self.cookie_values)

        class FakePage:
            def __init__(self):
                self.context = FakeContext()

            def evaluate(self, _script):
                return ""

        logs = []
        page = FakePage()

        def fake_goto(_page, url, **_kwargs):
            if url == DOINGCODING_ADMIN_LOGIN_URL:
                page.context.cookie_values = [{"name": "csrftoken", "value": "login_token", "domain": "edu.doingcoding.com", "path": "/admin"}]
            return None

        with patch("practice.data.language_v2.crawl._goto_with_retries", side_effect=fake_goto) as goto_mock:
            token = ensure_doingcoding_admin_csrf(page, logger=logs.append)

        self.assertEqual(token, "login_token")
        self.assertEqual(goto_mock.call_args_list[0].args[1], DOINGCODING_CSRF_SEED_URL)
        self.assertEqual(goto_mock.call_args_list[1].args[1], DOINGCODING_CSRF_FALLBACK_URL)
        self.assertEqual(goto_mock.call_args_list[2].args[1], DOINGCODING_ADMIN_LOGIN_URL)
        self.assertIn("[관리자 로그인 준비] /admin/login 접속", logs)
        self.assertEqual(logs[-1], "[관리자 로그인 준비] csrftoken 확보 성공")

    def test_ensure_doingcoding_admin_csrf_raises_when_profile_website_and_login_all_fail(self):
        class FakeContext:
            def cookies(self):
                return []

        class FakePage:
            def __init__(self):
                self.context = FakeContext()

            def evaluate(self, _script):
                return ""

        logs = []
        with patch("practice.data.language_v2.crawl._goto_with_retries"):
            with self.assertRaises(RuntimeError):
                ensure_doingcoding_admin_csrf(FakePage(), logger=logs.append)

        self.assertEqual(logs[-1], "[관리자 로그인 준비] csrftoken 없음")

    def test_extracts_sections_by_heading_instead_of_fixed_indexes(self):
        document = html.fromstring(
            """
            <div id="problem-main">
              <div class="wrapper">
                <h2>01. [반복-for 기초1] 1부터 5까지 출력하기</h2>
              </div>
            </div>
            <div id="problem-content">
              <p>문제 설명</p>
              <p>for문을 사용하여 1부터 5까지 출력합니다.</p>
              <p>추가 안내 문단</p>
              <p>입력</p>
              <p>입력은 없습니다.</p>
              <p>출력</p>
              <p>1부터 5까지 순서대로 출력합니다.</p>
            </div>
            """
        )

        content_root = _find_doingcoding_content_root(document)
        self.assertIsNotNone(content_root)
        self.assertEqual(
            _find_doingcoding_title(document),
            "01. [반복-for 기초1] 1부터 5까지 출력하기",
        )
        self.assertEqual(
            _extract_section_after_heading(content_root, SECTION_HEADINGS["description"]),
            "for문을 사용하여 1부터 5까지 출력합니다.\n\n추가 안내 문단",
        )
        self.assertEqual(
            _extract_section_after_heading(content_root, SECTION_HEADINGS["input"]),
            "입력은 없습니다.",
        )
        self.assertEqual(
            _extract_section_after_heading(content_root, SECTION_HEADINGS["output"]),
            "1부터 5까지 순서대로 출력합니다.",
        )

    def test_ignores_sample_blocks_when_collecting_sections(self):
        document = html.fromstring(
            """
            <div id="problem-main"><div><div class="title">샘플 검사 문제</div></div></div>
            <div id="problem-content">
              <p>문제 설명</p>
              <p>설명 본문입니다.</p>
              <p>입력</p>
              <p>입력 설명입니다.</p>
              <div class="sample-block">
                <div><div><pre>1 2</pre></div><div><pre>3</pre></div></div>
              </div>
              <p>출력</p>
              <p>출력 설명입니다.</p>
            </div>
            """
        )

        content_root = _find_doingcoding_content_root(document)
        self.assertEqual(
            _extract_section_after_heading(content_root, SECTION_HEADINGS["input"]),
            "입력 설명입니다.",
        )
        self.assertEqual(
            _extract_section_after_heading(content_root, SECTION_HEADINGS["output"]),
            "출력 설명입니다.",
        )

    def test_missing_required_fields_rejects_placeholders(self):
        missing = _missing_required_fields(
            {
                "title": "문제 제목",
                "description": "(내용 없음)",
                "input": "입력 설명",
                "output": "",
            }
        )
        self.assertEqual(missing, ["description", "output"])

    def test_extract_sample_pairs_without_consecutive_div_indexes(self):
        document = html.fromstring(
            """
            <div id="problem-content">
              <p>문제 설명</p>
              <p>설명 본문입니다.</p>
              <div class="notice">중간 안내 블록</div>
              <div class="sample-one">
                <div><div><pre>1 2</pre></div><div><pre>3</pre></div></div>
              </div>
              <div class="ad-banner">광고 자리</div>
              <div class="sample-two">
                <div><div><pre>4 5</pre></div><div><pre>9</pre></div></div>
              </div>
              <p>힌트</p>
              <div><div><div><div>힌트 본문</div></div></div></div>
            </div>
            """
        )

        content_root = _find_doingcoding_content_root(document)
        self.assertEqual(
            _extract_sample_pairs(content_root),
            [("1 2", "3"), ("4 5", "9")],
        )

    def test_pick_best_code_prefers_complete_multiline_source(self):
        code = _pick_best_code(
            [
                "print('short')",
                "for i in range(3):\n    print(i)",
                "",
            ]
        )
        self.assertEqual(code, "for i in range(3):\n    print(i)")

    def test_goto_with_retries_retries_until_selector_is_ready(self):
        class FakeResponse:
            status = 200

        class FakePage:
            def __init__(self):
                self.goto_calls = 0
                self.wait_calls = 0
                self.timeout_calls = []

            def goto(self, url, wait_until, timeout):
                self.goto_calls += 1
                return FakeResponse()

            def wait_for_selector(self, selector, timeout):
                self.wait_calls += 1
                if self.wait_calls < 2:
                    raise RuntimeError(f"{selector} not ready")

            def wait_for_timeout(self, ms):
                self.timeout_calls.append(ms)

        page = FakePage()
        response = _goto_with_retries(page, "http://example.com", ready_selector="#ready", attempts=3)

        self.assertEqual(response.status, 200)
        self.assertEqual(page.goto_calls, 2)
        self.assertEqual(page.timeout_calls, [500])

    def test_parse_testcase_bundle_uses_info_mapping(self):
        temp_dir = CURRENT_DIR / "_tmp_bundle_test"
        temp_dir.mkdir(exist_ok=True)
        try:
            bundle_path = temp_dir / "cases.zip"
            extract_dir = temp_dir / "extract"
            with zipfile.ZipFile(bundle_path, "w") as archive:
                archive.writestr(
                    "info",
                    json.dumps(
                        {
                            "spj": False,
                            "test_cases": {
                                "1": {
                                    "input_name": "1.in",
                                    "output_name": "1.out",
                                    "input_size": 4,
                                    "output_size": 2,
                                }
                            },
                        },
                        ensure_ascii=False,
                    ),
                )
                archive.writestr("1.in", "1 2\n")
                archive.writestr("1.out", "3\n")

            bundle = parse_testcase_bundle(str(bundle_path), str(extract_dir))

            self.assertEqual(bundle["info"]["test_cases"]["1"]["input_name"], "1.in")
            self.assertEqual(bundle["cases"][0]["input_text"], "1 2\n")
            self.assertEqual(bundle["cases"][0]["output_text"], "3\n")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_render_testcases_md_includes_metadata_and_cases(self):
        markdown = render_testcases_md(
            {
                "info": {"spj": False, "test_cases": {"1": {"input_name": "1.in", "output_name": "1.out"}}},
                "cases": [
                    {
                        "id": "1",
                        "input_name": "1.in",
                        "output_name": "1.out",
                        "input_text": "1 2\n",
                        "output_text": "3\n",
                        "meta": {},
                    }
                ],
            }
        )

        self.assertIn("## 5. 채점용 테스트케이스", markdown)
        self.assertIn('"input_name": "1.in"', markdown)
        self.assertIn("### 테스트케이스 1 입력", markdown)
        self.assertIn("### 테스트케이스 1 출력", markdown)

    def test_render_templates_md_uses_requested_section_number(self):
        markdown = render_templates_md({"Python3": "print(1)\n"}, section_number=6)

        self.assertIn("## 6. 코드 템플릿", markdown)
        self.assertIn("```python", markdown)


    def test_login_doingcoding_admin_fills_credentials_and_waits_for_problem_page(self):
        class FakeLocator:
            def __init__(self, page, selector):
                self.page = page
                self.selector = selector

            @property
            def first(self):
                return self

            def click(self, force=False):
                self.page.locator_clicks.append((self.selector, force))

            def fill(self, value):
                self.page.locator_fills.append((self.selector, value))

            def press(self, key):
                self.page.locator_presses.append((self.selector, key))
                raise RuntimeError("locator enter failed")

            def evaluate(self, script):
                self.page.locator_evaluates.append((self.selector, script))

        class FakePage:
            def __init__(self):
                self.locator_fills = []
                self.locator_presses = []
                self.locator_clicks = []
                self.waited = []
                self.goto_args = []
                self.timeout_calls = []
                self.function_calls = []
                self.load_states = []
                self.locator_evaluates = []
                self.url = DOINGCODING_ADMIN_LOGIN_URL
                self.context = type(
                    "FakeContext",
                    (),
                    {
                        "cookies": lambda self_inner: [
                            {"name": "csrftoken", "value": "token", "domain": "edu.doingcoding.com", "path": "/admin"}
                        ]
                    },
                )()

            def goto(self, url, wait_until, timeout):
                self.goto_args.append((url, wait_until, timeout))
                return None

            def wait_for_selector(self, selector, timeout, state="visible"):
                self.waited.append((selector, timeout, state))
                if selector == DOINGCODING_ADMIN_ID_SELECTOR:
                    self.url = DOINGCODING_ADMIN_LOGIN_URL

            def wait_for_function(self, script, timeout):
                self.function_calls.append((script, timeout))

            def wait_for_load_state(self, state):
                self.load_states.append(state)

            def wait_for_timeout(self, ms):
                self.timeout_calls.append(ms)

            def locator(self, selector):
                return FakeLocator(self, selector)

            @property
            def keyboard(self):
                class Keyboard:
                    def press(self_inner, key):
                        raise AssertionError("keyboard fallback should not be used in this test")

                return Keyboard()

        page = FakePage()
        logs = []
        with patch("practice.data.language_v2.crawl.ensure_doingcoding_admin_csrf", return_value="token") as ensure_mock:
            login_doingcoding_admin(page, "admin_id", "admin_pw", logger=logs.append)

        self.assertEqual(page.locator_fills, [(DOINGCODING_ADMIN_ID_SELECTOR, "admin_id"), (DOINGCODING_ADMIN_PASSWORD_SELECTOR, "admin_pw")])
        self.assertEqual(page.locator_presses, [(DOINGCODING_ADMIN_PASSWORD_SELECTOR, "Enter")])
        self.assertEqual(
            page.locator_clicks[:2],
            [(DOINGCODING_ADMIN_ID_SELECTOR, False), (DOINGCODING_ADMIN_PASSWORD_SELECTOR, False)],
        )
        self.assertEqual(page.goto_args[0][0], DOINGCODING_ADMIN_LOGIN_URL)
        self.assertEqual(page.goto_args[1][0], DOINGCODING_ADMIN_PROBLEMS_URL)
        self.assertEqual(page.load_states, ["domcontentloaded"])
        self.assertEqual(page.timeout_calls, [1000])
        self.assertEqual(len(page.function_calls), 1)
        self.assertEqual(
            page.waited[:2],
            [
                (DOINGCODING_ADMIN_ID_SELECTOR, 10000, "visible"),
                (DOINGCODING_ADMIN_PASSWORD_SELECTOR, 10000, "attached"),
            ],
        )
        self.assertIn(page.waited[-1][0], DOINGCODING_ADMIN_SEARCH_SELECTORS)
        self.assertIn("[관리자 로그인] csrf 확보 후 /admin/login 재진입", logs)
        self.assertIn("[관리자 로그인] 로그인 폼 확인 완료", logs)
        self.assertIn("[관리자 로그인] 제출 전 상태: url=http://edu.doingcoding.com/admin/login, csrftoken=있음, cookies=1", logs)
        ensure_mock.assert_called_once_with(page, logger=logs.append)

    def test_login_doingcoding_admin_reenters_login_page_after_csrf_seed_page(self):
        class FakeLocator:
            def __init__(self, page, selector):
                self.page = page
                self.selector = selector

            @property
            def first(self):
                return self

            def click(self, force=False):
                self.page.locator_clicks.append((self.selector, force))

            def fill(self, value):
                self.page.locator_fills.append((self.selector, value))

            def press(self, key):
                self.page.locator_presses.append((self.selector, key))
                raise RuntimeError("locator enter failed")

            def evaluate(self, script):
                self.page.locator_evaluates.append((self.selector, script))

        class FakePage:
            def __init__(self):
                self.locator_clicks = []
                self.locator_fills = []
                self.locator_presses = []
                self.locator_evaluates = []
                self.goto_args = []
                self.waited = []
                self.function_calls = []
                self.load_states = []
                self.timeout_calls = []
                self.url = DOINGCODING_CSRF_SEED_URL
                self.context = type(
                    "FakeContext",
                    (),
                    {
                        "cookies": lambda self_inner: [
                            {"name": "csrftoken", "value": "token", "domain": "edu.doingcoding.com", "path": "/admin"}
                        ]
                    },
                )()

            def goto(self, url, wait_until, timeout):
                self.goto_args.append((url, wait_until, timeout))
                self.url = url
                return None

            def wait_for_selector(self, selector, timeout, state="visible"):
                self.waited.append((selector, timeout, state))
                if selector == DOINGCODING_ADMIN_ID_SELECTOR:
                    self.url = DOINGCODING_ADMIN_LOGIN_URL

            def wait_for_function(self, script, timeout):
                self.function_calls.append((script, timeout))

            def wait_for_load_state(self, state):
                self.load_states.append(state)

            def wait_for_timeout(self, ms):
                self.timeout_calls.append(ms)

            def locator(self, selector):
                return FakeLocator(self, selector)

            @property
            def keyboard(self):
                class Keyboard:
                    def press(self_inner, key):
                        raise AssertionError("keyboard fallback should not be used in this test")

                return Keyboard()

        page = FakePage()
        with patch("practice.data.language_v2.crawl.ensure_doingcoding_admin_csrf", return_value="token"):
            login_doingcoding_admin(page, "admin_id", "admin_pw")

        self.assertEqual(page.goto_args[0][0], DOINGCODING_ADMIN_LOGIN_URL)
        self.assertEqual(page.waited[0], (DOINGCODING_ADMIN_ID_SELECTOR, 10000, "visible"))
        self.assertEqual(page.waited[1], (DOINGCODING_ADMIN_PASSWORD_SELECTOR, 10000, "attached"))
        self.assertEqual(page.locator_fills[:2], [(DOINGCODING_ADMIN_ID_SELECTOR, "admin_id"), (DOINGCODING_ADMIN_PASSWORD_SELECTOR, "admin_pw")])

    def test_login_doingcoding_admin_clicks_button_when_enter_does_not_finish_login(self):
        class FakeLocator:
            def __init__(self, page, selector):
                self.page = page
                self.selector = selector

            @property
            def first(self):
                return self

            def click(self, force=False):
                self.page.locator_clicks.append((self.selector, force))

            def fill(self, value):
                self.page.locator_fills.append((self.selector, value))

            def press(self, key):
                self.page.locator_presses.append((self.selector, key))
                if self.selector == DOINGCODING_ADMIN_PASSWORD_SELECTOR:
                    self.page.password_enter_attempted = True

            def evaluate(self, script):
                self.page.locator_evaluates.append((self.selector, script))
                if self.selector == DOINGCODING_ADMIN_PASSWORD_SELECTOR:
                    raise RuntimeError("requestSubmit failed")

        class FakePage:
            def __init__(self):
                self.locator_fills = []
                self.locator_presses = []
                self.locator_clicks = []
                self.locator_evaluates = []
                self.goto_args = []
                self.function_calls = 0
                self.load_states = []
                self.keyboard_presses = []
                self.password_enter_attempted = False
                self.url = DOINGCODING_ADMIN_LOGIN_URL
                self.context = type(
                    "FakeContext",
                    (),
                    {
                        "cookies": lambda self_inner: [
                            {"name": "csrftoken", "value": "token", "domain": "edu.doingcoding.com", "path": "/admin"}
                        ]
                    },
                )()

            def goto(self, url, wait_until, timeout):
                self.goto_args.append((url, wait_until, timeout))
                return None

            def wait_for_selector(self, selector, timeout, state="visible"):
                if selector == DOINGCODING_ADMIN_ID_SELECTOR:
                    self.url = DOINGCODING_ADMIN_LOGIN_URL
                return None

            def wait_for_function(self, script, timeout):
                self.function_calls += 1
                if self.function_calls == 1:
                    raise RuntimeError("still on login")

            def wait_for_load_state(self, state):
                self.load_states.append(state)

            def wait_for_timeout(self, _ms):
                return None

            def locator(self, selector):
                return FakeLocator(self, selector)

            @property
            def keyboard(self):
                page = self

                class Keyboard:
                    def press(self_inner, key):
                        page.keyboard_presses.append(key)

                return Keyboard()

        page = FakePage()
        with patch("practice.data.language_v2.crawl.ensure_doingcoding_admin_csrf", return_value="token"):
            login_doingcoding_admin(page, "admin_id", "admin_pw")

        self.assertEqual(page.goto_args[0][0], DOINGCODING_ADMIN_LOGIN_URL)
        self.assertEqual(page.locator_presses, [(DOINGCODING_ADMIN_PASSWORD_SELECTOR, "Enter")])
        self.assertEqual(page.keyboard_presses, ["Enter"])
        self.assertNotIn((DOINGCODING_ADMIN_LOGIN_BUTTON_SELECTOR, True), page.locator_clicks)
        self.assertEqual(page.function_calls, 2)

    def test_attempt_admin_login_submit_uses_force_click_after_enter_and_keyboard_fail(self):
        class FakeLocator:
            def __init__(self, page, selector):
                self.page = page
                self.selector = selector

            @property
            def first(self):
                return self

            def click(self, force=False):
                self.page.locator_clicks.append((self.selector, force))
                if self.selector == 'button:has-text("GO")':
                    return None

            def press(self, key):
                self.page.locator_presses.append((self.selector, key))
                raise RuntimeError("locator enter failed")

            def evaluate(self, script):
                self.page.locator_evaluates.append((self.selector, script))
                if self.selector == DOINGCODING_ADMIN_PASSWORD_SELECTOR:
                    raise RuntimeError("requestSubmit failed")

        class FakePage:
            def __init__(self):
                self.locator_clicks = []
                self.locator_presses = []
                self.locator_evaluates = []
                self.keyboard_presses = []
                self.function_calls = 0

            def locator(self, selector):
                return FakeLocator(self, selector)

            @property
            def keyboard(self):
                page = self

                class Keyboard:
                    def press(self_inner, key):
                        page.keyboard_presses.append(key)

                return Keyboard()

            def wait_for_function(self, script, timeout):
                self.function_calls += 1
                if self.function_calls < 3:
                    raise RuntimeError("login still pending")

        page = FakePage()
        _attempt_admin_login_submit(page)

        self.assertEqual(page.locator_presses, [(DOINGCODING_ADMIN_PASSWORD_SELECTOR, "Enter")])
        self.assertEqual(page.keyboard_presses, ["Enter"])
        self.assertIn(('button:has-text("GO")', True), page.locator_clicks)

    def test_attempt_admin_login_submit_handles_request_submit_failure(self):
        class FakeLocator:
            def __init__(self, page, selector):
                self.page = page
                self.selector = selector

            @property
            def first(self):
                return self

            def click(self, force=False):
                self.page.locator_clicks.append((self.selector, force))
                if self.selector != DOINGCODING_ADMIN_PASSWORD_SELECTOR:
                    raise RuntimeError("click failed")

            def press(self, key):
                self.page.locator_presses.append((self.selector, key))

            def evaluate(self, script):
                self.page.locator_evaluates.append((self.selector, script))
                if self.selector == DOINGCODING_ADMIN_PASSWORD_SELECTOR:
                    raise RuntimeError("requestSubmit failed")

        class FakePage:
            def __init__(self):
                self.locator_clicks = []
                self.locator_presses = []
                self.locator_evaluates = []
                self.keyboard_presses = []
                self.function_calls = 0

            def locator(self, selector):
                return FakeLocator(self, selector)

            @property
            def keyboard(self):
                page = self

                class Keyboard:
                    def press(self_inner, key):
                        page.keyboard_presses.append(key)
                        raise RuntimeError("keyboard enter failed")

                return Keyboard()

            def wait_for_function(self, script, timeout):
                self.function_calls += 1
                return None

        page = FakePage()
        _attempt_admin_login_submit(page)

        self.assertEqual(page.locator_presses, [(DOINGCODING_ADMIN_PASSWORD_SELECTOR, "Enter")])
        self.assertGreaterEqual(len(page.locator_clicks), 1)

    def test_login_doingcoding_admin_raises_with_cookie_diagnostics_on_failure(self):
        class FakeLocator:
            def __init__(self, page, selector):
                self.page = page
                self.selector = selector

            @property
            def first(self):
                return self

            def click(self, force=False):
                self.page.locator_clicks.append((self.selector, force))

            def fill(self, value):
                self.page.locator_fills.append((self.selector, value))

        class FakeContext:
            def cookies(self):
                return [{"name": "csrftoken", "value": "token", "domain": "edu.doingcoding.com", "path": "/admin"}]

        class FakePage:
            def __init__(self):
                self.locator_clicks = []
                self.locator_fills = []
                self.context = FakeContext()
                self.url = DOINGCODING_ADMIN_LOGIN_URL

            def goto(self, url, wait_until, timeout):
                self.url = url
                return None

            def wait_for_selector(self, selector, timeout, state="visible"):
                if selector == DOINGCODING_ADMIN_ID_SELECTOR:
                    self.url = DOINGCODING_ADMIN_LOGIN_URL
                return None

            def wait_for_timeout(self, _ms):
                return None

            def locator(self, selector):
                return FakeLocator(self, selector)

        logs = []
        page = FakePage()
        with patch("practice.data.language_v2.crawl.ensure_doingcoding_admin_csrf", return_value="token"), \
            patch("practice.data.language_v2.crawl._attempt_admin_login_submit", side_effect=RuntimeError("submit failed")), \
            patch("practice.data.language_v2.crawl.attempt_admin_login_via_request", return_value=False) as request_mock:
            with self.assertRaises(RuntimeError) as raised:
                login_doingcoding_admin(page, "admin_id", "admin_pw", logger=logs.append)

        self.assertIn("CSRF cookie/token mismatch 가능성", str(raised.exception))
        self.assertIn("[관리자 로그인] 최종 실패: url=http://edu.doingcoding.com/admin/login, csrftoken=있음, sessionid=없음", logs)
        request_mock.assert_called_once()
    def test_download_doingcoding_testcases_saves_zip_after_row_match(self):
        class FakeDownload:
            suggested_filename = "P101v0701.zip"

            def __init__(self):
                self.saved_path = None

            def save_as(self, path):
                self.saved_path = path

        class FakeDownloadContext:
            def __init__(self, download):
                self.value = download

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

        class FakePage:
            def __init__(self):
                self.download = FakeDownload()
                self.fills = []
                self.presses = []
                self.clicks = []
                self.waited = []
                self.failed_selectors = {
                    DOINGCODING_ADMIN_SEARCH_SELECTORS[0],
                    DOINGCODING_ADMIN_ROW_SELECTORS[0],
                    DOINGCODING_ADMIN_DOWNLOAD_BUTTON_SELECTORS[0],
                }

            def wait_for_selector(self, selector, timeout, state="visible"):
                self.waited.append((selector, timeout, state))
                if selector in self.failed_selectors:
                    raise RuntimeError(f"{selector} missing")

            def wait_for_timeout(self, _ms):
                return None

            def fill(self, selector, value):
                self.fills.append((selector, value))

            def press(self, selector, key):
                self.presses.append((selector, key))

            def text_content(self, selector):
                if selector in DOINGCODING_ADMIN_ROW_SELECTORS:
                    return "P101v0701 문제 행"
                return ""

            def expect_download(self):
                return FakeDownloadContext(self.download)

            def click(self, selector):
                self.clicks.append(selector)

        temp_dir = CURRENT_DIR / "_tmp_admin_download_test"
        temp_dir.mkdir(exist_ok=True)
        try:
            page = FakePage()
            download_path = download_doingcoding_testcases(page, "P101v0701", str(temp_dir))

            self.assertEqual(page.fills, [(DOINGCODING_ADMIN_SEARCH_SELECTORS[1], "P101v0701")])
            self.assertEqual(page.presses, [(DOINGCODING_ADMIN_SEARCH_SELECTORS[1], "Enter")])
            self.assertEqual(page.clicks, [DOINGCODING_ADMIN_DOWNLOAD_BUTTON_SELECTORS[1]])
            self.assertTrue(download_path.endswith("P101v0701.zip"))
            self.assertTrue(page.download.saved_path.endswith("P101v0701.zip"))
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_open_doingcoding_problem_editor_searches_row_and_clicks_edit(self):
        class FakePage:
            def __init__(self):
                self.fills = []
                self.presses = []
                self.clicks = []
                self.waited = []
                self.failed_selectors = {
                    DOINGCODING_ADMIN_SEARCH_SELECTORS[0],
                    DOINGCODING_ADMIN_ROW_SELECTORS[0],
                    DOINGCODING_ADMIN_EDIT_BUTTON_SELECTORS[0],
                    DOINGCODING_ADMIN_TESTCASE_UPLOAD_BUTTON_SELECTORS[0],
                    DOINGCODING_ADMIN_TESTCASE_SAVE_BUTTON_SELECTORS[0],
                }

            def wait_for_selector(self, selector, timeout, state="visible"):
                self.waited.append((selector, timeout, state))
                if selector in self.failed_selectors:
                    raise RuntimeError(f"{selector} missing")

            def wait_for_timeout(self, _ms):
                return None

            def fill(self, selector, value):
                self.fills.append((selector, value))

            def press(self, selector, key):
                self.presses.append((selector, key))

            def text_content(self, selector):
                if selector in DOINGCODING_ADMIN_ROW_SELECTORS:
                    return "P101v0701 문제 행"
                return ""

            def click(self, selector):
                self.clicks.append(selector)

        page = FakePage()
        logs = []

        open_doingcoding_problem_editor(page, "P101v0701", logger=logs.append)

        self.assertEqual(page.fills, [(DOINGCODING_ADMIN_SEARCH_SELECTORS[1], "P101v0701")])
        self.assertEqual(page.presses, [(DOINGCODING_ADMIN_SEARCH_SELECTORS[1], "Enter")])
        self.assertEqual(page.clicks, [DOINGCODING_ADMIN_EDIT_BUTTON_SELECTORS[1]])
        self.assertEqual(
            logs,
            [
                "[관리자 업로드] 문제 검색: P101v0701",
                "[관리자 업로드] 문제 수정 화면 진입: P101v0701",
            ],
        )

    def test_upload_doingcoding_testcases_uses_file_chooser_then_saves(self):
        zip_path = CURRENT_DIR / "_tmp_upload_case.zip"
        zip_path.write_text("zip", encoding="utf-8")
        try:
            class FakeChooser:
                def __init__(self):
                    self.path = None

                def set_files(self, path):
                    self.path = path

            class FakeChooserContext:
                def __init__(self, chooser):
                    self.value = chooser

                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc, tb):
                    return False

            class FakePage:
                def __init__(self):
                    self.url = "http://edu.doingcoding.com/admin/problems"
                    self.chooser = FakeChooser()
                    self.fills = []
                    self.presses = []
                    self.clicks = []
                    self.waited = []
                    self.failed_selectors = {
                        DOINGCODING_ADMIN_SEARCH_SELECTORS[0],
                        DOINGCODING_ADMIN_ROW_SELECTORS[0],
                        DOINGCODING_ADMIN_EDIT_BUTTON_SELECTORS[0],
                        DOINGCODING_ADMIN_TESTCASE_UPLOAD_BUTTON_SELECTORS[0],
                        DOINGCODING_ADMIN_TESTCASE_SAVE_BUTTON_SELECTORS[0],
                    }

                def wait_for_selector(self, selector, timeout, state="visible"):
                    self.waited.append((selector, timeout, state))
                    if selector in self.failed_selectors:
                        raise RuntimeError(f"{selector} missing")

                def wait_for_timeout(self, _ms):
                    return None

                def fill(self, selector, value):
                    self.fills.append((selector, value))

                def press(self, selector, key):
                    self.presses.append((selector, key))

                def text_content(self, selector):
                    if selector in DOINGCODING_ADMIN_ROW_SELECTORS:
                        return "P101v0701 문제 행"
                    if selector == "body":
                        return "저장 성공"
                    return ""

                def click(self, selector):
                    self.clicks.append(selector)

                def expect_file_chooser(self, timeout):
                    self.expect_timeout = timeout
                    return FakeChooserContext(self.chooser)

                def wait_for_function(self, _script, timeout):
                    self.wait_function_timeout = timeout
                    return None

            page = FakePage()
            logs = []

            result = upload_doingcoding_testcases(
                page,
                "P101v0701",
                str(zip_path),
                logger=logs.append,
            )

            self.assertEqual(result["status"], "uploaded")
            self.assertEqual(page.chooser.path, str(zip_path))
            self.assertEqual(
                page.clicks,
                [
                    DOINGCODING_ADMIN_EDIT_BUTTON_SELECTORS[1],
                    DOINGCODING_ADMIN_TESTCASE_UPLOAD_BUTTON_SELECTORS[1],
                    DOINGCODING_ADMIN_TESTCASE_SAVE_BUTTON_SELECTORS[1],
                ],
            )
            self.assertIn("[관리자 업로드] ZIP 입력 방식: filechooser", logs)
            self.assertEqual(result["problem_id"], "P101v0701")
        finally:
            zip_path.unlink(missing_ok=True)

    def test_upload_doingcoding_testcases_falls_back_to_input_file(self):
        zip_path = CURRENT_DIR / "_tmp_upload_case.zip"
        zip_path.write_text("zip", encoding="utf-8")
        try:
            class FakeLocator:
                def __init__(self):
                    self.first = self
                    self.path = None

                def set_input_files(self, path):
                    self.path = path

            class FakePage:
                def __init__(self):
                    self.url = "http://edu.doingcoding.com/admin/problems"
                    self.file_locator = FakeLocator()
                    self.clicks = []
                    self.fills = []
                    self.presses = []
                    self.waited = []
                    self.failed_selectors = {
                        DOINGCODING_ADMIN_SEARCH_SELECTORS[0],
                        DOINGCODING_ADMIN_ROW_SELECTORS[0],
                        DOINGCODING_ADMIN_EDIT_BUTTON_SELECTORS[0],
                        DOINGCODING_ADMIN_TESTCASE_UPLOAD_BUTTON_SELECTORS[0],
                        DOINGCODING_ADMIN_TESTCASE_SAVE_BUTTON_SELECTORS[0],
                    }

                def wait_for_selector(self, selector, timeout, state="visible"):
                    self.waited.append((selector, timeout, state))
                    if selector in self.failed_selectors:
                        raise RuntimeError(f"{selector} missing")

                def wait_for_timeout(self, _ms):
                    return None

                def fill(self, selector, value):
                    self.fills.append((selector, value))

                def press(self, selector, key):
                    self.presses.append((selector, key))

                def text_content(self, selector):
                    if selector in DOINGCODING_ADMIN_ROW_SELECTORS:
                        return "P101v0701 문제 행"
                    if selector == "body":
                        return "저장 성공"
                    return ""

                def click(self, selector):
                    self.clicks.append(selector)

                def expect_file_chooser(self, timeout):
                    raise RuntimeError(f"no chooser {timeout}")

                def locator(self, selector):
                    if selector == DOINGCODING_ADMIN_TESTCASE_FILE_INPUT_SELECTORS[0]:
                        return self.file_locator
                    raise RuntimeError("unexpected locator")

                def wait_for_function(self, _script, timeout):
                    self.wait_function_timeout = timeout
                    return None

            page = FakePage()

            upload_doingcoding_testcases(page, "P101v0701", str(zip_path))

            self.assertEqual(page.file_locator.path, str(zip_path))
            self.assertEqual(
                page.clicks,
                [
                    DOINGCODING_ADMIN_EDIT_BUTTON_SELECTORS[1],
                    DOINGCODING_ADMIN_TESTCASE_UPLOAD_BUTTON_SELECTORS[1],
                    DOINGCODING_ADMIN_TESTCASE_SAVE_BUTTON_SELECTORS[1],
                ],
            )
        finally:
            zip_path.unlink(missing_ok=True)

    def test_upload_doingcoding_testcases_with_session_relogs_once_after_failure(self):
        session = DoingCodingAdminSession(context=object(), page="shared-page", username="admin", password="secret")
        logs = []
        with patch(
            "practice.data.language_v2.crawl.upload_doingcoding_testcases",
            side_effect=[RuntimeError("expired"), {"status": "uploaded"}],
        ) as upload_mock, patch("practice.data.language_v2.crawl.login_doingcoding_admin") as login_mock:
            result = upload_doingcoding_testcases_with_session(
                session, "P101v0701", "bundle.zip", logger=logs.append
            )

        self.assertEqual(result, {"status": "uploaded"})
        self.assertEqual(upload_mock.call_count, 2)
        login_mock.assert_called_once_with("shared-page", "admin", "secret", logger=logs.append)
        self.assertEqual(
            logs,
            [
                "[관리자 세션] 기존 로그인 세션 재사용",
                "[관리자 세션] 세션 재로그인 시도",
            ],
        )

    def test_find_first_working_selector_falls_back_to_next_candidate(self):
        class FakePage:
            def wait_for_selector(self, selector, timeout, state="visible"):
                if selector == "bad":
                    raise RuntimeError("bad selector")
                return None

        selector = _find_first_working_selector(FakePage(), ["bad", "good"], timeout=1000, require_visible=False)
        self.assertEqual(selector, "good")

    def test_open_doingcoding_admin_session_logs_in_once_and_returns_session(self):
        class FakeContext:
            def __init__(self):
                self.page = object()
                self.closed = False

            def new_page(self):
                return self.page

            def close(self):
                self.closed = True

        class FakeBrowser:
            def __init__(self):
                self.context = FakeContext()

            def new_context(self, accept_downloads):
                self.accept_downloads = accept_downloads
                return self.context

        logs = []
        browser = FakeBrowser()
        with patch("practice.data.language_v2.crawl.login_doingcoding_admin") as login_mock:
            session = open_doingcoding_admin_session(browser, "admin", "secret", logger=logs.append)

        self.assertIsInstance(session, DoingCodingAdminSession)
        self.assertTrue(browser.accept_downloads)
        self.assertIs(session.page, browser.context.page)
        login_mock.assert_called_once_with(browser.context.page, "admin", "secret", logger=logs.append)
        self.assertEqual(logs[:2], ["[관리자 세션] 초기화 시작", "[관리자 세션] 로그인 완료, 이후 문제에 재사용"])

    def test_close_doingcoding_admin_session_closes_context_once(self):
        class FakeContext:
            def __init__(self):
                self.closed = False

            def close(self):
                self.closed = True

        session = DoingCodingAdminSession(FakeContext(), object(), "admin", "secret")
        close_doingcoding_admin_session(session)
        self.assertTrue(session.context.closed)

    def test_collect_doingcoding_testcases_with_session_reuses_existing_page(self):
        session = DoingCodingAdminSession(context=object(), page="shared-page", username="admin", password="secret")
        logs = []
        with patch("practice.data.language_v2.crawl.download_doingcoding_testcases", return_value="bundle.zip") as download_mock:
            bundle_path = collect_doingcoding_testcases_with_session(session, "P101v0701", str(CURRENT_DIR), logger=logs.append)

        self.assertEqual(bundle_path, "bundle.zip")
        download_mock.assert_called_once_with("shared-page", "P101v0701", str(CURRENT_DIR))
        self.assertEqual(logs, ["[관리자 세션] 기존 로그인 세션 재사용"])

    def test_collect_doingcoding_testcases_with_session_relogs_once_after_download_failure(self):
        session = DoingCodingAdminSession(context=object(), page="shared-page", username="admin", password="secret")
        logs = []
        with patch(
            "practice.data.language_v2.crawl.download_doingcoding_testcases",
            side_effect=[RuntimeError("expired"), "bundle.zip"],
        ) as download_mock, patch("practice.data.language_v2.crawl.login_doingcoding_admin") as login_mock:
            bundle_path = collect_doingcoding_testcases_with_session(session, "P101v0701", str(CURRENT_DIR), logger=logs.append)

        self.assertEqual(bundle_path, "bundle.zip")
        self.assertEqual(download_mock.call_count, 2)
        login_mock.assert_called_once_with("shared-page", "admin", "secret", logger=logs.append)
        self.assertEqual(
            logs,
            [
                "[관리자 세션] 기존 로그인 세션 재사용",
                "[관리자 세션] 세션 재로그인 시도",
            ],
        )

    def test_collect_doingcoding_testcases_logs_in_downloads_and_parses_bundle(self):
        class FakePage:
            pass

        class FakeContext:
            def __init__(self):
                self.page = FakePage()
                self.closed = False

            def new_page(self):
                return self.page

            def close(self):
                self.closed = True

        class FakeBrowser:
            def __init__(self):
                self.context = FakeContext()

            def new_context(self, accept_downloads):
                self.accept_downloads = accept_downloads
                return self.context

        temp_dir = CURRENT_DIR / "_tmp_collect_testcases"
        temp_dir.mkdir(exist_ok=True)
        try:
            browser = FakeBrowser()
            with patch("practice.data.language_v2.crawl.open_doingcoding_admin_session") as open_mock, \
                patch("practice.data.language_v2.crawl.collect_doingcoding_testcases_with_session", return_value=str(temp_dir / "bundle.zip")) as collect_mock, \
                patch("practice.data.language_v2.crawl.close_doingcoding_admin_session") as close_mock, \
                patch("practice.data.language_v2.crawl.parse_testcase_bundle", return_value={"info": {"spj": False}, "cases": [{"id": "1"}]}) as parse_mock:
                open_mock.return_value = DoingCodingAdminSession(browser.context, browser.context.page, "admin", "secret")
                bundle = collect_doingcoding_testcases(
                    browser,
                    "P101v0701",
                    "admin",
                    "secret",
                    base_download_dir=str(temp_dir),
                )

            self.assertEqual(bundle, {"info": {"spj": False}, "cases": [{"id": "1"}]})
            open_mock.assert_called_once()
            collect_mock.assert_called_once()
            close_mock.assert_called_once()
            parse_mock.assert_called_once()
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_scrape_doingcoding_does_not_collect_testcases_when_option_is_disabled(self):
        class FakeLocator:
            def __init__(self, selector):
                self.selector = selector

            @property
            def first(self):
                return self

            def wait_for(self, timeout=None):
                raise RuntimeError("not found")

            def inner_text(self):
                return ""

            def count(self):
                return 0

        class FakePage:
            def goto(self, url, wait_until, timeout):
                return type("Response", (), {"status": 200})()

            def wait_for_selector(self, selector, timeout=None):
                return None

            def wait_for_timeout(self, _ms):
                return None

            def content(self):
                return """
                <div>
                  <div id="problem-main"><div><div class="title">문제 제목</div></div></div>
                  <div id="problem-content">
                    <p>문제 설명</p>
                    <p>문제 본문 설명</p>
                    <p>입력</p>
                    <p>입력 설명</p>
                    <p>출력</p>
                    <p>출력 설명</p>
                  </div>
                </div>
                """

            def locator(self, selector):
                return FakeLocator(selector)

        class FakeBrowser:
            def new_page(self):
                return FakePage()

            def close(self):
                return None

        class FakePlaywright:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            class chromium:
                @staticmethod
                def launch(headless=True):
                    return FakeBrowser()

        with patch("practice.data.language_v2.crawl.sync_playwright", return_value=FakePlaywright()), \
            patch("practice.data.language_v2.crawl.collect_doingcoding_testcases") as collect_mock:
            title, markdown = __import__("practice.data.language_v2.crawl", fromlist=["scrape_doingcoding"]).scrape_doingcoding(
                "http://edu.doingcoding.com/problem/P101v0701",
                get_testcases=False,
            )

        self.assertEqual(title, "문제 제목")
        self.assertIn("문제 제목", markdown)
        collect_mock.assert_not_called()

    def test_scrape_doingcoding_collects_testcases_when_option_is_enabled(self):
        class FakeLocator:
            def __init__(self, selector):
                self.selector = selector

            @property
            def first(self):
                return self

            def wait_for(self, timeout=None):
                raise RuntimeError("not found")

            def inner_text(self):
                return ""

            def count(self):
                return 0

        class FakePage:
            def goto(self, url, wait_until, timeout):
                return type("Response", (), {"status": 200})()

            def wait_for_selector(self, selector, timeout=None):
                return None

            def wait_for_timeout(self, _ms):
                return None

            def content(self):
                return """
                <div>
                  <div id="problem-main"><div><div class="title">문제 제목</div></div></div>
                  <div id="problem-content">
                    <p>문제 설명</p>
                    <p>문제 본문 설명</p>
                    <p>입력</p>
                    <p>입력 설명</p>
                    <p>출력</p>
                    <p>출력 설명</p>
                  </div>
                </div>
                """

            def locator(self, selector):
                return FakeLocator(selector)

        class FakeBrowser:
            def new_page(self):
                return FakePage()

            def close(self):
                return None

        class FakePlaywright:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            class chromium:
                @staticmethod
                def launch(headless=True):
                    return FakeBrowser()

        with patch("practice.data.language_v2.crawl.sync_playwright", return_value=FakePlaywright()), \
            patch(
                "practice.data.language_v2.crawl.collect_doingcoding_testcases",
                return_value={"info": {}, "cases": [{"id": "1", "input_text": "1\n", "output_text": "2\n", "input_name": "1.in", "output_name": "1.out", "meta": {}}]},
            ) as collect_mock:
            title, markdown = __import__("practice.data.language_v2.crawl", fromlist=["scrape_doingcoding"]).scrape_doingcoding(
                "http://edu.doingcoding.com/problem/P101v0701",
                get_testcases=True,
                admin_username="admin",
                admin_password="secret",
            )

        self.assertEqual(title, "문제 제목")
        self.assertIn("채점용 테스트케이스", markdown)
        collect_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
