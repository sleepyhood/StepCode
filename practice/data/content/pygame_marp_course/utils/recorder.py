import os
import sys
import pygame
from PIL import Image

class PygameRecorder:
    """
    Pygame 화면을 캡처하여 GIF 애니메이션으로 저장하는 유틸리티 클래스입니다.
    여러 레슨에서 공통으로 재사용할 수 있습니다.
    """
    def __init__(self, screen, output_filename="../assets/output_animation.gif", fps=15):
        """
        초기화 메서드
        :param screen: 캡처할 Pygame의 display surface (보통 screen)
        :param output_filename: 저장할 GIF의 상대/절대 경로 (기본값: "../assets/output_animation.gif")
        :param fps: 생성될 GIF의 초당 프레임 수
        """
        self.screen = screen
        self.frames = []
        self.fps = fps
        self.is_recording = True
        
        # 실행 중인 메인 스크립트(예: step1_teacher_capture.py)의 위치를 절대경로로 가져옵니다.
        main_script_path = os.path.abspath(sys.argv[0])
        base_dir = os.path.dirname(main_script_path)
        
        # 절대경로가 입력된 경우 그대로 사용하고, 상대경로인 경우 메인 스크립트 위치 기준으로 조합합니다.
        if os.path.isabs(output_filename):
            self.output_path = output_filename
        else:
            self.output_path = os.path.abspath(os.path.join(base_dir, output_filename))
            
        # 파일이 저장될 폴더 경로를 추출하고, 존재하지 않으면 자동으로 생성합니다.
        output_dir = os.path.dirname(self.output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

    def capture(self):
        """
        현재 Pygame 화면을 캡처하여 내부 프레임 리스트에 추가합니다.
        메인 게임 루프 내에서 pygame.display.flip() 직후에 호출하는 것이 가장 좋습니다.
        """
        if not self.is_recording:
            return

        # Pygame 화면(Surface) 데이터를 문자열로 추출하여 PIL Image 객체로 변환
        size = self.screen.get_size()
        image_data = pygame.image.tostring(self.screen, 'RGB')
        image = Image.frombytes('RGB', size, image_data)
        
        self.frames.append(image)

    def save(self):
        """
        지금까지 수집된 프레임들을 하나의 애니메이션 GIF 파일로 저장합니다.
        프로그램이 종료되기 직전(pygame.quit() 주변)에 호출합니다.
        """
        if not self.frames:
            print("저장할 프레임이 없습니다. (capture()가 한 번도 호출되지 않음)")
            return

        duration = int(1000 / self.fps) # 프레임당 표시 시간(ms) 계산

        print(f"GIF 애니메이션 생성 중... (총 {len(self.frames)} 프레임)")
        
        # 첫 번째 프레임을 기준으로 나머지 프레임들을 이어붙여 GIF로 저장
        self.frames[0].save(
            self.output_path,
            save_all=True,
            append_images=self.frames[1:],
            duration=duration,
            loop=0  # 0은 무한 반복을 의미
        )
        print(f"✅ 성공적으로 저장되었습니다: {self.output_path}")

    def toggle_recording(self):
        """
        특정 키보드 이벤트 등에 연결하여 캡처를 일시 정지하거나 재개할 수 있습니다.
        """
        self.is_recording = not self.is_recording
        state = "재개" if self.is_recording else "일시 정지"
        print(f"캡처 기능이 {state}되었습니다.")
