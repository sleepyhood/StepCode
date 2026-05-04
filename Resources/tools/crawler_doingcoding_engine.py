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
import random

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
    
    def convert_img(self, el, text, **kwargs):
        """헤딩 내부에서도 이미지를 텍스트로 치환하지 않고 ![]() 형식을 유지하도록 오버라이드"""
        alt = el.get('alt') or ''
        src = el.get('src') or ''
        title = el.get('title') or ''
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        return '![%s](%s%s)' % (alt, src, title_part)

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
DOINGCODING_ADMIN_TESTCASE_API = "http://edu.doingcoding.com/api/admin/test_case?problem_id={db_id}"
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
    'xpath=//*[@id="app"]//table/tbody/tr[1]',
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


def _to_yaml(data):
    """딕셔너리를 간단한 YAML 문자열로 변환 (프론트매터용)"""
    lines = []
    for k, v in data.items():
        if isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - \"{item}\"")
        elif isinstance(v, str):
            # 줄바꿈이나 따옴표가 포함된 경우 안전하게 처리
            safe_v = v.replace('"', '\\"')
            lines.append(f"{k}: \"{safe_v}\"")
        else:
            lines.append(f"{k}: {v}")
    return "\n".join(lines)

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


def _extract_section_html_after_heading(content_root, labels):
    """
    특정 헤더 이후의 내용을 HTML 문자열로 추출합니다. (이미지 수집용)
    """
    children = list(_iter_direct_children(content_root))
    for index, child in enumerate(children):
        text = _element_text(child)
        if not _matches_heading(text, labels):
            continue

        chunks = []
        for sibling in children[index + 1 :]:
            sibling_text = _element_text(sibling)
            # 다음 섹션 헤더를 만나면 중단
            if _looks_like_section_heading(sibling_text):
                break
            # HTML 요소 자체를 문자열로 변환
            chunks.append(html.tostring(sibling, encoding="unicode"))

        if chunks:
            return "".join(chunks)

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


def download_doingcoding_testcases(page, problem_id, download_dir, db_id):
    """
    UI 검색 및 클릭 대신, 관리자 세션 쿠키를 이용해 직접 API로 테스트케이스 ZIP을 다운로드합니다.
    db_id (숫자 ID)를 필수 파라미터로 사용합니다.
    """
    if not db_id:
        raise ValueError(f"테스트케이스 다운로드를 위해 db_id가 필요합니다. (problem_id: {problem_id})")

    os.makedirs(download_dir, exist_ok=True)
    
    # 1. API URL 구성 (db_id 사용)
    download_url = DOINGCODING_ADMIN_TESTCASE_API.format(db_id=db_id)
    
    # 2. 직접 API 요청
    response = page.request.get(download_url)
    if not response.ok:
        raise RuntimeError(f"테스트케이스 API 호출 실패 (상태: {response.status}, URL: {download_url})")
    
    # 3. 파일명 결정 및 저장
    suggested_filename = f"{problem_id}.zip"
    cd_header = response.headers.get("content-disposition", "")
    if "filename=" in cd_header:
        suggested_filename = cd_header.split("filename=")[-1].strip('" ')

    download_path = os.path.join(download_dir, suggested_filename)
    with open(download_path, "wb") as f:
        f.write(response.body())
        
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
    session, problem_id, download_dir, logger=None, db_id=None
):
    _emit_log(logger, "[관리자 세션] 기존 로그인 세션 재사용")
    try:
        return download_doingcoding_testcases(session.page, problem_id, download_dir, db_id=db_id)
    except Exception:
        _emit_log(logger, "[관리자 세션] 세션 재로그인 시도")
        login_doingcoding_admin(
            session.page, session.username, session.password, logger=logger
        )
        return download_doingcoding_testcases(session.page, problem_id, download_dir, db_id=db_id)

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
    db_id=None,
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
            db_id=db_id,
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
    
    # 샘플 입출력 렌더링 (동적 모드 fallback 포함)
    samples_md = ""
    for idx, sample_data in enumerate(data.get("samples", []), 1):
        s_in = sample_data[0]
        s_out = sample_data[1]
        explain_md = sample_data[2] if len(sample_data) > 2 else ""
        
        samples_md += f"### 예시 입력 {idx}\n```text\n{s_in}\n```\n\n### 예시 출력 {idx}\n```text\n{s_out}\n```\n\n"
        if explain_md.strip():
            samples_md += f"{explain_md}\n\n"

    # [동적 모드 fallback] 표준 샘플이 없으면 custom_example 섹션 사용 (Case A)
    if not samples_md.strip():
        custom_example_md = data.get("custom_example_md", "").strip()
        if custom_example_md:
            samples_md = custom_example_md  # 이미지/표 포함 예시 그대로 삽입
        else:
            samples_md = "*(이 문제는 공개된 예시가 없습니다. 첨부 파일을 참고하세요.)*"  # Case C

    # 서브태스크 제목 번호를 4로, 힌트를 5로 변경하여 깔끔하게 조립
    subtask_section = f"## 4. 서브태스크\n\n{data['subtask_md']}\n\n---\n\n" if data.get('has_subtask') else ""
    hint_section = f"## 5. 힌트\n{data['hint_md']}\n\n---\n\n"
    
    # [신규] 첨부 섹션 조립 (노트 아래, 출처 위에 배치)
    attachment_section = ""
    if data.get("attachment_md") and data["attachment_md"].strip():
        attachment_section = f"## 6. 첨부\n\n{data['attachment_md']}\n\n---\n\n"

    # [동적 모드] extra_sections 렌더링 (구현, 제출할 수 있는 언어, custom_* 등)
    extra_sections_md = ""
    for sec_title, sec_content in data.get("extra_sections", []):
        if sec_content.strip():
            extra_sections_md += f"## {sec_title}\n\n{sec_content}\n\n---\n\n"

    # 🚨 [개선 2] Prefix를 통한 플랫폼 식별자 부여 (기본값 'bj')
    prefix = data.get('prefix', 'bj')
    platform_name = "baekjoon" if prefix == "bj" else "doingcoding"

    if platform_name == "doingcoding":
        id_str = f"id: {data['problem_id']}\nlegacy_id: {data['problem_id']}"
    else:
        id_str = f"id: {prefix}_{data['problem_id']}"

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
{id_str}
title: "{data['title']}"
platform: "{platform_name}"
is_scraped: true
is_existent: true
level: {data['level']}
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

