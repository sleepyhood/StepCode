import pygame
import sys
import random
import os

# =========================================================
# 🧑‍💻 [학생 작업 구역] 1~5차시 유지 + 6차시: 이미지 및 무한 스크롤
# =========================================================

# [6차시] 배경 좌표 변수
bg_y = 0

def load_assets():
    global img_ship, img_meteor, img_bg
    
    # 실행 환경에 구애받지 않는 절대 경로 설정
    current_path = os.path.dirname(__file__)
    assets_path = os.path.join(current_path, "assets")
    
    try:
        img_ship = pygame.image.load(os.path.join(assets_path, "ship.png")).convert_alpha()
        img_meteor = pygame.image.load(os.path.join(assets_path, "meteor.png")).convert_alpha()
        img_bg = pygame.image.load(os.path.join(assets_path, "background.png")).convert()
        
        img_ship = pygame.transform.scale(img_ship, (50, 50))
        img_meteor = pygame.transform.scale(img_meteor, (40, 40))
        img_bg = pygame.transform.scale(img_bg, (800, 600))
    except Exception as e:
        print(f"이미지 로드 실패: {e}")
        img_ship = None
        img_meteor = None
        img_bg = None

# --- 게임 로직 함수들 (1~5차시와 동일) ---
def move_ship(keys):
    global ship_rect
    speed = 5
    if keys[pygame.K_LEFT]: ship_rect.x -= speed
    if keys[pygame.K_RIGHT]: ship_rect.x += speed
    if ship_rect.left < 0: ship_rect.left = 0
    if ship_rect.right > 800: ship_rect.right = 800

def spawn_meteor():
    global meteors
    meteor_size = random.randint(20, 80)
    random_x = random.randint(0, 800 - meteor_size)
    new_meteor = pygame.Rect(random_x, -meteor_size, meteor_size, meteor_size)
    meteors.append(new_meteor)

def update_meteors():
    global meteors
    meteor_speed = 7 + difficulty
    for meteor in meteors:
        meteor.y += meteor_speed
    meteors = [m for m in meteors if m.top < 600]

def check_collision():
    global game_over, lives
    for meteor in meteors:
        if ship_rect.colliderect(meteor):
            lives -= 1
            meteors.clear()
            if lives <= 0: game_over = True
            break

def update_score():
    global score, difficulty
    score += 1
    difficulty = score // 300

# --- [6차시] 그리기 함수들 (이미지 적용) ---
def draw_background(surface):
    global bg_y
    if img_bg:
        if not game_over:
            bg_y += 2
        if bg_y >= 600: bg_y = 0
        surface.blit(img_bg, (0, bg_y))
        surface.blit(img_bg, (0, bg_y - 600))
    else:
        surface.fill((30, 30, 50))

def draw_ship(surface):
    if img_ship:
        surface.blit(img_ship, ship_rect)
    else:
        pygame.draw.rect(surface, (0, 255, 255), ship_rect)

def draw_meteors(surface):
    for m in meteors:
        if img_meteor:
            scaled_meteor = pygame.transform.scale(img_meteor, (m.width, m.height))
            surface.blit(scaled_meteor, m)
        else:
            pygame.draw.rect(surface, (255, 100, 100), m)

# =========================================================
# ⚙️ [게임 엔진 구역]
# =========================================================

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("우주선 운석 피하기 - 최종 완성본 (6차시)")
clock = pygame.time.Clock()

load_assets()

ship_rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 50)
meteors = []
game_over = False
score = 0
difficulty = 0
lives = 3

SPAWN_METEOR_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_METEOR_EVENT, 600)

font_large = pygame.font.SysFont(None, 72)
font_small = pygame.font.SysFont(None, 36)

def draw_hud(surface):
    score_text = font_small.render(f"SCORE: {score}", True, (255, 255, 255))
    level_text = font_small.render(f"LEVEL: {difficulty}", True, (255, 255, 0))
    lives_text = font_small.render(f"LIVES: {'O '*lives}", True, (50, 255, 50))
    surface.blit(score_text, (10, 10))
    surface.blit(level_text, (10, 40))
    surface.blit(lives_text, (10, 70))

def draw_game_over(surface):
    # 게임 오버 텍스트 생성
    text_over = font_large.render("GAME OVER", True, (255, 50, 50))
    text_restart = font_small.render("Press 'R' to Restart", True, (200, 200, 200))
    
    # 화면 중앙 좌표 계산
    over_rect = text_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    restart_rect = text_restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    
    # 화면에 그리기
    surface.blit(text_over, over_rect)
    surface.blit(text_restart, restart_rect)

def main():
    global game_over, score, difficulty, lives
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over and event.type == SPAWN_METEOR_EVENT:
                spawn_meteor()
                
        keys = pygame.key.get_pressed()
        if not game_over:
            move_ship(keys)
            update_meteors()
            check_collision()
            update_score()
        else:
            if keys[pygame.K_r]:
                game_over = False
                meteors.clear()
                score = 0
                difficulty = 0
                lives = 3

        draw_background(screen)
        draw_meteors(screen)
        draw_ship(screen)
        draw_hud(screen)
        
        # [수정] 게임 오버 시 문구 출력 호출
        if game_over:
            draw_game_over(screen)
        
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
