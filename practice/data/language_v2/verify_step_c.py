"""
Step C 검증: 5개 시나리오 전체 분기 경로 시뮬레이션
 - S0: 404 dummy 존재 → SKIP
 - S1: 파일 없음 → SKIP
 - S2: 특수 배지 존재 → Full Re-crawl
 - S3: 일반 배지, 정위치 → CORRECT_SKIP
 - S4: 일반 배지, 위치 틀림 → PATCH_ONLY
 - S5: badges 없는 레거시 → LIGHT_CRAWL
"""
import os, sys, shutil, json
sys.path.insert(0, r"c:\Users\osw\Desktop\Workspace\Projects\StepCode\practice\data\language_v2")
from crawl import analyze_badge_status, has_special_badge, patch_file_badges

TEST_DIR = r"c:\Users\osw\Desktop\Workspace\Projects\StepCode\practice\data\language_v2\_test_step_c"
DUMMY_DIR = os.path.join(TEST_DIR, "404_not_found")
os.makedirs(TEST_DIR, exist_ok=True)
os.makedirs(DUMMY_DIR, exist_ok=True)

def make_file(path, content):
    with open(path, "w", encoding="utf-8-sig") as f:
        f.write(content)

# 파일 생성
make_file(os.path.join(DUMMY_DIR, "bj_9999.md"), "---\nis_existent: false\n---\n")
make_file(os.path.join(TEST_DIR, "bj_2000.md"), """\
---
id: bj_2000
badges: ["인터랙티브"]
source_url: "https://www.acmicpc.net/problem/2000"
---
""")
make_file(os.path.join(TEST_DIR, "bj_3000.md"), """\
---
id: bj_3000
badges: ["다국어"]
source_url: "https://www.acmicpc.net/problem/3000"
---
""")
make_file(os.path.join(TEST_DIR, "bj_4000.md"), """\
---
id: bj_4000
source_url: "https://www.acmicpc.net/problem/4000"
badges: ["다국어"]
---
""")
make_file(os.path.join(TEST_DIR, "bj_5000.md"), """\
---
id: bj_5000
source_url: "https://www.acmicpc.net/problem/5000"
---
""")

def simulate(current_id):
    filename = f"bj_{current_id}.md"
    base_fp = os.path.join(TEST_DIR, filename)
    dummy_fp = os.path.join(DUMMY_DIR, filename)
    logs = []

    # GUARD-1
    if os.path.exists(dummy_fp):
        return "SKIPPED_404", logs

    # GUARD-2
    if not os.path.exists(base_fp):
        return "SKIPPED_NOFILE", logs

    # STEP 1
    status, badges = analyze_badge_status(base_fp)
    logs.append(f"status={status}, badges={badges}")

    # STEP 2
    if has_special_badge(badges):
        return "FULL_RECRAWL", logs
    elif status == "CORRECT":
        return "CORRECT_SKIP", logs
    elif status == "WRONG_POSITION":
        return "PATCH_ONLY", logs
    else:
        return "LIGHT_CRAWL", logs

scenarios = [
    (9999, "SKIPPED_404",   "404 더미 파일 존재"),
    (8888, "SKIPPED_NOFILE","파일 자체 없음"),
    (2000, "FULL_RECRAWL",  "특수 배지(인터랙티브) → Full Re-crawl"),
    (3000, "CORRECT_SKIP",  "일반 배지 + 정위치 → 스킵"),
    (4000, "PATCH_ONLY",    "일반 배지 + 위치 틀림 → 패치만"),
    (5000, "LIGHT_CRAWL",   "badges 없는 레거시 → 경량 크롤링"),
]

print("=" * 60)
print("Step C: 전체 분기 시뮬레이션")
print("=" * 60)
all_pass = True
for id_, expected, desc in scenarios:
    result, logs = simulate(id_)
    ok = result == expected
    if not ok: all_pass = False
    s = "✅ PASS" if ok else "❌ FAIL"
    print(f"[{s}] ID={id_} | {desc}")
    print(f"  기대: {expected} / 실제: {result}")
    for l in logs: print(f"  LOG: {l}")

print()
print("최종:", "✅ 전체 통과" if all_pass else "❌ 실패 케이스 있음")
shutil.rmtree(TEST_DIR)
print("임시 파일 정리 완료")
