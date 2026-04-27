import os
import re
import shutil
from typing import Dict, Optional, Tuple
from playwright.sync_api import BrowserContext

def get_score_priority(result_text: str) -> int:
    """점수 텍스트를 파싱하여 우선순위 점수를 반환합니다."""
    if "맞았습니다" in result_text or "100점" in result_text:
        return 10000
    
    match = re.search(r'(\d+)점', result_text)
    if match:
        return int(match.group(1))
    
    return 0

def get_best_solutions(context: BrowserContext, user_id: str, logger=print) -> Dict[str, Dict]:
    """
    Phase 1: 최적 제출 번호 선별
    status 페이지를 순회하며 각 문제별로 가장 높은 점수(또는 최신)의 제출 번호를 수집합니다.
    """
    best_solutions = {}
    page = context.new_page()
    
    try:
        # result_id=4는 '맞았습니다'를 의미하며, 서브태스크 등 점수가 있는 문제도 포함될 수 있음
        url = f"https://www.acmicpc.net/status?user_id={user_id}&result_id=4"
        logger(f"[Phase 1] 정답 목록 스캔 시작: {url}")
        
        while True:
            response = page.goto(url, wait_until="domcontentloaded", timeout=60000)
            if not response or response.status != 200:
                logger(f"⚠️ 페이지 로드 실패: {url}")
                break
                
            # 테이블 순회
            rows = page.query_selector_all("table#status-table tbody tr")
            if not rows:
                break
                
            for row in rows:
                # td 0: 제출 번호, 1: 유저 ID, 2: 문제 번호, 3: 결과
                cols = row.query_selector_all("td")
                if len(cols) < 4:
                    continue
                    
                try:
                    sid = cols[0].inner_text().strip()
                    pid = cols[2].inner_text().strip()
                    result_text = cols[3].inner_text().strip()
                except Exception:
                    continue
                    
                score = get_score_priority(result_text)
                
                # 업데이트 로직 (점수가 더 높거나, 점수는 같은데 sid가 더 최신인 경우)
                if pid not in best_solutions:
                    best_solutions[pid] = {"sid": sid, "score": score, "text": result_text}
                else:
                    current_best = best_solutions[pid]
                    if score > current_best["score"] or (score == current_best["score"] and int(sid) > int(current_best["sid"])):
                        best_solutions[pid] = {"sid": sid, "score": score, "text": result_text}
                        
            # 다음 페이지로 이동
            next_button = page.query_selector("a#next_page")
            if next_button:
                href = next_button.get_attribute("href")
                if href:
                    url = "https://www.acmicpc.net" + href
                else:
                    break
            else:
                break
                
        logger(f"[Phase 1] 총 {len(best_solutions)}개의 최적 정답 코드를 선별했습니다.")
        return best_solutions
        
    finally:
        page.close()

def map_language_to_markdown(baekjoon_lang: str) -> str:
    """백준 언어명을 마크다운 코드블록 언어명으로 변환합니다."""
    lang_lower = baekjoon_lang.lower()
    if "python" in lang_lower or "pypy" in lang_lower:
        return "python"
    if "c++" in lang_lower or "cpp" in lang_lower:
        return "cpp"
    if lang_lower.startswith("c ") or lang_lower == "c":
        return "c"
    if "java" in lang_lower:
        return "java"
    if "c#" in lang_lower:
        return "csharp"
    if "javascript" in lang_lower or "node" in lang_lower:
        return "javascript"
    if "ruby" in lang_lower:
        return "ruby"
    if "swift" in lang_lower:
        return "swift"
    if "go" in lang_lower:
        return "go"
    if "rust" in lang_lower:
        return "rust"
    if "kotlin" in lang_lower:
        return "kotlin"
    return "text"

