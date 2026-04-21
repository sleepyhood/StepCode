import os
import sys
from crawl import scrape_baekjoon
from playwright.sync_api import sync_playwright

def test():
    save_dir = os.path.join(os.getcwd(), "test_output")
    os.makedirs(save_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        print("Scraping 1000...")
        title, md_content = scrape_baekjoon("https://www.acmicpc.net/problem/1000", save_dir=save_dir, context=context)
        print("Title:", title)
        print("MD Content length:", len(md_content) if md_content else 0)
        
        print("Scraping 1001...")
        title2, md_content2 = scrape_baekjoon("https://www.acmicpc.net/problem/1001", save_dir=save_dir, context=context)
        print("Title:", title2)
        print("MD Content length:", len(md_content2) if md_content2 else 0)
        
        context.close()
        browser.close()

if __name__ == "__main__":
    test()
