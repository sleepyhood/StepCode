import pygame
import sys
import random
import os

# 현재 파일 위치에서 6단계 위(StepCode 루트)로 이동 후 Resources/tools 경로 계산
tools_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../../Resources/tools"))
if tools_path not in sys.path:
    sys.path.append(tools_path)
from util_pygame_recorder import PygameRecorder
# =========================================================
# 🧑‍💻 [학생 작업 구역] 1~3차시 유지 + 4차시: 점수와 난이도
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

# --- 2차시: 운석 생성과 낙하 (+ 4차시 난이도 반영) ---
def spawn_meteor():
    global meteors
    meteor_size = 40
    random_x = random.randint(0, 800 - meteor_size)
    new_meteor = pygame.Rect(random_x, -meteor_size, meteor_size, meteor_size)
    meteors.append(new_meteor)

def update_meteors():
    global meteors
    # [4차시 수정] 기존 속도(7)에 난이도(difficulty) 값을 더해줍니다!
    meteor_speed = 7 + difficulty
    
    for meteor in meteors:
        meteor.y += meteor_speed
    meteors = [m for m in meteors if m.top < 600]

# --- 3차시: 충돌 검사와 재시작 (+ 4차시 점수 초기화 반영) ---
def check_collision():
    global game_over
    for meteor in meteors:
        if ship_rect.colliderect(meteor):
            game_over = True
            break

def check_restart(keys):
    global game_over, meteors, ship_rect, score, difficulty
    if keys[pygame.K_r]:
        game_over = False
        meteors.clear()
        ship_rect.x = 400 - 25
        # [4차시 수정] 다시 시작할 때 점수와 난이도도 0으로 초기화합니다.
        score = 0
        difficulty = 0

# --- 4차시 작업 목표: 점수와 난이도 증가 ---
def update_score():
    """
    살아남은 시간만큼 점수를 올리고, 점수에 따라 난이도를 올립니다.
    """
    global score, difficulty
    
    # 1. 점수 1점씩 올리기 (1초에 60번 불리므로 금방 오릅니다)
    score += 1
    
    # 2. 300점이 오를 때마다 난이도(레벨)가 1씩 오르게 수학 수식 적용 구하기
    difficulty = score // 300


# =========================================================
# ⚙️ [게임 엔진 구역] 건드리지 마세요!
# =========================================================

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("우주선 운석 피하기 - 교사용 완성본 (4차시)")
clock = pygame.time.Clock()

# --- 상태 변수 ---
ship_color = (0, 255, 255)
ship_rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 50)
meteor_color = (255, 100, 100)
meteors = []
game_over = False

# 4차시 엔진에 추가됨
score = 0
difficulty = 0

SPAWN_METEOR_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_METEOR_EVENT, 600)

font_large = pygame.font.SysFont(None, 72)
font_small = pygame.font.SysFont(None, 36)

def draw_ship(surface):
    pygame.draw.rect(surface, ship_color, ship_rect)

def draw_meteors(surface):
    for m in meteors:
        pygame.draw.rect(surface, meteor_color, m)

def draw_hud(surface):
    # 4차시에 화면에 점수를 그려주는 기능 추가
    score_text = font_small.render(f"SCORE: {score}", True, (255, 255, 255))
    level_text = font_small.render(f"LEVEL: {difficulty}", True, (255, 255, 0))
    surface.blit(score_text, (10, 10))
    surface.blit(level_text, (10, 40))

def draw_game_over(surface):
    text_over = font_large.render("GAME OVER", True, (255, 50, 50))
    text_restart = font_small.render("Press 'R' to Restart", True, (200, 200, 200))
    
    over_rect = text_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    restart_rect = text_restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    
    surface.blit(text_over, over_rect)
    surface.blit(text_restart, restart_rect)

def main():
    recorder = PygameRecorder(screen, "../assets/output_animation.gif")
    frame_count = 0  # 프레임 카운트 변수 추가
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not game_over and event.type == SPAWN_METEOR_EVENT:
                spawn_meteor()
                
        keys = pygame.key.get_pressed()
        
        # --- 논리 업데이트 구역 ---
        if not game_over:
            move_ship(keys)
            update_meteors()
            check_collision()
            update_score() # 4차시: 점수 올리기 트리거
        else:
            check_restart(keys)
            
        # --- 화면 그리기 구역 ---
        screen.fill((30, 30, 50))
        draw_ship(screen)
        draw_meteors(screen)
        draw_hud(screen) # 4차시: HUD 그리기 추가
        
        if game_over:
            draw_game_over(screen)
        
        pygame.display.flip()
        clock.tick(60)
        frame_count += 1
        if frame_count % 4 == 0:
            recorder.capture()

    recorder.save()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
