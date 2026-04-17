from playwright.sync_api import sync_playwright

def test_api_request():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        url = "https://solved.ac/api/v3/problem/show?problemId=1000"
        
        print("Fetching via context request...")
        response = context.request.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
        print("Status:", response.status)
        try:
            print("Response:", response.json())
        except Exception as e:
            print("Error parsing JSON:", e)

        print("\nFetching via page.evaluate fetch...")
        try:
            page.goto("https://solved.ac/")
            page.wait_for_timeout(3000) # wait for cloudflare to pass on solved.ac
            json_data = page.evaluate("""async () => {
                const res = await fetch('https://solved.ac/api/v3/problem/show?problemId=1000');
                return await res.json();
            }""")
            print("Fetch returned:", json_data.get('problemId'))
        except Exception as e:
            print("Fetch failed:", e)

        browser.close()

if __name__ == "__main__":
    test_api_request()
