import math
import random
import pygame

# =========================
# 기본 설정
# =========================
WIDTH, HEIGHT = 960, 600
FPS = 120

PLAYER_SPEED = 320.0
PLAYER_RADIUS = 18
PLAYER_MAX_HP = 100
PLAYER_IFRAME = 0.65  # 피격 무적(초)

BULLET_SPEED = 780.0
BULLET_RADIUS = 5
BULLET_LIFETIME = 1.2  # 초
FIRE_RATE = 1.0       ### 초당 발사 수(연사속도)

# ===== 탄창/장전 설정 =====
MAG_SIZE = 20              ### 탄창 크기
AMMO_RESERVE_START = 120   ### 예비 탄약(전체 총알 개수)
RELOAD_TIME = 1.25         ### 장전 시간(초)

ENEMY_RADIUS = 16
ENEMY_BASE_SPEED = 400.0 ### 적의 이동속도

# ===== 적 최대 수/속도 설정 =====
ENEMY_MAX_COUNT = 50           ### 화면에 존재 가능한 적 최대 마리 수
ENEMY_SPEED_GAIN_PER_SEC = 6.0  ### 시간 1초당 속도 증가량
ENEMY_MAX_BONUS_SPEED = 500.0   ### 적의 최대 이동속도

SPAWN_START_INTERVAL = 0.220  ### 몬스터 생성 주기
SPAWN_MIN_INTERVAL = 0.22    ### 몬스터 생성 주기 최소값
SPAWN_ACCEL = 0.010          ### 시간이 지날수록 스폰 간격 감소 = 시간이 지날수록 주기가 짧아짐.

BG = (15, 16, 20)
WHITE = (240, 240, 245)

def get_font(size):
    return pygame.font.Font(None, size)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def circle_collide(p1, r1, p2, r2):
    return (p1 - p2).length_squared() <= (r1 + r2) ** 2

def rand_spawn_pos():
    # 화면 바깥/가장자리에서 스폰
    side = random.choice(["L", "R", "T", "B"])
    margin = 40
    if side == "L":
        return pygame.Vector2(-margin, random.uniform(0, HEIGHT))
    if side == "R":
        return pygame.Vector2(WIDTH + margin, random.uniform(0, HEIGHT))
    if side == "T":
        return pygame.Vector2(random.uniform(0, WIDTH), -margin)
    return pygame.Vector2(random.uniform(0, WIDTH), HEIGHT + margin)

def draw_reload_bar_over_player(screen, player_pos, player_radius, reload_timer, reload_time):
    # 진행률: 0.0 ~ 1.0
    progress = 1.0 - (reload_timer / reload_time)
    progress = max(0.0, min(1.0, progress))

    w, h = 70, 8
    x = int(player_pos.x - w / 2)
    y = int(player_pos.y - player_radius - 18)

    # 화면 밖으로 안 나가게 클램프
    x = clamp(x, 4, WIDTH - w - 4)
    y = clamp(y, 4, HEIGHT - h - 4)

    pygame.draw.rect(screen, (60, 60, 70), (x, y, w, h), border_radius=5)
    pygame.draw.rect(screen, (255, 220, 110), (x, y, int(w * progress), h), border_radius=5)
    pygame.draw.rect(screen, (200, 200, 210), (x, y, w, h), 2, border_radius=5)

class Bullet:
    def __init__(self, pos, vel):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.life = BULLET_LIFETIME

    def update(self, dt):
        self.pos += self.vel * dt
        self.life -= dt

    def dead(self):
        if self.life <= 0:
            return True
        if self.pos.x < -120 or self.pos.x > WIDTH + 120 or self.pos.y < -120 or self.pos.y > HEIGHT + 120:
            return True
        return False

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 220, 110), self.pos, BULLET_RADIUS)

class Enemy:
    def __init__(self, pos, speed):
        self.pos = pygame.Vector2(pos)
        self.speed = speed
        self.hp = 1

    def update(self, dt, player_pos):
        d = player_pos - self.pos
        if d.length_squared() > 0.0001:
            d = d.normalize()
        self.pos += d * self.speed * dt

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 90, 110), self.pos, ENEMY_RADIUS)
        pygame.draw.circle(screen, (255, 250, 250), self.pos, 3)

