import os
import sys
import tkinter as tk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Resources.tools.extract_scores import ScoreExtractorApp

def run_test():
    root = tk.Tk()
    app = ScoreExtractorApp(root)
    root.update()
    
    # stdout으로 출력되도록 log 함수 덮어쓰기
    original_log = app.log
    def print_log(msg):
        print(f"[LOG] {msg}", flush=True)
        original_log(msg)
    app.log = print_log

    print("실제 세션 로그인 로직(Playwright) 검증 시작...", flush=True)
    try:
        session = app._login_playwright("http://edu.doingcoding.com", "test_user", "test_pass", False)
        if session:
            print("세션 획득 성공! 쿠키 내역:")
            print(session.cookies.get_dict())
        else:
            print("세션을 반환받지 못했습니다. (비밀번호 오류일 수 있으나 로직 자체는 진행됨)")
    except Exception as e:
        print("로그인 로직 진행 중 에러 발생:", e)
        
    print("검증 종료.", flush=True)
    root.destroy()

if __name__ == "__main__":
    run_test()