def extract_code_and_language(context: BrowserContext, pid: str, sid: str, logger=print) -> Tuple[Optional[str], Optional[str]]:
    """
    Phase 2: 소스 코드 및 언어 추출
    /submit/{pid}/{sid} 페이지에서 코드와 언어 이름을 추출합니다.
    """
    page = context.new_page()
    try:
        url = f"https://www.acmicpc.net/submit/{pid}/{sid}"
        page.goto(url, wait_until="domcontentloaded")
        
        # 1. 언어 추출 (수정 페이지의 언어 선택 드롭다운 활용)
        lang_element = page.query_selector("select[name='language'] option[selected]")
        if not lang_element:
            # fallback: 선택된 인덱스 기반
            lang_element = page.evaluate_handle("document.querySelector(\"select[name='language']\").options[document.querySelector(\"select[name='language']\").selectedIndex]")
        
        language_name = "Unknown"
        if lang_element:
            try:
                language_name = lang_element.inner_text().strip()
            except Exception:
                pass
                
        # 2. 소스 코드 추출
        # 백준 제출 수정 페이지는 CodeMirror를 사용하거나 textarea를 사용함
        code = page.evaluate('''() => {
            let cm = document.querySelector('.CodeMirror');
            if (cm && cm.CodeMirror) {
                return cm.CodeMirror.getValue();
            }
            let ta = document.querySelector('textarea[name="source"]');
            if (ta) {
                return ta.value;
            }
            return null;
        }''')
        
        if not code:
            # 로딩 시간이 필요할 수 있으므로 1초 대기 후 재시도
            page.wait_for_timeout(1000)
            code = page.evaluate('''() => {
                let cm = document.querySelector('.CodeMirror');
                if (cm && cm.CodeMirror) {
                    return cm.CodeMirror.getValue();
                }
                let ta = document.querySelector('textarea[name="source"]');
                if (ta) {
                    return ta.value;
                }
                return null;
            }''')
            
        return code, language_name
    except Exception as e:
        logger(f"⚠️ 코드 추출 실패 (pid:{pid}, sid:{sid}): {e}")
        return None, None
    finally:
        page.close()

def merge_code_to_md(md_filepath: str, code: str, language_name: str, result_text: str = "", logger=print) -> bool:
    """
    Phase 3: 마크다운 파일 병합
    """
    if not os.path.exists(md_filepath):
        return False
        
    try:
        with open(md_filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            
        target_heading = "## [정답 및 해설 (Ground Truth)]"
        
        if target_heading not in content:
            # 정답 및 해설 섹션이 없으면 추가
            content += f"\n\n{target_heading}\n"
        
        parts = content.split(target_heading)
        before_heading = parts[0]
        
        md_lang = map_language_to_markdown(language_name)
        
        new_content = before_heading + target_heading + "\n\n"
        new_content += f"### 내 풀이 (언어: {language_name})\n"
        if result_text:
            new_content += f"> **결과:** {result_text}\n\n"
        new_content += f"```{md_lang}\n"
        new_content += code.strip() + "\n"
        new_content += "```\n"
        
        with open(md_filepath, 'w', encoding='utf-8-sig') as f:
            f.write(new_content)
            
        return True
    except Exception as e:
        logger(f"⚠️ 파일 병합 실패 ({md_filepath}): {e}")
        return False

def copy_md_and_resources(src_md_path: str, dest_md_path: str, logger=print) -> bool:
    """마크다운 파일과 내부의 로컬 리소스(이미지 등)를 대상 폴더로 복사합니다."""
    if not os.path.exists(src_md_path):
        return False
        
    src_dir = os.path.dirname(os.path.abspath(src_md_path))
    dest_dir = os.path.dirname(os.path.abspath(dest_md_path))
    
    os.makedirs(dest_dir, exist_ok=True)
    
    try:
        shutil.copy2(src_md_path, dest_md_path)
        
        with open(src_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        md_img_pattern = r'!\[.*?\]\((?!http[s]?://)(.*?)\)'
        html_img_pattern = r'<img\s+[^>]*src=[\'"](?!http[s]?://)(.*?)[\'"]'
        
        resources = []
        resources.extend(re.findall(md_img_pattern, content))
        resources.extend(re.findall(html_img_pattern, content))
        
        for res_path in resources:
            res_path = res_path.strip().split()[0]
            src_res_path = os.path.normpath(os.path.join(src_dir, res_path))
            dest_res_path = os.path.normpath(os.path.join(dest_dir, res_path))
            
            if os.path.exists(src_res_path) and os.path.isfile(src_res_path):
                os.makedirs(os.path.dirname(dest_res_path), exist_ok=True)
                shutil.copy2(src_res_path, dest_res_path)
                
        return True
    except Exception as e:
        logger(f"⚠️ 복사 중 오류 발생: {e}")
        return False
