import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_selenium():
    print("Selenium 테스트 시작")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("http://edu.doingcoding.com")
    time.sleep(2)
    
    try:
        btn = driver.find_element(By.XPATH, '//*[@id="header"]/ul/div[2]/button[1]')
        print("✅ 버튼 발견:", btn.text)
    except Exception as e:
        print("❌ 버튼 찾기 실패:", e)
        
    driver.quit()
    print("Selenium 테스트 완료")

if __name__ == "__main__":
    test_selenium()
