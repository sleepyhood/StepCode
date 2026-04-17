from playwright.sync_api import sync_playwright
import json

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = "https://solved.ac/api/v3/problem/show?problemId=1000"
        response = page.goto(url)
        print("Status:", response.status)
        print("Content-Type:", response.headers.get("content-type"))
        try:
            print("Response text length:", len(response.text()))
            print("JSON via response.json():", response.json().get('problemId'))
        except Exception as e:
            print("Error getting response text:", e)
            
        try:
            json_text = page.evaluate("() => document.body.innerText")
            print("DOM innerText:", json_text[:100])
        except Exception as e:
            print("Error getting innerText:", e)
        browser.close()

if __name__ == "__main__":
    test()