{attachment_section}{extra_sections_md}{subtask_section}

{hint_section}

## [정답 및 해설 (Ground Truth)]

### 모범 코드 (Python)
**(백준 크롤러에서는 정답 코드를 긁어올 수 없으므로, 선생님께서 아래에 직접 보충해 주세요)**

```python
A, B = map(int, input().split())
print(A + B)
```
"""

def extract_sections_dynamic(page, url, save_dir, problem_id, context=None):
    """
    [동적 모드 전용] Playwright page로 로드된 백준 문제 페이지에서
    모든 <section> 태그를 순회하여 콘텐츠를 수집합니다.

    반환값: mdx_data에 병합할 딕셔너리
    {
        "description": str,
        "input_desc": str,
        "output_desc": str,
        "samples": list[(in, out, explain)],
        "custom_example_md": str,   # custom_example 섹션 (예시 fallback)
        "subtask_md": str,
        "has_subtask": bool,
        "hint_md": str,
        "has_hint": bool,
        "attachment_md": str,
        "extra_sections": list[(title, md)],  # 동적 수집 섹션 (구현, 제출언어 등)
    }
    """
    # 스킵할 섹션 id (메타데이터로 따로 처리되거나 불필요)
    SKIP_IDS = {"source", "problem-judge-info"}
    # 표준 입출력 샘플 섹션 id 패턴
    import re as _re

    result = {
        "description": "",
        "input_desc": "",
        "output_desc": "",
        "samples": [],
        "custom_example_md": "",
        "subtask_md": "",
        "has_subtask": False,
        "hint_md": "(힌트가 없습니다.)",
        "has_hint": False,
        "attachment_md": "",
        "extra_sections": [],
    }

    # 1. 전체 HTML을 BeautifulSoup으로 파싱
    from bs4 import BeautifulSoup
    html_content = page.content()
    soup = BeautifulSoup(html_content, "html.parser")

    # 2. 표준 샘플 I/O 수집 (Playwright locator 사용 — 기존 방식 유지)
    i = 1
    while True:
        in_sel  = f"pre.sampledata#sample-input-{i}"
        out_sel = f"pre.sampledata#sample-output-{i}"
        if page.locator(in_sel).count() > 0 and page.locator(out_sel).count() > 0:
            s_in  = page.locator(in_sel).inner_text().strip()
            s_out = page.locator(out_sel).inner_text().strip()
            explain_sel = f"#problem_sample_explain_{i}"
            explain_md = ""
            if page.locator(explain_sel).count() > 0:
                explain_html = page.locator(explain_sel).inner_html()
                explain_md = process_html_and_download_images(explain_html, url, save_dir, problem_id, context=context)
            result["samples"].append((s_in, s_out, explain_md))
            i += 1
        else:
            break

    # 3. section 태그 순회
    sections = soup.select("#problem-body section")
    for sec in sections:
        sec_id = (sec.get("id") or "").strip()

        # 스킵 대상
        if sec_id in SKIP_IDS:
            continue
        # 표준 샘플 섹션 (sampleinputN, sampleoutputN) — 이미 위에서 처리
        if _re.match(r"^sample(input|output)\d+$", sec_id, _re.IGNORECASE):
            continue

        # 제목 추출
        title_tag = sec.find(["h2", "h3"])
        display_title = title_tag.get_text(strip=True) if title_tag else ""

        # 본문 추출 (div.problem-text 내부 HTML)
        content_div = sec.find("div", class_="problem-text")
        if not content_div:
            continue
        content_html = str(content_div)
        content_md = process_html_and_download_images(content_html, url, save_dir, problem_id, context=context)
        content_text = content_md.strip()

        if not content_text:
            continue  # 빈 섹션 스킵

        # 4. 섹션 ID/제목에 따라 고정 필드에 배치
        if sec_id == "description":
            result["description"] = content_md

        elif sec_id == "input":
            result["input_desc"] = content_md

        elif sec_id == "output":
            result["output_desc"] = content_md

        elif sec_id == "limit":
            # 제한은 description 뒤에 append
            result["description"] += f"\n\n### 제한\n{content_md}"

        elif sec_id == "subtask":
            result["subtask_md"] = content_md
            result["has_subtask"] = True

        elif sec_id == "hint":
            result["hint_md"] = content_md
            result["has_hint"] = True

        elif _re.match(r"^custom_att+achment$", sec_id):
            # custom_attachment 또는 custom_atttachment (오타 변종) 통합
            result["attachment_md"] = content_md

        elif sec_id == "custom_example":
            # 이미지/표가 포함된 예시 섹션 (표준 sample-input-N 대체)
            result["custom_example_md"] = content_md

        else:
            # 그 외 모든 동적 섹션 (custom_implementation, language_restrict 등)
            result["extra_sections"].append((display_title, content_md))

    # 5. 빈칸 채우기
    if not result["description"].strip():
        result["description"] = "(본문이 없는 문제입니다.)"
    if not result["input_desc"].strip():
        result["input_desc"] = "(입력 조건이 없습니다.)"
    if not result["output_desc"].strip():
        result["output_desc"] = "(출력 조건이 없습니다.)"

    print(f"  [Dynamic] {problem_id}번 섹션 수집 완료 — "
          f"samples={len(result['samples'])}, "
          f"custom_example={'있음' if result['custom_example_md'] else '없음'}, "
          f"extra={len(result['extra_sections'])}개")
    return result


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
        problem_id = url.split("/")[-1]
        
        # --- [1. 관리자 세션 확보] ---
        local_admin_session = admin_session
        if local_admin_session is None and admin_username and admin_password:
            try:
                local_admin_session = open_doingcoding_admin_session(
                    browser, admin_username, admin_password, logger=logger
                )
            except Exception as e:
                _emit_log(logger, f"  [오류] 관리자 세션 생성 실패: {e}")

        # --- [2. API 데이터 선제적 수집] ---
        api_data = {}
        if local_admin_session:
            try:
                api_url = f"http://edu.doingcoding.com/api/problem?problem_id={problem_id}"
                response = local_admin_session.page.request.get(api_url)
                
                # 404인 경우 특수 신호 반환
                if response.status == 404:
                    return "404_NOT_FOUND", None, "NULL"
                
                if response.ok:
                    json_res = response.json()
                    api_data = json_res.get("data", {})
                    
                    # 데이터가 없거나(None), 문자열인 경우(에러 메시지 등) 404로 간주
                    if not api_data or isinstance(api_data, str):
                        _emit_log(logger, f"  [확인] API 응답에 유효한 데이터가 없음: {problem_id}")
                        return "404_NOT_FOUND", None, "NULL"
                        
                    _emit_log(logger, f"  [API] 문제 데이터 수집 성공: {problem_id}")
                else:
                    # 404를 포함한 모든 실패 상태에 대해 격리 처리
                    _emit_log(logger, f"  [오류] API 호출 실패 (상태: {response.status})")
                    return "404_NOT_FOUND", None, "NULL"

            except Exception as e:
                _emit_log(logger, f"  [오류] API 호출 중 예외: {e}")

        # --- [3. 데이터 초기화 및 매핑] ---
        title = api_data.get("title", "Unknown Title")
        time_limit = f"{api_data.get('time_limit', 1000)/1000:g}s"
        memory_limit = f"{api_data.get('memory_limit', 256)}MB"
        db_id = api_data.get("id", "")
        scraped_tags = api_data.get("tags", [])
        supported_languages = api_data.get("languages", [])
        accepted_user_count = api_data.get("accepted_number", 0)
        level = api_data.get("difficulty", "Unrated")
        authors = []
        if api_data.get("created_by"):
            authors.append(api_data["created_by"].get("username", ""))
        
        hint_text = api_data.get("hint", "")
        has_hint = "true" if hint_text and len(hint_text.strip()) > 0 else "false"
        
        # 샘플 데이터 매핑
        samples = []
        for s in api_data.get("samples", []):
            samples.append((s.get("input", ""), s.get("output", "")))

        # 템플릿(코드) 매핑
        templates = api_data.get("template", {})

        # --- [4. 이미지 유무 검사 및 분기] ---
        full_html_body = (api_data.get("description") or "") + (api_data.get("input_description") or "") + \
                         (api_data.get("output_description") or "") + (api_data.get("hint") or "")
        has_images = "<img" in full_html_body.lower()
        
        # API 데이터를 기본값으로 설정 (이미지 다운로드 로직 포함)
        api_base_url = "http://edu.doingcoding.com" # API 데이터의 이미지는 도메인 루트 기준일 가능성이 높음
        save_dir = testcase_download_dir
        
        description = process_html_and_download_images(api_data.get("description", ""), api_base_url, save_dir, problem_id, context=browser)
        input_desc = process_html_and_download_images(api_data.get("input_description", ""), api_base_url, save_dir, problem_id, context=browser)
        output_desc = process_html_and_download_images(api_data.get("output_description", ""), api_base_url, save_dir, problem_id, context=browser)
        hint_text = process_html_and_download_images(api_data.get("hint", ""), api_base_url, save_dir, problem_id, context=browser)
        
        save_dir = testcase_download_dir

        if has_images:
            _emit_log(logger, f"  [수집] 본문 내 이미지 감지됨. UI 크롤링 병행.")
            _goto_with_retries(
                page,
                url,
                wait_until="domcontentloaded",
                timeout=10000,
                ready_selector="#problem-main",
                attempts=2,
            )
            page.wait_for_timeout(1000) # 중요: 동적 콘텐츠(Vue/React 등)가 그려질 시간 확보

            # UI에서 섹션별 HTML 추출 및 이미지 처리
            problem_content_el = page.locator("#problem-content")
            if problem_content_el.count() > 0:
                titles_els = page.locator("#problem-content .title").all()
                contents_els = page.locator("#problem-content .content").all()
                
                for t_el, c_el in zip(titles_els, contents_els):
                    t_text = t_el.inner_text().strip()
                    c_html = c_el.inner_html()
                    
                    processed_html = process_html_and_download_images(c_html, url, save_dir, problem_id, context=browser)
                    md_text = processed_html
                    
                    if _matches_heading(t_text, SECTION_HEADINGS["description"]):
                        description = md_text
                    elif _matches_heading(t_text, SECTION_HEADINGS["input"]):
                        input_desc = md_text
                    elif _matches_heading(t_text, SECTION_HEADINGS["output"]):
                        output_desc = md_text
                    elif _matches_heading(t_text, SECTION_HEADINGS["hint"]):
                        hint_text = md_text
        else:
            _emit_log(logger, f"  [수집] 텍스트 중심 문제 (API 데이터 활용)")
            # 이미 위에서 API 데이터를 기반으로 이미지를 처리했으므로 추가 작업 불필요
            pass

        # --- [5. 테스트케이스 수집 (선택)] ---
        if get_testcases and local_admin_session:
            _emit_log(logger, f"  [수집] 테스트케이스 다운로드 시도: {problem_id}")
            try:
                # 개편된 API 방식의 다운로드 함수 호출 (db_id 필수 전달)
                download_doingcoding_testcases(local_admin_session.page, problem_id, save_dir, db_id=db_id)
                _emit_log(logger, f"  [수집] 테스트케이스 저장 성공.")
            except Exception as de:
                _emit_log(logger, f"  [오류] 테스트케이스 다운로드 실패: {de}")

        # --- [6. 최종 마크다운 조립] ---
        # API 데이터가 samples를 가지고 있으므로 이를 그대로 사용 (위에서 이미 mapping 완료)
        
        # 프론트매터 생성
        front_matter = {
            "id": problem_id,
            "db_id": db_id,
            "legacy_id": problem_id,
            "title": title,
            "platform": "doingcoding",
            "level": level,
            "tags": scraped_tags,
            "authors": authors,
            "supported_languages": supported_languages,
            "time_limit": time_limit,
            "memory_limit": memory_limit,
            "accepted_user_count": accepted_user_count,
            "has_hint": has_hint,
            "archived_at": datetime.now().strftime("%Y-%m-%d"),
        }

        # 템플릿 코드 처리
        template_blocks = ""
        if get_templates and templates:
            for lang, code in templates.items():
                if code and code.strip():
                    template_blocks += f"\n## {lang} Template\n\n```{lang.lower()}\n{code}\n```\n"

        # 최종 내용 조립
        # 최종 내용 조립
        md_output = f"""---
{_to_yaml(front_matter)}
---

