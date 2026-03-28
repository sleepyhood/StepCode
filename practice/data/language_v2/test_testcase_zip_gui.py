import shutil
import sys
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from gui_crawler import CrawlerApp
from testcase_zip_export import (
    build_default_zip_name,
    build_testcase_preview,
    export_testcases_to_zip,
    parse_testcases_from_markdown,
)

REFERENCE_MD = CURRENT_DIR / "lv03_input" / "_docs" / "reference" / "01_dc_P101v0301.md"


class FakeVar:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class FakeButton:
    def __init__(self):
        self.state = None

    def config(self, **kwargs):
        if "state" in kwargs:
            self.state = kwargs["state"]


class FakeLabel:
    def __init__(self):
        self.text = ""

    def config(self, **kwargs):
        if "text" in kwargs:
            self.text = kwargs["text"]


class FakeText:
    def __init__(self):
        self.value = ""
        self.state = "disabled"

    def config(self, **kwargs):
        if "state" in kwargs:
            self.state = kwargs["state"]

    def delete(self, _start, _end):
        self.value = ""

    def insert(self, _index, text):
        self.value += text

    def get(self, _start, _end):
        return self.value


class TestcaseZipExportTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = CURRENT_DIR / "_tmp_testcase_zip"
        self.temp_dir.mkdir(exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_testcases_from_reference_markdown(self):
        md_text = REFERENCE_MD.read_text(encoding="utf-8")

        cases = parse_testcases_from_markdown(md_text)

        self.assertEqual(len(cases), 5)
        self.assertEqual(cases[0]["id"], "1")
        self.assertEqual(cases[0]["input_text"], "1")
        self.assertEqual(cases[0]["output_text"], "1")
        self.assertEqual(cases[-1]["id"], "5")

    def test_build_testcase_preview_shows_only_top_three(self):
        md_text = REFERENCE_MD.read_text(encoding="utf-8")

        preview = build_testcase_preview(parse_testcases_from_markdown(md_text), limit=3)

        self.assertIn("총 테스트케이스: 5개", preview)
        self.assertIn("[1] 입력:", preview)
        self.assertIn("[3] 출력:", preview)
        self.assertNotIn("[4] 입력:", preview)
        self.assertIn("... 외 2개", preview)

    def test_parse_testcases_renumbers_sparse_case_ids(self):
        md_text = """## 5. 채점용 테스트케이스

### 테스트케이스 2 입력
```text
A
```

### 테스트케이스 2 출력
```text
B
```

### 테스트케이스 4 입력
```text
C
```

### 테스트케이스 4 출력
```text
D
```

### 테스트케이스 7 입력
```text
E
```

### 테스트케이스 7 출력
```text
F
```
"""

        cases = parse_testcases_from_markdown(md_text)

        self.assertEqual([case["id"] for case in cases], ["1", "2", "3"])
        self.assertEqual([case["source_id"] for case in cases], ["2", "4", "7"])

    def test_parse_testcases_raises_for_mismatched_pairs(self):
        md_text = """## 5. 채점용 테스트케이스

### 테스트케이스 1 입력
```text
only input
```
"""

        with self.assertRaises(ValueError):
            parse_testcases_from_markdown(md_text)

    def test_export_testcases_to_zip_uses_sequential_filenames(self):
        md_text = REFERENCE_MD.read_text(encoding="utf-8")
        cases = parse_testcases_from_markdown(md_text)

        zip_path = export_testcases_to_zip(cases, self.temp_dir, "sample.zip")

        with zipfile.ZipFile(zip_path) as archive:
            names = archive.namelist()
            self.assertEqual(
                names,
                [
                    "1.in",
                    "1.out",
                    "2.in",
                    "2.out",
                    "3.in",
                    "3.out",
                    "4.in",
                    "4.out",
                    "5.in",
                    "5.out",
                ],
            )

    def test_export_testcases_to_zip_normalizes_newlines(self):
        cases = [{"id": "1", "input_text": "1\r\n2\r\n", "output_text": "3\r\n"}]

        zip_path = export_testcases_to_zip(cases, self.temp_dir, "newline.zip")

        with zipfile.ZipFile(zip_path) as archive:
            self.assertEqual(archive.read("1.in").decode("utf-8"), "1\n2\n")
            self.assertEqual(archive.read("1.out").decode("utf-8"), "3\n")


class TestcaseZipGuiTests(unittest.TestCase):
    def make_app(self):
        app = CrawlerApp.__new__(CrawlerApp)
        app.loaded_testcases = []
        app.selected_testcase_markdown = ""
        app.testcase_zip_name = FakeVar("")
        app.testcase_zip_dir = FakeVar(str(self.temp_dir))
        app.testcase_md_path = FakeVar("")
        app.testcase_count_label = FakeLabel()
        app.testcase_preview_area = FakeText()
        app.export_testcase_zip_btn = FakeButton()
        app._append_log = lambda _message: None
        return app

    def setUp(self):
        self.temp_dir = CURRENT_DIR / "_tmp_testcase_gui"
        self.temp_dir.mkdir(exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_testcase_markdown_updates_preview_and_default_zip_name(self):
        app = self.make_app()

        success = CrawlerApp.load_testcase_markdown(app, str(REFERENCE_MD))

        self.assertTrue(success)
        self.assertEqual(len(app.loaded_testcases), 5)
        self.assertEqual(app.testcase_count_label.text, "총 테스트케이스: 5개")
        self.assertIn("[1] 입력:", app.testcase_preview_area.get("1.0", "end"))
        self.assertEqual(
            app.testcase_zip_name.get(),
            build_default_zip_name(str(REFERENCE_MD)),
        )

    def test_load_testcase_markdown_disables_export_on_parse_error(self):
        broken_md = self.temp_dir / "broken.md"
        broken_md.write_text(
            "## 5. 채점용 테스트케이스\n\n### 테스트케이스 1 입력\n```text\n1\n```\n",
            encoding="utf-8",
        )
        app = self.make_app()

        success = CrawlerApp.load_testcase_markdown(app, str(broken_md))

        self.assertFalse(success)
        self.assertEqual(app.testcase_count_label.text, "총 테스트케이스: 0개")
        self.assertEqual(app.export_testcase_zip_btn.state, "disabled")
        self.assertIn("불러오기 실패:", app.testcase_preview_area.get("1.0", "end"))

    def test_export_testcase_zip_creates_zip_and_reports_success(self):
        app = self.make_app()
        CrawlerApp.load_testcase_markdown(app, str(REFERENCE_MD))
        app.testcase_zip_name.set("cases.zip")
        info_messages = []

        with patch("gui_crawler.messagebox.showinfo", side_effect=lambda title, message: info_messages.append((title, message))), \
            patch("gui_crawler.messagebox.showerror") as error_mock:
            CrawlerApp.export_testcase_zip(app)

        error_mock.assert_not_called()
        self.assertEqual(len(info_messages), 1)
        zip_path = self.temp_dir / "cases.zip"
        self.assertTrue(zip_path.exists())
        with zipfile.ZipFile(zip_path) as archive:
            self.assertIn("1.in", archive.namelist())


if __name__ == "__main__":
    unittest.main()
