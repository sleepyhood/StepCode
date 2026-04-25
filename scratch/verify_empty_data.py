import sys
import os
from unittest.mock import MagicMock

# Path to the script we are testing
SCRIPT_PATH = r"c:\Users\DCT2\Desktop\DCT2_공유폴더\StepCode\Resources\tools\extract_scores.py"

# Mocking necessary classes for excel generation
class MockWorkbook:
    def __init__(self):
        self.active = MagicMock()
        self.active.title = "Scores"
    def save(self, path):
        print(f"File saved to {path}")

# Import parts of the file or mock the class
import tkinter as tk
from openpyxl import Workbook

# We need to import the class from the original file
sys.path.append(os.path.dirname(SCRIPT_PATH))
from extract_scores import ScoreExtractorApp

def test_empty_data_excel():
    print("Testing _generate_excel with EMPTY data...")
    root = tk.Tk()
    app = ScoreExtractorApp(root)
    
    empty_data = []
    problem_ids = ["P1", "P2"]
    save_dir = r"c:\Users\DCT2\Desktop\DCT2_공유폴더\StepCode\scratch"
    
    try:
        # Mocking the save part to not actually create a file if not needed, 
        # but let's see if it runs without UnboundLocalError
        app._generate_excel(empty_data, problem_ids, save_dir)
        print("Success: _generate_excel ran without UnboundLocalError.")
    except UnboundLocalError:
        print("Fail: UnboundLocalError occurred.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        root.destroy()

if __name__ == "__main__":
    test_empty_data_excel()
