import pygame
import sys
import random
import os

# 현재 파일 위치에서 6단계 위(StepCode 루트)로 이동 후 Resources/tools 경로 계산
tools_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../../Resources/tools"))
if tools_path not in sys.path:
    sys.path.append(tools_path)
# 이제 util_pygame_recorder 파일에서 PygameRecorder 클래스를 직접 가져옵니다.
from util_pygame_recorder import PygameRecorder

# =========================================================
# 🧑‍💻 [학생 작업 구역] 1차시 코드 (완성) + 2차시: 운석 생성과 낙하
# =========================================================

# --- 1차시 완성 코드 ---
def move_ship(keys):
    global ship_rect
    speed = 5
    if keys[pygame.K_LEFT]:
        ship_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        ship_rect.x += speed
    if ship_rect.left < 0:
        ship_rect.left = 0
    if ship_rect.right > 800:
        ship_rect.right = 800

# --- 2차시 작업 목표 ---
def spawn_meteor():
    """
    화면 맨 위(y=0)의 임의의 위치(x)에 운석을 새롭게 생성합니다.
    """
    global meteors
    
    meteor_size = 40
    # 0부터 (화면너비 - 운석크기) 사이의 임의의 x좌표 뽑기
    random_x = random.randint(0, 800 - meteor_size)
    
    # 운석 사각형 생성 (최상단인 y=-meteor_size 에서 시작하게 함)
    new_meteor = pygame.Rect(random_x, -meteor_size, meteor_size, meteor_size)
    
    # 리스트에 추가
    meteors.append(new_meteor)

def update_meteors():
    """
    모든 운석을 아래로 떨어뜨립니다.
    화면 밑으로 벗어난 운석은 리스트에서 제거합니다.
    """
    global meteors
    meteor_speed = 7
    
    # 리스트에 있는 모든 운석에 대해 반복
    for meteor in meteors:
        meteor.y += meteor_speed # 아래로 이동
        
    # 화면 밖(600 초과)으로 나간 운석들 지우기
    # (파이썬 리스트 내포 문법이나, 복사를 이용해 안전하게 삭제)
    meteors = [m for m in meteors if m.top < 600]


# =========================================================
# ⚙️ [게임 엔진 구역] 건드리지 마세요!
# =========================================================

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("우주선 운석 피하기 - 교사용 완성본 (2차시)")
clock = pygame.time.Clock()

ship_color = (0, 255, 255)
ship_rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 50)

# 운석 상태 관리 변수
meteor_color = (255, 100, 100) # 붉은색
meteors = []

# 운석 생성 타이머 (커스텀 이벤트 활용)
SPAWN_METEOR_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_METEOR_EVENT, 600) # 0.6초마다 이벤트 발생

def draw_ship(surface):
    pygame.draw.rect(surface, ship_color, ship_rect)

def draw_meteors(surface):
    for m in meteors:
        pygame.draw.rect(surface, meteor_color, m)

def main():
    recorder = PygameRecorder(screen, "../assets/output_animation.gif")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 정해진 시간(0.6초)마다 이벤트가 발생하면 학생이 만든 함수 호출
            if event.type == SPAWN_METEOR_EVENT:
                spawn_meteor()
                
        keys = pygame.key.get_pressed()
        
        # 1차시 함수 호출
        move_ship(keys)
        
        # 2차시 학생 작성 함수(업데이트) 호출
        update_meteors()
        
        # 화면 그리기
        screen.fill((30, 30, 50))
        draw_ship(screen)
        draw_meteors(screen)
        
        pygame.display.flip()
        clock.tick(60)
        recorder.capture()

    recorder.save()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
