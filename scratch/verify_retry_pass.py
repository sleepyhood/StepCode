import sys
import os
import time
import random
from unittest.mock import MagicMock

class MockApp:
    def __init__(self):
        self.min_delay_var = MagicMock()
        self.min_delay_var.get.return_value = 0.01
        self.max_delay_var = MagicMock()
        self.max_delay_var.get.return_value = 0.02
        self.batch_size_var = MagicMock()
        self.batch_size_var.get.return_value = 5 # Big enough to not trigger batch in this small list
        self.batch_pause_var = MagicMock()
        self.batch_pause_var.get.return_value = 0.1
        self.auto_relogin_var = MagicMock()
        self.auto_relogin_var.get.return_value = False
        
        # Test students
        self.student_list = ["s1", "s2_error", "s3", "s4_error"]
        self.stop_event = MagicMock()
        self.stop_event.is_set.return_value = False
        self.log_messages = []

    def log(self, msg):
        print(f"[LOG] {msg}")
        self.log_messages.append(msg)

    def _login(self, base_url, username, password):
        print(">> _login called successfully")
        return "NEW_SESSION_OBJECT"

def test_retry_logic():
    app = MockApp()
    
    print("Testing 2-Pass Retry Logic...")
    
    # Simulate environment
    is_mock = False
    use_browser = False
    HAS_SELENIUM = False
    base_url = "http://test.com"
    admin_id = "admin"
    admin_pw = "pass"
    headless = True
    session = "OLD_SESSION"
    
    # Copied Logic Start
    current_students = app.student_list
    max_retries = 1
    
    for attempt in range(max_retries + 1):
        if not current_students or app.stop_event.is_set():
            break
            
        if attempt > 0:
            app.log("="*50)
            app.log(f"⚠️ 1차 수집 실패자 {len(current_students)}명에 대한 2차 재수집을 준비합니다.")
            app.log("🕒 서버 IP 차단 해제를 위해 60초간 대기합니다...")
            # Simulate 60s wait quickly
            for idx in range(6, 0, -1): # Changed from 60 to 6 for quick testing
                if app.stop_event.is_set(): break
                if idx % 10 == 0 or idx <= 5: 
                    app.log(f"   남은 대기 시간: {idx}초")
            
            if app.stop_event.is_set(): break
            
            if not is_mock:
                app.log("🔄 재수집 전 세션을 완전히 초기화(재로그인)합니다...")
                new_session = app._login(base_url, admin_id, admin_pw)
                if new_session:
                    session = new_session
                    app.log("✅ 재수집용 세션 갱신 성공!")
        
        error_students = []
        
        for i, username in enumerate(current_students):
            if app.stop_event.is_set():
                break
                
            prefix_msg = "2차 조회 중" if attempt > 0 else "조회 중"
            app.log(f"{prefix_msg} ({i+1}/{len(current_students)}): {username}")
            
            has_error = False
            try:
                # Force error for testing
                if attempt == 0 and "error" in username:
                    raise Exception("Forced error in attempt 1")
                elif attempt == 1 and username == "s4_error":
                    raise Exception("Forced error in attempt 2")
            except Exception as e:
                app.log(f"  ! Exception: {e}")
                error_students.append(username)
                has_error = True
            finally:
                if has_error and not is_mock:
                    app.log("[WARNING] 에러 감지됨. 연쇄 차단 방지를 위해 5초간 추가 쿨다운 대기...")
                    
        current_students = error_students
        
    final_error_students = current_students
    
    # Validation
    print("\n--- Validation ---")
    print(f"Final error students: {final_error_students}")
    if final_error_students == ["s4_error"]:
        print("Success: Retry logic works as expected.")
    else:
        print("Fail: Logic is broken.")

if __name__ == "__main__":
    test_retry_logic()
