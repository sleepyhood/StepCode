@echo off
setlocal

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" "scripts\pdf_page_capture_gui.py"
) else (
    python "scripts\pdf_page_capture_gui.py"
)
