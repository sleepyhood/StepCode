from playwright.sync_api import sync_playwright
from lxml import html
from dataclasses import dataclass
import json
import os
import re
import shutil
import tempfile
import zipfile
from urllib.parse import urlparse
import requests
import time
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from datetime import datetime # 🚨 상단 임포트 섹션에 추가하거나 함수 내에 추가


# 기존 import들 아래에 추가
class ProblemNotFoundError(Exception):
    """문제가 서버에 존재하지 않는 경우(404) 발생하는 예외"""
    pass


class CustomMarkdownConverter(MarkdownConverter):
    def convert_sup(self, el, text, **kwargs):
        return f"<sup>{text}</sup>"
    def convert_sub(self, el, text, **kwargs):
        return f"<sub>{text}</sub>"
    def convert_u(self, el, text, **kwargs):
        return f"<u>{text}</u>"

def md(html, **options):
    return CustomMarkdownConverter(**options).convert(html)
from urllib.parse import urljoin

SECTION_HEADINGS = {
    "description": ["문제 설명", "문제설명", "설명"],
    "input": ["입력"],
    "output": ["출력"],
    "hint": ["힌트"],
}
REQUIRED_FIELD_PLACEHOLDERS = {"", "(내용 없음)"}
DOINGCODING_CSRF_SEED_URL = "http://edu.doingcoding.com/api/profile"
DOINGCODING_CSRF_FALLBACK_URL = "http://edu.doingcoding.com/api/website"
DOINGCODING_ADMIN_LOGIN_URL = "http://edu.doingcoding.com/admin/login"
DOINGCODING_ADMIN_PROBLEMS_URL = "http://edu.doingcoding.com/admin/problems"
DOINGCODING_ADMIN_ID_SELECTOR = 'xpath=//*[@id="app"]/form/div[1]/div/div/input'
DOINGCODING_ADMIN_PASSWORD_SELECTOR = 'xpath=//*[@id="app"]/form/div[2]/div/div/input'
DOINGCODING_ADMIN_LOGIN_BUTTON_SELECTOR = 'xpath=//*[@id="app"]/form/div[3]/div/button'
DOINGCODING_ADMIN_SEARCH_SELECTORS = [
    'xpath=//*[@id="app"]/div/div[3]/div[1]/div[1]/header/div[2]/div/div/input',
    'xpath=//*[@id="app"]//header//input',
    "css=header input",
    'css=input[type="text"]',
]
DOINGCODING_ADMIN_ROW_SELECTORS = [
    'xpath=//*[@id="app"]/div/div[3]/div[1]/div[1]/div/div[1]/div[4]/div[2]/table/tbody/tr',
    'xpath=//*[@id="app"]//table/tbody/tr',
    "css=table tbody tr",
]
DOINGCODING_ADMIN_DOWNLOAD_BUTTON_SELECTORS = [
    'xpath=//*[@id="app"]/div/div[3]/div[1]/div[1]/div/div[1]/div[4]/div[2]/table/tbody/tr/td[7]/div/div/div[2]/button',
    'xpath=//*[@id="app"]//table/tbody/tr[1]//button',
    "css=table tbody tr button",
]
DOINGCODING_ADMIN_EDIT_BUTTON_SELECTORS = [
    'xpath=//*[@id="app"]/div/div[3]/div[1]/div[1]/div/div[1]/div[4]/div[2]/table/tbody/tr/td[7]/div/div/div[1]',
    'xpath=//*[@id="app"]//table/tbody/tr[1]/td[7]//div/div/div[1]',
]
DOINGCODING_ADMIN_TESTCASE_UPLOAD_BUTTON_SELECTORS = [
    'xpath=//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[11]/div[2]/div/div/div/div/button',
    'xpath=//*[@id="app"]//form//button',
]
DOINGCODING_ADMIN_TESTCASE_SAVE_BUTTON_SELECTORS = [
    'xpath=//*[@id="app"]/div/div[3]/div[1]/div/div/form/button',
    'xpath=//*[@id="app"]//form/button',
]
DOINGCODING_ADMIN_TESTCASE_LIST_SELECTORS = [
    'xpath=//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[11]/div[2]/div/div/div/ul',
    'xpath=//*[@id="app"]//form//ul',
]
DOINGCODING_ADMIN_TESTCASE_FILE_INPUT_SELECTORS = [
    'css=input[type="file"]',
]


@dataclass
class DoingCodingAdminSession:
    context: object
    page: object
    username: str
    password: str
    owns_context: bool = True


def _clean_text(value):
    if not value:
        return ""
    value = value.replace("\xa0", " ")
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()

def get_solvedac_tier_name(level):
    if level == 0:
        return "Unrated"

    tiers = ["브론즈", "실버", "골드", "플래티넘", "다이아몬드", "루비"]
    tier_idx = (level - 1) // 5
    sub_tier = 5 - ((level - 1) % 5)

    # 로마자 변환 (1->I, 2->II, 3->III, 4->IV, 5->V)
    roman_numerals = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}

    if tier_idx < len(tiers):
        return f"{tiers[tier_idx]} {roman_numerals[sub_tier]}"
    return "마스터" # 31 이상

# --- [여기에 1단계 함수 추가] ---
import json

def get_solvedac_level_and_tags(context, problem_id):
    """
    Playwright 브라우저 컨텍스트의 '새 탭'을 이용해 Solved.ac API를 호출합니다.
    공유된 통신망을 사용하므로 Cloudflare 봇 탐지를 우회합니다.
    """
    url = f"https://solved.ac/api/v3/problem/show?problemId={problem_id}"
    print(f"  🔍 [Solved.ac API] 수준 및 태그 정보를 수집 중... (문제: {problem_id})")
    
    # API 조회를 위한 임시 탭(Page) 생성
    api_page = context.new_page()
    
    try:
        # 페이지 접속 (가시성을 위해 창을 유지하며 로드)
        response = api_page.goto(url, wait_until="domcontentloaded", timeout=30000)
        
        # 🚨 [신규] 404 Not Found 확인 시 즉시 예외 발생 (더미 파일 생성을 위함)
        if response.status == 404:
            raise ProblemNotFoundError(f"Solved.ac 확인 결과 존재하지 않는 문제입니다 (404): {problem_id}")
            
        # 🚨 [패치됨] 고정 대기 대신, JSON 응답 고유 키가 나타날 때까지 대기 (최대 5초)
        try:
            api_page.wait_for_function("() => document.body.innerText.includes('problemId')", timeout=5000)
        except Exception:
            pass
        
        if response.status == 200:
            # 화면에 출력된 순수 JSON 텍스트 파싱 (방어적 추출)
            json_text = api_page.evaluate("() => document.body.innerText")
            data = json.loads(json_text)
            
            level = data.get("level", 0)
            
            tags = []
            tag_keys = [] # 🚨 영문 키 저장을 위한 리스트 추가
            for tag in data.get("tags", []):
                tag_keys.append(tag.get("key")) # 🚨 영문 키(bruteforcing 등) 수집
                for display in tag.get("displayNames", []):
                    if display.get("language") == "ko":
                        tags.append(display.get("name"))
            
            if level > 0:
                print(f"    ✅ [Solved.ac 성공] Level: {level}, Tags: {len(tags)}개 추출 완료")

            # 추가 정보 추출
            extra = {
                "archived_at": datetime.now().strftime("%Y-%m-%d"), # 🚨 오늘 날짜 추가
                "sprout": data.get("sprout", False),
                "official": data.get("official", False),
                "is_solvable": data.get("isSolvable", True), # 🚨 추가
                "gives_no_rating": data.get("givesNoRating", False), # 🚨 추가
                "accepted_user_count": data.get("acceptedUserCount", 0),
                "average_tries": round(data.get("averageTries", 0), 2),
                "is_level_locked": data.get("isLevelLocked", False), # 🚨 추가
                "voted_user_count": data.get("votedUserCount", 0), # 🚨 추가
                "tag_keys": tag_keys, # 🚨 추가
                "titleKo": data.get("titleKo", "") # 🚨 제목 대조를 위해 추가
            }
            return level, tags, extra
            
        elif response.status == 429:
            print(f"  🚨 [경고] API 호출 제한! 60초 대기 후 재시도합니다... (문제: {problem_id})")
            api_page.wait_for_timeout(60000)
            return get_solvedac_level_and_tags(context, problem_id)
            
        else:
            print(f"  ⚠️ Solved.ac API 통신 실패 (상태 코드: {response.status})")
            return 0, [], {}
            
    except ProblemNotFoundError:
        # 404 에러는 상위로 던져서 더미 파일을 생성하게 함
        raise
    except Exception as e:
        print(f"  ⚠️ Solved.ac API 에러 ({problem_id}): {e}")
        return 0, [], {}
    finally:
        # 데이터를 무사히 가져왔든 에러가 났든 임시 탭은 반드시 닫아줍니다.
        api_page.close()

# --- [여기에 2단계 함수 추가] ---
import re

import time
import random

