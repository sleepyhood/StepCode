import os
import queue
import shutil
import sys
import unittest
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from gui_crawler import CrawlerApp, build_output_filepath
from gui_crawler import (
    DOINGCODING_ADMIN_ID_ENV,
    DOINGCODING_ADMIN_PASSWORD_ENV,
    resolve_admin_credentials,
)


class FakeLogArea:
    def __init__(self):
        self.messages = []

    def config(self, **kwargs):
        return None

    def insert(self, _index, text):
        self.messages.append(text)

    def see(self, _index):
        return None

    def delete(self, _start, _end):
        self.messages.clear()


class FakeButton:
    def __init__(self):
        self.state = None
        self.text = None

    def config(self, **kwargs):
        if "state" in kwargs:
            self.state = kwargs["state"]
        if "text" in kwargs:
            self.text = kwargs["text"]


class FakeRoot:
    def __init__(self):
        self.after_calls = []

    def after(self, delay, callback):
        self.after_calls.append((delay, callback))


class GuiStage5Tests(unittest.TestCase):
    def test_process_ui_queue_updates_widgets_on_main_thread(self):
        app = CrawlerApp.__new__(CrawlerApp)
        app.ui_queue = queue.Queue()
        app.log_area = FakeLogArea()
        app.start_btn = FakeButton()
        app.root = FakeRoot()

        app.ui_queue.put(("log", "worker message"))
        app.ui_queue.put(("button", ("normal", "done")))

        CrawlerApp.process_ui_queue(app)

        self.assertEqual(app.log_area.messages, ["worker message\n"])
        self.assertEqual(app.start_btn.state, "normal")
        self.assertEqual(app.start_btn.text, "done")
        self.assertEqual(len(app.root.after_calls), 1)

    def test_build_output_filepath_avoids_overwriting_existing_files(self):
        temp_dir = CURRENT_DIR / "_tmp_build_output_test"
        temp_dir.mkdir(exist_ok=True)
        try:
            first = temp_dir / "01_dc_test.md"
            first.write_text("existing", encoding="utf-8")

            second_path = build_output_filepath(str(temp_dir), "01_dc_test.md")

            self.assertTrue(second_path.endswith("01_dc_test_1.md"))
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_resolve_admin_credentials_prefers_inputs_then_env(self):
        original_id = os.environ.get(DOINGCODING_ADMIN_ID_ENV)
        original_pw = os.environ.get(DOINGCODING_ADMIN_PASSWORD_ENV)
        os.environ[DOINGCODING_ADMIN_ID_ENV] = "env_id"
        os.environ[DOINGCODING_ADMIN_PASSWORD_ENV] = "env_pw"
        try:
            self.assertEqual(resolve_admin_credentials("typed_id", "typed_pw"), ("typed_id", "typed_pw"))
            self.assertEqual(resolve_admin_credentials("", ""), ("env_id", "env_pw"))
        finally:
            if original_id is None:
                os.environ.pop(DOINGCODING_ADMIN_ID_ENV, None)
            else:
                os.environ[DOINGCODING_ADMIN_ID_ENV] = original_id
            if original_pw is None:
                os.environ.pop(DOINGCODING_ADMIN_PASSWORD_ENV, None)
            else:
                os.environ[DOINGCODING_ADMIN_PASSWORD_ENV] = original_pw

    def test_crawl_process_accepts_show_browser_argument(self):
        app = CrawlerApp.__new__(CrawlerApp)
        app.ui_queue = queue.Queue()
        app.log = lambda _message: None
        app.ui_queue.put = lambda _item: None

        app.crawl_process(
            target_ids=[],
            domain="doingcoding",
            template="http://edu.doingcoding.com/problem/{id}",
            save_path=str(CURRENT_DIR),
            get_templates=False,
            get_testcases=False,
            admin_username="",
            admin_password="",
            show_browser=True,
        )


if __name__ == "__main__":
    unittest.main()
