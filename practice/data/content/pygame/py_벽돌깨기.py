# -*- coding: utf-8 -*-
# breakout.py
import sys
import random
import pygame

# ---------------------------
# 설정값
# ---------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60

PADDLE_W, PADDLE_H = 110, 16
PADDLE_Y_OFFSET = 40
PADDLE_SPEED = 520  # px/s

BALL_R = 9
BALL_SPEED = 420  # px/s

### BRICK_COLS, BRICK_ROWS로 벽돌 개수 조정
BRICK_COLS = 30
BRICK_ROWS = 6
BRICK_GAP = 6
BRICK_TOP = 70
BRICK_H = 22
BRICK_MARGIN_X = 40  # 좌우 여백

LIVES = 3

# ✅ 아이템(멀티볼) 설정
ITEM_DROP_CHANCE = 0.28   ### 벽돌 깨질 때 아이템 나올 확률(0~1)
ITEM_SIZE = 18
ITEM_FALL_SPEED = 240     # px/s
EXTRA_BALLS_ON_PICK = 1   # 먹으면 추가되는 공 개수(1이면 1개 추가)

# ---------------------------
# 유틸
# ---------------------------
def clamp(v, a, b):
    return max(a, min(b, v))

# ---------------------------
# 초기화
# ---------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout (벽돌깨기) - Pygame")
clock = pygame.time.Clock()

def get_korean_font(size: int) -> pygame.font.Font:
    candidates = [
        "Malgun Gothic",     # Windows: 맑은 고딕
        "AppleGothic",       # macOS
        "NanumGothic",       # Linux (나눔고딕)
        "Noto Sans CJK KR",
        "Noto Sans KR",
        "Dotum", "Gulim"
    ]
    for name in candidates:
        path = pygame.font.match_font(name)
        if path:
            return pygame.font.Font(path, size)
    return pygame.font.Font(None, size)

font = get_korean_font(28)
big_font = get_korean_font(56)
small_font = get_korean_font(18)

# ---------------------------
# 게임 오브젝트 생성
# ---------------------------
def make_bricks():
    bricks = []
    total_w = WIDTH - 2 * BRICK_MARGIN_X
    brick_w = (total_w - (BRICK_COLS - 1) * BRICK_GAP) // BRICK_COLS

    for r in range(BRICK_ROWS):
        for c in range(BRICK_COLS):
            x = BRICK_MARGIN_X + c * (brick_w + BRICK_GAP)
            y = BRICK_TOP + r * (BRICK_H + BRICK_GAP)
            rect = pygame.Rect(x, y, brick_w, BRICK_H)
            color = pygame.Color(0)
            color.hsva = (r * 28 % 360, 70, 95, 100)
            bricks.append({"rect": rect, "color": color})
    return bricks

def normalize_ball_speed(vx, vy, target=BALL_SPEED):
    speed = (vx * vx + vy * vy) ** 0.5
    if speed == 0:
        return target, 0
    s = target / speed
    return vx * s, vy * s

def make_ball_on_paddle(paddle_rect, offset=0.0):
    x = paddle_rect.centerx + offset
    y = paddle_rect.top - BALL_R - 1
    vx = random.choice([-1, 1]) * (BALL_SPEED * 0.45)
    vy = -BALL_SPEED
    return {
        "pos": [float(x), float(y)],
        "vel": [float(vx), float(vy)],
        "launched": False,
        "offset": float(offset),  # 발사 전 패들 중심 기준 좌우 위치
    }

def reset_balls_on_paddle(paddle_rect):
    # 기본 1개 공으로 리셋(패들에 붙어있음)
    return [make_ball_on_paddle(paddle_rect, 0.0)]

# ---------------------------
# 충돌 처리
# ---------------------------
def ball_rect(ball_pos):
    return pygame.Rect(int(ball_pos[0] - BALL_R), int(ball_pos[1] - BALL_R), BALL_R * 2, BALL_R * 2)

def reflect_from_rect(prev_rect, cur_rect, target_rect, vx, vy):
    if prev_rect.right <= target_rect.left and cur_rect.right > target_rect.left:
        vx = -abs(vx)
    elif prev_rect.left >= target_rect.right and cur_rect.left < target_rect.right:
        vx = abs(vx)
    elif prev_rect.bottom <= target_rect.top and cur_rect.bottom > target_rect.top:
        vy = -abs(vy)
    elif prev_rect.top >= target_rect.bottom and cur_rect.top < target_rect.bottom:
        vy = abs(vy)
    else:
        vy = -vy
    return vx, vy

# ---------------------------
# 아이템(멀티볼) 처리
# ---------------------------
def spawn_item_from_brick(brick_rect):
    cx = brick_rect.centerx
    cy = brick_rect.centery
    rect = pygame.Rect(0, 0, ITEM_SIZE, ITEM_SIZE)
    rect.center = (cx, cy)
    return {"rect": rect, "vy": ITEM_FALL_SPEED}

