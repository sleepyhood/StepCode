import pygame
import sys
import random

# =========================================================
# 🧑‍💻 [학생 작업 구역] 1~2차시 유지 + 3차시: 충돌과 재시작
# =========================================================

# --- 1차시: 우주선 이동 ---
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

# --- 2차시: 운석 생성과 낙하 ---
def spawn_meteor():
    global meteors
    meteor_size = 40
    random_x = random.randint(0, 800 - meteor_size)
    new_meteor = pygame.Rect(random_x, -meteor_size, meteor_size, meteor_size)
    meteors.append(new_meteor)

def update_meteors():
    global meteors
    meteor_speed = 7
    
    # 안전한 삭제를 위해 복사본[:]을 순회합니다.
    for meteor in meteors[:]:
        meteor.y += meteor_speed
        
        # 화면 밖(600 초과)으로 나간 운석들 지우기
        if meteor.top > 600:
            meteors.remove(meteor)

# --- 3차시 작업 목표: 충돌 검사와 재시작 ---
def check_collision():
    """
    우주선과 운석이 부딪혔는지 검사합니다.
    """
    global game_over
    
    # 1. 운석 리스트를 하나씩 꺼내어 확인
    for meteor in meteors:
        # 2. 우주선 사각형(ship_rect)과 운석 사각형(meteor)이 겹치면!
        if ship_rect.colliderect(meteor):
            game_over = True  # 게임 오버 상태로 변경
            break             # 하나라도 부딪히면 반복검사 종료

def check_restart(keys):
    """
    게임 오버 상태일 때 R 키를 누르면 게임을 다시 시작합니다.
    """
    global game_over, meteors, ship_rect
    
    # 3. 키보드 'R' 키를 눌렀는지 확인
    if keys[pygame.K_r]:
        game_over = False    # 상대를 정상으로 복구
        meteors.clear()      # 떨어지던 운석들 모두 초기화(비우기)
        ship_rect.x = 400 - 25 # 우주선을 중앙으로 원상복구


# =========================================================
# ⚙️ [게임 엔진 구역] 건드리지 마세요!
# =========================================================

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("우주선 운석 피하기 - 교사용 완성본 (3차시)")
clock = pygame.time.Clock()

# --- 상태 변수 ---
ship_color = (0, 255, 255)
ship_rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 50)
meteor_color = (255, 100, 100)
meteors = []
game_over = False  # 3차시 엔진에 추가됨

SPAWN_METEOR_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_METEOR_EVENT, 600)

# --- 텍스트 폰트 설정 (초보자 배려: 기본 폰트 사용) ---
font_large = pygame.font.SysFont(None, 72)
font_small = pygame.font.SysFont(None, 36)

def draw_ship(surface):
    pygame.draw.rect(surface, ship_color, ship_rect)

def draw_meteors(surface):
    for m in meteors:
        pygame.draw.rect(surface, meteor_color, m)

def draw_game_over(surface):
    # 게임 오버 문자 렌더링
    text_over = font_large.render("GAME OVER", True, (255, 50, 50))
    text_restart = font_small.render("Press 'R' to Restart", True, (200, 200, 200))
    
    over_rect = text_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    restart_rect = text_restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    
    surface.blit(text_over, over_rect)
    surface.blit(text_restart, restart_rect)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # 게임 오버가 아닐 때만 운석 생성 타이머 작동
            if not game_over and event.type == SPAWN_METEOR_EVENT:
                spawn_meteor()
                
        keys = pygame.key.get_pressed()
        
        # --- 논리 업데이트 구역 ---
        if not game_over:
            move_ship(keys)
            update_meteors()
            check_collision() # 3차시에 만든 충돌 검사
        else:
            check_restart(keys) # 게임 오버일 때만 재시작 검사
            
        # --- 화면 그리기 구역 ---
        screen.fill((30, 30, 50))
        draw_ship(screen)
        draw_meteors(screen)
        
        if game_over:
            draw_game_over(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
