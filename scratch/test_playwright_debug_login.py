import os
from playwright.sync_api import sync_playwright

def run_debug():
    base_url = "http://edu.doingcoding.com/login"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        page.goto(base_url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)
        
        print("로그인 폼(ID) XPath 확인 중...")
        try:
            element = page.locator('xpath=/html/body/div[3]/div[2]/div/div/div[2]/div/form/div[1]/div/div[1]/input')
            if element.count() > 0:
                print("✅ ID 필드 발견!")
            else:
                print("❌ ID 필드가 DOM에 존재하지 않습니다.")
        except Exception as e:
            print("XPath 검사 중 에러:", e)
            
        print("입력창 셀렉터 검색 (input[type='text'], input[name='username'])")
        inputs = page.locator('input')
        print(f"전체 input 요소 개수: {inputs.count()}")
        
        browser.close()

if __name__ == "__main__":
    run_debug()
