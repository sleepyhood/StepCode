import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

random.seed(1804 + case_num)

if case_num == 1:
    print("http://a.com?age=1&score=1")
elif case_num == 2:
    print("http://site.com/page?age=25&score=100")
elif case_num == 3:
    print("http://site.com/page?age=15&score=200")
elif case_num == 15:
    print("http://sub.domain.site.com/v1/user/profile/query?score=1000&extra=xyz&age=1000")
else:
    age = random.randint(1, 999)
    score = random.randint(1, 999)
    domains = ["http://myweb.com/api", "https://service.net/user", "http://app.io/v2", "https://test.kr/page"]
    base = random.choice(domains)
    if random.choice([True, False]):
        url = f"{base}?age={age}&score={score}"
    else:
        url = f"{base}?param=val&score={score}&tag=abc&age={age}"
    print(url)
