from crawl import scrape_baekjoon
import os

def test():
    # Test scraping problem 1000
    print("Testing scrape_baekjoon for problem 1000")
    # Using context=None, so scrape_baekjoon will create its own browser and context
    title, md = scrape_baekjoon("https://www.acmicpc.net/problem/1000", save_dir=os.getcwd())
    print("Title:", title)
    if md:
        # Check if tier is printed
        print("MD length:", len(md))
        print("First 200 chars:")
        print(md[:200])

if __name__ == "__main__":
    test()
