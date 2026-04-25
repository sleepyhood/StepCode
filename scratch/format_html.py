import bs4

with open("scratch/debug_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, "html.parser")
pretty = soup.prettify()

with open("scratch/debug_page_pretty.html", "w", encoding="utf-8") as f:
    f.write(pretty)