def add_extra_balls(balls, paddle_rect, count=1):
    # ✅ 기준이 될 "날아다니는 공" 하나 선택
    flying = [b for b in balls if b["launched"]]
    base = random.choice(flying) if flying else None

    for _ in range(count):
        if base is not None:
            # ✅ 새 공 생성 위치 = 기존 공 위치
            bx = float(base["pos"][0])
            by = float(base["pos"][1])

            # 속도는 기존 공 속도를 살짝 흔들어서(겹침 방지)
            vx = float(base["vel"][0]) + random.uniform(-0.35, 0.35) * BALL_SPEED
            vy = float(base["vel"][1]) + random.uniform(-0.35, 0.35) * BALL_SPEED

            # 너무 수평으로만 가면 재미없어서 y 성분 최소 보정(선택)
            if abs(vy) < 0.25 * BALL_SPEED:
                vy = -0.25 * BALL_SPEED if vy <= 0 else 0.25 * BALL_SPEED

            vx, vy = normalize_ball_speed(vx, vy, BALL_SPEED)

            # 같은 위치에 딱 겹치면 바로 충돌 판정 꼬일 수 있어서 위치도 살짝 벌림(선택)
            bx += random.uniform(-BALL_R * 2, BALL_R * 2)
            by += random.uniform(-BALL_R * 2, BALL_R * 2)
        else:
            # 예외: 날아다니는 공이 없다면(거의 없음) 기존 방식(패들 위)로
            bx = paddle_rect.centerx
            by = paddle_rect.top - BALL_R - 1
            vx = random.uniform(-1.0, 1.0) * BALL_SPEED
            vy = -abs(BALL_SPEED)
            vx, vy = normalize_ball_speed(vx, vy, BALL_SPEED)

        balls.append({
            "pos": [bx, by],
            "vel": [vx, vy],
            "launched": True,
            "offset": 0.0
        })


