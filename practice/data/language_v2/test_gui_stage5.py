import queue
import shutil
import sys
import unittest
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from gui_crawler import CrawlerApp, build_output_filepath


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


if __name__ == "__main__":
    unittest.main()