class Player:
    def __init__(self):
        self.pos = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.hp = PLAYER_MAX_HP
        self.ifr = 0.0

    def update(self, dt, keys):
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move.x += 1
        if move.length_squared() > 0:
            move = move.normalize()
        self.pos += move * PLAYER_SPEED * dt
        self.pos.x = clamp(self.pos.x, PLAYER_RADIUS, WIDTH - PLAYER_RADIUS)
        self.pos.y = clamp(self.pos.y, PLAYER_RADIUS, HEIGHT - PLAYER_RADIUS)

        if self.ifr > 0:
            self.ifr -= dt

    def hit(self, dmg):
        if self.ifr > 0:
            return False
        self.hp = max(0, self.hp - dmg)
        self.ifr = PLAYER_IFRAME
        return True

    def draw(self, screen, aim_pos):
        if self.ifr > 0 and int(self.ifr * 12) % 2 == 0:
            color = (120, 170, 255)
        else:
            color = (90, 160, 255)

        pygame.draw.circle(screen, color, self.pos, PLAYER_RADIUS)
        d = pygame.Vector2(aim_pos) - self.pos
        if d.length_squared() > 0.0001:
            d = d.normalize()
        tip = self.pos + d * (PLAYER_RADIUS + 10)
        pygame.draw.line(screen, (230, 240, 255), self.pos, tip, 3)

