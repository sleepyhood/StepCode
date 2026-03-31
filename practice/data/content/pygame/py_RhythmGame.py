import pygame
import random
import math

# -----------------------------
# 설정
# -----------------------------
WIDTH, HEIGHT = 900, 700
FPS = 120

LANES = 4
### 키 입력 부분 변경가능
LANE_KEYS = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]

### 여기는 그냥 UI
LANE_LABELS = ["D", "F", "J", "K"]

HIT_LINE_Y = int(HEIGHT * 0.82)
NOTE_RADIUS = 18

SPAWN_Y = -60
SPEED_PX_PER_SEC = 750

PERFECT = 0.045
GOOD = 0.090
MISS = 0.140

START_DELAY = 2.0
HIT_OFFSET = 0.0

# -----------------------------
### 수동 채보 (초 단위)
### 첫번째 값은 시간, 두번째 값은 내려오는 라인(위치 0 ~ 3)
# -----------------------------
BEATMAP_TIME = [
    [0.50, 0], [1.00, 1], [1.50, 2], [2.00, 3],
    [2.50, 0], [3.00, 1], [3.50, 2], [4.00, 3],

    [4.50, 0], [4.75, 1],
    [5.00, 2], [5.25, 1],
    [5.50, 3], [5.75, 2],
    [6.00, 0], [6.25, 2],

    [6.50, 1], [6.75, 3],
    [7.00, 0], [7.25, 1],
    [7.50, 2], [7.75, 3],
    [8.00, 0], [8.25, 3],

    [8.50, 0], [8.75, 1], [9.00, 2], [9.25, 3],
    [9.50, 1], [9.75, 2], [10.00, 1], [10.25, 3],
    [10.50, 0], [10.75, 2], [11.00, 1], [11.25, 3],

    [11.50, 0], [11.50, 3],
    [12.00, 1], [12.00, 2],

    [12.50, 0], [12.625, 1], [12.750, 2], [12.875, 3],
    [13.000, 2], [13.125, 1], [13.250, 3], [13.375, 0],
    [13.500, 1], [13.625, 2], [13.750, 1], [13.875, 3],

    [14.25, 0], [14.50, 2],
    [14.75, 1], [15.00, 3],
    [15.25, 0], [15.50, 3],
    [15.75, 1], [16.00, 2],

    [16.25, 0], [16.50, 1], [16.75, 2], [17.00, 3],
    [17.25, 3], [17.50, 2], [17.75, 1], [18.00, 0],

    [18.25, 0], [18.50, 1], [18.75, 2], [19.00, 3],
    [19.167, 1], [19.334, 2], [19.501, 1], [19.668, 3],
    [19.85, 0], [20.10, 2], [20.35, 1], [20.60, 3],

    [20.85, 0], [20.85, 3],
    [21.10, 1], [21.10, 2],

    [21.50, 0], [21.625, 1], [21.750, 2], [21.875, 3],
    [22.00, 0], [22.125, 3],

    [22.50, 0], [23.00, 1], [23.50, 2], [24.00, 3],
    [24.50, 2], [25.00, 1],
    [25.50, 0], [26.00, 3],

    [26.50, 0], [26.50, 3],
]


# -----------------------------
# 노트 데이터 구조
# -----------------------------
class Note:
    __slots__ = ("time", "lane", "hit", "judged")

    def __init__(self, time_sec, lane):
        self.time = float(time_sec)
        self.lane = int(lane)
        self.hit = False
        self.judged = False


# -----------------------------
# 히트 이펙트(스파크) 파티클
# -----------------------------
class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "ttl", "radius", "color")

    def __init__(self, x, y, vx, vy, ttl, radius, color):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.life = float(ttl)
        self.ttl = float(ttl)
        self.radius = float(radius)
        self.color = color


