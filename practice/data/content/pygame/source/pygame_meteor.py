import random
import pygame

pygame.init()

WIDTH = 600
HEIGHT = 800

FPS = 60
SHIP_W = 60
SHIP_H = 30
SHIP_SPEED = 7
METEOR_INTERVAL = 40  # 프레임마다 생성 간격

BG_COLOR = (10, 10, 25)
SHIP_COLOR = (80, 170, 255)
METEOR_COLOR = (140, 140, 140)
TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteor Dodge")
clock = pygame.time.Clock()
font_score = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 64)
font_mid = pygame.font.SysFont(None, 36)


def reset_game():
    global ship_x, ship_y, meteors, score, frame_count, game_over
    random.seed(0)  # 매번 같은 패턴으로 시작하도록 고정
    ship_x = WIDTH // 2 - SHIP_W // 2
    ship_y = HEIGHT - 80
    meteors = []
    score = 0
    frame_count = 0
    game_over = False


def spawn_meteor():
    r = random.randint(15, 30)
    x = random.randint(r, WIDTH - r)
    speed = random.randint(4, 8)
    meteors.append({
        "x": x,
        "y": -r,
        "r": r,
        "speed": speed,
    })


def ship_rect():
    return pygame.Rect(ship_x, ship_y, SHIP_W, SHIP_H)


def meteor_rect(meteor):
    r = meteor["r"]
    return pygame.Rect(meteor["x"] - r, meteor["y"] - r, r * 2, r * 2)


def update_game(keys):
    global ship_x, frame_count, score, game_over, meteors

    if game_over:
        return

    if keys[pygame.K_LEFT]:
        ship_x -= SHIP_SPEED
    if keys[pygame.K_RIGHT]:
        ship_x += SHIP_SPEED

    ship_x = max(0, min(WIDTH - SHIP_W, ship_x))

    frame_count += 1
    score += 1

    if frame_count % METEOR_INTERVAL == 0:
        spawn_meteor()

    for meteor in meteors:
        meteor["y"] += meteor["speed"]

    meteors = [m for m in meteors if m["y"] - m["r"] <= HEIGHT]

    s_rect = ship_rect()
    for meteor in meteors:
        if s_rect.colliderect(meteor_rect(meteor)):
            game_over = True
            break


def draw_text_center(text, font, color, center_pos):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=center_pos)
    screen.blit(surface, rect)


def draw_ship():
    body = ship_rect()
    pygame.draw.rect(screen, SHIP_COLOR, body)

    nose = pygame.Rect(ship_x + 20, ship_y - 12, 20, 12)
    pygame.draw.rect(screen, SHIP_COLOR, nose)


def draw_meteors():
    for meteor in meteors:
        pygame.draw.circle(
            screen,
            METEOR_COLOR,
            (meteor["x"], meteor["y"]),
            meteor["r"]
        )


def draw_hud():
    text = font_score.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(text, (15, 15))


def draw_game_over():
    draw_text_center("GAME OVER", font_big, TEXT_COLOR, (WIDTH // 2, HEIGHT // 2 - 30))
    draw_text_center("Press R to restart", font_mid, TEXT_COLOR, (WIDTH // 2, HEIGHT // 2 + 25))


def draw_scene():
    screen.fill(BG_COLOR)
    draw_ship()
    draw_meteors()
    draw_hud()

    if game_over:
        draw_game_over()


def main():
    reset_game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()

        keys = pygame.key.get_pressed()
        update_game(keys)
        draw_scene()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()