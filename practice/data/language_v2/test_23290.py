import sys
import os

sys.path.append(r'c:\Users\osw\Desktop\Workspace\Projects\StepCode\practice\data\language_v2')

from crawl import scrape_baekjoon

urls = [
    "https://www.acmicpc.net/problem/23290",
    "https://www.acmicpc.net/problem/18576"
]

for url in urls:
    problem_id = url.split("/")[-1]
    title, md = scrape_baekjoon(url)
    with open(f"test_{problem_id}.md", "w", encoding="utf-8") as f:
        f.write(md)
    print(f"DONE {problem_id}")
