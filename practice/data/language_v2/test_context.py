from playwright.sync_api import sync_playwright
import json

def test_context_reuse():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        # Use a realistic User-Agent to avoid immediate block
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        print("--- First Call ---")
        page1 = context.new_page()
        res1 = page1.goto("https://solved.ac/api/v3/problem/show?problemId=1000")
        print("Status 1:", res1.status)
        page1.wait_for_timeout(3000)
        try:
            print("Level 1:", json.loads(page1.evaluate("() => document.body.innerText")).get("level"))
        except:
            print("Failed 1")
        page1.close()

        print("--- Second Call ---")
        page2 = context.new_page()
        res2 = page2.goto("https://solved.ac/api/v3/problem/show?problemId=1001")
        print("Status 2:", res2.status)
        page2.wait_for_timeout(1000)
        try:
            print("Level 2:", json.loads(page2.evaluate("() => document.body.innerText")).get("level"))
        except:
            print("Failed 2")
        page2.close()

        browser.close()

if __name__ == "__main__":
    test_context_reuse()
