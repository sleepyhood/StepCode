import re
import json
import os
import sys

# crawl.py를 직접 import해서 두 함수가 정상 동작하는지 확인
script_dir = r"c:\Users\osw\Desktop\Workspace\Projects\StepCode\practice\data\language_v2"
sys.path.insert(0, script_dir)

from crawl import analyze_badge_status, patch_file_badges

print("✅ Import 성공: analyze_badge_status, patch_file_badges\n")

# ----- 테스트용 임시 파일 생성 -----
TEST_DIR = os.path.join(script_dir, "_test_badge_verify")
os.makedirs(TEST_DIR, exist_ok=True)

cases = [
    ("CORRECT_case.md", """---
id: bj_1000
tag_keys: ["math"]
badges: ["스페셜 저지"]
source_url: "https://www.acmicpc.net/problem/1000"
---
# 본문
"""),
    ("WRONG_POSITION_case.md", """---
id: bj_1001
tag_keys: ["math"]
source_url: "https://www.acmicpc.net/problem/1001"
badges: ["인터랙티브"]
---
# 본문
"""),
    ("MISSING_case.md", """---
id: bj_1002
tag_keys: ["math"]
source_url: "https://www.acmicpc.net/problem/1002"
---
# 본문
"""),
]

for fname, content in cases:
    fpath = os.path.join(TEST_DIR, fname)
    with open(fpath, "w", encoding="utf-8-sig") as f:
        f.write(content)

# ---- 테스트 실행 -----
print("=" * 50)
for fname, _ in cases:
    fpath = os.path.join(TEST_DIR, fname)
    status, badges = analyze_badge_status(fpath)
    print(f"[{fname}] => Status: {status}, Badges: {badges}")

    if status == "WRONG_POSITION":
        result = patch_file_badges(fpath, badges)
        with open(fpath, "r", encoding="utf-8-sig") as f:
            patched = f.read()
        print(f"  → 패치 결과: {result}")
        print(f"  → 패치된 프론트매터:\n{patched[:300]}")
        # 재검증
        status2, badges2 = analyze_badge_status(fpath)
        print(f"  → 재검증 Status: {status2}, Badges: {badges2}")
    print()

# ---- 클린업 -----
import shutil
shutil.rmtree(TEST_DIR)
print("✅ 테스트 완료 및 임시 파일 정리됨")