def process_html_and_download_images(html_content, base_url, save_dir, problem_id, context=None):
    if not html_content or not html_content.strip():
        return ""
        
    # 1. 래핑 (Raw LaTeX 기호 보호)
    html_content = re.sub(r'\\\[(.*?)\\\]', r'<div class="raw-display-math">\1</div>', html_content, flags=re.DOTALL)
    html_content = re.sub(r'\\\((.*?)\\\)', r'<span class="raw-inline-math">\1</span>', html_content, flags=re.DOTALL)

    soup = BeautifulSoup(html_content, 'html.parser')
    math_placeholders = {}
    placeholder_idx = 0

    # 2. MathJax 3.0+ (mjx-container) 대응
    for mjx in soup.find_all('mjx-container'):
        latex = ""
        is_display = mjx.get('display') == "true"
        
        annotation = mjx.find('annotation', encoding='application/x-tex')
        copytext = mjx.find(class_='mjx-copytext')
        
        if annotation and annotation.string:
            latex = annotation.string.strip()
        elif copytext:
            latex = copytext.get_text().strip()
            latex = re.sub(r'^\\\[|\\\]$', '', latex).strip()
            latex = re.sub(r'^\\\(|\\\)$', '', latex).strip()
            latex = re.sub(r'^\$\$|\$\$$', '', latex).strip()
            latex = re.sub(r'^\$|\$$', '', latex).strip()
        else:
            latex = mjx.get_text().strip()

        placeholder = f"@@MATH{placeholder_idx}@@"
        
        if is_display:
            math_placeholders[placeholder] = f"\n\n$$ {latex} $$\n\n"
            new_tag = soup.new_tag("p")
        else:
            math_placeholders[placeholder] = f" ${latex}$ "
            new_tag = soup.new_tag("span")
            
        new_tag.string = placeholder
        mjx.replace_with(new_tag)
        placeholder_idx += 1

    # 3. MathJax 2.0 대응
    for script in soup.find_all("script", type=lambda t: t and "math/tex" in t):
        latex_code = script.string or ""
        placeholder = f"@@MATH{placeholder_idx}@@"        
        
        if "mode=display" in script.get("type", ""):
            math_placeholders[placeholder] = f"\n\n$$ {latex_code.strip()} $$\n\n"
            new_tag = soup.new_tag("p")
        else:
            math_placeholders[placeholder] = f" ${latex_code.strip()}$ "
            new_tag = soup.new_tag("span")
            
        new_tag.string = placeholder
        script.replace_with(new_tag)
        placeholder_idx += 1
        
    # 4. 정규식 래핑 클래스 처리 (안전한 정규식 검색 사용)
    for math_el in soup.find_all(class_=re.compile(r"^raw-")):
        latex_code = math_el.string or math_el.get_text()
        placeholder = f"@@MATH{placeholder_idx}@@"
        
        # class 속성은 리스트로 반환되므로 안전하게 확인
        classes = math_el.get('class', [])
        if any("display" in c for c in classes):
            math_placeholders[placeholder] = f"\n\n$$ {latex_code.strip()} $$\n\n"
            new_tag = soup.new_tag("p")
        else:
            math_placeholders[placeholder] = f" ${latex_code.strip()}$ "
            new_tag = soup.new_tag("span")
            
        new_tag.string = placeholder
        math_el.replace_with(new_tag)
        placeholder_idx += 1

    # 5. 이미지 다운로드 로직
    images_dir = os.path.join(save_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    for img in soup.find_all('img'):
        src = img.get('src')
        if not src:
            continue
            
        # 🚨 [패치 1] Base64 이미지 데이터는 다운로드 시도하지 않고 패스
        if src.startswith("data:image/"):
            continue 
            
        # 🚨 [패치 1.5] 구형 수식 이미지 탐지 (alt에 백슬래시가 있거나 src에 equation/latex 포함 시 수식 텍스트로 치환)
        alt_text = img.get('alt', '').strip()
        if ('\\' in alt_text and '{' in alt_text) or ('equation' in src or 'latex' in src):
            math_latex = alt_text if alt_text else src.split('tex=')[-1]
            new_tag = soup.new_tag("span")
            new_tag.string = f" ${math_latex}$ "
            img.replace_with(new_tag)
            continue
            
        img_url = urljoin(base_url, src)
        import hashlib
        # 파일명 추출 (경로 끝이 슬래시인 경우 방어)
        src_path = src.split('?')[0].strip('/')
        original_filename = os.path.basename(src_path)
        if not original_filename or original_filename == "preview":
            # 파일명이 없거나 preview 같은 일반적인 이름이면 URL 해시로 고유이름 생성
            hash_name = hashlib.md5(img_url.encode()).hexdigest()[:8]
            original_filename = f"img_{hash_name}.png"
            
        local_filename = f"{problem_id}_{original_filename}"
        local_filepath = os.path.join(images_dir, local_filename)
        # 🚨 [추가] 이미 이미지가 있다면 다운로드 생략 (시간 단축)
        if os.path.exists(local_filepath):
            img['src'] = f"./images/{local_filename}"
            continue

        try:
            if context is not None:
                response = context.request.get(img_url, timeout=30000)
                if response.status == 200:
                    with open(local_filepath, 'wb') as f:
                        f.write(response.body())
                    img['src'] = f"./images/{local_filename}"
                    # 순간적인 트래픽 폭주 방지
                    time.sleep(random.uniform(0.5, 1.5))
            else:
                # context가 없을 경우의 Fallback
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(img_url, stream=True, timeout=10, headers=headers)
                
                if response.status_code == 200:
                    with open(local_filepath, 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    img['src'] = f"./images/{local_filename}"
        except Exception as e:
            print(f"⚠️ 이미지 다운로드 에러: {img_url} - {e}")

    modified_html = str(soup)
    
    # 🚨 [패치 2] 기하학 도형(svg, path), 동영상(iframe), ASCII 아트(pre, code) 절대 보존 구역 설정
    safe_keep_tags = ['sup', 'sub', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'svg', 'path', 'iframe', 'pre', 'code']
    # 테이블 셀 내부의 이미지 보존 (기본적으로 strip 되는 현상 방지)
    keep_inline = ['td', 'th', 'a', 'span', 'p', 'div', 'strong', 'b', 'em', 'i']
    
    try:
        markdown_text = md(modified_html, heading_style="ATX", keep=safe_keep_tags, keep_inline_images_in=keep_inline)
    except Exception as e:
        print(f"⚠️ Markdown 변환 중 심각한 에러 발생 (HTML 강제 유지 모드로 렌더링): {e}")
        # 최후의 수단: 에러가 나면 div, span까지 모두 살려서 어떻게든 저장시킵니다.
        markdown_text = md(modified_html, heading_style="ATX", keep=safe_keep_tags + ['div', 'span', 'p'], keep_inline_images_in=keep_inline)
    
    # 6. Placeholder 롤백
    for placeholder, original_math in math_placeholders.items():
        markdown_text = markdown_text.replace(placeholder, original_math)
        
    return markdown_text.strip()


def process_html_and_download_attachments(html_content, base_url, save_dir, problem_id, context=None):
    """
    HTML 본문에서 첨부 파일 링크를 찾아 다운로드하고, 
    로컬 경로로 치환된 마크다운 문자열을 반환합니다.
    """
    if not html_content or not html_content.strip():
        return ""

    soup = BeautifulSoup(html_content, 'html.parser')
    attachments_dir = os.path.join(save_dir, "attachments")
    os.makedirs(attachments_dir, exist_ok=True)

    for a in soup.find_all('a'):
        href = a.get('href')
        if not href:
            continue
            
        file_url = urljoin(base_url, href)
        
        # 파일명 추출 (링크 텍스트를 우선적으로 고려)
        link_text = a.get_text().strip()
        # 파일명으로 부적합한 문자 치환
        safe_link_text = re.sub(r'[^\w\.-]', '_', link_text)
        
        # 텍스트에 확장자가 포함되어 있고 적절한 길이인 경우 파일명으로 채택
        if '.' in safe_link_text and 1 <= len(safe_link_text.split('.')[-1]) <= 5:
            original_filename = safe_link_text
        else:
            # 폴백: URL에서 추출 (경로 끝이 슬래시인 경우 방어)
            src_path = href.split('?')[0].strip('/')
            original_filename = os.path.basename(src_path)
            if not original_filename:
                import hashlib
                hash_name = hashlib.md5(file_url.encode()).hexdigest()[:8]
                original_filename = f"file_{hash_name}"
            
        local_filename = f"{problem_id}_{original_filename}"
        local_filepath = os.path.join(attachments_dir, local_filename)

        # 이미 파일이 있다면 다운로드 생략
        if os.path.exists(local_filepath):
            a['href'] = f"./attachments/{local_filename}"
            continue

        try:
            if context is not None:
                response = context.request.get(file_url, timeout=30000)
                if response.status == 200:
                    with open(local_filepath, 'wb') as f:
                        f.write(response.body())
                    a['href'] = f"./attachments/{local_filename}"
                    time.sleep(random.uniform(0.5, 1.5))
            else:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(file_url, stream=True, timeout=20, headers=headers)
                if response.status_code == 200:
                    with open(local_filepath, 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    a['href'] = f"./attachments/{local_filename}"
        except Exception as e:
            print(f"⚠️ 첨부 파일 다운로드 에러: {file_url} - {e}")

    modified_html = str(soup)
    return md(modified_html, heading_style="ATX").strip()

# def process_html_and_download_images(html_content, base_url, save_dir, problem_id, context=context):
#     """
#     HTML 본문에서 이미지를 찾아 다운로드하고, 
#     로컬 경로로 치환된 마크다운 문자열을 반환합니다.
#     """
#     # 내용이 없으면 빈 문자열 반환
#     if not html_content or not html_content.strip():
#         return ""

#     soup = BeautifulSoup(html_content, 'html.parser')
    
#     # 🚨 [수학 수식(MathJax) 원본 복원 로직 추가] 🚨
#     # 1. MathJax가 화면에 렌더링하기 위해 만든 시각적 껍데기 요소들을 모두 파괴(삭제)합니다.
#     for el in soup.find_all(class_=lambda c: c and any(m in c for m in ['MathJax', 'MathJax_Preview', 'mjx'])):
#         el.decompose()
        
#     # 2. 백준이 숨겨둔 원본 LaTeX 코드가 담긴 script 태그를 찾습니다.
#     for script in soup.find_all("script", type=lambda t: t and "math/tex" in t):
#         latex_code = script.string or ""
#         # 3. Next.js(MDX)가 인식할 수 있는 수학 수식 문법($ $)으로 예쁘게 치환합니다.
#         if "mode=display" in script.get("type", ""):
#             script.replace_with(f"$${latex_code}$$")
#         else:
#             script.replace_with(f"${latex_code}$")

#     # 이미지를 저장할 하위 폴더 생성 (현재 저장 폴더 내의 'images' 폴더)
#     images_dir = os.path.join(save_dir, "images")
#     os.makedirs(images_dir, exist_ok=True)
    
#     # 본문 내의 모든 img 태그 탐색
#     for img in soup.find_all('img'):
#         src = img.get('src')
#         if not src:
#             continue
            
#         # 절대 경로 URL로 변환 (상대 경로 방어)
#         img_url = urljoin(base_url, src)
        
#         # 파일명 추출 및 로컬 저장 경로 설정 (쿼리 파라미터 제거)
#         original_filename = os.path.basename(src.split('?')[0])
#         if not original_filename:
#             original_filename = "image.png" # 파일명이 없을 경우를 대비한 기본값
            
#         # 중복 방지를 위해 파일명 앞에 문제번호(problem_id)를 붙임
#         local_filename = f"{problem_id}_{original_filename}"
#         local_filepath = os.path.join(images_dir, local_filename)
        
#         # 이미지 다운로드
#         try:
#             # 봇 차단을 막기 위해 헤더 추가
#             headers = {"User-Agent": "Mozilla/5.0"}
#             response = requests.get(img_url, stream=True, timeout=10, headers=headers)
            
#             if response.status_code == 200:
#                 with open(local_filepath, 'wb') as f:
#                     for chunk in response.iter_content(1024):
#                         f.write(chunk)
                
#                 # HTML 태그의 src를 다운로드한 로컬 경로로 수정
#                 # (Next.js 및 MDX 환경에 맞게 ./images/ 경로 사용)
#                 img['src'] = f"./images/{local_filename}"
#             else:
#                 print(f"⚠️ 이미지 다운로드 실패 (상태 코드 {response.status_code}): {img_url}")
                
#         except Exception as e:
#             print(f"⚠️ 이미지 다운로드 에러: {img_url} - {e}")
            
#     # 수정된 HTML을 마크다운으로 변환 (heading_style="ATX"는 # 방식의 헤딩 적용)
#     modified_html = str(soup)
#     markdown_text = md(modified_html, heading_style="ATX")
    
#     return markdown_text.strip()
# ------------------------------

def _normalize_heading(text):
    cleaned = _clean_text(text)
    return re.sub(r"[\s:：\-\[\]\(\)]", "", cleaned)


def _matches_heading(text, candidates):
    normalized = _normalize_heading(text)
    return any(normalized == _normalize_heading(candidate) for candidate in candidates)


def _iter_direct_children(element):
    for child in element.xpath("./*"):
        yield child


def _element_text(element):
    return _clean_text("".join(element.itertext()))


def _has_pre_descendant(element):
    return bool(element.xpath(".//pre"))


def _looks_like_section_heading(text):
    return any(
        _matches_heading(text, candidates) for candidates in SECTION_HEADINGS.values()
    )


def _extract_section_after_heading(content_root, labels):
    children = list(_iter_direct_children(content_root))
    for index, child in enumerate(children):
        text = _element_text(child)
        if not _matches_heading(text, labels):
            continue

        chunks = []
        for sibling in children[index + 1 :]:
            sibling_text = _element_text(sibling)
            if not sibling_text:
                continue
            if _looks_like_section_heading(sibling_text):
                break
            if _has_pre_descendant(sibling):
                break
            chunks.append(sibling_text)

        if chunks:
            return "\n\n".join(chunks)

    return ""


def _find_doingcoding_content_root(tree):
    roots = tree.xpath('//*[@id="problem-content"]')
    return roots[0] if roots else None


def _find_doingcoding_title(tree):
    xpath_candidates = [
        '//*[@id="problem-main"]//*[self::h1 or self::h2 or self::h3][1]',
        '//*[@id="problem-main"]/div[3]/div[1]/div/div',
        '//*[@id="problem-main"]//*[contains(@class, "title")][1]',
    ]
    for xpath_expr in xpath_candidates:
        nodes = tree.xpath(xpath_expr)
        if not nodes:
            continue
        text = _element_text(nodes[0])
        if text:
            return text

    nodes = tree.xpath('//*[@id="problem-main"]//*')
    for node in nodes:
        text = _element_text(node)
        if text and len(text) <= 200:
            return text
    return ""


def _missing_required_fields(field_map):
    missing = []
    for name, value in field_map.items():
        text = _clean_text(value)
        if text in REQUIRED_FIELD_PLACEHOLDERS:
            missing.append(name)
    return missing


def _extract_sample_pairs(content_root):
    samples = []
    for child in _iter_direct_children(content_root):
        text = _element_text(child)
        if _matches_heading(text, SECTION_HEADINGS["hint"]):
            break

        pre_nodes = child.xpath(".//pre")
        if len(pre_nodes) < 2:
            continue

        pre_texts = [_clean_text("".join(node.itertext())) for node in pre_nodes]
        pre_texts = [text for text in pre_texts if text or text == ""]

        pair_count = len(pre_texts) // 2
        for index in range(pair_count):
            sample_input = pre_texts[index * 2]
            sample_output = pre_texts[index * 2 + 1]
            samples.append((sample_input, sample_output))

    return samples


def _normalize_code_text(value):
    if not value:
        return ""
    text = value.replace("\xa0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def _pick_best_code(candidates):
    normalized = []
    for candidate in candidates:
        text = _normalize_code_text(candidate)
        if text:
            normalized.append(text)
    if not normalized:
        return ""
    normalized.sort(key=lambda item: (item.count("\n"), len(item)), reverse=True)
    return normalized[0]


def _extract_editor_code(page):
    candidates = page.evaluate(
        """() => {
            const values = [];

            document.querySelectorAll('.CodeMirror').forEach((element) => {
                const editor = element.CodeMirror;
                if (editor && typeof editor.getValue === 'function') {
                    values.push(editor.getValue());
                }
            });

            document.querySelectorAll('textarea').forEach((element) => {
                if (element.value) {
                    values.push(element.value);
                }
            });

            document.querySelectorAll('.CodeMirror-code').forEach((element) => {
                const text = element.innerText || element.textContent || '';
                if (text) {
                    values.push(text);
                }
            });

            document.querySelectorAll('pre code, pre').forEach((element) => {
                const text = element.innerText || element.textContent || '';
                if (text) {
                    values.push(text);
                }
            });

            return values;
        }"""
    )
    return _pick_best_code(candidates)


def _goto_with_retries(
    page,
    url,
    wait_until="domcontentloaded",
    timeout=30000,
    ready_selector=None,
    attempts=3,
    referer=None,
    ready_selector_state="visible",  # 🔧 [FIX] 12096처럼 title이 hidden인 경우 "attached" 전달
):
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            if referer:
                response = page.goto(url, wait_until=wait_until, timeout=timeout, referer=referer)
            else:
                response = page.goto(url, wait_until=wait_until, timeout=timeout)
            status = response.status if response is not None else "no-response"
            print(f"[접속] {url} (시도 {attempt}/{attempts}, 상태: {status})")

            # --- 추가: 404 감지 시 즉시 중단 및 예외 발생 ---
            if status == 404:
                raise ProblemNotFoundError(f"문제를 찾을 수 없습니다 (404): {url}")
            # ------------------------------------------

            if ready_selector:
                page.wait_for_selector(ready_selector, timeout=timeout, state=ready_selector_state)
            return response
        except ProblemNotFoundError:
            # 404 에러는 재시도가 무의미하므로 즉시 상위로 던짐
            raise
        except Exception as exc:
            last_error = exc
            print(f"[재시도] {url} (시도 {attempt}/{attempts}) 실패: {exc}")
            if attempt < attempts:
                page.wait_for_timeout(500 * attempt)
    raise last_error


def _emit_log(logger, message):
    # datetime은 crawl.py 상단(L15)에 이미 임포트되어 있으므로 바로 사용 가능
    timestamp = datetime.now().strftime("[%H:%M:%S] ")
    if callable(logger):
        logger(message)
    print(timestamp + message) # <--- 터미널 출력에도 시간 추가    
    # if callable(logger):
    #     logger(message)
    # print(message)


def _find_first_working_selector(page, selectors, timeout=10000, require_visible=False):
    state = "visible" if require_visible else "attached"
    last_error = None
    for selector in selectors:
        try:
            page.wait_for_selector(selector, timeout=timeout, state=state)
            return selector
        except Exception as exc:
            last_error = exc
    raise last_error


def extract_cookie_value(cookies, name, domain_hint="edu.doingcoding.com"):
    matches = [cookie for cookie in cookies if cookie.get("name") == name]
    if not matches:
        return None

    prioritized = []
    for cookie in matches:
        domain = cookie.get("domain", "")
        path = cookie.get("path", "")
        score = 0
        if domain_hint and domain_hint in domain:
            score += 2
        if "/admin" in path:
            score += 1
        prioritized.append((score, len(path), cookie))

    prioritized.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return prioritized[0][2].get("value")


def debug_admin_cookie_state(context):
    cookies = context.cookies()
    csrftoken = extract_cookie_value(cookies, "csrftoken")
    sessionid = extract_cookie_value(cookies, "sessionid")
    return {
        "cookie_count": len(cookies),
        "has_csrftoken": csrftoken is not None,
        "has_sessionid": sessionid is not None,
    }


def ensure_doingcoding_admin_csrf(page, logger=None):
    def _read_document_cookie():
        try:
            document_cookie = page.evaluate("() => document.cookie")
        except Exception:
            return None

        for token in document_cookie.split(";"):
            name, _, value = token.strip().partition("=")
            if name == "csrftoken" and value:
                return value
        return None

    _emit_log(logger, "[관리자 로그인 준비] /api/profile 접속")
    response = _goto_with_retries(
        page,
        DOINGCODING_CSRF_SEED_URL,
        wait_until="domcontentloaded",
        timeout=10000,
        ready_selector=None,
        attempts=3,
    )
    status = response.status if response is not None else "no-response"
    _emit_log(logger, f"[관리자 로그인 준비] /api/profile 상태: {status}")

    csrftoken = extract_cookie_value(page.context.cookies(), "csrftoken")
    if not csrftoken:
        csrftoken = _read_document_cookie()

    if not csrftoken:
        _emit_log(logger, "[관리자 로그인 준비] /api/website 접속")
        fallback_response = _goto_with_retries(
            page,
            DOINGCODING_CSRF_FALLBACK_URL,
            wait_until="domcontentloaded",
            timeout=10000,
            ready_selector=None,
            attempts=3,
        )
        fallback_status = (
            fallback_response.status if fallback_response is not None else "no-response"
        )
        _emit_log(logger, f"[관리자 로그인 준비] /api/website 상태: {fallback_status}")
        csrftoken = (
            extract_cookie_value(page.context.cookies(), "csrftoken")
            or _read_document_cookie()
        )

    if not csrftoken:
        _emit_log(logger, "[관리자 로그인 준비] /admin/login 접속")
        _goto_with_retries(
            page,
            DOINGCODING_ADMIN_LOGIN_URL,
            wait_until="domcontentloaded",
            timeout=10000,
            ready_selector=DOINGCODING_ADMIN_ID_SELECTOR,
            attempts=3,
        )
        csrftoken = (
            extract_cookie_value(page.context.cookies(), "csrftoken")
            or _read_document_cookie()
        )

    if csrftoken:
        _emit_log(logger, "[관리자 로그인 준비] csrftoken 확보 성공")
        return csrftoken

    _emit_log(logger, "[관리자 로그인 준비] csrftoken 없음")
    raise RuntimeError("관리자 로그인 전 csrftoken 쿠키를 확보하지 못했습니다.")


def _wait_for_admin_login_success(page, timeout=5000):
    page.wait_for_function(
        """() => {
            const path = window.location.pathname || "";
            return !path.includes('/admin/login');
        }""",
        timeout=timeout,
    )


def _attempt_admin_login_submit(page, logger=None):
    password_locator = page.locator(DOINGCODING_ADMIN_PASSWORD_SELECTOR)
    login_button = page.locator(DOINGCODING_ADMIN_LOGIN_BUTTON_SELECTOR)
    go_button = page.locator('button:has-text("GO")').first

    try:
        _emit_log(logger, "[관리자 로그인] 제출 시도 1: locator Enter")
        password_locator.click()
        password_locator.press("Enter")
        _wait_for_admin_login_success(page, timeout=5000)
        return
    except Exception:
        pass

    try:
        _emit_log(logger, "[관리자 로그인] 제출 시도 2: keyboard Enter")
        password_locator.click()
        page.keyboard.press("Enter")
        _wait_for_admin_login_success(page, timeout=5000)
        return
    except Exception:
        pass

    try:
        _emit_log(logger, "[관리자 로그인] 제출 시도 3: form requestSubmit")
        password_locator.evaluate(
            """(element) => {
                const form = element.form || element.closest('form');
                if (form && typeof form.requestSubmit === 'function') {
                    form.requestSubmit();
                    return true;
                }
                if (form) {
                    form.submit();
                    return true;
                }
                return false;
            }"""
        )
        _wait_for_admin_login_success(page, timeout=5000)
        return
    except Exception:
        pass

    try:
        _emit_log(logger, "[관리자 로그인] 제출 시도 4: GO 버튼 force click")
        go_button.click(force=True)
        _wait_for_admin_login_success(page, timeout=5000)
        return
    except Exception:
        pass

    try:
        _emit_log(logger, "[관리자 로그인] 제출 시도 5: 로그인 버튼 force click")
        login_button.click(force=True)
        _wait_for_admin_login_success(page, timeout=5000)
        return
    except Exception:
        pass

    _emit_log(logger, "[관리자 로그인] 제출 시도 6: 로그인 버튼 JS click")
    login_button.evaluate(
        """(element) => {
            element.click();
        }"""
    )
    _wait_for_admin_login_success(page, timeout=5000)


def attempt_admin_login_via_request(
    context, username, password, csrftoken, logger=None
):
    _emit_log(
        logger,
        "[관리자 로그인] 네트워크 기반 fallback은 비활성 상태입니다. 성공 요청 payload 확인 후 활성화가 필요합니다.",
    )
    return False


def _load_testcase_info_from_dir(extract_dir):
    info_candidates = [
        os.path.join(extract_dir, "info"),
        os.path.join(extract_dir, "info.json"),
    ]
    for candidate in info_candidates:
        if not os.path.exists(candidate):
            continue
        with open(candidate, "r", encoding="utf-8") as info_file:
            return json.load(info_file)
    return {}


def _read_text_file(path):
    with open(path, "r", encoding="utf-8") as source_file:
        return source_file.read().replace("\r\n", "\n").replace("\r", "\n")


def _pair_testcase_files(extract_dir, info):
    paired = []
    info_cases = info.get("test_cases", {}) if isinstance(info, dict) else {}
    if info_cases:

        def _sort_key(item):
            key = item[0]
            return (0, int(key)) if str(key).isdigit() else (1, str(key))

        for case_id, meta in sorted(info_cases.items(), key=_sort_key):
            input_name = meta.get("input_name")
            output_name = meta.get("output_name")
            if not input_name or not output_name:
                continue
            input_path = os.path.join(extract_dir, input_name)
            output_path = os.path.join(extract_dir, output_name)
            if not os.path.exists(input_path) or not os.path.exists(output_path):
                continue
            paired.append(
                {
                    "id": str(case_id),
                    "input_name": input_name,
                    "output_name": output_name,
                    "input_text": _read_text_file(input_path),
                    "output_text": _read_text_file(output_path),
                    "meta": meta,
                }
            )
        return paired

    discovered_inputs = {}
    discovered_outputs = {}
    for entry in os.listdir(extract_dir):
        full_path = os.path.join(extract_dir, entry)
        if not os.path.isfile(full_path):
            continue
        stem, ext = os.path.splitext(entry)
        if ext == ".in":
            discovered_inputs[stem] = entry
        elif ext == ".out":
            discovered_outputs[stem] = entry

    for stem in sorted(
        set(discovered_inputs) & set(discovered_outputs),
        key=lambda value: (0, int(value)) if value.isdigit() else (1, value),
    ):
        paired.append(
            {
                "id": stem,
                "input_name": discovered_inputs[stem],
                "output_name": discovered_outputs[stem],
                "input_text": _read_text_file(
                    os.path.join(extract_dir, discovered_inputs[stem])
                ),
                "output_text": _read_text_file(
                    os.path.join(extract_dir, discovered_outputs[stem])
                ),
                "meta": {},
            }
        )
    return paired


def parse_testcase_bundle(bundle_path, extract_dir):
    with zipfile.ZipFile(bundle_path) as archive:
        archive.extractall(extract_dir)

    info = _load_testcase_info_from_dir(extract_dir)
    cases = _pair_testcase_files(extract_dir, info)
    return {"info": info, "cases": cases, "extract_dir": extract_dir}


def render_testcases_md(testcase_bundle, section_number=5):
    cases = testcase_bundle.get("cases", [])
    info = testcase_bundle.get("info", {})
    if not cases:
        return ""

    sections = [f"## {section_number}. 채점용 테스트케이스", ""]
    if info:
        sections.extend(
            [
                "### 메타데이터",
                "```json",
                json.dumps(info, ensure_ascii=False, indent=4),
                "```",
                "",
            ]
        )

    for case in cases:
        case_id = case["id"]
        sections.extend(
            [
                f"### 테스트케이스 {case_id} 입력",
                "```text",
                case["input_text"].rstrip("\n"),
                "```",
                "",
                f"### 테스트케이스 {case_id} 출력",
                "```text",
                case["output_text"].rstrip("\n"),
                "```",
                "",
            ]
        )

    sections.append("---")
    sections.append("")
    return "\n".join(sections)


def render_templates_md(templates, section_number=5):
    if not templates:
        return ""
    templates_md = [f"## {section_number}. 코드 템플릿", ""]
    for lang, code in templates.items():
        lang_tag = "python" if "Python" in lang else lang.lower()
        templates_md.extend(
            [
                f"### {lang}",
                f"```{lang_tag}",
                code,
                "```",
                "",
            ]
        )
    templates_md.extend(["---", ""])
    return "\n".join(templates_md)


def login_doingcoding_admin(page, username, password, logger=None):
    if not username or not password:
        raise ValueError("관리자 로그인 계정 정보가 필요합니다.")

    csrftoken = ensure_doingcoding_admin_csrf(page, logger=logger)
    _emit_log(logger, "[관리자 로그인] csrf 확보 후 /admin/login 재진입")
    _goto_with_retries(
        page,
        DOINGCODING_ADMIN_LOGIN_URL,
        wait_until="domcontentloaded",
        timeout=10000,
        ready_selector=DOINGCODING_ADMIN_ID_SELECTOR,
        attempts=3,
    )
    page.wait_for_selector(
        DOINGCODING_ADMIN_PASSWORD_SELECTOR, timeout=10000, state="attached"
    )
    _emit_log(logger, "[관리자 로그인] 로그인 폼 확인 완료")

    page.locator(DOINGCODING_ADMIN_ID_SELECTOR).click()
    page.locator(DOINGCODING_ADMIN_ID_SELECTOR).fill(username)
    page.locator(DOINGCODING_ADMIN_PASSWORD_SELECTOR).click()
    page.locator(DOINGCODING_ADMIN_PASSWORD_SELECTOR).fill(password)
    cookie_state = debug_admin_cookie_state(page.context)
    _emit_log(
        logger,
        f"[관리자 로그인] 제출 전 상태: url={page.url}, csrftoken={'있음' if bool(csrftoken) else '없음'}, cookies={cookie_state['cookie_count']}",
    )

    try:
        _attempt_admin_login_submit(page, logger=logger)
    except Exception as exc:
        cookie_state = debug_admin_cookie_state(page.context)
        _emit_log(
            logger,
            f"[관리자 로그인] 최종 실패: url={page.url}, csrftoken={'있음' if cookie_state['has_csrftoken'] else '없음'}, sessionid={'있음' if cookie_state['has_sessionid'] else '없음'}",
        )
        attempt_admin_login_via_request(
            page.context, username, password, csrftoken, logger=logger
        )
        raise RuntimeError(
            "관리자 로그인 실패: CSRF cookie/token mismatch 가능성"
        ) from exc

    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)
    _goto_with_retries(
        page,
        DOINGCODING_ADMIN_PROBLEMS_URL,
        wait_until="domcontentloaded",
        timeout=10000,
        ready_selector=None,
        attempts=3,
    )
    _find_first_working_selector(
        page, DOINGCODING_ADMIN_SEARCH_SELECTORS, timeout=15000, require_visible=False
    )
    return True


def download_doingcoding_testcases(page, problem_id, download_dir):
    os.makedirs(download_dir, exist_ok=True)
    search_selector = _find_first_working_selector(
        page,
        DOINGCODING_ADMIN_SEARCH_SELECTORS,
        timeout=15000,
        require_visible=False,
    )
    row_selector = _find_first_working_selector(
        page,
        DOINGCODING_ADMIN_ROW_SELECTORS,
        timeout=15000,
        require_visible=False,
    )
    download_selector = _find_first_working_selector(
        page,
        DOINGCODING_ADMIN_DOWNLOAD_BUTTON_SELECTORS,
        timeout=15000,
        require_visible=False,
    )

    page.fill(search_selector, problem_id)
    page.press(search_selector, "Enter")
    page.wait_for_timeout(1000)
    page.wait_for_selector(row_selector, timeout=15000, state="attached")
    row_text = _clean_text(page.text_content(row_selector) or "")
    if problem_id not in row_text:
        raise RuntimeError(
            f"관리자 문제 목록에서 문제 ID를 확인하지 못했습니다: {problem_id}"
        )

    with page.expect_download() as download_info:
        page.click(download_selector)
    download = download_info.value
    suggested_filename = download.suggested_filename or f"{problem_id}.zip"
    download_path = os.path.join(download_dir, suggested_filename)
    download.save_as(download_path)
    return download_path


def _search_doingcoding_problem_row(page, problem_id):
    search_selector = _find_first_working_selector(
        page,
        DOINGCODING_ADMIN_SEARCH_SELECTORS,
        timeout=15000,
        require_visible=False,
    )
    row_selector = _find_first_working_selector(
        page,
        DOINGCODING_ADMIN_ROW_SELECTORS,
        timeout=15000,
        require_visible=False,
    )

    page.fill(search_selector, problem_id)
    page.press(search_selector, "Enter")
    page.wait_for_timeout(1000)
    page.wait_for_selector(row_selector, timeout=15000, state="attached")
    row_text = _clean_text(page.text_content(row_selector) or "")
    if problem_id not in row_text:
        raise RuntimeError(
            f"관리자 문제 목록에서 문제 ID를 확인하지 못했습니다: {problem_id}"
        )
    return search_selector, row_selector


def _set_doingcoding_testcase_zip(page, zip_path):
    upload_selector = _find_first_working_selector(
        page,
        DOINGCODING_ADMIN_TESTCASE_UPLOAD_BUTTON_SELECTORS,
        timeout=15000,
        require_visible=False,
    )
    if hasattr(page, "expect_file_chooser"):
        try:
            with page.expect_file_chooser(timeout=3000) as chooser_info:
                page.click(upload_selector)
            chooser_info.value.set_files(zip_path)
            return "filechooser"
        except Exception:
            pass

    page.click(upload_selector)

    last_error = None
    for selector in DOINGCODING_ADMIN_TESTCASE_FILE_INPUT_SELECTORS:
        try:
            locator = page.locator(selector).first
            if hasattr(locator, "set_input_files"):
                locator.set_input_files(zip_path)
                return "input"
        except Exception as exc:
            last_error = exc
    raise RuntimeError("테스트케이스 ZIP 파일 입력 요소를 찾지 못했습니다.") from last_error


def _wait_for_doingcoding_admin_save_success(page):
    success_keywords = [
        "저장 성공",
        "수정 성공",
        "등록 성공",
        "업로드 성공",
        "저장되었습니다",
        "완료되었습니다",
    ]

    try:
        current_path = urlparse(getattr(page, "url", "") or "").path.rstrip("/")
        if current_path == "/admin/problems":
            return
    except Exception:
        pass

    try:
        page.wait_for_function(
            """(keywords) => {
                const path = (window.location.pathname || '').replace(/\\/+$/, '');
                const bodyText = ((document.body && document.body.innerText) || '')
                    .replace(/\\s+/g, ' ')
                    .trim();
                return (
                    path === '/admin/problems' ||
                    keywords.some((keyword) => bodyText.includes(keyword))
                );
            }""",
            success_keywords,
            timeout=15000,
        )
        return
    except Exception:
        pass

    try:
        testcase_list_selector = _find_first_working_selector(
            page,
            DOINGCODING_ADMIN_TESTCASE_LIST_SELECTORS,
            timeout=15000,
            require_visible=False,
        )
        testcase_list_text = _clean_text(page.text_content(testcase_list_selector) or "")
        if testcase_list_text:
            return
    except Exception:
        pass

    try:
        current_path = urlparse(getattr(page, "url", "") or "").path.rstrip("/")
        search_selector = _find_first_working_selector(
            page,
            DOINGCODING_ADMIN_SEARCH_SELECTORS,
            timeout=15000,
            require_visible=False,
        )
        if current_path == "/admin/problems":
            page.wait_for_selector(search_selector, timeout=3000, state="attached")
            return
    except Exception:
        pass

    try:
        body_text = _clean_text(page.text_content("body") or "")
        if any(keyword in body_text for keyword in success_keywords):
            return
    except Exception:
        pass

    raise RuntimeError("테스트케이스 저장 완료 상태를 확인하지 못했습니다.")


def open_doingcoding_problem_editor(page, problem_id, logger=None):
    _emit_log(logger, f"[관리자 업로드] 문제 검색: {problem_id}")
    _search_doingcoding_problem_row(page, problem_id)
    edit_selector = _find_first_working_selector(
        page,
        DOINGCODING_ADMIN_EDIT_BUTTON_SELECTORS,
        timeout=15000,
        require_visible=False,
    )
    _emit_log(logger, f"[관리자 업로드] 문제 수정 화면 진입: {problem_id}")
    page.click(edit_selector)
    _find_first_working_selector(
        page,
        DOINGCODING_ADMIN_TESTCASE_UPLOAD_BUTTON_SELECTORS,
        timeout=15000,
        require_visible=False,
    )
    _find_first_working_selector(
        page,
        DOINGCODING_ADMIN_TESTCASE_SAVE_BUTTON_SELECTORS,
        timeout=15000,
        require_visible=False,
    )


def upload_doingcoding_testcases(page, problem_id, zip_path, logger=None):
    if not zip_path or not os.path.isfile(zip_path):
        raise ValueError(f"업로드할 ZIP 파일을 찾지 못했습니다: {zip_path}")
    if not zip_path.lower().endswith(".zip"):
        raise ValueError(f"ZIP 파일만 업로드할 수 있습니다: {zip_path}")

    open_doingcoding_problem_editor(page, problem_id, logger=logger)
    _emit_log(logger, f"[관리자 업로드] ZIP 선택: {os.path.basename(zip_path)}")
    upload_mode = _set_doingcoding_testcase_zip(page, zip_path)
    _emit_log(logger, f"[관리자 업로드] ZIP 입력 방식: {upload_mode}")

    save_selector = _find_first_working_selector(
        page,
        DOINGCODING_ADMIN_TESTCASE_SAVE_BUTTON_SELECTORS,
        timeout=15000,
        require_visible=False,
    )
    _emit_log(logger, "[관리자 업로드] 저장 버튼 클릭")
    page.click(save_selector)
    _wait_for_doingcoding_admin_save_success(page)
    _emit_log(logger, f"[관리자 업로드] 저장 완료: {problem_id}")
    return {"problem_id": problem_id, "zip_path": zip_path, "status": "uploaded"}


def open_doingcoding_admin_session(
    browser_or_context, admin_username, admin_password, logger=None
):
    _emit_log(logger, "[관리자 세션] 초기화 시작")
    if hasattr(browser_or_context, 'new_context'):
        context = browser_or_context.new_context(accept_downloads=True)
        owns_context = True
    else:
        # If it's a PersistentContext, it doesn't have 'new_context'
        context = browser_or_context
        owns_context = False

    page = context.new_page()
    try:
        login_doingcoding_admin(page, admin_username, admin_password, logger=logger)
        _emit_log(logger, "[관리자 세션] 로그인 완료, 이후 문제에 재사용")
        return DoingCodingAdminSession(
            context=context,
            page=page,
            username=admin_username,
            password=admin_password,
            owns_context=owns_context,
        )
    except Exception:
        if owns_context:
            context.close()
        raise


def close_doingcoding_admin_session(session):
    if not session:
        return
    if session.owns_context:
        session.context.close()


def collect_doingcoding_testcases_with_session(
    session, problem_id, download_dir, logger=None
):
    _emit_log(logger, "[관리자 세션] 기존 로그인 세션 재사용")
    try:
        return download_doingcoding_testcases(session.page, problem_id, download_dir)
    except Exception:
        _emit_log(logger, "[관리자 세션] 세션 재로그인 시도")
        login_doingcoding_admin(
            session.page, session.username, session.password, logger=logger
        )
        return download_doingcoding_testcases(session.page, problem_id, download_dir)


def upload_doingcoding_testcases_with_session(
    session, problem_id, zip_path, logger=None
):
    _emit_log(logger, "[관리자 세션] 기존 로그인 세션 재사용")
    try:
        return upload_doingcoding_testcases(
            session.page, problem_id, zip_path, logger=logger
        )
    except Exception:
        _emit_log(logger, "[관리자 세션] 세션 재로그인 시도")
        login_doingcoding_admin(
            session.page, session.username, session.password, logger=logger
        )
        return upload_doingcoding_testcases(
            session.page, problem_id, zip_path, logger=logger
        )


def collect_doingcoding_testcases(
    browser,
    problem_id,
    admin_username,
    admin_password,
    base_download_dir=None,
    logger=None,
):
    work_root = base_download_dir or os.getcwd()
    temp_dir = tempfile.mkdtemp(prefix=f"dc_tc_{problem_id}_", dir=work_root)
    session = None
    try:
        session = open_doingcoding_admin_session(
            browser,
            admin_username,
            admin_password,
            logger=logger,
        )
        bundle_path = collect_doingcoding_testcases_with_session(
            session,
            problem_id,
            temp_dir,
            logger=logger,
        )
        extract_dir = os.path.join(temp_dir, "extract")
        bundle = parse_testcase_bundle(bundle_path, extract_dir)
        return {"info": bundle.get("info", {}), "cases": bundle.get("cases", [])}
    finally:
        close_doingcoding_admin_session(session)
        shutil.rmtree(temp_dir, ignore_errors=True)


# --- [여기에 4단계 함수 추가] ---
def __parse_authors(author_list):
    """
    '문제를 만든 사람: gggkik' 같은 문자열 배열을 구조화된 객체 배열로 변환하되,
    예외 상황에서 터지지 않고 원본 문자열을 보존합니다.
    """
    structured = []
    if not isinstance(author_list, list):
        return structured
        
    role_map = {
        "만든": "creator",
        "출제": "creator",
        "검수": "tester",
        "번역": "translator",
        "데이터": "contributor",
        "기여": "contributor",
        "고친": "editor",
        "수정": "editor",
    }
    
    for author_str in author_list:
        if not isinstance(author_str, str):
            continue
            
        # ':' 또는 '：' 기준으로 자르기
        parts = re.split(r'[:：]', author_str, 1)
        if len(parts) == 2:
            role_kr = parts[0].strip()
            names_raw = parts[1].strip()
            
            names = [n.strip() for n in names_raw.split(',') if n.strip()]
            
            assigned_role = "author" # 기본값
            for kr_keyword, en_role in role_map.items():
                if kr_keyword in role_kr:
                    assigned_role = en_role
                    break
            
            structured.append({"role": assigned_role, "names": names})
        else:
            # 패턴 매칭 실패 시 유연하게 폴백
            structured.append({"role": "author", "names": [author_str.strip()]})
            
    return structured

def build_mdx_content(data):
    """
    수집된 딕셔너리 데이터를 바탕으로 Next.js 최적화 MDX 문자열을 생성합니다.
    """
    # 🚨 [개선 1] tags 배열에서 'baekjoon', 'scraped' 필터링 (UI 오염 방지)
    clean_tags = [tag for tag in data.get("tags", []) if tag not in ("baekjoon", "scraped")]
    tags_str = json.dumps(clean_tags, ensure_ascii=False)
    
    # 배열 데이터를 YAML 배열 포맷으로 안전하게 변환
    contest_str = json.dumps(data.get("contest", []), ensure_ascii=False)
    
    # 🚨 [개선 3] authors 필드 구조화 및 다중 포맷 대응
    authors_structured = __parse_authors(data.get("authors", []))
    if not authors_structured:
        authors_yaml = "authors: []"
    else:
        authors_yaml_lines = ["authors:"]
        for sa in authors_structured:
            authors_yaml_lines.append(f"  - role: \"{sa['role']}\"")
            if sa['names']:
                names_json = json.dumps(sa['names'], ensure_ascii=False)
                authors_yaml_lines.append(f"    names: {names_json}")
            else:
                authors_yaml_lines.append("    names: []")
        authors_yaml = "\n".join(authors_yaml_lines)
    
    # Boolean 값을 YAML 표준 소문자(true/false)로 변환
    has_subtask_str = "true" if data.get("has_subtask") else "false"
    has_hint_str = "true" if data.get("has_hint") else "false"
    
    # 샘플 입출력 렌더링
    samples_md = ""
    for idx, sample_data in enumerate(data.get("samples", []), 1):
        s_in = sample_data[0]
        s_out = sample_data[1]
        explain_md = sample_data[2] if len(sample_data) > 2 else ""
        
        samples_md += f"### 예시 입력 {idx}\n```text\n{s_in}\n```\n\n### 예시 출력 {idx}\n```text\n{s_out}\n```\n\n"
        if explain_md.strip():
            samples_md += f"{explain_md}\n\n"    
    # 서브태스크 제목 번호를 4로, 힌트를 5로 변경하여 깔끔하게 조립
    subtask_section = f"## 4. 서브태스크\n\n{data['subtask_md']}\n\n---\n\n" if data.get('has_subtask') else ""
    hint_section = f"## 5. 힌트\n{data['hint_md']}\n\n---\n\n"
    
    # [신규] 첨부 섹션 조립 (노트 아래, 출처 위에 배치)
    attachment_section = ""
    if data.get("attachment_md") and data["attachment_md"].strip():
        attachment_section = f"## 6. 첨부\n\n{data['attachment_md']}\n\n---\n\n"

    # 🚨 [개선 2] Prefix를 통한 플랫폼 식별자 부여 (기본값 'bj')
    prefix = data.get('prefix', 'bj')
    platform_name = "baekjoon" if prefix == "bj" else "doingcoding"

    # 상단에 불리언 변환 로직 추가
    sprout_str = "true" if data.get("sprout") else "false"
    official_str = "true" if data.get("official") else "false"
    level_locked_str = "true" if data.get("is_level_locked") else "false" # 🚨 추가
    solvable_str = "true" if data.get("is_solvable") else "false" # 🚨 추가
    no_rating_str = "true" if data.get("gives_no_rating") else "false" # 🚨 추가
    # 리스트 데이터를 YAML 형식 문자열로 변환 (tag_keys)
    tag_keys_str = json.dumps(data.get("tag_keys", []), ensure_ascii=False)
    badges_str = json.dumps(data.get("badges", []), ensure_ascii=False) # 🚨 [신규] 배지 배열 변환

    # 최종 마크다운 조립
    return f"""---
id: {prefix}_{data['problem_id']}
title: "{data['title']}"
platform: "{platform_name}"
is_scraped: true
is_existent: true
level: {data['level']}
tier: "{get_solvedac_tier_name(data['level'])}"
archived_at: "{data.get('archived_at', '')}"
sprout: {sprout_str} 
official: {official_str} 
is_solvable: {solvable_str} 
gives_no_rating: {no_rating_str}
accepted_user_count: {data.get('accepted_user_count', 0)} 
average_tries: {data.get('average_tries', 0)} 
is_level_locked: {level_locked_str}
voted_user_count: {data.get('voted_user_count', 0)}
time_limit: "{data['time_limit']}"
memory_limit: "{data['memory_limit']}"
has_subtask: {has_subtask_str}
has_hint: {has_hint_str}
contest: {contest_str}
{authors_yaml}
tags: {tags_str}
tag_keys: {tag_keys_str}
badges: {badges_str}
source_url: "{data['url']}"
---

# [{data['problem_id']}번] {data['title']}

## 1. 문제 설명
{data['description']}

---

## 2. 입출력 설명

* **입력:**
{data['input_desc']}

* **출력:**
{data['output_desc']}

---

## 3. 예시

{samples_md}

---

{attachment_section}
{subtask_section}

{hint_section}

## [정답 및 해설 (Ground Truth)]

### 모범 코드 (Python)
**(백준 크롤러에서는 정답 코드를 긁어올 수 없으므로, 선생님께서 아래에 직접 보충해 주세요)**

```python
A, B = map(int, input().split())
print(A + B)
```
"""

def patch_file_badges(filepath, badges):
    """
    기존 마크다운 파일의 프론트매터에 badges 필드만 삽입하거나 교체합니다.
    본문은 절대 수정하지 않습니다.
    반환값: True(성공), False(프론트매터 구조 이상)
    """
    import re as _re
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            content = f.read()

        # 프론트매터 분리: --- 으로 시작하고 끝나는 영역
        fm_match = _re.match(r"^(---\n)(.*?)(---\n?)(.*)", content, _re.DOTALL)
        if not fm_match:
            print(f"  ⚠️ [Light] 프론트매터 구조 이상: {filepath}")
            return False

        pre_delim  = fm_match.group(1)   # 첫 번째 ---\n
        frontmatter = fm_match.group(2)  # 프론트매터 본문
        end_delim  = fm_match.group(3)   # 두 번째 ---\n
        body       = fm_match.group(4)   # 마크다운 본문

        badges_str = json.dumps(badges, ensure_ascii=False)
        new_field  = f"badges: {badges_str}\n"

        if _re.search(r"^badges:", frontmatter, _re.MULTILINE):
            # 이미 존재 → 값만 교체
            frontmatter = _re.sub(
                r"^badges:.*$",
                new_field.rstrip(),
                frontmatter,
                flags=_re.MULTILINE
            )
        else:
            # 없으면 프론트매터 마지막 줄 바로 위에 삽입
            frontmatter = frontmatter.rstrip("\n") + "\n" + new_field

        new_content = pre_delim + frontmatter + end_delim + body
        with open(filepath, "w", encoding="utf-8-sig") as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"  ❌ [Light] 파일 패치 실패 ({filepath}): {e}")
        return False


def scrape_baekjoon_light(url, context=None):
    """
    [초고속 배지 패치용] 백준 문제 페이지에서 problem-label 배지 텍스트만 수집합니다.
    - Solved.ac API 호출 없음
    - 이미지/CSS/폰트 등 비텍스트 리소스 전면 차단
    - 반환값: badges_list (list[str]) | None (접속 실패)
    """
    own_playwright = None
    own_browser_context = False
    browser = None
    if context is None:
        own_playwright = sync_playwright().start()
        browser = own_playwright.chromium.launch(headless=False)
        context = browser.new_context()
        own_browser_context = True

    page = context.new_page()

    # ★ 리소스 최소화: 이미지·CSS·폰트·미디어 전면 차단
    BLOCK_TYPES = {"image", "stylesheet", "font", "media"}
    def _block_heavy(route):
        if route.request.resource_type in BLOCK_TYPES:
            route.abort()
        else:
            route.continue_()
    page.route("**/*", _block_heavy)
    # MathJax도 차단
    page.route(re.compile(r"mathjax", re.IGNORECASE), lambda r: r.abort())

    problem_id = url.split("/")[-1]
    try:
        print(f"  🏃 [Light] {problem_id}번 배지 수집 중...")
        _goto_with_retries(
            page,
            url,
            wait_until="domcontentloaded",
            timeout=20000,
            ready_selector="#problem_title",
            attempts=2,
        )
        badge_elements = page.locator("span.problem-label").all_inner_texts()
        badges = [b.strip() for b in badge_elements if b.strip()]
        print(f"  ✅ [Light] {problem_id}번 배지: {badges if badges else '없음'}")
        return badges
    except ProblemNotFoundError:
        print(f"  ⚠️ [Light] {problem_id}번: 페이지 없음(404) - 스킵")
        return None
    except Exception as e:
        print(f"  ❌ [Light] {problem_id}번 접속 실패: {e}")
        return None
    finally:
        page.close()
        if own_browser_context:
            context.close()
            browser.close()
            own_playwright.stop()


def scrape_baekjoon(url, save_dir=None, context=None):
    """
    백준 문제 페이지를 크롤링하여 이미지 다운로드 및 메타데이터가 포함된 MD 문자열을 반환합니다.
    """
    if save_dir is None:
        save_dir = os.getcwd()

    own_playwright = None
    own_browser_context = False
    browser = None
    if context is None:
        own_playwright = sync_playwright().start()
        browser = own_playwright.chromium.launch(headless=False)
        context = browser.new_context()
        own_browser_context = True

    try:
        page = context.new_page()

        # 🚨 [수정됨] 정규식을 사용하여 URL 경로 어디에든 mathjax가 포함되어 있으면 완벽히 차단
        page.route(re.compile(r"mathjax", re.IGNORECASE), lambda route: route.abort())
        
        problem_id = url.split("/")[-1]

        try:
            # 1. [Early Exit 방어 로직] Solved.ac API 연동을 가장 먼저 수행하여 404 조기 차단
            print(f"[{problem_id}번] Solved.ac API 기반 사전 검증 및 데이터 수집 시작...")
            level, algo_tags, extra_info = get_solvedac_level_and_tags(context, problem_id)
            tags_list = ["baekjoon", "scraped"] + algo_tags

            print(f"[{problem_id}번] 백준 본문 페이지 접속 및 파싱 시작...")
            _goto_with_retries(
                page,
                url,
                wait_until="domcontentloaded",
                timeout=30000,
                ready_selector="#problem_title",
                attempts=3,
                referer="https://www.acmicpc.net/problemset",
                ready_selector_state="attached",  # 🔧 [FIX] 12096처럼 title이 hidden인 경우 대응
            )
            
            # 🚨 [분장 3] 리퍼러 위조 + 마우스 스크롤 + 랜덤 체류 시간 (인간미 추가)
            import random
            scroll_height = random.randint(300, 700)
            page.mouse.wheel(0, scroll_height)
            page.wait_for_timeout(random.randint(500, 1500))

            # 1. Solved.ac API 연동 (1단계 함수 호출) - 위치 위로 이동됨

            # 2. 기본 메타데이터 추출 (시간, 메모리)
            problem_info = page.locator('#problem-info tbody tr td').all_inner_texts()
            time_limit = problem_info[0].strip() if len(problem_info) > 0 else "N/A"
            memory_limit = problem_info[1].strip() if len(problem_info) > 1 else "N/A"


            # 3. 출처 및 대회 경로 추출 (Category Breadcrumbs)
            # 백준 페이지의 '#source' 영역 내에서 '/category/'로 시작하는 링크만 수집합니다.
            contest_elements = page.locator('#source a[href^="/category/"]').all_inner_texts()
            
            # 수집된 텍스트 중 불필요한 메타 단어 제거
            contest_list = []
            filter_words = ["Olympiad", "출처", "문제", "상태", "제표", ""]
            for t in contest_elements:
                cleaned = t.strip()
                if cleaned and cleaned not in filter_words:
                    contest_list.append(cleaned)
            
            # 중복 제거
            contest_list = list(dict.fromkeys(contest_list))

            # 제작/검수진 추출 (기존 로직 유지하되 안전성 강화)
            source_section = page.locator('#source')
            author_list = []
            if source_section.locator('ul').count() > 0:
                li_elements = source_section.locator('ul li').all_inner_texts()
                author_list = [t.strip() for t in li_elements if t.strip()]
            # source_elements = page.locator('#source a').all_inner_texts()
            # raw_contest_list = [text.strip() for text in source_elements if text.strip() != "Olympiad"]
            # # dict.fromkeys()를 이용해 순서를 유지하며 중복 제거
            # contest_list = list(dict.fromkeys(raw_contest_list))

            # 4. 제목 추출
            # 🚨 체크를 먼저 하고 텍스트를 가져옵니다.
            title_element = page.locator("#problem_title")
            if title_element.count() == 0:
                print(f"  ⚠️ 무결성 체크 실패: 페이지에서 제목 요소를 찾을 수 없습니다.")
                return None, None
            
            title = title_element.text_content(timeout=5000).strip()
            # 🔧 [FIX] 페이지 제목이 비어있는 경우 (예: 12096번 IQ Test)
            # Solved.ac API에서 미리 수집한 titleKo를 폴백으로 사용
            if not title:
                fallback_title = extra_info.get('titleKo', '')
                if fallback_title:
                    title = fallback_title
                    print(f"  ⚠️ [{problem_id}번] #problem_title 비어있음 - Solved.ac 제목으로 폴백: '{title}'")
                else:
                    title = f"문제 {problem_id}"
            # title = page.locator("#problem_title").text_content(timeout=5000).strip()
            # title_element = page.locator("#problem_title")
            # if title_element.count() == 0:
            #     print(f"  ⚠️ 무결성 체크 실패: 페이지에서 제목 요소를 찾을 수 없습니다.")
            #     return None, None
            # Solved.ac API 제목과 대조 (제목이 너무 다르면 잘못된 페이지일 확률이 높음)
            # 🚨 [개선] 다국어/인터랙티브 배지 등 공백 무시하고 알맹이만 비교
            solvedac_title = extra_info.get('titleKo', '')
            if solvedac_title:
                clean_solved = re.sub(r'\s+', '', solvedac_title)
                clean_target = re.sub(r'\s+', '', title)
                if clean_solved not in clean_target and clean_target not in clean_solved:
                    print(f"  ⚠️ 무결성 체크 실패: API 제목('{solvedac_title}') vs 페이지 제목('{title}')")
                    return None, None
                    
            # 🚨 [신규] 배지(problem-label) 수집
            badge_elements = page.locator('span.problem-label').all_inner_texts()
            badges_list = [b.strip() for b in badge_elements if b.strip()]
            
            # 5. 본문 (문제/입력/출력) HTML 추출 및 로컬 이미지 변환 (2단계 함수 호출)
# 5. 본문 HTML 추출 및 로컬 이미지 변환 (안전 추출 함수 도입)
            
            # 요소가 존재할 때만 inner_html()을 실행하는 기본 헬퍼
            def get_html_safe(selector):
                if page.locator(selector).count() > 0:
                    return page.locator(selector).inner_html()
                return ""
                
            # 🚨 [추가] 백준의 불규칙한 HTML ID를 무시하고 '화면에 보이는 제목'으로 강제 추적하는 헬퍼
            def get_section_by_heading(heading_text):
                # h2 태그에 특정 텍스트가 있는 section을 찾고, 그 안의 본문(.problem-text)을 가져옵니다.
                # 🔧 [FIX] .first 사용: 함수 구현형 문제 등 동일 heading이 2개 이상인 경우
                # Playwright strict mode violation (2 elements matched) 방지
                selector = f"section:has(h2:has-text('{heading_text}')) .problem-text"
                if page.locator(selector).count() > 0:
                    return page.locator(selector).first.inner_html()
                return ""

            desc_html = get_html_safe("#problem_description")
            # 🚨 [추가] 다국어 대응: 한국어 본문이 없거나 너무 작으면 영문 본문(#problem_description_en) 시도
            if not desc_html or len(desc_html.strip()) < 20:
                desc_html = get_html_safe("#problem_description_en") or desc_html
            
            description = process_html_and_download_images(desc_html, url, save_dir, problem_id, context=context)

            input_html = get_html_safe("#problem_input") or get_html_safe("#problem_input_en")
            input_desc = process_html_and_download_images(input_html, url, save_dir, problem_id, context=context)

            output_html = get_html_safe("#problem_output") or get_html_safe("#problem_output_en")
            output_desc = process_html_and_download_images(output_html, url, save_dir, problem_id, context=context)


            # 🚨 [추가] 엣지 케이스 병합 전에 빈칸부터 먼저 채워줍니다!
            description = description if description.strip() else "(본문이 없는 문제입니다.)"
            input_desc = input_desc if input_desc.strip() else "(입력 조건이 없습니다.)"
            output_desc = output_desc if output_desc.strip() else "(출력 조건이 없습니다.)"


            # ----------------------------------------------------
            # 👇 Playwright의 강력한 선택자를 활용한 엣지 케이스 완벽 대응 👇
            # ----------------------------------------------------
            
            # 1. 인터랙션 (ID가 무엇이든 화면에 '인터랙션' 제목이 있으면 무조건 추출)
            interaction_html = get_section_by_heading("인터랙션") or get_html_safe("#problem_interaction") or get_html_safe("#problem_interact")
            if interaction_html:
                interaction_desc = process_html_and_download_images(interaction_html, url, save_dir, problem_id, context=context)
                if interaction_desc.strip():
                    # 🚨 기존에 '없습니다' 안내 문구가 있다면 지우고 인터랙션 룰로 대체
                    if "(입력 조건이 없습니다.)" in input_desc:
                        input_desc = ""
                    input_desc = f"(이 문제는 인터랙티브 문제입니다.)\n\n### 인터랙션\n{interaction_desc}\n\n" + input_desc
            # 2. '제한' 유령 섹션 방어
            limit_html = get_section_by_heading("제한") or get_html_safe("#problem_limit")
            if limit_html:
                limit_desc = process_html_and_download_images(limit_html, url, save_dir, problem_id, context=context)
                if limit_desc.strip():
                    description += f"\n\n### 제한\n{limit_desc}"

            # 3. '노트' 유령 섹션 방어 (제목으로 직접 타겟팅)
            note_html = get_section_by_heading("노트") or get_html_safe("#problem_note")
            if note_html:
                note_desc = process_html_and_download_images(note_html, url, save_dir, problem_id, context=context)
                if note_desc.strip():
                    # 🚨 기존에 '없습니다' 안내 문구가 있다면 지우고 노트로 대체
                    if "(출력 조건이 없습니다.)" in output_desc:
                        output_desc = ""
                    output_desc += f"\n\n### 노트\n{note_desc}"
            
            # 4. [신규] '첨부 (Attachment)' 섹션 수집
            attachment_html = get_section_by_heading("첨부") or get_html_safe("#problem_attachment")
            attachment_md = ""
            if attachment_html:
                attachment_md = process_html_and_download_attachments(attachment_html, url, save_dir, problem_id, context=context)
                
            # ----------------------------------------------------
            # 6. 서브태스크 처리
            subtask_locator = page.locator("#problem_subtask")
            has_subtask = subtask_locator.count() > 0
            subtask_md = ""
            if has_subtask:
                subtask_html = subtask_locator.inner_html()
                subtask_md = process_html_and_download_images(subtask_html, url, save_dir, problem_id, context=context)

            # 7. 힌트 처리
            hint_locator = page.locator("#problem_hint")
            has_hint = hint_locator.count() > 0 and hint_locator.inner_text().strip() != ""
            hint_md = ""
            if has_hint:
                hint_html = hint_locator.inner_html()
                # 🚨 [추가] 백준이 '노트'를 '힌트' HTML 태그 안에 욱여넣은 경우, 중복 추출(복사) 방지 로직
                if note_html and hint_html.strip() == note_html.strip():
                    has_hint = False
                    hint_md = "(힌트가 없습니다.)"
                else:
                    hint_md = process_html_and_download_images(hint_html, url, save_dir, problem_id, context=context)
            else:
                hint_md = "(힌트가 없습니다.)"

            # 8. 샘플 입출력 추출 (다중 샘플 대응) - 순수 텍스트 유지
            samples = []
            i = 1
            while True:
                # 🔧 [FIX] 2029번처럼 description 안에 동일 ID(<pre>)가 존재하는 경우
                # pre.sampledata 클래스 조건 추가로 실제 예제 박스만 정확히 타겟팅
                in_sel = f"pre.sampledata#sample-input-{i}"
                out_sel = f"pre.sampledata#sample-output-{i}"
                if page.locator(in_sel).count() > 0 and page.locator(out_sel).count() > 0:
                    s_in = page.locator(in_sel).inner_text().strip()
                    s_out = page.locator(out_sel).inner_text().strip()
                    
                    # 🚨 [추가] 샘플에 대한 '예제 설명' 추출 (이미지 포함된 마크다운 변환 활용)
                    explain_sel = f"#problem_sample_explain_{i}"
                    explain_md = ""
                    if page.locator(explain_sel).count() > 0:
                        explain_html = page.locator(explain_sel).inner_html()
                        explain_md = process_html_and_download_images(explain_html, url, save_dir, problem_id, context=context)
                        
                    samples.append((s_in, s_out, explain_md))
                    i += 1
                else:
                    break

        except ProblemNotFoundError:
            raise # 🚨 [버그 픽스] 404 에러를 상위(gui_crawler)로 전파하여 더미 파일 생성을 유도
        except Exception as e:
            print(f"크롤링 에러({problem_id}): {e}")
            return None, None
        finally:
            page.close()
            if own_browser_context:
                context.close()
                browser.close()
                own_playwright.stop()

        # 🚨 [엣지 케이스 대응] 엄격한 검사 폐지 및 빈칸 채우기 🚨
        
        # 1. 제목조차 없다면 진짜 잘못된 페이지이므로 버립니다.
        if not title or title.strip() == "" or title == "(내용 없음)":
            print(f"⚠️ 제목을 찾을 수 없는 페이지입니다 ({problem_id})")
            return None, None
            
        # 2. 본문이나 입출력이 아예 없는 기출/퍼즐 문제를 위한 방어 코드 (대체 텍스트 삽입)
        description = description if description.strip() else "(본문이 없는 문제입니다.)"
        input_desc = input_desc if input_desc.strip() else "(입력 조건이 없습니다.)"
        output_desc = output_desc if output_desc.strip() else "(출력 조건이 없습니다.)"
        
        # missing_fields = _missing_required_fields({
        #     "title": title,
        #     "description": description,
        #     "input": input_desc,
        #     "output": output_desc,
        # })
        # if missing_fields:
        #     print(f"필수 필드 누락으로 저장하지 않음({problem_id}): {', '.join(missing_fields)}")
        #     return None, None

        # 샘플 데이터는 build_mdx_content에서 조립됩니다.

        # 배열 데이터를 YAML 포맷 문자열로 안전하게 변환
        tags_str = '["' + '", "'.join(tags_list) + '"]' if tags_list else '[]'
        contest_str = '["' + '", "'.join(contest_list) + '"]' if contest_list else '[]'
        has_subtask_str = "true" if has_subtask else "false"
        has_hint_str = "true" if has_hint else "false"

                # 수집한 데이터를 하나의 딕셔너리로 묶어 4단계 렌더링 함수로 전달
        mdx_data = {
            "problem_id": problem_id,
            "title": title,
            "level": level,
            "time_limit": time_limit,
            "memory_limit": memory_limit,
            "has_subtask": has_subtask,
            "has_hint": has_hint,
            "contest": contest_list,
            "tags": tags_list,
            **extra_info,
            "authors": author_list, # [추가]
            "url": url, 
            "description": description,
            "input_desc": input_desc,
            "output_desc": output_desc,
            "samples": samples,
            "subtask_md": subtask_md,
            "hint_md": hint_md,
            "attachment_md": attachment_md, # [추가]
            "badges": badges_list # 🚨 [신규] 배지 정보 추가
        }

           # 4단계 함수 호출을 통해 깔끔하게 MDX 생성!
        md_content = build_mdx_content(mdx_data)

        # --- [3단계: 최종 무결성 검사] ---
        # 1. 본문(description)이 너무 짧은 경우 (비정상 수집)
        # 2. 결과물에 Cloudflare 차단 문구가 포함된 경우
        # 🚨 [개선] 다국어/인터랙티브 문제는 본문이 짧을 수 있으므로 전체 MD 길이를 함께 고려
        error_keywords = ["Access Denied", "403 Forbidden", "무단 접근"] # Cloudflare는 본문에 섞일 수 있어 제외하거나 정교화
        is_blocked = any(kw in md_content for kw in error_keywords) and "Cloudflare" in md_content
        
        if (len(description.strip()) < 5 and len(md_content) < 500) or is_blocked:
            print(f"  ⚠️ 무결성 체크 실패: 본문이 비어있거나 차단 페이지로 의심됩니다.")
            return None, None

    finally:
        try:
            if 'page' in locals() and page:
                page.close()
            if own_browser_context:
                if 'context' in locals() and context:
                    context.close()
                if browser:
                    browser.close()
                if own_playwright:
                    own_playwright.stop()
        except Exception:
            pass

    return title, md_content


# 이전버전: 백준 단순 텍스트로만 가져옴
# def scrape_baekjoon(url):
#     with sync_playwright() as p:
#         # headless=False로 띄워야 백준(acmicpc)의 봇 탐지(Cloudflare 등)를 우회하기 좋습니다.
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()

#         try:
#             _goto_with_retries(
#                 page,
#                 url,
#                 wait_until="domcontentloaded",
#                 timeout=10000,
#                 ready_selector="#problem_title",
#                 attempts=3,
#             )

#             # CSS Selector(id 기반)를 이용한 핵심 요소 추출
#             problem_id = url.split("/")[-1]
#             print(problem_id)
#             title = page.locator("#problem_title").text_content(timeout=5000).strip()
#             description = page.locator("#problem_description").inner_text().strip()
#             input_desc = page.locator("#problem_input").inner_text().strip()
#             output_desc = page.locator("#problem_output").inner_text().strip()

#             # 샘플 입출력 추출 (다중 샘플 대응)
#             samples = []
#             i = 1
#             while True:
#                 in_sel = f"#sample-input-{i}"
#                 out_sel = f"#sample-output-{i}"
#                 if (
#                     page.locator(in_sel).count() > 0
#                     and page.locator(out_sel).count() > 0
#                 ):
#                     s_in = page.locator(in_sel).inner_text().strip()
#                     s_out = page.locator(out_sel).inner_text().strip()
#                     samples.append((s_in, s_out))
#                     i += 1
#                 else:
#                     break

#             # 힌트 추출 (있을 수도, 없을 수도 있음)
#             hint = ""
#             if page.locator("#problem_hint").count() > 0:
#                 hint = page.locator("#problem_hint").inner_text().strip()

#         except Exception as e:
#             print(f"크롤링 에러: {e}")
#             return None, None
#         finally:
#             browser.close()

#         missing_fields = _missing_required_fields(
#             {
#                 "title": title,
#                 "description": description,
#                 "input": input_desc,
#                 "output": output_desc,
#             }
#         )
#         if missing_fields:
#             print(
#                 f"필수 필드 누락으로 저장하지 않음({problem_id}): {', '.join(missing_fields)}"
#             )
#             return None, None

#         # 샘플 MD 조립
#         samples_md = ""
#         for idx, (s_in, s_out) in enumerate(samples, 1):
#             samples_md += f"### 예시 입력 {idx}\n```text\n{s_in}\n```\n\n### 예시 출력 {idx}\n```text\n{s_out}\n```\n\n"

#         # 수석 감수자 권장 마크다운(MD) 템플릿에 맞추어 문자열 포매팅
#         md_content = f"""---
# id: bj_{problem_id}
# tags: [baekjoon, scraped]
# source: {url}
# ---

# # [{problem_id}번] {title}

# ## 1. 문제 설명
# {description}

# ---

# ## 2. 입출력 설명

# * **입력:**
# {input_desc}

# * **출력:**
# {output_desc}

# ---

# ## 3. 예시

# {samples_md}---

# ## 4. 힌트
# {hint if hint else "(힌트가 없습니다.)"}

# ---

# <!-- ANSWER_START -->
# ## [정답 및 해설 (Ground Truth)]

# ### 모범 코드 (Python)
# **(백준 크롤러에서는 정답 코드를 긁어올 수 없으므로, 선생님께서 아래에 직접 보충해 주세요)**

# ```python
# A, B = map(int, input().split())
# print(A + B)
# ```
# <!-- ANSWER_END -->
# """
#         return title, md_content


def scrape_doingcoding(
    url,
    get_templates=False,
    get_testcases=False,
    admin_username=None,
    admin_password=None,
    testcase_download_dir=None,
    show_browser=False,
    logger=None,
    browser=None,
    admin_session=None,
):
    owned_playwright = None
    owned_browser = False
    if browser is None:
        playwright_factory = sync_playwright()
        if hasattr(playwright_factory, "start"):
            owned_playwright = playwright_factory.start()
        else:
            owned_playwright = playwright_factory
        # 자체 학원 사이트는 봇 탐지가 약할 수 있으므로 headless=True로 1초 만에 수집 가능
        browser = owned_playwright.chromium.launch(headless=not show_browser)
        owned_browser = True

    page = browser.new_page()

    try:
        # 타임아웃을 넉넉하게 주고 네트워크 통신이 끝날 때까지 기다립니다.
        _goto_with_retries(
            page,
            url,
            wait_until="domcontentloaded",
            timeout=10000,
            ready_selector="#problem-main",
            attempts=3,
        )

        problem_id = url.split("/")[-1]
        tree = html.fromstring(page.content())
        content_root = _find_doingcoding_content_root(tree)

        # 요소가 없을 경우에 봇이 죽지 않도록 방어 코드(Safe Extraction)를 적용합니다.
        def get_text(xpath, timeout=2000):
            try:
                el = page.locator(xpath).first
                el.wait_for(timeout=timeout)
                return el.inner_text().strip()
            except:
                return "(내용 없음)"

        title = _find_doingcoding_title(tree) or get_text(
            '//*[@id="problem-main"]/div[3]/div[1]/div/div', 5000
        )
        if title == "(내용 없음)" or not _clean_text(title):
            # 제목마저 못가져오면 진짜 아예 페이지가 없거나 로딩이 실패한 것임
            raise Exception("제목 요소를 찾을 수 없음")

        description = ""
        input_desc = ""
        output_desc = ""
        if content_root is not None:
            description = _extract_section_after_heading(
                content_root, SECTION_HEADINGS["description"]
            )
            input_desc = _extract_section_after_heading(
                content_root, SECTION_HEADINGS["input"]
            )
            output_desc = _extract_section_after_heading(
                content_root, SECTION_HEADINGS["output"]
            )

        description = description or get_text('//*[@id="problem-content"]/p[2]')
        input_desc = input_desc or get_text('//*[@id="problem-content"]/p[4]')
        output_desc = output_desc or get_text('//*[@id="problem-content"]/p[6]')

        # 샘플 입출력 추출 (다중 샘플 대응)
        samples = (
            _extract_sample_pairs(content_root) if content_root is not None else []
        )
        if not samples:
            i = 1
            while True:
                in_xpath = f'//*[@id="problem-content"]/div[{i}]/div/div[1]/pre'
                out_xpath = f'//*[@id="problem-content"]/div[{i}]/div/div[2]/pre'

                s_in = get_text(in_xpath, timeout=1000)
                s_out = get_text(out_xpath, timeout=1000)

                if s_in == "(내용 없음)" and s_out == "(내용 없음)":
                    break

                samples.append((s_in, s_out))
                i += 1

        # 힌트 추출 (사용자 제공 XPath)
        hint = get_text('//*[@id="problem-content"]/div[2]/div/div/div')

        # 코드 템플릿 추출 (C, C++, Python3, Java) - 옵션 선택 시에만 동작
        templates = {}
        if get_templates:
            try:
                # 언어 선택 드롭다운이 있는지 확인
                dropdown = page.locator("div.ivu-select-selection").first
                if dropdown.count() > 0:
                    for lang_name in ["C", "C++", "Python3", "Java"]:
                        # 드롭다운 클릭
                        dropdown.click()
                        page.wait_for_timeout(500)

                        # 해당 언어 옵션 클릭
                        lang_option = page.locator(
                            f'li.ivu-select-item:has-text("{lang_name}")'
                        ).first
                        if lang_option.count() > 0:
                            lang_option.click()
                            page.wait_for_timeout(500)

                            # 새로고침(초기화) 버튼 클릭 시도 (템플릿 강제 로드)
                            reset_btn = page.locator("button.ivu-btn-icon-only")
                            if reset_btn.count() > 0:
                                reset_btn.first.click()
                                page.wait_for_timeout(500)
                                # 확인 모달의 '예' 버튼
                                confirm_btn = page.locator(
                                    'button.ivu-btn-primary:has-text("예")'
                                )
                                if confirm_btn.count() > 0:
                                    confirm_btn.click()
                                    page.wait_for_timeout(1000)

                            code_text = _extract_editor_code(page)
                            if code_text:
                                templates[lang_name] = code_text
            except Exception as te:
                # 템플릿 추출 실패는 전체 크롤링 실패로 간주하지 않음
                print(f"템플릿 추출 중 경미한 에러 (문제 없음): {te}")

        testcase_bundle = {}
        if get_testcases:
            if admin_session is not None:
                work_root = testcase_download_dir or os.getcwd()
                temp_dir = tempfile.mkdtemp(
                    prefix=f"dc_tc_{problem_id}_", dir=work_root
                )
                try:
                    bundle_path = collect_doingcoding_testcases_with_session(
                        admin_session,
                        problem_id,
                        temp_dir,
                        logger=logger,
                    )
                    extract_dir = os.path.join(temp_dir, "extract")
                    bundle = parse_testcase_bundle(bundle_path, extract_dir)
                    testcase_bundle = {
                        "info": bundle.get("info", {}),
                        "cases": bundle.get("cases", []),
                    }
                finally:
                    shutil.rmtree(temp_dir, ignore_errors=True)
            else:
                testcase_bundle = collect_doingcoding_testcases(
                    browser,
                    problem_id,
                    admin_username,
                    admin_password,
                    base_download_dir=testcase_download_dir,
                    logger=logger,
                )

    except Exception as e:
        print(f"XPath 크롤링 에러({url}): {e}")
        return None, None
    finally:
        if hasattr(page, "close"):
            page.close()
        if owned_browser:
            browser.close()
        if owned_playwright is not None and hasattr(owned_playwright, "stop"):
            owned_playwright.stop()

    missing_fields = _missing_required_fields(
        {
            "title": title,
            "description": description,
            "input": input_desc,
            "output": output_desc,
        }
    )
    if missing_fields:
        print(
            f"필수 필드 누락으로 저장하지 않음({problem_id}): {', '.join(missing_fields)}"
        )
        return None, None

    # 샘플 MD 조립
    samples_md = ""
    for idx, (s_in, s_out) in enumerate(samples, 1):
        samples_md += f"### 예시 입력 {idx}\n```text\n{s_in}\n```\n\n### 예시 출력 {idx}\n```text\n{s_out}\n```\n\n"

    next_section_number = 5
    testcases_md = ""
    if testcase_bundle:
        testcases_md = render_testcases_md(
            testcase_bundle, section_number=next_section_number
        )
        next_section_number += 1

    templates_md = render_templates_md(templates, section_number=next_section_number)

    # 수석 감수자 권장 마크다운(MD) 템플릿에 맞추어 문자열 포매팅
    md_content = f"""---
id: dc_{problem_id}
tags: [doingcoding, scraped]
source: {url}
---

# [{problem_id}번] {title}

## 1. 문제 설명
{description}

---

## 2. 입출력 설명

* **입력:**
{input_desc}

* **출력:**
{output_desc}

---

## 3. 예시

{samples_md}---

## 4. 힌트
{hint if hint and hint != "(내용 없음)" else "(힌트가 없습니다.)"}

---

{testcases_md}{templates_md}<!-- ANSWER_START -->
## [정답 및 해설 (Ground Truth)]

### 모범 코드 (Python)
**(백준 크롤러에서는 정답 코드를 긁어올 수 없으므로, 선생님께서 아래에 직접 보충해 주세요)**

```python
A, B = map(int, input().split())
print(A + B)
```
<!-- ANSWER_END -->
"""
    return title, md_content


if __name__ == "__main__":
    target_url = "http://edu.doingcoding.com/problem/P101v0701"
    print(f"[크롤링 시작] {target_url}")

    title, md_output = scrape_doingcoding(target_url, get_templates=False)

    if md_output:
        # 결과를 현재 폴더에 저장
        save_path = f"01_dc_{target_url.split('/')[-1]}.md"
        with open(save_path, "w", encoding="utf-8-sig") as f:
            f.write(md_output)
        print(f"[성공] 크롤링 완료! 파일이 저장되었습니다: '{save_path}'")
