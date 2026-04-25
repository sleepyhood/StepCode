import os
import sys
import tkinter as tk
from unittest.mock import patch, MagicMock

# 모듈 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Resources.tools.extract_scores import ScoreExtractorApp

def run_test():
    root = tk.Tk()
    app = ScoreExtractorApp(root)
    
    # requests.Session 모킹
    with patch('requests.Session') as MockSession:
        mock_session_instance = MagicMock()
        MockSession.return_value = mock_session_instance
        
        # 1. GET 요청 시 가상의 csrftoken 쿠키 반환 설정
        mock_session_instance.cookies.get.side_effect = lambda k: "fake_csrf_token_123" if k == 'csrftoken' else None
        
        # 2. POST 요청 시 정상 응답 반환 설정
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {"error": None, "data": "success"}
        mock_session_instance.post.return_value = mock_post_response
        
        # _login 함수 호출
        result = app._login("http://dummy-url.com", "admin", "password123")
        
        # 검증 로직
        assert result is not None, "로그인이 성공해야 하지만 None을 반환했습니다."
        assert result == mock_session_instance, "반환된 세션이 올바르지 않습니다."
        
        # GET 호출 확인
        mock_session_instance.get.assert_called_with("http://dummy-url.com", timeout=10)
        
        # POST 호출 인자 확인
        call_args = mock_session_instance.post.call_args
        assert call_args is not None, "POST 요청이 호출되지 않았습니다."
        
        url, = call_args[0]
        kwargs = call_args[1]
        
        assert url == "http://dummy-url.com/api/login"
        assert kwargs['json'] == {"username": "admin", "password": "password123"}
        assert "X-CSRFToken" in kwargs['headers']
        assert kwargs['headers']["X-CSRFToken"] == "fake_csrf_token_123"
        assert kwargs['headers']["Referer"] == "http://dummy-url.com/login"
        
        print("✅ 자체 검증(Mock Test) 완료: CSRF 토큰 추출 및 헤더 삽입, 로그인 로직이 완벽하게 동작합니다.")

if __name__ == "__main__":
    run_test()