def draw_hud(screen, font, small_font, hp, score, time_s, paused, ammo_in_mag, ammo_reserve):
    # HP 바
    bar_w, bar_h = 240, 18
    x, y = 16, 14
    pygame.draw.rect(screen, (60, 60, 70), (x, y, bar_w, bar_h), border_radius=6)
    fill = int(bar_w * (hp / PLAYER_MAX_HP))
    pygame.draw.rect(screen, (90, 160, 255), (x, y, fill, bar_h), border_radius=6)
    pygame.draw.rect(screen, (200, 200, 210), (x, y, bar_w, bar_h), 2, border_radius=6)

    txt1 = font.render(f"Score: {score}", True, WHITE)
    txt2 = small_font.render(f"Time: {time_s:0.1f}s", True, WHITE)
    txt3 = small_font.render(f"Ammo: {ammo_in_mag}/{MAG_SIZE}  Reserve: {ammo_reserve}", True, WHITE)

    screen.blit(txt1, (16, 42))
    screen.blit(txt2, (16, 70))
    screen.blit(txt3, (16, 96))

    if paused:
        t = font.render("PAUSED (Press P)", True, WHITE)
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 14))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Top-Down Shooter (pygame)")
    clock = pygame.time.Clock()

    font = get_font(32)
    small_font = get_font(22)
    big_font = get_font(56)

    state = "menu"  # menu | play | gameover
    paused = False

    player = Player()
    bullets = []
    enemies = []

    score = 0
    game_time = 0.0

    spawn_interval = SPAWN_START_INTERVAL
    spawn_timer = 0.0

    fire_cooldown = 0.0

    # ===== 탄창/장전 상태 =====
    ammo_in_mag = MAG_SIZE
    ammo_reserve = AMMO_RESERVE_START
    reloading = False
    reload_timer = 0.0

    def start_reload():
        nonlocal reloading, reload_timer, ammo_in_mag, ammo_reserve
        if reloading:
            return
        if ammo_in_mag >= MAG_SIZE:
            return
        if ammo_reserve <= 0:
            return
        reloading = True
        reload_timer = RELOAD_TIME

    def finish_reload():
        nonlocal reloading, reload_timer, ammo_in_mag, ammo_reserve
        need = MAG_SIZE - ammo_in_mag
        load = min(need, ammo_reserve)
        ammo_in_mag += load
        ammo_reserve -= load
        reloading = False
        reload_timer = 0.0

    def reset():
        nonlocal player, bullets, enemies, score, game_time
        nonlocal spawn_interval, spawn_timer, fire_cooldown, paused, state
        nonlocal ammo_in_mag, ammo_reserve, reloading, reload_timer

        player = Player()
        bullets = []
        enemies = []
        score = 0
        game_time = 0.0
        spawn_interval = SPAWN_START_INTERVAL
        spawn_timer = 0.0
        fire_cooldown = 0.0
        paused = False

        ammo_in_mag = MAG_SIZE
        ammo_reserve = AMMO_RESERVE_START
        reloading = False
        reload_timer = 0.0

        state = "play"

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        dt = min(dt, 1 / 20)  # 프레임 튐 방지용 캡

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if state == "menu":
                    if event.key == pygame.K_SPACE:
                        reset()

                elif state == "play":
                    if event.key == pygame.K_p:
                        paused = not paused
                    if event.key == pygame.K_r:  # 수동 장전
                        start_reload()

                elif state == "gameover":
                    if event.key == pygame.K_r:
                        reset()
                    if event.key == pygame.K_SPACE:
                        state = "menu"

        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        # =========================
        # 업데이트
        # =========================
        if state == "play" and not paused:
            game_time += dt

            # 난이도: 시간이 지날수록 스폰 간격 감소
            spawn_interval = max(SPAWN_MIN_INTERVAL, SPAWN_START_INTERVAL - game_time * SPAWN_ACCEL)

            # 이동
            player.update(dt, keys)

            # 장전 진행
            if reloading:
                reload_timer -= dt
                if reload_timer <= 0:
                    finish_reload()

            # 발사(연사) - 탄창 체크
            fire_cooldown -= dt
            if mouse_buttons[0] and fire_cooldown <= 0:
                if reloading:
                    pass
                elif ammo_in_mag <= 0:
                    start_reload()
                else:
                    d = pygame.Vector2(mouse_pos) - player.pos
                    if d.length_squared() < 1e-6:
                        d = pygame.Vector2(1, 0)
                    else:
                        d = d.normalize()

                    vel = d * BULLET_SPEED
                    bullets.append(Bullet(player.pos + d * (PLAYER_RADIUS + 6), vel))
                    fire_cooldown = 1.0 / FIRE_RATE 

                    ammo_in_mag -= 1
                    if ammo_in_mag == 0:
                        start_reload()

            # 탄환 업데이트
            for b in bullets:
                b.update(dt)
            bullets = [b for b in bullets if not b.dead()]

            # 적 스폰(최대 마리 수 제한)
            spawn_timer += dt
            while spawn_timer >= spawn_interval:
                spawn_timer -= spawn_interval
                if len(enemies) >= ENEMY_MAX_COUNT:
                    continue

                pos = rand_spawn_pos()
                speed = ENEMY_BASE_SPEED + min(ENEMY_MAX_BONUS_SPEED, game_time * ENEMY_SPEED_GAIN_PER_SEC)
                enemies.append(Enemy(pos, speed))

            # 적 업데이트
            for e in enemies:
                e.update(dt, player.pos)

            # 충돌: 탄환-적
            alive_enemies = []
            for e in enemies:
                for b in bullets:
                    if circle_collide(e.pos, ENEMY_RADIUS, b.pos, BULLET_RADIUS):
                        b.life = 0
                        e.hp -= 1
                        if e.hp <= 0:
                            score += 10
                        break
                if e.hp > 0:
                    alive_enemies.append(e)
            enemies = alive_enemies
            bullets = [b for b in bullets if not b.dead()]

            # 충돌: 적-플레이어 (접촉 피해)
            for e in enemies:
                if circle_collide(e.pos, ENEMY_RADIUS, player.pos, PLAYER_RADIUS):
                    if player.hit(12):
                        d = player.pos - e.pos
                        if d.length_squared() > 0.0001:
                            d = d.normalize()
                            player.pos += d * 18

            if player.hp <= 0:
                state = "gameover"
                paused = False

        # =========================
        # 렌더링
        # =========================
        screen.fill(BG)

        if state == "menu":
            title = big_font.render("TOP-DOWN SHOOTER", True, WHITE)
            s1 = small_font.render("WASD/Arrow: Move   Mouse: Aim   LMB: Shoot", True, WHITE)
            s2 = small_font.render("R: Reload   P: Pause", True, WHITE)
            s3 = small_font.render("Space: Start   ESC: Quit", True, WHITE)

            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))
            screen.blit(s1, (WIDTH // 2 - s1.get_width() // 2, 280))
            screen.blit(s2, (WIDTH // 2 - s2.get_width() // 2, 312))
            screen.blit(s3, (WIDTH // 2 - s3.get_width() // 2, 344))

        elif state == "play":
            for b in bullets:
                b.draw(screen)
            for e in enemies:
                e.draw(screen)

            player.draw(screen, mouse_pos)

            # 장전 바: 캐릭터 머리 위
            if reloading:
                draw_reload_bar_over_player(screen, player.pos, PLAYER_RADIUS, reload_timer, RELOAD_TIME)

            draw_hud(
                screen, small_font, small_font,
                player.hp, score, game_time, paused,
                ammo_in_mag, ammo_reserve
            )

            pygame.draw.circle(screen, (220, 220, 230), mouse_pos, 6, 1)

        elif state == "gameover":
            title = big_font.render("GAME OVER", True, WHITE)
            s1 = font.render(f"Score: {score}", True, WHITE)
            s2 = small_font.render(f"Time Survived: {game_time:0.1f}s", True, WHITE)
            s3 = small_font.render("R: Restart   Space: Menu   ESC: Quit", True, WHITE)

            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
            screen.blit(s1, (WIDTH // 2 - s1.get_width() // 2, 290))
            screen.blit(s2, (WIDTH // 2 - s2.get_width() // 2, 330))
            screen.blit(s3, (WIDTH // 2 - s3.get_width() // 2, 380))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
