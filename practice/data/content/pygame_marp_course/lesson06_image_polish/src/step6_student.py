import pygame
import sys
import random
import os

# =========================================================
# 🧑‍💻 [학생 작업 구역] 1~5차시 유지 + 6차시: 이미지 적용
# =========================================================

# [6차시] 배경 좌표 변수
bg_y = 0

def load_assets():
    """
    이미지 리소스를 불러오고 크기를 조절합니다.
    """
    global img_ship, img_meteor, img_bg
    
    # 실행 위치와 상관없이 이미지를 찾을 수 있도록 절대 경로를 설정합니다.
    current_path = os.path.dirname(__file__)
    assets_path = os.path.join(current_path, "assets")
    
    try:
        # TODO: [1] 우주선(ship.png), 운석(meteor.png), 배경(background.png)을 불러오세요.
        # 힌트: pygame.image.load(os.path.join(assets_path, "파일명.png")).convert_alpha()
        pass
        
        # TODO: [2] 이미지 크기를 조절하세요. (우주선: 50x50, 운석: 40x40, 배경: 800x600)
        # 힌트: pygame.transform.scale(이미지변수, (가로, 세로))
        pass
        
    except Exception as e:
        print(f"이미지 로드 실패: {e} (사각형으로 대체됩니다)")
        img_ship, img_meteor, img_bg = None, None, None

# --- 1~5차시 게임 로직 (수정 불필요) ---
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
    
    # 안전한 삭제를 위해 복사본[:]을 순회합니다.
    for meteor in meteors[:]:
        meteor.y += meteor_speed
        
        # 화면 밖(600 초과)으로 나간 운석들 지우기
        if meteor.top > 600:
            meteors.remove(meteor)

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

# --- [6차시] 그리기 함수 수정 구역 ---

def draw_background(surface):
    """
    배경 이미지를 출력합니다. (심화: 무한 스크롤 구현)
    """
    global bg_y
    if img_bg:
        # TODO: [3] 배경이 아래로 흐르게 만드세요. (bg_y 증가 및 600 도달 시 리셋)
        
        # TODO: [4] blit을 사용하여 배경 이미지 두 장을 위아래로 이어 붙여 그리세요.
        surface.blit(img_bg, (0, 0)) # 임시 코드 (수정 필요)
    else:
        surface.fill((30, 30, 50))

def draw_ship(surface):
    """
    우주선 이미지를 출력합니다.
    """
    if img_ship:
        # TODO: [5] 사각형 대신 우주선 이미지를 ship_rect 위치에 그리세요.
        # surface.blit(...)
        pass
    else:
        pygame.draw.rect(surface, (0, 255, 255), ship_rect)

def draw_meteors(surface):
    """
    모든 운석 이미지를 출력합니다.
    """
    for m in meteors:
        if img_meteor:
            # TODO: [6] 각 운석(m)의 크기에 맞게 이미지를 스케일링하여 그리세요.
            # scaled = pygame.transform.scale(img_meteor, (m.width, m.height))
            pass
        else:
            pygame.draw.rect(surface, (255, 100, 100), m)

# =========================================================
# ⚙️ [게임 엔진 구역] 건드리지 마세요!
# =========================================================

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("우주선 운석 피하기 - 학생 실습본 (6차시)")
clock = pygame.time.Clock()

img_ship, img_meteor, img_bg = None, None, None
load_assets() # 이미지 로드 실행

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
    text_over = font_large.render("GAME OVER", True, (255, 50, 50))
    text_restart = font_small.render("Press 'R' to Restart", True, (200, 200, 200))
    over_rect = text_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    restart_rect = text_restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    surface.blit(text_over, over_rect)
    surface.blit(text_restart, restart_rect)

def main():
    global game_over, score, difficulty, lives
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if not game_over and event.type == SPAWN_METEOR_EVENT: spawn_meteor()
                
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
                score, difficulty, lives = 0, 0, 3

        draw_background(screen)
        draw_meteors(screen)
        draw_ship(screen)
        draw_hud(screen)
        if game_over: draw_game_over(screen)
        
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
