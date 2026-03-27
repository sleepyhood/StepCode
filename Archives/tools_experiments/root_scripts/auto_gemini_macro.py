import fitz  # PyMuPDF 라이브러리 (pip install PyMuPDF)
import google.generativeai as genai # (pip install google-generativeai)
from PIL import Image
import io
import time
import os

def process_pdf_pages_with_gemini(pdf_path, output_md_path, api_key, start_page=0, end_page=None):
    """
    PDF의 각 페이지를 이미지로 캡처하여 Gemini API로 전송하고,
    마크다운 해설을 받아 파일로 차곡차곡 자동 저장하는 매크로.
    """
    
    print("🚀 Gemini API 설정 중...")
    genai.configure(api_key=api_key)
    
    # 사용할 AI 모델 (시각 자료 분석에 가장 뛰어난 최신 모델)
    model = genai.GenerativeModel('gemini-1.5-pro') 
    
    print(f"📖 PDF 파일 여는 중: {os.path.basename(pdf_path)}")
    doc = fitz.open(pdf_path)
    
    if end_page is None:
        end_page = len(doc) - 1 # 마지막 페이지까지
        
    print(f"총 {end_page - start_page + 1}장의 페이지를 분석합니다. (인공지능이 눈으로 읽는 중...)\n")
    
    # 결과를 저장할 마크다운 파일 초기화
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write("# 🤖 AI 자동 생성 페이지별 해설지\n\n")

    # 약속된 프롬프트 양식
    prompt_template = """
    첨부된 이미지는 중등부 영재반 교사용 교재의 한 페이지입니다.
    본문에 수록된 '실전 문제'들을 분석해서, 실제 수업에서 판서하며 쓸 수 있도록 
    상세한 '수업용 해설 텍스트 스크립트'를 아래 마크다운 양식에 맞춰 작성해 주세요.
    (만약 이 페이지에 연습문제만 있거나, 이론 설명만 있다면 "본 페이지에는 실전 문제가 없습니다." 라고만 짧게 답변할 것.)
    
    [작업 조건]
    1. 대상 범위: 교재의 실전 본문 문제만 다룰 것. (단순 '연습문제'는 무시할 것)
    2. 시각 자료: 문제에 표나 그림, 기호가 있다면 텍스트만으로 이미지가 연상되도록 친절하게 묘사해서 풀이할 것.
    3. 어조: 중학생 눈높이에 맞춘 다정하고 명확한 선생님 말투.
    
    [출력 양식]
    ### 📝 {문제 번호}. {핵심 키워드}
    **문제:** {문제의 원문 텍스트}
    
    **✅ 정답: {정답 번호 및 기호}**
    
    **💡 선생님을 위한 풀이 가이드:**
    * **출제 의도:** ...
    * **상세 풀이:**
      1. ...
      2. ...
    ---
    """

    for i in range(start_page, end_page + 1):
        actual_page_num = i + 1
        print(f"⏳ [{actual_page_num}/{len(doc)}] 페이지 캡처 및 분석 요청 중...")
        
        page = doc[i]
        
        # 1. 캡처 해상도 설정 (글씨와 표가 선명하게 보이도록 확대 캡처)
        zoom = 2.0 
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # 2. 픽셀 데이터를 Python 이미지(PIL) 객체로 변환
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        
        try:
            # 3. Gemini에게 이미지와 프롬프트를 함께 던져주기 (멀티모달)
            response = model.generate_content([prompt_template, image])
            
            # 4. 답변을 받아서 결과 MD 파일에 이어쓰기(Append)
            with open(output_md_path, 'a', encoding='utf-8') as f:
                f.write(f"## 📄 --- Page {actual_page_num} ---\n\n")
                f.write(response.text + "\n\n")
                
            print(f"✅ [{actual_page_num}/{len(doc)}] 페이지 해설지 기록 완료!")
            
            # (선택) API 호출 제한(Rate Limit)을 방지하기 위해 5초 정도 휴식
            time.sleep(5)
            
        except Exception as e:
            print(f"❌ [{actual_page_num}/{len(doc)}] 페이지 변환 중 에러 발생: {e}")
            with open(output_md_path, 'a', encoding='utf-8') as f:
                f.write(f"## 📄 --- Page {actual_page_num} ---\n\n")
                f.write(f"⚠️ 에러 발생으로 해설을 생성하지 못했습니다. ({e})\n\n")

    print(f"\n🎉 모든 작업이 끝났습니다! 결과물 확인: {output_md_path}")

if __name__ == "__main__":
    # ==========================================
    # ⚙️ 사용자 설정 영역 (이곳을 수정하세요!)
    # ==========================================
    
    # 1. 구글 인공지능 API 키 (무료 발급 가능)
    MY_GEMINI_API_KEY = "여기에_API_키를_붙여넣으세요" 
    
    # 2. 분석할 원본 PDF 경로
    SOURCE_PDF = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\jungol\중등\2026년_1차_중등_수업_교사용_해설_2019-2025.pdf"
    
    # 3. 최종 생성될 마크다운 파일 저장 경로
    OUTPUT_MARKDOWN = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\최종_자동추출_결과.md"
    
    # 4. 분석을 시작할 페이지 번호 (0부터 시작하므로, 3은 4페이지를 의미함)
    START = 3 
    
    print("-" * 50)
    print("구글 Gemini API 키를 입력한 뒤 아래 주석(#)을 풀면 매크로가 실행됩니다.")
    print("-" * 50)
    
    # TODO: API 키를 발급받아 입력한 후, 아래 줄의 맨 앞 '#'을 지우고 실행하세요!
    # process_pdf_pages_with_gemini(SOURCE_PDF, OUTPUT_MARKDOWN, MY_GEMINI_API_KEY, start_page=START)
