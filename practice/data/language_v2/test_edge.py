import sys
import os

sys.path.append(r'c:\Users\osw\Desktop\Workspace\Projects\StepCode\practice\data\language_v2')

from crawl import scrape_baekjoon

urls = [
    "https://www.acmicpc.net/problem/18576",
    "https://www.acmicpc.net/problem/15683",
    "https://www.acmicpc.net/problem/18831",
    "https://www.acmicpc.net/problem/33452",
    "https://www.acmicpc.net/problem/14891",
    "https://www.acmicpc.net/problem/23290",
    "https://www.acmicpc.net/problem/34844",
    "https://www.acmicpc.net/problem/32666",
]

for url in urls:
    problem_id = url.split("/")[-1]
    print(f"Testing URL: {url}")
    try:
        title, md = scrape_baekjoon(url)
        if title is None:
            print(f"  FAILED: returned None")
        else:
            print(f"  SUCCESS: {title}")
            with open(f"test_{problem_id}.md", "w", encoding="utf-8") as f:
                f.write(md)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