# ---------------------------
# 게임 상태
# ---------------------------
paddle = pygame.Rect((WIDTH - PADDLE_W)//2, HEIGHT - PADDLE_Y_OFFSET, PADDLE_W, PADDLE_H)
bricks = make_bricks()

balls = reset_balls_on_paddle(paddle)  # ✅ 여러 공
items = []                             # ✅ 떨어지는 아이템들

score = 0
lives = LIVES
game_over = False
game_win = False

# ---------------------------
# 메인 루프
# ---------------------------
while True:
    dt = clock.tick(FPS) / 1000.0

    # ---- 이벤트 ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_r:
                # 전체 재시작
                paddle.x = (WIDTH - PADDLE_W)//2
                bricks = make_bricks()
                balls = reset_balls_on_paddle(paddle)
                items = []
                score = 0
                lives = LIVES
                game_over = False
                game_win = False

            if event.key == pygame.K_SPACE and (not game_over) and (not game_win):
                # ✅ 발사: 아직 launched=False인 공들 전부 발사
                for b in balls:
                    if not b["launched"]:
                        b["launched"] = True
                        b["vel"][0], b["vel"][1] = normalize_ball_speed(b["vel"][0], b["vel"][1], BALL_SPEED)

    keys = pygame.key.get_pressed()

    # ---- 업데이트 ----
    if not game_over and not game_win:
        # 패들 이동
        move_dir = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_dir -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_dir += 1

        paddle.x += int(move_dir * PADDLE_SPEED * dt)
        paddle.x = clamp(paddle.x, 0, WIDTH - paddle.width)

        # 공 업데이트(여러 개)
        dead_ball_indices = set()

        for bi, b in enumerate(balls):
            # 발사 전이면 패들에 붙어서 따라다님
            if not b["launched"]:
                b["pos"][0] = paddle.centerx + b["offset"]
                b["pos"][1] = paddle.top - BALL_R - 1
                continue

            prev = ball_rect(b["pos"]).copy()

            b["pos"][0] += b["vel"][0] * dt
            b["pos"][1] += b["vel"][1] * dt
            cur = ball_rect(b["pos"])

            # 벽 반사
            if b["pos"][0] - BALL_R <= 0:
                b["pos"][0] = BALL_R
                b["vel"][0] = abs(b["vel"][0])
            if b["pos"][0] + BALL_R >= WIDTH:
                b["pos"][0] = WIDTH - BALL_R
                b["vel"][0] = -abs(b["vel"][0])
            if b["pos"][1] - BALL_R <= 0:
                b["pos"][1] = BALL_R
                b["vel"][1] = abs(b["vel"][1])

            # 바닥으로 떨어짐: ✅ 이 공만 제거. 공이 0개가 되면 그때 라이프 감소
            if b["pos"][1] - BALL_R > HEIGHT:
                dead_ball_indices.add(bi)
                continue

            # 패들 충돌
            cur = ball_rect(b["pos"])
            if cur.colliderect(paddle) and b["vel"][1] > 0:
                offset = (b["pos"][0] - paddle.centerx) / (paddle.width / 2)
                offset = clamp(offset, -1.0, 1.0)
                b["vel"][0] = offset * BALL_SPEED
                b["vel"][1] = -abs(b["vel"][1])
                b["vel"][0], b["vel"][1] = normalize_ball_speed(b["vel"][0], b["vel"][1], BALL_SPEED)
                b["pos"][1] = paddle.top - BALL_R - 1

            # 벽돌 충돌
            cur = ball_rect(b["pos"])
            hit_index = -1
            hit_rect = None
            for i, br in enumerate(bricks):
                if cur.colliderect(br["rect"]):
                    hit_index = i
                    hit_rect = br["rect"]
                    b["vel"][0], b["vel"][1] = reflect_from_rect(prev, cur, br["rect"], b["vel"][0], b["vel"][1])
                    score += 10
                    break

            if hit_index != -1:
                bricks.pop(hit_index)
                b["vel"][0], b["vel"][1] = normalize_ball_speed(b["vel"][0], b["vel"][1], BALL_SPEED)

                # ✅ 랜덤 아이템 드랍
                if random.random() < ITEM_DROP_CHANCE and hit_rect is not None:
                    items.append(spawn_item_from_brick(hit_rect))

            # 승리 체크(벽돌 0)
            if len(bricks) == 0:
                game_win = True

        # ✅ 떨어진 공들 제거
        if dead_ball_indices:
            balls = [b for i, b in enumerate(balls) if i not in dead_ball_indices]

        # ✅ 공이 전부 사라졌을 때만 라이프 감소 + 공 리셋
        if len(balls) == 0:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                balls = reset_balls_on_paddle(paddle)

        # ✅ 아이템 업데이트
        dead_items = []
        for ii, it in enumerate(items):
            it["rect"].y += int(it["vy"] * dt)

            # 패들이 먹으면: 공 추가
            if it["rect"].colliderect(paddle):
                add_extra_balls(balls, paddle, EXTRA_BALLS_ON_PICK)
                dead_items.append(ii)
                continue

            # 화면 밖이면 제거
            if it["rect"].top > HEIGHT:
                dead_items.append(ii)

        if dead_items:
            items = [it for i, it in enumerate(items) if i not in set(dead_items)]

    # ---- 렌더링 ----
    screen.fill((245, 248, 255))

    # 벽돌
    for br in bricks:
        pygame.draw.rect(screen, br["color"], br["rect"], border_radius=6)
        pygame.draw.rect(screen, (30, 30, 40), br["rect"], 1, border_radius=6)

    # 패들
    pygame.draw.rect(screen, (60, 90, 210), paddle, border_radius=10)
    pygame.draw.rect(screen, (20, 25, 40), paddle, 1, border_radius=10)

    # 공(여러 개)
    for b in balls:
        pygame.draw.circle(screen, (235, 70, 70), (int(b["pos"][0]), int(b["pos"][1])), BALL_R)
        pygame.draw.circle(screen, (20, 25, 40), (int(b["pos"][0]), int(b["pos"][1])), BALL_R, 1)

    # ✅ 아이템(멀티볼)
    for it in items:
        pygame.draw.rect(screen, (255, 200, 60), it["rect"], border_radius=6)
        pygame.draw.rect(screen, (20, 25, 40), it["rect"], 1, border_radius=6)
        # + 표시(옵션)
        cx, cy = it["rect"].center
        pygame.draw.line(screen, (20, 25, 40), (cx - 5, cy), (cx + 5, cy), 2)
        pygame.draw.line(screen, (20, 25, 40), (cx, cy - 5), (cx, cy + 5), 2)

    # UI
    ui = font.render(f"Score: {score}    Lives: {lives}    Balls: {len(balls)}    (Space: 발사, R: 재시작)", True, (25, 30, 45))
    screen.blit(ui, (20, 16))

    hint = small_font.render(f"아이템: 랜덤 드랍({int(ITEM_DROP_CHANCE*100)}%) / 먹으면 공 +{EXTRA_BALLS_ON_PICK}", True, (60, 70, 95))
    screen.blit(hint, (20, 48))

    if game_over:
        msg = big_font.render("GAME OVER", True, (30, 30, 45))
        sub = font.render("R: 재시작 / ESC: 종료", True, (30, 30, 45))
        screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))
        screen.blit(sub, sub.get_rect(center=(WIDTH//2, HEIGHT//2 + 28)))

    if game_win:
        msg = big_font.render("YOU WIN!", True, (30, 30, 45))
        sub = font.render("R: 재시작 / ESC: 종료", True, (30, 30, 45))
        screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))
        screen.blit(sub, sub.get_rect(center=(WIDTH//2, HEIGHT//2 + 28)))

    pygame.display.flip()
