"""
gui_crawler.py의 light_mode 분기에 추가된 GUARD 로직을 시뮬레이션하여 검증합니다.
실제 Playwright 없이 순수 파일 존재 여부 기반으로 동작 흐름을 추적합니다.
"""
import os
import shutil
import json

TEST_DIR = r"c:\Users\osw\Desktop\Workspace\Projects\StepCode\practice\data\language_v2\_test_guard_verify"
DUMMY_DIR = os.path.join(TEST_DIR, "404_not_found")
os.makedirs(TEST_DIR, exist_ok=True)
os.makedirs(DUMMY_DIR, exist_ok=True)

# --- 테스트용 파일 준비 ---
# Case A: 정상 파일 (CORRECT 배지)
with open(os.path.join(TEST_DIR, "bj_1000.md"), "w", encoding="utf-8-sig") as f:
    f.write("""---
id: bj_1000
badges: ["다국어"]
source_url: "https://www.acmicpc.net/problem/1000"
---
# 본문
""")

# Case B: 404 더미 파일
with open(os.path.join(DUMMY_DIR, "bj_9999.md"), "w", encoding="utf-8-sig") as f:
    f.write("""---
id: bj_9999
is_existent: false
---
""")

# Case C: 원본 파일 자체가 없음 (신규 ID)
# bj_5555.md → 존재하지 않음

# --- GUARD 로직 시뮬레이션 ---
sys_path_temp = r"c:\Users\osw\Desktop\Workspace\Projects\StepCode\practice\data\language_v2"
import sys
sys.path.insert(0, sys_path_temp)
from crawl import analyze_badge_status

def simulate_light_mode(current_id, save_path):
    filename = f"bj_{current_id}.md"
    base_filepath = os.path.join(save_path, filename)
    dummy_dir = os.path.join(save_path, "404_not_found")
    dummy_filepath = os.path.join(dummy_dir, filename)

    log_lines = []

    # [GUARD 1] 404 더미 파일 존재 여부
    if os.path.exists(dummy_filepath):
        log_lines.append(f"⏩ [Light] {current_id}번: 삭제된 문제 (404) - 스킵")
        return "SKIPPED_404", log_lines

    # [GUARD 2] 원본 파일 미존재 여부
    if not os.path.exists(base_filepath):
        log_lines.append(f"⏩ [Light] {current_id}번: 기존 파일 없음 - 스킵")
        return "SKIPPED_NOFILE", log_lines

    # [STEP 1] 상태 분석
    status, badges = analyze_badge_status(base_filepath)
    log_lines.append(f"  analyze → Status: {status}, Badges: {badges}")

    if status == "CORRECT":
        log_lines.append(f"✅ [Light] {current_id}번: 이미 정위치에 존재 - 스킵")
        return "CORRECT_SKIP", log_lines
    elif status == "WRONG_POSITION":
        log_lines.append(f"🔧 [Light] {current_id}번: 위치 교정 중...")
        return "PATCHED", log_lines
    else:
        log_lines.append(f"🏃 [Light] {current_id}번: 정보 없음 - 크롤링 시작...")
        return "CRAWL_NEEDED", log_lines


# --- 검증 실행 ---
test_cases = [
    (1000, "정상 파일 (배지 정위치)"),
    (9999, "404 더미 파일 존재"),
    (5555, "원본 파일 없음 (신규 ID)"),
]

print("=" * 55)
print("GUARD 로직 시뮬레이션 검증")
print("=" * 55)
expected = {1000: "CORRECT_SKIP", 9999: "SKIPPED_404", 5555: "SKIPPED_NOFILE"}
all_pass = True

for id_, desc in test_cases:
    result, logs = simulate_light_mode(id_, TEST_DIR)
    ok = result == expected[id_]
    status_str = "✅ PASS" if ok else "❌ FAIL"
    print(f"\n[{status_str}] ID={id_} | {desc}")
    print(f"  기대: {expected[id_]} / 실제: {result}")
    for line in logs:
        print(f"  LOG: {line}")
    if not ok:
        all_pass = False

print()
print("=" * 55)
print("최종 결과:", "✅ 전체 통과" if all_pass else "❌ 실패 케이스 있음")

# 정리
shutil.rmtree(TEST_DIR)
print("임시 파일 정리 완료")
