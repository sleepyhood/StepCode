import random
import math
import pygame

# =========================
# 설정(원하는 대로 바꿔도 됨)
# =========================
WIDTH, HEIGHT = 900, 600
FPS = 120

SESSION_SECONDS = 30          # 한 판 시간(초)
TARGET_RADIUS = 28            # 타겟 "초기" 반지름(px)
TARGET_MARGIN = 16            # 화면 가장자리 여백(px) - 타겟이 잘리지 않도록

# 추가: 타겟이 줄어들며 사라지는 시간(ms)
TARGET_LIFETIME_MS = 1200     # 기본 수명(ms)
TARGET_LIFETIME_JITTER = 400  # 수명 랜덤 가산(ms) (0이면 고정)

### 동시에 등장 가능한 타겟 개수(매번 1~MAX 중 랜덤으로 유지)
MAX_TARGETS = 40

SHOW_CROSSHAIR = True         # 조준선 표시 여부
BACKGROUND = (18, 18, 22)
TEXT = (230, 230, 235)

# =========================
# 유틸
# =========================

### 거리를 비교할 때 왜 루트를 안 쓸까?
def dist2(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx*dx + dy*dy

def rand_target_pos(radius: int, margin: int, last_pos=None, existing_positions=None):
    left = margin + radius
    right = WIDTH - (margin + radius)
    top = margin + radius
    bottom = HEIGHT - (margin + radius)

    existing_positions = existing_positions or []

    # 너무 가까운 위치 연속/겹침 방지
    for _ in range(80):
        x = random.randint(left, right)
        y = random.randint(top, bottom)

        ok = True

        if last_pos is not None:
            if (x - last_pos[0]) ** 2 + (y - last_pos[1]) ** 2 < (radius * 2) ** 2:
                ok = False

        if ok:
            for p in existing_positions:
                if (x - p[0]) ** 2 + (y - p[1]) ** 2 < (radius * 2) ** 2:
                    ok = False
                    break

        if ok:
            return (x, y)

    return (x, y)

def get_korean_font(size):
    candidates = [
        "malgungothic",   # Windows: 맑은 고딕
        "applegothic",    # macOS: AppleGothic
        "nanumgothic",    # Linux/기타: 나눔고딕
        "notosanscjkkr",  # Noto CJK KR (이름이 환경마다 다를 수 있음)
        "notosanskr",     # Noto Sans KR
    ]
    for name in candidates:
        f = pygame.font.SysFont(name, size)
        if f is not None:
            return f
    return pygame.font.SysFont(None, size)  # 최후 fallback

# =========================
# 메인
# =========================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Aim Trainer (pygame)")
    clock = pygame.time.Clock()

    font = get_korean_font(28)
    big_font = get_korean_font(48)

    state = "menu"  # menu | running | done

    # 게임 데이터
    session_start_ms = 0

    # 타겟: 여러 개 관리
    targets = []   # 각 원소: {"pos":(x,y), "spawn_ms":int, "life_ms":int, "r0":int}
    last_target_pos = None

    shots = 0
    hits = 0
    misses = 0
    reaction_times = []  # ms (히트한 타겟의 등장 후 클릭까지)

    def make_target():
        nonlocal last_target_pos
        now = pygame.time.get_ticks()
        life = TARGET_LIFETIME_MS + (random.randint(0, TARGET_LIFETIME_JITTER) if TARGET_LIFETIME_JITTER > 0 else 0)

        existing = [t["pos"] for t in targets]
        pos = rand_target_pos(TARGET_RADIUS, TARGET_MARGIN, last_target_pos, existing_positions=existing)
        last_target_pos = pos

        return {"pos": pos, "spawn_ms": now, "life_ms": life, "r0": TARGET_RADIUS}

    def refill_targets():
        # 매번 1~MAX_TARGETS 중 랜덤한 목표 개수를 정하고 그만큼 채움
        desired = random.randint(1, MAX_TARGETS)
        while len(targets) < desired:
            targets.append(make_target())

    def reset_game():
        nonlocal session_start_ms, targets, last_target_pos
        nonlocal shots, hits, misses, reaction_times, state

        shots = 0
        hits = 0
        misses = 0
        reaction_times = []
        last_target_pos = None

        targets = []
        refill_targets()

        session_start_ms = pygame.time.get_ticks()
        state = "running"

    def end_game():
        nonlocal state
        state = "done"

    def current_radius(t):
        now = pygame.time.get_ticks()
        age = now - t["spawn_ms"]
        if age <= 0:
            return t["r0"]
        ratio = 1.0 - (age / float(t["life_ms"]))
        if ratio < 0.0:
            ratio = 0.0
        r = int(max(0, round(t["r0"] * ratio)))
        return r

    running = True
    while running:
        dt = clock.tick(FPS)

        # ----- 이벤트 처리 -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if state == "menu":
                    if event.key == pygame.K_SPACE:
                        reset_game()

                elif state == "done":
                    if event.key == pygame.K_r:
                        reset_game()
                    if event.key == pygame.K_SPACE:
                        state = "menu"

                elif state == "running":
                    if event.key == pygame.K_r:
                        reset_game()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == "running":
                    shots += 1
                    mouse = pygame.mouse.get_pos()

                    # 클릭 지점에 맞은 타겟 중 "가장 가까운" 타겟 1개 처리
                    hit_idx = -1
                    best_d2 = None

                    for i, t in enumerate(targets):
                        r = current_radius(t)
                        if r <= 0:
                            continue
                        d2 = dist2(mouse, t["pos"])
                        if d2 <= r * r:
                            if best_d2 is None or d2 < best_d2:
                                best_d2 = d2
                                hit_idx = i

                    if hit_idx != -1:
                        hits += 1
                        now = pygame.time.get_ticks()
                        rt = now - targets[hit_idx]["spawn_ms"]
                        reaction_times.append(rt)

                        # 맞은 타겟 제거
                        targets.pop(hit_idx)

                        # 제거 후, 랜덤 개수로 다시 채워 "여러 개가 한 번에" 나올 수 있게 함
                        refill_targets()
                    else:
                        misses += 1

        # ----- 상태 업데이트 -----
        if state == "running":
            elapsed = (pygame.time.get_ticks() - session_start_ms) / 1000.0
            if elapsed >= SESSION_SECONDS:
                end_game()
            else:
                # 수명 끝난(반지름 0) 타겟 제거 + 다시 채우기
                before = len(targets)
                targets = [t for t in targets if current_radius(t) > 0]
                if len(targets) != before:
                    refill_targets()

        # ----- 그리기 -----
        screen.fill(BACKGROUND)

        if state == "menu":
            title = big_font.render("Aim Trainer", True, TEXT)
            hint1 = font.render("Space: 시작", True, TEXT)
            hint2 = font.render("ESC: 종료", True, TEXT)

            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 220))
            screen.blit(hint1, (WIDTH // 2 - hint1.get_width() // 2, 300))
            screen.blit(hint2, (WIDTH // 2 - hint2.get_width() // 2, 335))

        elif state == "running":
            # 타겟(여러 개) - 줄어들며 사라짐
            for t in targets:
                r = current_radius(t)
                if r <= 0:
                    continue
                pygame.draw.circle(screen, (255, 70, 90), t["pos"], r)
                pygame.draw.circle(screen, (255, 235, 240), t["pos"], max(2, r // 6))

            # 크로스헤어
            if SHOW_CROSSHAIR:
                mx, my = pygame.mouse.get_pos()
                pygame.draw.line(screen, (120, 120, 130), (mx - 12, my), (mx + 12, my), 1)
                pygame.draw.line(screen, (120, 120, 130), (mx, my - 12), (mx, my + 12), 1)

            # HUD
            elapsed = (pygame.time.get_ticks() - session_start_ms) / 1000.0
            left = max(0.0, SESSION_SECONDS - elapsed)



            ### 정확도 계산하는 부분
            acc = (hits / shots * 100.0) if shots > 0 else 0.0
            avg_rt = (sum(reaction_times) / len(reaction_times)) if reaction_times else 0.0

            hud1 = font.render(f"Time: {left:5.1f}s", True, TEXT)
            hud2 = font.render(f"Hits: {hits}  Miss: {misses}  Shots: {shots}", True, TEXT)
            hud3 = font.render(f"Acc: {acc:5.1f}%  Avg RT: {avg_rt:6.1f} ms", True, TEXT)
            hud4 = font.render("R: 재시작  |  ESC: 종료", True, TEXT)

            screen.blit(hud1, (16, 14))
            screen.blit(hud2, (16, 44))
            screen.blit(hud3, (16, 74))
            screen.blit(hud4, (16, HEIGHT - 34))

        elif state == "done":
            acc = (hits / shots * 100.0) if shots > 0 else 0.0
            avg_rt = (sum(reaction_times) / len(reaction_times)) if reaction_times else 0.0
            best_rt = min(reaction_times) if reaction_times else 0

            title = big_font.render("Result", True, TEXT)
            line1 = font.render(f"Hits: {hits}", True, TEXT)
            line2 = font.render(f"Miss: {misses}", True, TEXT)
            line3 = font.render(f"Shots: {shots}", True, TEXT)
            line4 = font.render(f"Accuracy: {acc:.1f}%", True, TEXT)
            line5 = font.render(f"Avg Reaction: {avg_rt:.1f} ms", True, TEXT)
            line6 = font.render(f"Best Reaction: {best_rt} ms", True, TEXT)
            hint = font.render("R: 재시작  |  Space: 메뉴  |  ESC: 종료", True, TEXT)

            cx = WIDTH // 2
            y = 170
            screen.blit(title, (cx - title.get_width() // 2, y))
            y += 70
            for line in (line1, line2, line3, line4, line5, line6):
                screen.blit(line, (cx - line.get_width() // 2, y))
                y += 34
            screen.blit(hint, (cx - hint.get_width() // 2, HEIGHT - 70))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
