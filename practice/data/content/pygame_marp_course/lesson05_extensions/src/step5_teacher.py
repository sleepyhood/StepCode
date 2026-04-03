import pygame
import sys
import random

# =========================================================
# 🧑‍💻 [학생 작업 구역] 1~4차시 유지 + 5차시: 선택형 확장 기능
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

# --- 2차시 & [확장 1] 운석 크기 랜덤 ---
def spawn_meteor():
    global meteors
    
    # [5차시 확장1] 운석 크기를 20~80 사이로 무작위로 만듭니다.
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

# --- 3차시 & [확장 2] 목숨(Lives) 시스템 ---
def check_collision():
    global game_over, lives
    for meteor in meteors:
        if ship_rect.colliderect(meteor):
            # [5차시 확장2] 바로 죽지 않고 목숨을 1개 줄입니다.
            lives -= 1
            
            # 부딪힌 직후 바로 또 다른 운석에 연속으로 맞지 않게 화면을 비워줍니다.
            meteors.clear() 
            
            # 목숨이 0 이하라면 진짜로 게임 오버 처리
            if lives <= 0:
                game_over = True
            break

def check_restart(keys):
    global game_over, meteors, ship_rect, score, difficulty, lives
    if keys[pygame.K_r]:
        game_over = False
        meteors.clear()
        ship_rect.x = 400 - 25
        score = 0
        difficulty = 0
        # [5차시 확장2] 다시 시작할 때 목숨을 3개로 복구합니다.
        lives = 3

# --- 4차시 점수/난이도 ---
def update_score():
    global score, difficulty
    score += 1
    difficulty = score // 300


# =========================================================
# ⚙️ [게임 엔진 구역] 건드리지 마세요!
# =========================================================

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("우주선 운석 피하기 - 교사용 완성본 (5차시)")
clock = pygame.time.Clock()

ship_color = (0, 255, 255)
ship_rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 50)
meteor_color = (255, 100, 100)
meteors = []

# 상태 변수 모음
game_over = False
score = 0
difficulty = 0
lives = 3 # 5차시 목숨 변수 엔진에 기본 추가

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
    score_text = font_small.render(f"SCORE: {score}", True, (255, 255, 255))
    level_text = font_small.render(f"LEVEL: {difficulty}", True, (255, 255, 0))
    # 5차시에 생명력 렌더링 추가 (하트 문자 등)
    lives_text = font_small.render(f"LIVES: {'O '*lives}", True, (50, 255, 50))
    
    surface.blit(score_text, (10, 10))
    surface.blit(level_text, (10, 40))
    surface.blit(lives_text, (10, 70))

def draw_game_over(surface):
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
            
            if not game_over and event.type == SPAWN_METEOR_EVENT:
                spawn_meteor()
                
        keys = pygame.key.get_pressed()
        
        if not game_over:
            move_ship(keys)
            update_meteors()
            check_collision()
            update_score()
        else:
            check_restart(keys)
            
        screen.fill((30, 30, 50))
        draw_ship(screen)
        draw_meteors(screen)
        draw_hud(screen) 
        
        if game_over:
            draw_game_over(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
