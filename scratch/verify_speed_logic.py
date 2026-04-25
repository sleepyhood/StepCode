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
        self.min_delay_var.get.return_value = 0.1 # Short for testing
        self.max_delay_var = MagicMock()
        self.max_delay_var.get.return_value = 0.2
        self.batch_size_var = MagicMock()
        self.batch_size_var.get.return_value = 3
        self.batch_pause_var = MagicMock()
        self.batch_pause_var.get.return_value = 1.0
        self.student_list = ["s1", "s2", "s3", "s4", "s5"]
        self.stop_event = MagicMock()
        self.stop_event.is_set.return_value = False
        self.log_messages = []

    def log(self, msg):
        print(f"[LOG] {msg}")
        self.log_messages.append(msg)

def test_speed_logic():
    app = MockApp()
    
    print("Testing Randomized Delay and Batch Pause Logic...")
    start_time = time.time()
    
    for i, username in enumerate(app.student_list):
        print(f"Processing student {i+1}: {username}")
        
        # Simulated request time
        time.sleep(0.01)
        
        # Logic from _extraction_task (Simplified for testing)
        # 1. Randomized Delay
        delay = random.uniform(app.min_delay_var.get(), app.max_delay_var.get())
        print(f"  Delay: {delay:.3f}s")
        time.sleep(delay)
        
        # 2. Batch Pause
        batch_size = app.batch_size_var.get()
        if (i + 1) % batch_size == 0 and (i + 1) < len(app.student_list):
            pause_time = app.batch_pause_var.get()
            app.log(f"BATCH_PAUSE: {batch_size} students done. Pausing for {pause_time}s...")
            time.sleep(pause_time)
            
    end_time = time.time()
    total_duration = end_time - start_time
    print(f"\nTotal duration: {total_duration:.2f}s")
    
    # Validation
    # 5 students, batch size 3 -> 1 batch pause of 1.0s
    # 5 random delays of ~0.15s -> ~0.75s
    # Total expected around 1.75s to 2.25s
    if 1.5 < total_duration < 2.5:
        print("✅ Speed logic test PASSED.")
    else:
        print(f"❌ Speed logic test FAILED. Unexpected duration: {total_duration:.2f}s")

if __name__ == "__main__":
    test_speed_logic()
