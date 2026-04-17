import requests

def test_requests():
    url = "https://solved.ac/api/v3/problem/show?problemId=1000"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    print("Requests Status:", response.status_code)
    try:
        print("Response:", response.json())
    except Exception as e:
        print("Error parsing JSON:", e)
        print("Text:", response.text[:200])

if __name__ == "__main__":
    test_requests()
