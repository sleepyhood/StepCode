import pygame
import sys

# =========================================================
# 🧑‍💻 [학생 작업 구역] 1차시: 우주선 좌우 이동하기
# =========================================================

def move_ship(keys):
    """
    키보드 입력에 따라 우주선을 좌우로 움직입니다.
    화면 밖으로 나가지 않도록 제한합니다.
    """
    global ship_rect
    
    speed = 5
    
    # [1] 왼쪽 화살표 키를 누르면 왼쪽으로 이동
    if keys[pygame.K_LEFT]:
        ship_rect.x -= speed
        
    # [2] 오른쪽 화살표 키를 누르면 오른쪽으로 이동
    if keys[pygame.K_RIGHT]:
        ship_rect.x += speed
        
    # [3] 화면 밖으로 나가지 않게 제한 (화면 가로 크기: 800, 우주선 가로 크기: 50)
    if ship_rect.left < 0:
        ship_rect.left = 0
    if ship_rect.right > 800:
        ship_rect.right = 800


# =========================================================
# ⚙️ [게임 엔진 구역] 건드리지 마세요!
# =========================================================

# --- 초기화 ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("우주선 운석 피하기 - 기준 복구본")
clock = pygame.time.Clock()

# --- 게임 상태 변수 ---
# 초보자 배려: 이미지가 없어도 실행되도록 사각형으로 우주선 대체
ship_color = (0, 255, 255) # 청록색
ship_rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 50)

def draw_ship(surface):
    pygame.draw.rect(surface, ship_color, ship_rect)

def main():
    running = True
    while running:
        # 1. 이벤트 확인
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # 2. 사용자 입력 확인
        keys = pygame.key.get_pressed()
        
        # 3. 우주선 이동 (학생 작성 함수 호출)
        move_ship(keys)
        
        # 4. 화면 그리기
        screen.fill((30, 30, 50)) # 어두운 남색 배경
        draw_ship(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
