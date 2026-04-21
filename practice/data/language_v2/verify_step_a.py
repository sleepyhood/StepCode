"""Step A 검증: SPECIAL_BADGES 상수와 has_special_badge() 함수 단위 테스트"""
import sys
sys.path.insert(0, r"c:\Users\osw\Desktop\Workspace\Projects\StepCode\practice\data\language_v2")
from crawl import SPECIAL_BADGES, has_special_badge

tests = [
    (["다국어"],                              False,  "일반 배지만"),
    (["인터랙티브"],                          True,   "인터랙티브"),
    (["스페셜 저지", "다국어"],               True,   "스페셜 저지 + 다국어"),
    ([],                                     False,  "빈 리스트"),
    (["채점 준비 중"],                        True,   "채점 준비 중"),
    (["함수 구현", "클래스 구현"],            True,   "함수/클래스 구현"),
    (["다국어", "피드백"],                    True,   "피드백"),
    (["서브태스크", "점수"],                  True,   "서브태스크+점수"),
]

print("=" * 55)
print("Step A: has_special_badge() 단위 테스트")
print("=" * 55)
all_pass = True
for badges, expected, desc in tests:
    result = has_special_badge(badges)
    ok = result == expected
    if not ok:
        all_pass = False
    status = "✅ PASS" if ok else "❌ FAIL"
    print(f"  [{status}] {desc}: {badges} → {result} (기대: {expected})")

print()
print(f"SPECIAL_BADGES 집합 ({len(SPECIAL_BADGES)}개):", SPECIAL_BADGES)
print()
print("최종:", "✅ 전체 통과" if all_pass else "❌ 실패 케이스 있음")
