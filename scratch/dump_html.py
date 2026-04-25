import os
from playwright.sync_api import sync_playwright

def run_debug():
    base_url = "http://edu.doingcoding.com"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        page.goto(base_url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)
        
        html_content = page.content()
        with open("scratch/debug_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print("HTML 저장 완료")
        browser.close()

if __name__ == "__main__":
    run_debug()
