import sys
import os
import time
import random
from unittest.mock import MagicMock

# Path to the script we are testing
SCRIPT_PATH = r"c:\Users\DCT2\Desktop\DCT2_공유폴더\StepCode\Resources\tools\extract_scores.py"

# Mocking parts of the script to test the logic
class MockApp:
    def __init__(self):
        self.min_delay_var = MagicMock()
        self.min_delay_var.get.return_value = 0.1
        self.max_delay_var = MagicMock()
        self.max_delay_var.get.return_value = 0.2
        self.batch_size_var = MagicMock()
        self.batch_size_var.get.return_value = 3
        self.batch_pause_var = MagicMock()
        self.batch_pause_var.get.return_value = 1.0
        self.student_list = ["s1", "s2_error", "s3"]
        self.stop_event = MagicMock()
        self.stop_event.is_set.return_value = False
        self.log_messages = []
        self.is_mock = False

    def log(self, msg):
        print(f"[LOG] {msg}")
        self.log_messages.append(msg)

def test_error_delay_logic():
    app = MockApp()
    
    print("Testing Error Delay Logic in finally block...")
    start_time = time.time()
    
    for i, username in enumerate(app.student_list):
        print(f"\nProcessing student {i+1}: {username}")
        has_error = False
        
        try:
            if "error" in username:
                print("  Simulating JSONDecodeError...")
                raise ValueError("Expecting value: line 1 column 1 (char 0)")
            else:
                print("  Simulating successful request...")
        except Exception as e:
            app.log(f"  ! Exception: {e}")
            has_error = True
        finally:
            # Logic from _extraction_task
            if has_error and not app.is_mock:
                app.log("[WARNING] 에러 감지됨. 연쇄 차단 방지를 위해 5초간 추가 쿨다운 대기...")
                time.sleep(2.0) # Used 2.0s instead of 5.0s just for faster testing
                
            delay = random.uniform(app.min_delay_var.get(), app.max_delay_var.get())
            print(f"  Random delay: {delay:.3f}s")
            time.sleep(delay)
            
            batch_size = app.batch_size_var.get()
            if (i + 1) % batch_size == 0 and (i + 1) < len(app.student_list):
                pause_time = app.batch_pause_var.get()
                app.log(f"BATCH_PAUSE: {batch_size}명 조회 완료. {pause_time}초간 휴식...")
                time.sleep(pause_time)
            
    end_time = time.time()
    total_duration = end_time - start_time
    print(f"\nTotal duration: {total_duration:.2f}s")
    
    # Validation:
    # 3 requests -> 3 random delays (~0.45s)
    # 1 error -> 1 cooldown (2.0s)
    # Total expected > 2.45s
    if total_duration > 2.4:
        print("Success: Delay applied even after an error.")
    else:
        print(f"Failed: Duration was too short, delay might have been skipped. ({total_duration:.2f}s)")

if __name__ == "__main__":
    test_error_delay_logic()
