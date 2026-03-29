import os
import queue
import shutil
import sys
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from gui_crawler import CrawlerApp, build_output_filepath
from gui_crawler import (
    DOINGCODING_ADMIN_ID_ENV,
    DOINGCODING_ADMIN_PASSWORD_ENV,
    close_doingcoding_admin_session,
    open_doingcoding_admin_session,
    resolve_admin_credentials,
    upload_doingcoding_testcases_with_session,
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


class FakeVar:
    def __init__(self, value=None):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class FakeFrame:
    def __init__(self):
        self.pack_calls = []
        self.hidden = False

    def pack(self, **kwargs):
        self.pack_calls.append(kwargs)
        self.hidden = False

    def pack_forget(self):
        self.hidden = True


class FakeEntry:
    def __init__(self, value=""):
        self.value = value

    def delete(self, _start, _end):
        self.value = ""

    def insert(self, _index, value):
        self.value = value

    def get(self):
        return self.value


class FakeLabel:
    def __init__(self):
        self.text = None

    def config(self, **kwargs):
        if "text" in kwargs:
            self.text = kwargs["text"]


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

    def test_crawl_process_opens_admin_session_once_for_doingcoding_testcases_batch(self):
        app = CrawlerApp.__new__(CrawlerApp)
        app.ui_queue = queue.Queue()
        app.log = lambda _message: None
        app.ui_queue.put = lambda _item: None

        class FakeBrowser:
            def close(self):
                return None

        class FakePlaywright:
            def __init__(self):
                self.stopped = False
                self.chromium = self

            def launch(self, headless=True):
                self.headless = headless
                return FakeBrowser()

            def stop(self):
                self.stopped = True

        admin_session = object()
        with patch("gui_crawler.sync_playwright") as sync_mock, \
            patch("gui_crawler.open_doingcoding_admin_session", return_value=admin_session) as open_mock, \
            patch("gui_crawler.close_doingcoding_admin_session") as close_mock, \
            patch("gui_crawler.scrape_doingcoding", return_value=("제목", "본문")) as scrape_mock, \
            patch("gui_crawler.build_output_filepath", side_effect=lambda save_path, filename: str(Path(save_path) / filename)):
            sync_mock.return_value.start.return_value = FakePlaywright()
            app.crawl_process(
                target_ids=["P101v0701", "P101v0702"],
                domain="doingcoding",
                template="http://edu.doingcoding.com/problem/{id}",
                save_path=str(CURRENT_DIR),
                get_templates=False,
                get_testcases=True,
                admin_username="admin",
                admin_password="secret",
                show_browser=True,
            )

        open_mock.assert_called_once()
        close_mock.assert_called_once_with(admin_session)
        self.assertEqual(scrape_mock.call_count, 2)
        self.assertTrue(all(call.kwargs["admin_session"] is admin_session for call in scrape_mock.call_args_list))
        self.assertTrue(all(call.kwargs["browser"] is not None for call in scrape_mock.call_args_list))

    def test_crawl_process_does_not_open_admin_session_when_testcases_disabled(self):
        app = CrawlerApp.__new__(CrawlerApp)
        app.ui_queue = queue.Queue()
        app.log = lambda _message: None
        app.ui_queue.put = lambda _item: None

        with patch("gui_crawler.open_doingcoding_admin_session") as open_mock, \
            patch("gui_crawler.close_doingcoding_admin_session") as close_mock, \
            patch("gui_crawler.scrape_doingcoding", return_value=("제목", "본문")) as scrape_mock, \
            patch("gui_crawler.build_output_filepath", side_effect=lambda save_path, filename: str(Path(save_path) / filename)):
            app.crawl_process(
                target_ids=["P101v0701"],
                domain="doingcoding",
                template="http://edu.doingcoding.com/problem/{id}",
                save_path=str(CURRENT_DIR),
                get_templates=False,
                get_testcases=False,
                admin_username="",
                admin_password="",
                show_browser=False,
            )

        open_mock.assert_not_called()
        close_mock.assert_called_once_with(None)
        scrape_mock.assert_called_once()
        self.assertIsNone(scrape_mock.call_args.kwargs["admin_session"])
        self.assertIsNone(scrape_mock.call_args.kwargs["browser"])

    def test_set_doingcoding_option_visibility_hides_options_and_resets_flags_for_baekjoon(self):
        app = CrawlerApp.__new__(CrawlerApp)
        app.domain_var = FakeVar("baekjoon")
        app.doingcoding_options_frame = FakeFrame()
        app.frame_dir = object()
        app.get_templates_var = FakeVar(True)
        app.get_testcases_var = FakeVar(True)
        app.show_browser_var = FakeVar(True)

        CrawlerApp._set_doingcoding_option_visibility(app)

        self.assertTrue(app.doingcoding_options_frame.hidden)
        self.assertFalse(app.get_templates_var.get())
        self.assertFalse(app.get_testcases_var.get())
        self.assertFalse(app.show_browser_var.get())

    def test_set_doingcoding_option_visibility_shows_options_for_doingcoding(self):
        app = CrawlerApp.__new__(CrawlerApp)
        app.domain_var = FakeVar("doingcoding")
        app.doingcoding_options_frame = FakeFrame()
        app.get_templates_var = FakeVar(False)
        app.get_testcases_var = FakeVar(False)
        app.show_browser_var = FakeVar(False)

        CrawlerApp._set_doingcoding_option_visibility(app)

        self.assertFalse(app.doingcoding_options_frame.hidden)
        self.assertEqual(app.doingcoding_options_frame.pack_calls[-1], {"fill": "x", "pady": (12, 0)})

    def test_update_url_template_switches_defaults_and_hides_doingcoding_options_for_baekjoon(self):
        app = CrawlerApp.__new__(CrawlerApp)
        app.domain_var = FakeVar("baekjoon")
        app.url_template = FakeEntry("http://edu.doingcoding.com/problem/{id}")
        app.prefix_id = FakeEntry("P101v")
        app.start_id = FakeEntry("0701")
        app.end_id = FakeEntry("0710")
        app.doingcoding_options_frame = FakeFrame()
        app.frame_dir = object()
        app.get_templates_var = FakeVar(True)
        app.get_testcases_var = FakeVar(True)
        app.show_browser_var = FakeVar(True)

        CrawlerApp.update_url_template(app)

        self.assertEqual(app.url_template.get(), "https://www.acmicpc.net/problem/{id}")
        self.assertEqual(app.prefix_id.get(), "")
        self.assertEqual(app.start_id.get(), "1000")
        self.assertEqual(app.end_id.get(), "1005")
        self.assertTrue(app.doingcoding_options_frame.hidden)

    def test_update_url_template_switches_defaults_and_shows_doingcoding_options(self):
        app = CrawlerApp.__new__(CrawlerApp)
        app.domain_var = FakeVar("doingcoding")
        app.url_template = FakeEntry("https://www.acmicpc.net/problem/{id}")
        app.prefix_id = FakeEntry("")
        app.start_id = FakeEntry("1000")
        app.end_id = FakeEntry("1005")
        app.doingcoding_options_frame = FakeFrame()
        app.frame_dir = object()
        app.get_templates_var = FakeVar(False)
        app.get_testcases_var = FakeVar(False)
        app.show_browser_var = FakeVar(False)

        CrawlerApp.update_url_template(app)

        self.assertEqual(app.url_template.get(), "http://edu.doingcoding.com/problem/{id}")
        self.assertEqual(app.prefix_id.get(), "P101v")
        self.assertEqual(app.start_id.get(), "0701")
        self.assertEqual(app.end_id.get(), "0710")
        self.assertFalse(app.doingcoding_options_frame.hidden)

    def test_refresh_upload_summary_enables_button_when_problem_and_zip_are_ready(self):
        app = CrawlerApp.__new__(CrawlerApp)
        app.upload_problem_id = FakeVar("P101v0701")
        app.upload_zip_path = FakeVar("C:/tmp/case.zip")
        app.upload_summary_label = FakeLabel()
        app.upload_testcase_btn = FakeButton()

        CrawlerApp._refresh_upload_summary(app)

        self.assertIn("P101v0701", app.upload_summary_label.text)
        self.assertIn("case.zip", app.upload_summary_label.text)
        self.assertEqual(app.upload_testcase_btn.state, "normal")

    def test_refresh_upload_summary_disables_button_when_missing_values(self):
        app = CrawlerApp.__new__(CrawlerApp)
        app.upload_problem_id = FakeVar("")
        app.upload_zip_path = FakeVar("")
        app.upload_summary_label = FakeLabel()
        app.upload_testcase_btn = FakeButton()

        CrawlerApp._refresh_upload_summary(app)

        self.assertEqual(app.upload_summary_label.text, "문제 ID와 ZIP 파일을 선택해 주세요.")
        self.assertEqual(app.upload_testcase_btn.state, "disabled")

    def test_upload_testcase_zip_calls_upload_with_selected_problem_and_zip(self):
        app = CrawlerApp.__new__(CrawlerApp)
        app.upload_problem_id = FakeVar("P101v0701")
        temp_zip = CURRENT_DIR / "_tmp_upload_gui.zip"
        temp_zip.write_text("zip", encoding="utf-8")
        app.upload_zip_path = FakeVar(str(temp_zip))
        app.admin_username = FakeEntry("admin")
        app.admin_password = FakeEntry("secret")
        app.show_browser_var = FakeVar(False)
        app.log = lambda _message: None
        logged = []
        app._append_log = logged.append

        class FakeBrowser:
            def close(self):
                return None

        class FakePlaywright:
            def __init__(self):
                self.chromium = self

            def launch(self, headless=True):
                self.headless = headless
                return FakeBrowser()

            def stop(self):
                return None

        admin_session = object()
        try:
            with patch("gui_crawler.sync_playwright") as sync_mock, \
                patch("gui_crawler.open_doingcoding_admin_session", return_value=admin_session) as open_mock, \
                patch("gui_crawler.close_doingcoding_admin_session") as close_mock, \
                patch("gui_crawler.upload_doingcoding_testcases_with_session", return_value={"problem_id": "P101v0701", "zip_path": str(temp_zip), "status": "uploaded"}) as upload_mock, \
                patch("gui_crawler.messagebox.showinfo") as info_mock, \
                patch("gui_crawler.messagebox.showerror") as error_mock:
                sync_mock.return_value.start.return_value = FakePlaywright()
                CrawlerApp.upload_testcase_zip(app)

            open_mock.assert_called_once()
            upload_mock.assert_called_once_with(admin_session, "P101v0701", str(temp_zip), logger=app.log)
            close_mock.assert_called_once_with(admin_session)
            info_mock.assert_called_once()
            error_mock.assert_not_called()
            self.assertTrue(any("완료" in message for message in logged))
        finally:
            temp_zip.unlink(missing_ok=True)

    def test_upload_testcase_zip_rejects_missing_zip_file(self):
        app = CrawlerApp.__new__(CrawlerApp)
        app.upload_problem_id = FakeVar("P101v0701")
        app.upload_zip_path = FakeVar(str(CURRENT_DIR / "missing.zip"))
        app.admin_username = FakeEntry("admin")
        app.admin_password = FakeEntry("secret")
        app.show_browser_var = FakeVar(False)
        app.log = lambda _message: None
        app._append_log = lambda _message: None

        with patch("gui_crawler.messagebox.showerror") as error_mock:
            CrawlerApp.upload_testcase_zip(app)

        error_mock.assert_called_once()

    def test_resolve_initial_dir_prefers_last_dir_for_same_kind(self):
        app = CrawlerApp.__new__(CrawlerApp)
        app.last_md_dir = str(CURRENT_DIR)
        app.last_zip_dir = str(CURRENT_DIR / "_zip_recent")
        app.last_directory_dir = str(CURRENT_DIR / "_dir_recent")
        Path(app.last_zip_dir).mkdir(exist_ok=True)
        Path(app.last_directory_dir).mkdir(exist_ok=True)
        try:
            resolved = CrawlerApp._resolve_initial_dir(
                app, "md", current_path=str(CURRENT_DIR / "sub" / "file.md")
            )
            self.assertEqual(resolved, str(CURRENT_DIR))
        finally:
            shutil.rmtree(app.last_zip_dir, ignore_errors=True)
            shutil.rmtree(app.last_directory_dir, ignore_errors=True)

    def test_resolve_initial_dir_falls_back_to_parent_of_current_path(self):
        app = CrawlerApp.__new__(CrawlerApp)
        missing_dir = str(CURRENT_DIR / "_missing_last_dir")
        app.last_md_dir = missing_dir
        current_file = CURRENT_DIR / "_docs" / "sample.md"
        current_file.parent.mkdir(exist_ok=True)
        try:
            resolved = CrawlerApp._resolve_initial_dir(app, "md", current_path=str(current_file))
            self.assertEqual(resolved, str(current_file.parent))
        finally:
            shutil.rmtree(current_file.parent, ignore_errors=True)

    def test_remember_selected_path_updates_each_kind_separately(self):
        app = CrawlerApp.__new__(CrawlerApp)
        md_dir = CURRENT_DIR / "_tmp_md_recent"
        zip_dir = CURRENT_DIR / "_tmp_zip_recent"
        dir_dir = CURRENT_DIR / "_tmp_directory_recent"
        md_dir.mkdir(exist_ok=True)
        zip_dir.mkdir(exist_ok=True)
        dir_dir.mkdir(exist_ok=True)
        try:
            CrawlerApp._remember_selected_path(app, "md", str(md_dir / "a.md"))
            CrawlerApp._remember_selected_path(app, "zip", str(zip_dir / "a.zip"))
            CrawlerApp._remember_selected_path(app, "directory", str(dir_dir))

            self.assertEqual(app.last_md_dir, str(md_dir))
            self.assertEqual(app.last_zip_dir, str(zip_dir))
            self.assertEqual(app.last_directory_dir, str(dir_dir))
        finally:
            shutil.rmtree(md_dir, ignore_errors=True)
            shutil.rmtree(zip_dir, ignore_errors=True)
            shutil.rmtree(dir_dir, ignore_errors=True)

    def test_select_testcase_markdown_uses_last_md_dir_and_remembers_selection(self):
        app = CrawlerApp.__new__(CrawlerApp)
        recent_dir = CURRENT_DIR / "_tmp_recent_md"
        recent_dir.mkdir(exist_ok=True)
        selected_file = recent_dir / "selected.md"
        selected_file.write_text("content", encoding="utf-8")
        app.last_md_dir = str(recent_dir)
        app.testcase_md_path = FakeVar("")
        app.testcase_preview_area = FakeLogArea()
        app.export_testcase_zip_btn = FakeButton()
        app.testcase_count_label = FakeLabel()
        app.testcase_zip_name = FakeVar("")
        app.loaded_testcases = []
        app.selected_testcase_markdown = ""
        try:
            with patch("gui_crawler.filedialog.askopenfilename", return_value=str(selected_file)) as dialog_mock, \
                patch.object(CrawlerApp, "load_testcase_markdown", return_value=True) as load_mock:
                CrawlerApp.select_testcase_markdown(app)

            self.assertEqual(dialog_mock.call_args.kwargs["initialdir"], str(recent_dir))
            self.assertEqual(app.last_md_dir, str(recent_dir))
            self.assertEqual(app.testcase_md_path.get(), str(selected_file))
            load_mock.assert_called_once_with(str(selected_file))
        finally:
            shutil.rmtree(recent_dir, ignore_errors=True)

    def test_load_testcase_markdown_refreshes_default_zip_name_for_new_file(self):
        app = CrawlerApp.__new__(CrawlerApp)
        first_file = CURRENT_DIR / "_tmp_case_a.md"
        second_file = CURRENT_DIR / "_tmp_case_b.md"
        first_file.write_text("first", encoding="utf-8")
        second_file.write_text("second", encoding="utf-8")
        app.testcase_zip_name = FakeVar("")
        app.loaded_testcases = []
        app.selected_testcase_markdown = ""
        app.testcase_preview_area = FakeLogArea()
        app.export_testcase_zip_btn = FakeButton()
        app.testcase_count_label = FakeLabel()

        try:
            with patch("gui_crawler.parse_testcases_from_markdown", return_value=[{"input": "1", "output": "2"}]), \
                patch("gui_crawler.build_testcase_preview", return_value="preview"), \
                patch("gui_crawler.build_default_zip_name", side_effect=["first.zip", "second.zip"]):
                self.assertTrue(CrawlerApp.load_testcase_markdown(app, str(first_file)))
                self.assertEqual(app.testcase_zip_name.get(), "first.zip")

                self.assertTrue(CrawlerApp.load_testcase_markdown(app, str(second_file)))
                self.assertEqual(app.testcase_zip_name.get(), "second.zip")
        finally:
            first_file.unlink(missing_ok=True)
            second_file.unlink(missing_ok=True)

    def test_select_upload_zip_file_uses_last_zip_dir_and_remembers_selection(self):
        app = CrawlerApp.__new__(CrawlerApp)
        recent_dir = CURRENT_DIR / "_tmp_recent_zip"
        recent_dir.mkdir(exist_ok=True)
        selected_file = recent_dir / "selected.zip"
        selected_file.write_text("content", encoding="utf-8")
        app.last_zip_dir = str(recent_dir)
        app.upload_zip_path = FakeVar("")
        app.upload_problem_id = FakeVar("")
        app.upload_summary_label = FakeLabel()
        app.upload_testcase_btn = FakeButton()
        app.selected_upload_zip_path = ""
        try:
            with patch("gui_crawler.filedialog.askopenfilename", return_value=str(selected_file)) as dialog_mock:
                CrawlerApp.select_upload_zip_file(app)

            self.assertEqual(dialog_mock.call_args.kwargs["initialdir"], str(recent_dir))
            self.assertEqual(app.last_zip_dir, str(recent_dir))
            self.assertEqual(app.upload_zip_path.get(), str(selected_file))
            self.assertEqual(app.selected_upload_zip_path, str(selected_file))
        finally:
            shutil.rmtree(recent_dir, ignore_errors=True)

    def test_select_dir_uses_last_directory_dir_and_remembers_selection(self):
        app = CrawlerApp.__new__(CrawlerApp)
        recent_dir = CURRENT_DIR / "_tmp_recent_directory"
        target_dir = CURRENT_DIR / "_tmp_selected_directory"
        recent_dir.mkdir(exist_ok=True)
        target_dir.mkdir(exist_ok=True)
        app.last_directory_dir = str(recent_dir)
        app.save_dir = FakeVar("")
        try:
            with patch("gui_crawler.filedialog.askdirectory", return_value=str(target_dir)) as dialog_mock:
                CrawlerApp.select_dir(app)

            self.assertEqual(dialog_mock.call_args.kwargs["initialdir"], str(recent_dir))
            self.assertEqual(app.last_directory_dir, str(target_dir))
            self.assertEqual(app.save_dir.get(), str(target_dir))
        finally:
            shutil.rmtree(recent_dir, ignore_errors=True)
            shutil.rmtree(target_dir, ignore_errors=True)

    def test_init_builds_notebook_with_three_tabs(self):
        try:
            root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"Tk runtime unavailable: {exc}")
        try:
            root.withdraw()
            app = CrawlerApp(root)

            self.assertEqual(len(app.notebook.tabs()), 3)
            self.assertEqual(app.notebook.tab(app.notebook.tabs()[0], "text"), "크롤링")
            self.assertEqual(app.notebook.tab(app.notebook.tabs()[1], "text"), "테스트케이스 ZIP 생성")
            self.assertEqual(app.notebook.tab(app.notebook.tabs()[2], "text"), "테스트케이스 업로드")
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()