# -----------------------------
# 게임
# -----------------------------
class RhythmGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Python Rhythm Game (D/F/J/K)")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_big = pygame.font.SysFont("malgungothic", 44)
        self.font = pygame.font.SysFont("malgungothic", 24)
        self.font_small = pygame.font.SysFont("malgungothic", 18)

        beatmap = sorted(BEATMAP_TIME, key=lambda x: x[0])
        self.notes = [Note(t, lane) for (t, lane) in beatmap]

        self.reset()

    def reset(self):
        global HIT_OFFSET
        self.running = True
        self.paused = False

        # ✅ 시작 대기 상태: SPACE 누르면 그때부터 타이머 시작
        self.waiting = True
        self.t_start_real = pygame.time.get_ticks() / 1000.0
        self.start_delay = START_DELAY

        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.count_perfect = 0
        self.count_good = 0
        self.count_miss = 0
        self.last_judgement = ""
        self.last_judge_time = 0.0

        for n in self.notes:
            n.hit = False
            n.judged = False

        self.finished = False

        # 입력 피드백/이펙트
        self.lane_flash = [0.0] * LANES
        self.hit_particles = []

    def start_game(self):
        # SPACE를 누르는 순간을 "0초 기준"으로 잡음
        self.waiting = False
        self.t_start_real = pygame.time.get_ticks() / 1000.0
        self.start_delay = START_DELAY

        # 카운트다운 표시가 깔끔하게 뜨도록
        self.last_judgement = ""
        self.last_judge_time = 0.0

    def current_time(self):
        if self.waiting:
            return 0.0  # 대기중에는 시간 흐름을 사용하지 않음(노트 표시 X)
        now = pygame.time.get_ticks() / 1000.0
        return (now - self.t_start_real) - self.start_delay

    def lane_x(self, lane):
        lane_w = WIDTH // 6
        total_w = lane_w * LANES
        left = (WIDTH - total_w) // 2
        return left + lane * lane_w + lane_w // 2

    def lane_rect(self, lane):
        lane_w = WIDTH // 6
        total_w = lane_w * LANES
        left = (WIDTH - total_w) // 2
        top = 80
        bottom = HEIGHT - 40
        x0 = left + lane * lane_w
        return pygame.Rect(x0, top, lane_w, bottom - top)

    def spawn_hit_fx(self, lane, kind):
        x = self.lane_x(lane)
        y = HIT_LINE_Y

        if kind == "PERFECT":
            base = (255, 245, 200)
        else:
            base = (220, 240, 255)

        count = 14 if kind == "PERFECT" else 10
        for _ in range(count):
            ang = random.uniform(-math.pi, math.pi)
            spd = random.uniform(120.0, 320.0) if kind == "PERFECT" else random.uniform(90.0, 240.0)

            vx = math.cos(ang) * spd
            vy = math.sin(ang) * spd - random.uniform(80.0, 160.0)
            ttl = random.uniform(0.18, 0.30) if kind == "PERFECT" else random.uniform(0.15, 0.26)
            r = random.uniform(2.0, 4.0)

            self.hit_particles.append(Particle(x, y, vx, vy, ttl, r, base))

    def update_effects(self, dt):
        for i in range(LANES):
            if self.lane_flash[i] > 0.0:
                self.lane_flash[i] = max(0.0, self.lane_flash[i] - dt)

        if self.hit_particles:
            g = 1400.0
            drag = 0.985

            alive = []
            for p in self.hit_particles:
                p.life -= dt
                if p.life <= 0.0:
                    continue

                p.vy += g * dt
                p.vx *= drag
                p.vy *= drag
                p.x += p.vx * dt
                p.y += p.vy * dt
                alive.append(p)

            self.hit_particles = alive

    def draw_lanes(self):
        self.screen.fill((18, 18, 22))

        lane_w = WIDTH // 6
        total_w = lane_w * LANES
        left = (WIDTH - total_w) // 2
        top = 80
        bottom = HEIGHT - 40

        for i in range(LANES):
            rect = self.lane_rect(i)
            pygame.draw.rect(self.screen, (28, 28, 36), rect, border_radius=12)

            f = self.lane_flash[i]
            if f > 0.0:
                a = min(1.0, f / 0.12)
                alpha = int(140 * a)
                overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, alpha))
                self.screen.blit(overlay, rect.topleft)

        for i in range(LANES + 1):
            x = left + i * lane_w
            pygame.draw.line(self.screen, (55, 55, 70), (x, top), (x, bottom), 2)

        pygame.draw.line(self.screen, (210, 210, 220), (left, HIT_LINE_Y), (left + total_w, HIT_LINE_Y), 4)

        for i, label in enumerate(LANE_LABELS):
            x = self.lane_x(i)
            txt = self.font.render(label, True, (230, 230, 240))
            self.screen.blit(txt, (x - txt.get_width() // 2, HIT_LINE_Y + 18))

    def draw_notes(self, t):
        # waiting 중에는 노트 안 보이게
        if self.waiting:
            return

        for n in self.notes:
            if n.judged:
                continue

            dt = t - (n.time + HIT_OFFSET)
            y = HIT_LINE_Y + dt * SPEED_PX_PER_SEC

            if y < SPAWN_Y:
                continue
            if y > HEIGHT + 120:
                continue

            x = self.lane_x(n.lane)
            pygame.draw.circle(self.screen, (90, 200, 255), (x, int(y)), NOTE_RADIUS)
            pygame.draw.circle(self.screen, (220, 240, 255), (x, int(y)), NOTE_RADIUS, 3)

    def draw_hit_fx(self):
        for p in self.hit_particles:
            a = max(0.0, min(1.0, p.life / p.ttl))
            alpha = int(255 * a)

            r = max(1, int(p.radius))
            surf = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*p.color, alpha), (r + 1, r + 1), r)
            self.screen.blit(surf, (int(p.x) - (r + 1), int(p.y) - (r + 1)))

    def draw_ui(self, t):
        s = f"Score: {self.score:,}   Combo: {self.combo}   Max: {self.max_combo}"
        txt = self.font.render(s, True, (235, 235, 240))
        self.screen.blit(txt, (30, 22))

        stat = f"Perfect {self.count_perfect}   Good {self.count_good}   Miss {self.count_miss}"
        txt2 = self.font_small.render(stat, True, (200, 200, 210))
        self.screen.blit(txt2, (30, 52))

        off = f"Offset: {HIT_OFFSET:+.3f}s  ([-]/[+]로 조절)"
        txt3 = self.font_small.render(off, True, (200, 200, 210))
        self.screen.blit(txt3, (WIDTH - txt3.get_width() - 30, 22))

        # ✅ 시작 대기 메시지
        if self.waiting:
            msg = "Press SPACE to Start"
            c = self.font_big.render(msg, True, (240, 240, 255))
            self.screen.blit(c, (WIDTH // 2 - c.get_width() // 2, HEIGHT // 2 - 80))

            sub = "ESC: Quit   |   R: Restart"
            s2 = self.font.render(sub, True, (200, 200, 210))
            self.screen.blit(s2, (WIDTH // 2 - s2.get_width() // 2, HEIGHT // 2 - 20))
            return

        if self.last_judgement and (t - self.last_judge_time) < 0.5:
            jtxt = self.font_big.render(self.last_judgement, True, (255, 245, 200))
            self.screen.blit(jtxt, (WIDTH // 2 - jtxt.get_width() // 2, 120))

        # ✅ 카운트다운 (SPACE 누른 뒤에만)
        if t < 0:
            remain = -t
            msg = "Get Ready..."
            if remain < 1.0:
                msg = "1"
            elif remain < 2.0:
                msg = "2"
            elif remain < 3.0:
                msg = "3"
            c = self.font_big.render(msg, True, (240, 240, 255))
            self.screen.blit(c, (WIDTH // 2 - c.get_width() // 2, HEIGHT // 2 - 80))

        if self.finished:
            msg = "Finished!  [R] Restart  |  [ESC] Quit"
            tmsg = self.font.render(msg, True, (240, 240, 255))
            self.screen.blit(tmsg, (WIDTH // 2 - tmsg.get_width() // 2, HEIGHT // 2 + 10))

    def judge_hit(self, lane, t):
        self.lane_flash[lane] = 0.12

        cand = None
        for n in self.notes:
            if n.judged or n.lane != lane:
                continue
            cand = n
            break

        if cand is None:
            self.combo = 0
            self.last_judgement = "EMPTY"
            self.last_judge_time = t
            return

        diff = abs(t - (cand.time + HIT_OFFSET))

        if diff <= PERFECT:
            cand.hit = True
            cand.judged = True
            self.count_perfect += 1
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            self.score += 1000 + self.combo * 2
            self.last_judgement = "PERFECT"
            self.last_judge_time = t
            self.spawn_hit_fx(lane, "PERFECT")

        elif diff <= GOOD:
            cand.hit = True
            cand.judged = True
            self.count_good += 1
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            self.score += 600 + self.combo
            self.last_judgement = "GOOD"
            self.last_judge_time = t
            self.spawn_hit_fx(lane, "GOOD")

        else:
            self.combo = 0
            self.last_judgement = "BAD"
            self.last_judge_time = t

    def update_misses(self, t):
        # waiting/카운트다운 중에는 미스 처리하지 않게 하고 싶으면 아래 조건 유지
        if self.waiting:
            return

        for n in self.notes:
            if n.judged:
                continue
            if (t - (n.time + HIT_OFFSET)) > MISS:
                n.judged = True
                n.hit = False
                self.count_miss += 1
                self.combo = 0
                self.last_judgement = "MISS"
                self.last_judge_time = t

    def check_finished(self, t):
        for n in self.notes:
            if not n.judged:
                return False
        return t > (self.notes[-1].time + HIT_OFFSET + 1.0)

    def handle_events(self, t):
        global HIT_OFFSET

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_r:
                    self.reset()

                # ✅ 대기중 SPACE로 시작
                if event.key == pygame.K_SPACE and self.waiting:
                    self.start_game()

                # 대기 중엔 나머지 입력 처리(판정/일시정지 등) 안 함
                if self.waiting:
                    continue

                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    if self.paused:
                        self.pause_real = pygame.time.get_ticks() / 1000.0
                    else:
                        now = pygame.time.get_ticks() / 1000.0
                        self.t_start_real += (now - self.pause_real)

                # 오프셋 조절 (- / +)
                if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    HIT_OFFSET -= 0.005
                if event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                    HIT_OFFSET += 0.005

                for i, k in enumerate(LANE_KEYS):
                    if event.key == k and not self.finished and not self.paused and not self.waiting:
                        self.judge_hit(i, t)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            t = self.current_time()

            self.handle_events(t)
            self.update_effects(dt)

            if self.paused:
                self.draw_lanes()
                self.draw_notes(t)
                self.draw_hit_fx()
                self.draw_ui(t)
                pause_txt = self.font_big.render("PAUSED", True, (255, 220, 220))
                self.screen.blit(pause_txt, (WIDTH // 2 - pause_txt.get_width() // 2, HEIGHT // 2 - 30))
                pygame.display.flip()
                continue

            if (not self.finished) and (not self.waiting):
                self.update_misses(t)
                if self.check_finished(t):
                    self.finished = True

            self.draw_lanes()
            self.draw_notes(t)
            self.draw_hit_fx()
            self.draw_ui(t)

            help_msg = "Keys: D F J K  |  SPACE: Start  |  P: Pause  |  R: Restart  |  ESC: Quit"
            h = self.font_small.render(help_msg, True, (180, 180, 195))
            self.screen.blit(h, (WIDTH // 2 - h.get_width() // 2, HEIGHT - 28))

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = RhythmGame()
    game.run()
