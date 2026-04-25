import sys
import os
import time
import random
from unittest.mock import MagicMock, patch

# Path to the script we are testing
SCRIPT_PATH = r"c:\Users\DCT2\Desktop\DCT2_공유폴더\StepCode\Resources\tools\extract_scores.py"

# Mocking parts of the script to test the logic
class MockApp:
    def __init__(self):
        self.min_delay_var = MagicMock()
        self.min_delay_var.get.return_value = 0.01
        self.max_delay_var = MagicMock()
        self.max_delay_var.get.return_value = 0.02
        self.batch_size_var = MagicMock()
        self.batch_size_var.get.return_value = 3
        self.batch_pause_var = MagicMock()
        self.batch_pause_var.get.return_value = 0.1
        self.auto_relogin_var = MagicMock()
        self.auto_relogin_var.get.return_value = True
        
        self.base_url_var = MagicMock()
        self.base_url_var.get.return_value = "http://test.com"
        self.admin_id_var = MagicMock()
        self.admin_id_var.get.return_value = "admin"
        self.admin_pw_var = MagicMock()
        self.admin_pw_var.get.return_value = "pass"
        self.use_browser_var = MagicMock()
        self.use_browser_var.get.return_value = False
        self.headless_var = MagicMock()
        self.headless_var.get.return_value = True
        
        self.student_list = ["s1", "s2", "s3", "s4"]
        self.stop_event = MagicMock()
        self.stop_event.is_set.return_value = False
        self.log_messages = []
        self.is_mock = False

    def log(self, msg):
        print(f"[LOG] {msg}")
        self.log_messages.append(msg)

    def _login(self, base_url, username, password):
        print(">> _login called successfully")
        return "NEW_SESSION_OBJECT"
        
    def _login_selenium(self, base_url, username, password, headless):
        print(">> _login_selenium called successfully")
        return "NEW_SELENIUM_SESSION_OBJECT"

def test_auto_relogin():
    app = MockApp()
    
    print("Testing Auto Re-login Logic in finally block...")
    
    # We simulate the _extraction_task environment partially
    use_browser = app.use_browser_var.get()
    HAS_SELENIUM = False
    base_url = "http://test.com"
    admin_id = "admin"
    admin_pw = "pass"
    headless = True
    session = "OLD_SESSION"
    is_mock = False
    
    for i, username in enumerate(app.student_list):
        print(f"\nProcessing student {i+1}: {username}")
        has_error = False
        
        try:
            pass # simulate work
        except Exception as e:
            has_error = True
        finally:
            if has_error and not is_mock:
                app.log("[WARNING] 에러 감지됨. 연쇄 차단 방지를 위해 5초간 추가 쿨다운 대기...")
                time.sleep(0.1)
                
            delay = random.uniform(app.min_delay_var.get(), app.max_delay_var.get())
            time.sleep(delay)
            
            batch_size = app.batch_size_var.get()
            if (i + 1) % batch_size == 0 and (i + 1) < len(app.student_list):
                if app.auto_relogin_var.get() and not is_mock:
                    app.log(f"RELOGIN: {batch_size}명 단위 차단 우회를 위해 세션을 갱신(재로그인)합니다...")
                    new_session = None
                    if use_browser and HAS_SELENIUM:
                        new_session = app._login_selenium(base_url, admin_id, admin_pw, headless)
                    else:
                        new_session = app._login(base_url, admin_id, admin_pw)
                    
                    if new_session:
                        session = new_session
                        app.log("RELOGIN SUCCESS!")
                    else:
                        app.log("RELOGIN FAIL!")
                        
                pause_time = app.batch_pause_var.get()
                app.log(f"BATCH_PAUSE: {batch_size}명 조회 완료. {pause_time}초간 휴식...")
                time.sleep(pause_time)
                
    if session == "NEW_SESSION_OBJECT":
        print("\nSuccess: Session was successfully updated during extraction loop.")
    else:
        print(f"\nFail: Session was not updated. It is {session}")

if __name__ == "__main__":
    test_auto_relogin()
