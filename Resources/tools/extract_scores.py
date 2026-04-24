import sys
import os
import json
import time
import requests
from urllib.parse import quote, urlparse

# --- Configuration ---
BASE_URL = "http://edu.doingcoding.com"
LOGIN_ID = "osw1110"
LOGIN_PW = "lucky636!"
COOKIE_FILE = "cookies_tool.json"
TARGET_PREFIX = "ky_2026_01_26682_"  # 추출할 문제 ID 접두사

def get_authenticated_session(cookie_dict):
    session = requests.Session()
    domain = urlparse(BASE_URL).hostname
    for name, value in cookie_dict.items():
        if name == "timestamp":
            continue
        session.cookies.set(name, value, domain=domain, path="/")
    return session

def is_session_valid(session):
    try:
        res = session.get(f"{BASE_URL}/api/profile", timeout=10)
        if res.status_code != 200:
            return False
        return res.json().get("data", {}).get("user") is not None
    except Exception:
        return False

def login_and_get_session():
    # 이 툴은 간단하게 requests를 이용한 로그인을 시도하거나, 
    # 기존 프로젝트의 쿠키 파일을 참조하도록 설계할 수 있습니다.
    # 여기서는 가장 간단한 형태의 세션 획득 로직을 구현합니다.
    
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "r") as f:
            cookies = json.load(f)
        session = get_authenticated_session(cookies)
        if is_session_valid(session):
            print("[Auth] Using existing session.", flush=True)
            return session

    print("[Auth] Creating new session...", flush=True)
    
    legacy_cookie_path = r"C:\Users\DCT2\Desktop\DCT2_공유폴더\learning-tracker-api\src\cookies\osw1110.json"
    if os.path.exists(legacy_cookie_path):
        with open(legacy_cookie_path, "r") as f:
            cookies = json.load(f)
        session = get_authenticated_session(cookies)
        if is_session_valid(session):
            print(f"[Auth] Successfully loaded cookies from {legacy_cookie_path}", flush=True)
            with open(COOKIE_FILE, "w") as f:
                json.dump(cookies, f)
            return session
    
    print("[Auth] Failed to secure a valid session.", flush=True)
    return None

def get_all_students(session):
    print("[Fetch] Fetching all students from user_rank...", flush=True)
    url = f"{BASE_URL}/api/user_rank?offset=0&limit=100&rule=ACM"
    all_users = []
    offset = 0
    limit = 100
    
    while True:
        try:
            res = session.get(f"{BASE_URL}/api/user_rank?offset={offset}&limit={limit}&rule=ACM", timeout=10)
            data = res.json()
            if not data or "data" not in data:
                break
            
            results = data["data"].get("results", [])
            if not results:
                break
                
            usernames = [entry["user"]["username"] for entry in results]
            all_users.extend(usernames)
            print(f"  > Loaded {len(all_users)} students...", flush=True)
            
            if len(results) < limit:
                break
            offset += limit
            time.sleep(0.1) # 서버 부하 방지
        except Exception as e:
            print(f"  ! Error fetching student list: {e}", flush=True)
            break
            
    print(f"[Fetch] Total students found: {len(all_users)}", flush=True)
    return all_users

def fetch_scores_for_students(session, usernames, target_prefix):
    print(f"[Score] Starting score extraction for {len(usernames)} students (Target Prefix: {target_prefix})...", flush=True)
    all_data = []
    
    # 디버깅/테스트를 위해 처음에는 20명만 추출해보고 싶을 수 있으나, 
    # 여기서는 사용자 요청대로 전체를 대상으로 합니다.
    # 단, 서버 부하를 고려하여 지연 시간을 둡니다.
    
    for i, username in enumerate(usernames):
        try:
            res = session.get(f"{BASE_URL}/api/profile?username={quote(username)}", timeout=10)
            data = res.json()
            
            if data.get("error"):
                print(f"  ! Error for {username}: {data['error']}", flush=True)
                continue
                
            problems = data.get("data", {}).get("oi_problems_status", {}).get("problems", {})
            
            # 필터링 및 점수 추출
            student_scores = {"username": username}
            found_any = False
            for p_id_numeric, p_info in problems.items():
                p_id_string = p_info.get("_id", "")
                if p_id_string.startswith(target_prefix):
                    student_scores[p_id_string] = p_info.get("score", 0)
                    found_any = True
            
            if found_any:
                all_data.append(student_scores)
            
            if (i + 1) % 50 == 0:
                print(f"  > Processed {i + 1}/{len(usernames)} students...", flush=True)
            
            time.sleep(0.15) # 서버 부하 방지
        except Exception as e:
            print(f"  ! Exception for {username}: {e}", flush=True)
            
    print(f"[Score] Extraction complete. Found relevant data for {len(all_data)} students.", flush=True)
    return all_data

def save_to_csv(data, filename):
    if not data:
        print("[Save] No data to save.", flush=True)
        return
        
    print(f"[Save] Formatting data and saving to {filename}...", flush=True)
    
    # 모든 문제 ID 수집 (컬럼명 확정)
    all_problem_ids = set()
    for row in data:
        for key in row.keys():
            if key != "username":
                all_problem_ids.add(key)
    
    # 문제 ID 정렬 (오름차순)
    sorted_problem_ids = sorted(list(all_problem_ids))
    fieldnames = ["username"] + sorted_problem_ids
    
    import csv
    try:
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                # 점수가 없는 칸은 0 또는 빈칸으로 채울 수 있음. 여기서는 0으로 채움.
                output_row = {field: row.get(field, 0) for field in fieldnames}
                writer.writerow(output_row)
        print(f"[Save] Successfully saved to {filename}", flush=True)
    except Exception as e:
        print(f"[Save] Error saving CSV: {e}", flush=True)

def print_summary(data):
    if not data:
        return
        
    print("\n" + "="*50)
    print("📊 [Summary] Score Report")
    print("="*50)
    
    # 문제 ID별 통계 계산
    problem_ids = []
    for row in data:
        for key in row.keys():
            if key != "username" and key not in problem_ids:
                problem_ids.append(key)
    
    problem_ids.sort()
    
    print(f"{'Problem ID':<25} | {'100pts Count':<12} | {'Avg Score':<10}")
    print("-" * 50)
    
    for pid in problem_ids:
        scores = [row.get(pid, 0) for row in data]
        count_100 = sum(1 for s in scores if s >= 100)
        avg_score = sum(scores) / len(scores) if scores else 0
        print(f"{pid:<25} | {count_100:<12} | {avg_score:<10.2f}")
    
    print("="*50 + "\n")

if __name__ == "__main__":
    session = login_and_get_session()
    if session:
        print("[Auth] Login Success!", flush=True)
        students = get_all_students(session)
        if students:
            # 실전: 전체 학생 대상
            scores_data = fetch_scores_for_students(session, students, TARGET_PREFIX)
            if scores_data:
                save_to_csv(scores_data, "student_scores.csv")
                print_summary(scores_data)
            else:
                print("[Main] No data found for the given prefix.", flush=True)
    else:
        print("[Auth] Login Failed.", flush=True)
