import unittest

from practice.data.language_v2.crawl import (
    _extract_section_after_heading,
    _extract_sample_pairs,
    _goto_with_retries,
    _find_doingcoding_content_root,
    _find_doingcoding_title,
    _missing_required_fields,
    _pick_best_code,
    SECTION_HEADINGS,
)
from lxml import html


class DoingCodingStage1ParsingTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
