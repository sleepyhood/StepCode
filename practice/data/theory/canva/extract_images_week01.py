import fitz  # PyMuPDF
import os

def extract_images_from_pdf(pdf_path, output_folder):
    # 이미지를 저장할 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    print(f"'{pdf_path}'에서 이미지 추출을 시작합니다...")
    doc = fitz.open(pdf_path)
    image_count = 0
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        
        # 해당 페이지에 이미지가 존재할 경우
        if image_list:
            for img_index, img in enumerate(image_list):
                xref = img[0] # 이미지의 고유 참조 번호
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # 파일명 지정 (예: p017_01.png) - 앞서 정한 네이밍 규칙 반영
                # 페이지 번호는 1부터 시작하게 맞춤, 세 자리 수 포맷 적용 (p001_01.png 형식)
                image_filename = f"p{page_num + 1:03d}_{img_index + 1:02d}.{image_ext}"
                image_filepath = os.path.join(output_folder, image_filename)
                
                # 이미지 파일 저장
                with open(image_filepath, "wb") as f:
                    f.write(image_bytes)
                    
                image_count += 1
                
    doc.close()
    print(f"완료! 총 {image_count}개의 이미지가 '{output_folder}' 폴더에 저장되었습니다.")

# --- 실행 부 --- 
# 1차시 PDF 스캔본
pdf_file = r"c:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\1차시. 캔바 첫 세팅과 작업 영역 적응.pdf"
# 저장될 이미지 폴더 (week01 신설)
output_dir = r"c:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\images\week01"

extract_images_from_pdf(pdf_file, output_dir)
