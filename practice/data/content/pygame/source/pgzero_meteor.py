import random

WIDTH = 600
HEIGHT = 800

FPS = 60
SHIP_W = 60
SHIP_H = 30
SHIP_SPEED = 7
METEOR_INTERVAL = 40  

BG_COLOR = (10, 10, 25)
SHIP_COLOR = (80, 170, 255)
METEOR_COLOR = (140, 140, 140)
TEXT_COLOR = "white"


def reset_game():
    global ship_x, ship_y, meteors, score, frame_count, game_over
    random.seed(0)  
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
    return Rect((ship_x, ship_y), (SHIP_W, SHIP_H))


def meteor_rect(meteor):
    r = meteor["r"]
    return Rect((meteor["x"] - r, meteor["y"] - r), (r * 2, r * 2))


def update():
    global ship_x, frame_count, score, game_over, meteors

    if game_over:
        return

    if keyboard.left:
        ship_x -= SHIP_SPEED
    if keyboard.right:
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


def draw_ship():
    body = ship_rect()
    screen.draw.filled_rect(body, SHIP_COLOR)


    nose = Rect((ship_x + 20, ship_y - 12), (20, 12))
    screen.draw.filled_rect(nose, SHIP_COLOR)


def draw_meteors():
    for meteor in meteors:
        screen.draw.filled_circle(
            (meteor["x"], meteor["y"]),
            meteor["r"],
            METEOR_COLOR
        )


def draw_hud():
    screen.draw.text(f"Score: {score}", (15, 15), color=TEXT_COLOR, fontsize=36)


def draw_game_over():
    screen.draw.text(
        "GAME OVER",
        center=(WIDTH // 2, HEIGHT // 2 - 30),
        color=TEXT_COLOR,
        fontsize=64
    )
    screen.draw.text(
        "Press R to restart",
        center=(WIDTH // 2, HEIGHT // 2 + 25),
        color=TEXT_COLOR,
        fontsize=36
    )


def draw():
    screen.fill(BG_COLOR)
    draw_ship()
    draw_meteors()
    draw_hud()

    if game_over:
        draw_game_over()


def on_key_down(key):
    if game_over and key == keys.R:
        reset_game()


reset_game()