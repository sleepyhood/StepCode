# --- 라이브러리 호환성을 위한 패치 코드 (최상단에 추가) ---
import torchvision.transforms.functional as TF
import sys
sys.modules['torchvision.transforms.functional_tensor'] = TF
# ----------------------------------------------------------
import tkinter as tk
from tkinter import filedialog, messagebox
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
import cv2
import os
import filetype

def upscale_image_realesrgan():
    # 1. 파일 선택 (이미지)
    file_path = filedialog.askopenfilename(
        title="업스케일할 이미지를 선택하세요",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    
    if not file_path:
        return

    # 2. 모델 설정 및 로드 (RealESRGAN_x4plus.pth 파일이 스크립트 경로에 있어야 함)
    # 현재 실행 중인 파이썬 스크립트의 정확한 폴더 경로를 알아냅니다.
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 그 폴더 경로에 파일 이름을 합쳐서 절대 경로를 만듭니다.
    model_path = os.path.join(script_dir, "RealESRGAN_x4plus.pth")
    
    if not os.path.exists(model_path):
        messagebox.showerror("에러", f"모델 파일({model_path})을 찾을 수 없습니다.\n파일을 스크립트 경로에 넣어주세요.")
        return

    try:
        # 진행 상황 알림 (GUI가 멈추지 않게 하기 위해 간단한 메시지 박스 사용)
        progress_label.config(text="모델을 로드하는 중입니다...")
        root.update() # GUI 업데이트

        # RRDBNet 아키텍처 설정
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        
        # RealESRGANer 객체 생성 (4배 확대 설정)
        upsampler = RealESRGANer(
            scale=4,
            model_path=model_path,
            model=model,
            tile=0, # 타일링 사용 안 함 (메모리 부족 시 사용)
            tile_pad=10,
            pre_pad=0,
            half=False # False로 설정하여 CPU에서도 실행 가능하게 함 (GPU가 없다면 True로 설정 시 오류 발생 가능)
        )

        # 이미지 읽기
        img = cv2.imread(file_path)
        
        # 3. AI 업스케일링 실행 (시간이 꽤 걸릴 수 있습니다)
        print("업스케일링 중... 잠시만 기다려주세요.")
        progress_label.config(text="AI 업스케일링 중... 몇 분 소요될 수 있습니다.")
        root.update() # GUI 업데이트
        
        # 결과 이미지 얻기 (타일링 없이 전체 이미지 처리)
        output, _ = upsampler.enhance(img, outscale=4) 

        # 4. 저장 경로 선택
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],
            title="결과 이미지 저장"
        )

        if save_path:
            # 원본 파일의 확장자를 확인하여 저장 (filetype 라이브러리 활용)
            kind = filetype.guess(save_path)
            if kind:
                 cv2.imwrite(save_path, output)
            else:
                 cv2.imwrite(save_path + ".png", output) # 확장자가 없으면 .png로 저장
            
            messagebox.showinfo("완료", "이미지 업스케일링 및 저장이 완료되었습니다!")
            progress_label.config(text="준비 완료")
        else:
            progress_label.config(text="저장이 취소되었습니다.")
            
    except Exception as e:
        messagebox.showerror("오류 발생", f"처리 중 오류가 발생했습니다: {e}")
        progress_label.config(text="오류 발생")

# --- GUI 메인 창 설정 ---
root = tk.Tk()
root.title("Real-ESRGAN 최고 품질 이미지 업스케일러 (x4)")
root.geometry("500x300")

label_title = tk.Label(root, text="Real-ESRGAN AI 모델을 사용하여 이미지 품질을 4배 높입니다.", pady=20, font=("Helvetica", 12))
label_title.pack()

btn_upscale = tk.Button(root, text="이미지 선택 및 변환 시작", command=upscale_image_realesrgan, 
                        width=30, height=2, bg="#FF5722", fg="white", font=("Helvetica", 11, "bold"))
btn_upscale.pack(pady=20)

progress_label = tk.Label(root, text="준비 완료", pady=10, fg="blue")
progress_label.pack()

root.mainloop()