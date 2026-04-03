import pygame
import sys
import random

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
    
    # TODO: [1] 제일 위쪽에서 화면 가로 길이(800) 안의 임의의 위치(random_x)를 골라보세요.
    # 힌트: random.randint(0, 800 - meteor_size) 를 사용하세요.
    pass
    
    # TODO: [2] 골라진 x 위치와 y 좌표(-meteor_size 시작)로 새로운 운석 사각형(pygame.Rect)을 만드세요.
    pass
    
    # TODO: [3] 만든 운석 사각형을 meteors 리스트에 추가(append) 하세요!
    pass

def update_meteors():
    """
    모든 운석을 아래로 떨어뜨립니다.
    화면 밑으로 벗어난 운석은 리스트에서 제거합니다.
    """
    global meteors
    meteor_speed = 7
    
    # TODO: [4] meteors 리스트에 있는 모든 운석(사각형)의 y 좌표를 meteor_speed 만큼 증가시켜 아래로 이동하세요.
    # 힌트: for문을 사용하세요.
    pass
        
    # TODO: [5] 화면 밖(y좌표가 600 초과)으로 벗어난 운석은 삭제해야 컴퓨터가 느려지지 않습니다!
    # (선생님의 설명에 따라, 안전하게 지우는 방법을 작성해보세요)
    pass


# =========================================================
# ⚙️ [게임 엔진 구역] 건드리지 마세요!
# =========================================================

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("우주선 운석 피하기 - 학생 실습본 (2차시)")
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

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
