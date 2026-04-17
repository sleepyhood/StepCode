from playwright.sync_api import sync_playwright
import json

def get_solvedac_level_and_tags(browser, problem_id):
    url = f"https://solved.ac/api/v3/problem/show?problemId={problem_id}"
    api_page = browser.new_page()
    try:
        response = api_page.goto(url, wait_until="domcontentloaded", timeout=15000)
        api_page.wait_for_timeout(1500)
        if response.status == 200:
            json_text = api_page.evaluate("() => document.body.innerText")
            data = json.loads(json_text)
            return data.get("level", 0), data.get("tags", [])
        else:
            print(f"Status: {response.status}")
            print("Content:", api_page.evaluate("() => document.body.innerText")[:100])
    except Exception as e:
        print("Error:", e)
    finally:
        api_page.close()

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        print("Testing get_solvedac_level_and_tags with HEADLESS=TRUE...")
        level, tags = get_solvedac_level_and_tags(browser, 1000)
        print("Result Level:", level)
        browser.close()

if __name__ == "__main__":
    test()
