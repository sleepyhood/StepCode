import re
import os
import time
import markdown # <-- 새로 추가 (마크다운을 HTML로 변환)

try:
    import frontmatter
except ImportError:
    pass  # GUI에서 설치 안내 예정

from playwright.sync_api import sync_playwright

# uploader_engine.py 내부에 추가 및 수정
import json

# ==========================================
# 신규 추가: 로그인 전용 함수 (세션 저장)
# ==========================================
def perform_login(admin_id, admin_pwd, state_path="state.json", log_callback=print):
    """독립된 로그인 과정을 수행하고 세션(쿠키)을 파일로 저장합니다."""
    log_callback("[로그인 시작] 브라우저를 기동합니다...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            log_callback(" > [1/3] CSRF 토큰 확보를 위해 /api/profile 접속")
            page.goto("http://edu.doingcoding.com/api/profile", wait_until="domcontentloaded")
            time.sleep(1)
            
            login_url = "http://edu.doingcoding.com/admin/login"
            log_callback(f" > [2/3] 로그인 페이지 이동: {login_url}")
            page.goto(login_url, wait_until="domcontentloaded")
            
            page.wait_for_selector('//*[@id="app"]/form/div[1]/div/div/input')
            page.locator('//*[@id="app"]/form/div[1]/div/div/input').fill(admin_id)
            pw_input = page.locator('//*[@id="app"]/form/div[2]/div/div/input')
            pw_input.fill(admin_pwd)
            
            log_callback(" > [3/3] 로그인 정보 제출 및 세션 대기")
            pw_input.press("Enter")
            
            page.wait_for_timeout(1000)
            if "/admin/login" in page.url:
                page.locator('//*[@id="app"]/form/div[3]/div/button').click()
            
            page.wait_for_function("() => !window.location.pathname.includes('/admin/login')", timeout=10000)
            log_callback(" > 로그인 성공 확인 완료.")
            
            # [핵심] 로그인 성공 시 현재 브라우저의 쿠키/세션을 JSON으로 저장
            context.storage_state(path=state_path)
            log_callback(f" > ✅ 로그인 세션 저장 완료 ({state_path})")
            return True
            
        except Exception as e:
            log_callback(f" > ❌ 로그인 실패: {e}")
            return False
        finally:
            browser.close()

def parse_markdown(md_path):
    """MD 파일을 읽어 딕셔너리로 반환"""
    with open(md_path, 'r', encoding='utf-8-sig') as f:
        post = frontmatter.load(f)
    
    data = {
        'id': post.get('id', ''),
        'title': post.get('title', ''),
        'tags': post.get('tags', []),
        'supported_languages': post.get('supported_languages', []),
        'description': '',
        'input_desc': '',
        'output_desc': '',
        'hint': '',
        'samples': []
    }
    
    content = post.content
    
    # 정규식으로 각 섹션 추출
    desc_match = re.search(r'## 1\. 문제 설명\n(.*?)(?=## 2\. 입출력 설명|## 3\. 예시|## 4\. 힌트|$)', content, re.DOTALL)
    if desc_match:
        data['description'] = desc_match.group(1).strip()
        
    # ==========================================
    # 수정: 마크다운 기호를 무시하고 깔끔하게 입/출력 분리
    # ==========================================
    io_match = re.search(r'## 2\. 입출력 설명\n(.*?)(?=## 3\. 예시|## 4\. 힌트|$)', content, re.DOTALL)
    if io_match:
        io_content = io_match.group(1).strip()
        
        # '입력'과 '출력' 키워드 주변의 각종 마크다운 특수기호(*, -, #, 공백)를 모두 무시하고 자르는 똑똑한 정규식
        in_pattern = r'(?:^|\n)[\*\s\#\-]*\**입력(?: 설명)?\**\s*[:-]?\s*\n*(.*?)(?=(?:^|\n)[\*\s\#\-]*\**출력(?: 설명)?\**\s*[:-]?|$)'
        out_pattern = r'(?:^|\n)[\*\s\#\-]*\**출력(?: 설명)?\**\s*[:-]?\s*\n*(.*)'
        
        in_match = re.search(in_pattern, io_content, re.DOTALL | re.IGNORECASE)
        out_match = re.search(out_pattern, io_content, re.DOTALL | re.IGNORECASE)
        
        if out_match:
            data['input_desc'] = in_match.group(1).strip() if in_match else io_content
            data['output_desc'] = out_match.group(1).strip()
        else:
            # 기본적으로 반반 나누기 어렵지만, 줄바꿈으로 대략 추정
            parts = io_content.split('\n\n')
            data['input_desc'] = parts[0].strip() if len(parts) > 0 else ''
            data['output_desc'] = parts[1].strip() if len(parts) > 1 else ''

    hint_match = re.search(r'## 4\. 힌트\n(.*?)$', content, re.DOTALL)
    if hint_match:
        data['hint'] = hint_match.group(1).strip()

    # 예시 추출 (정규표현식)
    # ### 예시 입력 1\n```text\n(내용)\n```
    sample_in_matches = re.finditer(r'###\s*예시 입력\s*\d+\n*(?:```text\n|```\n)?(.*?)(?:```\n|```$)', content, re.DOTALL)
    sample_out_matches = re.finditer(r'###\s*예시 출력\s*\d+\n*(?:```text\n|```\n)?(.*?)(?:```\n|```$)', content, re.DOTALL)
    
    in_list = [m.group(1).strip() for m in sample_in_matches]
    out_list = [m.group(1).strip() for m in sample_out_matches]
    
    for i in range(min(len(in_list), len(out_list))):
        data['samples'].append((in_list[i], out_list[i]))

    return data

# ==========================================
# 수정 1: 리치 텍스트 에디터 주입 함수 변경
# ==========================================
# ==========================================
# 수정: 정확한 마크다운 버튼 XPath를 기반으로 작동하는 함수
# ==========================================
# ==========================================
# 수정 2: 포커스 뺏김 방지 및 정확한 텍스트 에어리어 타겟팅
# ==========================================
# ==========================================
# 최종 수정: 정확한 버튼 XPath와 텍스트창 XPath를 직접 받아 처리
# ==========================================
def fill_rich_text(page, md_btn_xpath, textarea_xpath, text):
    """마크다운 버튼을 클릭하고, 정확하게 지정된 textarea에 값을 채우는 함수"""
    if not text: return

    try:
        # (1) 마크다운 모드 ON (버튼 클릭)
        page.locator(md_btn_xpath).click()
        time.sleep(0.5) 
        
        # (2) 찾아주신 정확한 textarea에 텍스트 주입
        # force=True를 주어 숨겨져 있던 창이 활성화되는 찰나의 방해를 무시합니다.
        page.locator(textarea_xpath).click(force=True)
        page.locator(textarea_xpath).fill(text)
        time.sleep(0.5)
        
        # (3) 마크다운 모드 OFF (다시 클릭하여 위지윅으로 렌더링)
        page.locator(md_btn_xpath).click()
        time.sleep(0.5)
        
    except Exception as e:
        print(f" > 에디터 입력 중 오류 발생: {e}")
        return

    # # 1. 마크다운을 HTML로 변환 (표, 코드블록, 줄바꿈 인식 확장기능 포함)
    # html_content = markdown.markdown(text, extensions=['fenced_code', 'tables', 'nl2br'])
    
    # # 2. 에디터 영역에 HTML 통째로 주입 후 강제 업데이트 이벤트 발생
    # page.evaluate(f"""(xpath, html) => {{
    #     const editor = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    #     if (editor) {{
    #         editor.innerHTML = html;
    #         // 에디터(Simditor)가 변경된 HTML을 인식하여 백그라운드 폼에 반영하도록 이벤트 트리거
    #         editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
    #         editor.dispatchEvent(new Event('keyup', {{ bubbles: true }}));
    #         editor.dispatchEvent(new Event('blur', {{ bubbles: true }}));
    #     }}
    # }}""", xpath, html_content)
    # time.sleep(0.5)

# def fill_rich_text(page, xpath, text):
#     """리치 텍스트 에디터(div)에 값 채우기"""
#     if not text: return
#     locator = page.locator(xpath)
#     locator.click()
#     page.keyboard.insert_text(text)
#     time.sleep(0.5)

# def run_uploader(target_url, md_path, zip_path, admin_id="", admin_pwd="", log_callback=print):
def run_uploader(target_url, md_path, zip_path, state_path="state.json", log_callback=print):
    try:
        import frontmatter
    except ImportError:
        log_callback("에러: python-frontmatter 모듈이 설치되어 있지 않습니다. 'pip install python-frontmatter'를 실행하세요.")
        return False
        
    log_callback(f"[1/4] 마크다운 파싱 시작: {md_path}")
    try:
        data = parse_markdown(md_path)
        log_callback(f" > 파싱 완료: {data['title']} (예시 {len(data['samples'])}개)")
    except Exception as e:
        log_callback(f" > 파싱 에러: {e}")
        return False

    log_callback("[2/4] 브라우저 기동 (수동 로그인 대기 가능)")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # [핵심] 저장된 세션(쿠키) 파일이 있으면 적용하여 컨텍스트 생성
        if os.path.exists(state_path):
            context = browser.new_context(storage_state=state_path)
            log_callback(" > 인증된 세션(state.json)을 성공적으로 불러왔습니다.")
        else:
            context = browser.new_context()
            log_callback(" > ⚠️ 세션 파일이 없습니다. 로그아웃 상태일 수 있습니다.")
            
        page = context.new_page()
        
        # context = browser.new_context()
        # page = context.new_page()
        
        # 0. 관리자 로그인 (DoingCoding 특화 로직)
        # if admin_id and admin_pwd:
        #     try:
        #         # [단계 1] CSRF 토큰 및 쿠키 확보를 위한 시드 주소 접속
        #         log_callback(" > [로그인 1/3] CSRF 토큰 확보를 위해 /api/profile 접속")
        #         page.goto("http://edu.doingcoding.com/api/profile", wait_until="domcontentloaded")
        #         time.sleep(1)
                
        #         # [단계 2] 로그인 페이지 접속 및 입력
        #         login_url = "http://edu.doingcoding.com/admin/login"
        #         log_callback(f" > [로그인 2/3] 로그인 페이지 이동: {login_url}")
        #         page.goto(login_url, wait_until="domcontentloaded")
                
        #         # 셀렉터 대기
        #         page.wait_for_selector('//*[@id="app"]/form/div[1]/div/div/input')
                
        #         page.locator('//*[@id="app"]/form/div[1]/div/div/input').fill(admin_id)
        #         pw_input = page.locator('//*[@id="app"]/form/div[2]/div/div/input')
        #         pw_input.fill(admin_pwd)
                
        #         # [단계 3] 여러 방식으로 제출 시도 (Enter가 가장 확실함)
        #         log_callback(" > [로그인 3/3] 로그인 정보 제출 및 세션 대기")
        #         pw_input.press("Enter") # 1차 시도: Enter 키
                
        #         # 만약 페이지가 바뀌지 않는다면 클릭 시도
        #         page.wait_for_timeout(1000)
        #         if "/admin/login" in page.url:
        #             page.locator('//*[@id="app"]/form/div[3]/div/button').click()
                
        #         # 로그인 성공 대기 (URL에서 /admin/login이 사라질 때까지)
        #         page.wait_for_function(
        #             """() => !window.location.pathname.includes('/admin/login')""",
        #             timeout=10000
        #         )
        #         log_callback(" > 로그인 성공 확인 완료.")
                
        #     except Exception as e:
        #         log_callback(f" > ⚠️ 관리자 로그인 실패: {e}")
        #         log_callback(" > (수동으로 로그인을 완료하시면 잠시 후 스크립트가 재개됩니다.)")
        #         # 수동 로그인 대기 (최대 1분)
        #         try:
        #             page.wait_for_function(
        #                 """() => !window.location.pathname.includes('/admin/login')""",
        #                 timeout=60000
        #             )
        #         except: pass
        # 1. 타겟 페이지로 이동
        log_callback(f" > 타겟 페이지로 이동: {target_url}")
        # page.goto(target_url, wait_until="networkidle")
        page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
        log_callback(" > 페이지 로딩 중... (입력 폼 대기)")

        # page.wait_for_selector("//input[@placeholder='번호']", timeout=30000)
        page.wait_for_selector("input[placeholder='번호'], input[placeholder='Display ID']", timeout=30000)
        log_callback(" > 웹 페이지 로드 완료. 폼 입력을 시작합니다...")
        
        # ==========================================
        # 수정 2: 번호 및 제목 주입 방식 변경
        # ==========================================
        try:
            # 깨지기 쉬운 절대 XPath 대신, placeholder 속성으로 튼튼하게 요소를 탐색합니다.
            # Vue.js 환경에서 가장 잘 작동하는 Playwright의 기본 fill() 메서드 사용.
            id_xpath = '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[1]/div[1]/div/div/div[1]/input'
            title_xpath = '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[1]/div[2]/div/div/div[1]/input'
            
            page.locator(id_xpath).fill(str(data['id']))
            time.sleep(1)
            page.locator(title_xpath).fill(data['title'])
            time.sleep(1)

            log_callback(f" > 기본 정보(ID, 제목) 입력 완료.")
        except Exception as e:
            log_callback(f" > 기본 정보 입력 실패: {e}")
            
        # 2. 본문 리치 텍스트 (click & insert_text)
        # 2. 본문 리치 텍스트 (버튼 XPATH와 텍스트창 XPATH 명시적 전달)
        try:
            # 1) 문제 설명
            fill_rich_text(
                page, 
                '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[2]/div/div/div/div/div[1]/div[1]/ul/li[19]/a', 
                '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[2]/div/div/div/div/div[1]/div[3]/textarea',
                data['description']
            )
            
            # 2) 입력 설명
            fill_rich_text(
                page, 
                '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[3]/div[1]/div/div/div/div[1]/div[1]/ul/li[19]/a', 
                '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[3]/div[1]/div/div/div/div[1]/div[3]/textarea',
                data['input_desc']
            )
            
            # 3) 출력 설명
            fill_rich_text(
                page, 
                '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[3]/div[2]/div/div/div/div[1]/div[1]/ul/li[19]/a', 
                '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[3]/div[2]/div/div/div/div[1]/div[3]/textarea',
                data['output_desc']
            )
            
            # 4) 힌트 (데이터가 있을 경우에만)
            if data['hint']:
                fill_rich_text(
                    page, 
                    '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[8]/div/div/div[1]/div[1]/ul/li[19]/a', 
                    '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[8]/div/div/div[1]/div[3]/textarea',
                    data['hint']
                )
                
        except Exception as e:
            log_callback(f" > 본문 입력 실패: {e}")

        # ==========================================
        # 신규: 지원 언어 체크박스 제어 로직
        # ==========================================
        try:
            log_callback(" > 지원 언어 설정을 동기화합니다...")
            # 1. 언어별 XPath 매핑 딕셔너리
            language_xpaths = {
                "C": '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[5]/div[4]/div/div/div/label[1]/span[1]/input',
                "C++": '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[5]/div[4]/div/div/div/label[2]/span[1]/input',
                "Java": '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[5]/div[4]/div/div/div/label[3]/span[1]/input',
                "Python2": '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[5]/div[4]/div/div/div/label[4]/span[1]/input',
                "Python3": '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[5]/div[4]/div/div/div/label[5]/span[1]/input',
                "Golang": '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[5]/div[4]/div/div/div/label[6]/span[1]/input'
            }

            # 2. 모든 체크박스를 강제로 해제 (False 초기화)
            # 숨겨진 input 태그일 수 있으므로 force=True 옵션 사용
            for xpath in language_xpaths.values():
                page.locator(xpath).uncheck(force=True)
            time.sleep(0.5)

            # 3. MD 파일의 프론트매터에 정의된 언어만 골라서 체크 (True 설정)
            for lang in data.get('supported_languages', []):
                if lang in language_xpaths:
                    page.locator(language_xpaths[lang]).check(force=True)
            
            log_callback(" > 언어 설정 동기화 완료.")
        except Exception as e:
            log_callback(f" > 언어 설정 실패: {e}")

        # 3. 태그 입력
        try:
            for tag in data['tags']:
                page.locator('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[5]/div[3]/div/div/button').click()
                time.sleep(0.2)
                tag_input = page.locator('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[5]/div[3]/div/div/div/div[1]/input')
                tag_input.fill(tag)
                tag_input.press("Enter")
                time.sleep(0.2)
        except Exception as e:
            log_callback(f" > 태그 입력 실패: {e}")

        # 4. 예시 입력
        try:
            for i, (sample_in, sample_out) in enumerate(data['samples']):
                if i > 0:
                    page.locator('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[7]/button').click()
                    time.sleep(0.5)
                
                # 동적 XPath 생성
                idx_str = f"[{i+1}]" if i > 0 else ""
                base_xpath = f'//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[6]/div{idx_str}/div/div/div/div'
                
                # textarea에 값 채우기 (textarea는 보통 fill이 작동함)
                in_ta = page.locator(f'{base_xpath}/div[1]/div/div/div/textarea')
                out_ta = page.locator(f'{base_xpath}/div[2]/div/div/div/textarea')
                
                in_ta.fill(sample_in)
                out_ta.fill(sample_out)
        except Exception as e:
            log_callback(f" > 샘플 입력 실패: {e}")

        # 5. ZIP 업로드
        log_callback(f"[3/4] 테스트케이스 ZIP 업로드: {zip_path}")
        try:
            if os.path.exists(zip_path):
                with page.expect_file_chooser() as fc_info:
                    page.locator('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[11]/div[2]/div/div/div/div/button').click()
                file_chooser = fc_info.value
                file_chooser.set_files(zip_path)
                log_callback(" > ZIP 파일 선택 완료")
            else:
                log_callback(" > ⚠️ ZIP 파일을 찾을 수 없어 업로드를 생략합니다.")
        except Exception as e:
            log_callback(f" > ZIP 업로드 실패: {e}")

        log_callback("[4/4] 폼 입력 완료! 브라우저 창에서 최종 확인 후 저장 버튼을 직접 눌러주세요.")
        log_callback("종료를 원하시면 창을 닫거나 스크립트를 중지하세요.")
        
        # 수동 확인을 위해 잠시 대기
        try:
            page.wait_for_timeout(600000) # 10분 대기 (그 전에 창 닫으면 예외 발생하며 종료)
        except:
            pass

    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 5:
        run_uploader(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif len(sys.argv) > 3:
        run_uploader(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python uploader_engine.py <URL> <MD_PATH> <ZIP_PATH> [ADMIN_ID] [ADMIN_PWD]")
