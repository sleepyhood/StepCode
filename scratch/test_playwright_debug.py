import os
from playwright.sync_api import sync_playwright

def run_debug():
    print("디버그 스크립트 시작")
    base_url = "http://edu.doingcoding.com"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 뷰포트를 크게 설정
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        print(f"메인 페이지 접속 중: {base_url}")
        page.goto(base_url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)
        
        print("스크린샷 캡처 중...")
        page.screenshot(path="scratch/debug_login.png")
        
        print("로그인 버튼 XPath 확인 중...")
        try:
            element = page.locator('xpath=//*[@id="header"]/ul/div[2]/button[1]')
            if element.count() > 0:
                print("✅ 로그인 버튼 발견!")
                print(f"버튼 텍스트: {element.inner_text()}")
                print(f"버튼 보임 여부: {element.is_visible()}")
            else:
                print("❌ 로그인 버튼이 DOM에 존재하지 않습니다.")
        except Exception as e:
            print("XPath 검사 중 에러:", e)
            
        browser.close()
        print("디버그 종료")

if __name__ == "__main__":
    run_debug()