# {title}

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
"""
        # 예시(Sample) 반복문: 불렛 포인트 제거 및 헤더 기반으로 변경
        for i, (sin, sout) in enumerate(samples, 1):
            md_output += f"### 예시 입력 {i}\n```text\n{sin}\n```\n\n### 예시 출력 {i}\n```text\n{sout}\n```\n\n"
 
        # 힌트 섹션 (항상 생성하여 1-4번 구조 유지)
        md_output += "---\n\n## 4. 힌트\n"
        if hint_text and has_hint == "true":
            md_output += f"{hint_text}\n"
        else:
            md_output += "(힌트가 없습니다.)\n"


        # 마지막 구분선 및 템플릿 코드 추가
        md_output += f"---\n\n{template_blocks}"

#         md_output = f"""---
# {_to_yaml(front_matter)}
# ---

# # {title}

# ## 1. 문제 설명
# {description}

# ## 2. 입력
# {input_desc}

# ## 3. 출력
# {output_desc}

# ## 4. 예제 입출력
# """
#         for i, (sin, sout) in enumerate(samples, 1):
#             md_output += f"### 예제 {i}\n- **입력**: \n```text\n{sin}\n```\n- **출력**: \n```text\n{sout}\n```\n\n"

#         if hint_text and has_hint == "true":
#             md_output += f"## 5. 힌트\n{hint_text}\n"

#         md_output += template_blocks


        return title, md_output,  db_id

    except Exception as e:
        _emit_log(logger, f"  [치명적 오류] {problem_id} 수집 실패: {e}")
        raise e
    finally:
        if page:
            page.close()

if __name__ == "__main__":
    target_url = "http://edu.doingcoding.com/problem/P101v0101"
    print(f"[크롤링 시작] {target_url}")

    title, md_output, db_id = scrape_doingcoding(target_url, get_templates=False)

    if md_output:
        # 결과를 현재 폴더에 저장
        problem_id = target_url.split('/')[-1]
        save_path = f"{problem_id}_{db_id}.md"
        # save_path = f"01_dc_{target_url.split('/')[-1]}.md"
        with open(save_path, "w", encoding="utf-8-sig") as f:
            f.write(md_output)
        print(f"[성공] 크롤링 완료! 파일이 저장되었습니다: '{save_path}'")
